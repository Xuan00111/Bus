import pandas as pd
import numpy as np

# 读取预处理后的数据
df = pd.read_csv('cleaned_ICData.csv', parse_dates=['交易时间'])

# 仅保留刷卡类型为0的记录
df0 = df[df['刷卡类型'] == 0].copy()

# 1. 高峰小时识别：统计全天各小时刷卡量
df0['hour'] = df0['交易时间'].dt.hour
hourly_counts = df0.groupby('hour').size()
peak_hour = hourly_counts.idxmax()          # 刷卡量最大的小时（若并列取第一个）
peak_volume = hourly_counts.max()

print(f"高峰小时：{peak_hour:02d}:00 ~ {peak_hour+1:02d}:00，刷卡量：{peak_volume} 次")

# 2. 提取高峰小时内的数据
mask_peak = df0['hour'] == peak_hour
df_peak = df0[mask_peak].copy()

# 计算当天分钟数（从0:00开始）
df_peak['minute_of_day'] = df_peak['交易时间'].dt.hour * 60 + df_peak['交易时间'].dt.minute

# 高峰小时起始分钟数
base_minute = peak_hour * 60

# ---- 5分钟粒度统计 ----
# 计算5分钟窗口索引（0~11）
df_peak['win5'] = (df_peak['minute_of_day'] - base_minute) // 5
# 统计每个窗口的刷卡量
win5_counts = df_peak.groupby('win5').size()
max_win5_count = win5_counts.max()
# 找到最大窗口的索引（如果有多个，取第一个）
max_win5_idx = win5_counts.idxmax()
# 计算窗口的实际时间范围
win5_start_min = base_minute + max_win5_idx * 5
win5_end_min = win5_start_min + 5
win5_start_time = f"{win5_start_min // 60:02d}:{win5_start_min % 60:02d}"
win5_end_time = f"{win5_end_min // 60:02d}:{win5_end_min % 60:02d}"

# 计算PHF5
PHF5 = peak_volume / (12 * max_win5_count)

# ---- 15分钟粒度统计 ----
df_peak['win15'] = (df_peak['minute_of_day'] - base_minute) // 15
win15_counts = df_peak.groupby('win15').size()
max_win15_count = win15_counts.max()
max_win15_idx = win15_counts.idxmax()
win15_start_min = base_minute + max_win15_idx * 15
win15_end_min = win15_start_min + 15
win15_start_time = f"{win15_start_min // 60:02d}:{win15_start_min % 60:02d}"
win15_end_time = f"{win15_end_min // 60:02d}:{win15_end_min % 60:02d}"

PHF15 = peak_volume / (4 * max_win15_count)

# 输出结果（按题目格式）
print(f"最大5分钟刷卡量（{win5_start_time}~{win5_end_time}）：{max_win5_count} 次")
print(f"PHF5 = {peak_volume} / (12 × {max_win5_count}) = {PHF5:.4f}")
print(f"最大15分钟刷卡量（{win15_start_time}~{win15_end_time}）：{max_win15_count} 次")
print(f"PHF15 = {peak_volume} / (4 × {max_win15_count}) = {PHF15:.4f}")
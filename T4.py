import pandas as pd
import numpy as np

df = pd.read_csv('cleaned_ICData.csv', parse_dates=['交易时间'])  # 读取清洗数据

df0 = df[df['刷卡类型'] == 0].copy()               # 只保留正常刷卡记录

# 1. 找全天刷卡量最大的小时（高峰小时）
df0['hour'] = df0['交易时间'].dt.hour
hourly_counts = df0.groupby('hour').size()
peak_hour = hourly_counts.idxmax()
peak_volume = hourly_counts.max()

print(f"高峰小时：{peak_hour:02d}:00 ~ {peak_hour+1:02d}:00，刷卡量：{peak_volume} 次")

# 2. 提取高峰小时内的数据
mask_peak = df0['hour'] == peak_hour
df_peak = df0[mask_peak].copy()

df_peak['minute_of_day'] = df_peak['交易时间'].dt.hour * 60 + df_peak['交易时间'].dt.minute
base_minute = peak_hour * 60                          # 高峰小时起始分钟

# ----- 5分钟粒度 -----
df_peak['win5'] = (df_peak['minute_of_day'] - base_minute) // 5  # 窗口编号0~11
win5_counts = df_peak.groupby('win5').size()
max_win5_count = win5_counts.max()
max_win5_idx = win5_counts.idxmax()

win5_start_min = base_minute + max_win5_idx * 5
win5_end_min = win5_start_min + 5
win5_start_time = f"{win5_start_min // 60:02d}:{win5_start_min % 60:02d}"
win5_end_time = f"{win5_end_min // 60:02d}:{win5_end_min % 60:02d}"

PHF5 = peak_volume / (12 * max_win5_count)            # 12个5分钟窗口

# ----- 15分钟粒度 -----
df_peak['win15'] = (df_peak['minute_of_day'] - base_minute) // 15  # 窗口编号0~3
win15_counts = df_peak.groupby('win15').size()
max_win15_count = win15_counts.max()
max_win15_idx = win15_counts.idxmax()

win15_start_min = base_minute + max_win15_idx * 15
win15_end_min = win15_start_min + 15
win15_start_time = f"{win15_start_min // 60:02d}:{win15_start_min % 60:02d}"
win15_end_time = f"{win15_end_min // 60:02d}:{win15_end_min % 60:02d}"

PHF15 = peak_volume / (4 * max_win15_count)           # 4个15分钟窗口

# 输出
print(f"最大5分钟刷卡量（{win5_start_time}~{win5_end_time}）：{max_win5_count} 次")
print(f"PHF5 = {peak_volume} / (12 × {max_win5_count}) = {PHF5:.4f}")
print(f"最大15分钟刷卡量（{win15_start_time}~{win15_end_time}）：{max_win15_count} 次")
print(f"PHF15 = {peak_volume} / (4 × {max_win15_count}) = {PHF15:.4f}")

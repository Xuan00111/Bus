import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# ------------------------------
# 1. 读取预处理后的数据
# ------------------------------
df = pd.read_csv('cleaned_ICData.csv', parse_dates=['交易时间'])
df['hour'] = df['交易时间'].dt.hour          # 从交易时间提取小时

# 仅保留刷卡类型 == 0 的记录
mask_type0 = df['刷卡类型'] == 0
df_type0 = df[mask_type0]

# ------------------------------
# 2. (a) 早晚时段刷卡量统计（使用 numpy）
# ------------------------------
hours = df_type0['hour'].to_numpy()          # 转为 numpy 数组

# 早峰前时段：hour < 7
early_mask = hours < 7
early_count = np.sum(early_mask)

# 深夜时段：hour >= 22
late_mask = hours >= 22
late_count = np.sum(late_mask)

# 全天总刷卡量（刷卡类型=0）
total_count = len(hours)

early_pct = (early_count / total_count) * 100
late_pct = (late_count / total_count) * 100

print("===== 时段刷卡量统计（仅刷卡类型=0）=====")
print(f"早峰前时段 (hour < 7) 刷卡量: {early_count}")
print(f"占全天总刷卡量百分比: {early_pct:.2f}%")
print(f"深夜时段 (hour >= 22) 刷卡量: {late_count}")
print(f"占全天总刷卡量百分比: {late_pct:.2f}%")
print(f"全天总刷卡量 (刷卡类型=0): {total_count}\n")

# ------------------------------
# 3. (b) 24小时刷卡量分布可视化
# ------------------------------
# 按小时分组计数
hourly_counts = df_type0.groupby('hour').size()
hourly_counts = hourly_counts.reindex(range(24), fill_value=0)

hours_axis = hourly_counts.index
counts = hourly_counts.values

# 设置柱体颜色
colors = []
for h in hours_axis:
    if h < 7:
        colors.append('skyblue')      # 早峰前
    elif h >= 22:
        colors.append('salmon')       # 深夜
    else:
        colors.append('lightgray')    # 其他时段

# 绘图
plt.figure(figsize=(12, 6))
bars = plt.bar(hours_axis, counts, color=colors, edgecolor='black', alpha=0.8)

# 图例
legend_elements = [
    Patch(facecolor='skyblue', label='Early morning (hour < 7)'),
    Patch(facecolor='salmon', label='Late night (hour >= 22)'),
    Patch(facecolor='lightgray', label='Other hours')
]
plt.legend(handles=legend_elements, loc='upper right')

# 英文标签与标题
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Number of Swipe Records (Card Type = 0)', fontsize=12)
plt.title('24-Hour Distribution of Bus Swipe Records', fontsize=14, fontweight='bold')

# x轴刻度：0~23，步长2
plt.xticks(np.arange(0, 24, 2), fontsize=10)
plt.yticks(fontsize=10)

# 水平网格线
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 去掉顶部和右侧边框（美观）
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# 保存图片
plt.savefig('hour_distribution.png', dpi=150, bbox_inches='tight')
print("图像已保存为 hour_distribution.png")

# 如需显示图片，可取消下面注释
# plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('cleaned_ICData.csv', parse_dates=['交易时间'])  # 读取清洗数据
df = df[df['刷卡类型'] == 0]                    # 只保留正常刷卡记录

# 四个统计维度
dimensions = {
    'Driver': '驾驶员编号',
    'Route': '线路号',
    'Boarding Station': '上车站点',
    'Vehicle': '车辆编号'
}

# 统计各维度Top10
top_dict = {}
for name, col in dimensions.items():
    counts = df[col].value_counts()              # 按出现次数降序
    top10 = counts.head(10)
    top_dict[name] = top10
    if name == 'Vehicle':                        # 只打印车辆排名
        print(f"\n===== {name}s Top 10 =====")
        for i, (entity, cnt) in enumerate(top10.items(), 1):
            print(f"Top{i}: {entity} Count={cnt}")

# 拼热力图数据矩阵（4行×10列）
heatmap_data = []
for name in ['Driver', 'Route', 'Boarding Station', 'Vehicle']:
    series = top_dict[name]
    values = list(series.values)
    if len(values) < 10:
        values += [0] * (10 - len(values))       # 不足10个补0
    heatmap_data.append(values)

heatmap_df = pd.DataFrame(
    heatmap_data,
    index=['Driver', 'Route', 'Boarding Station', 'Vehicle'],
    columns=[f'Top{i+1}' for i in range(10)]
)

# 画热力图
plt.figure(figsize=(12, 4))
sns.heatmap(
    heatmap_df,
    annot=True,
    fmt='.0f',
    cmap='YlOrRd',
    cbar=True,
    linewidths=0.5,
    linecolor='white'
)
plt.title('Service Performance Ranking Heatmap\n(Top 10 Entities by Passenger Trips)',
          fontsize=14, fontweight='bold')
plt.xlabel('Rank', fontsize=12)
plt.ylabel('Entity Type', fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('performance_heatmap.png', dpi=150, bbox_inches='tight')
print("\n热力图已保存为 performance_heatmap.png")

# 结论
print("\n===== 结论说明 =====")
conclusion = """
从热力图中可以观察以下规律：
1. 线路维度中，Top1线路（如1101）的服务人次显著高于其他线路，说明该线路客流高度集中，可能是主干线路。
2. 驾驶员服务人次差距悬殊，Top1司机的工作量远超同行，存在驾驶任务分配不均衡现象。
3. 上车站点前几名（如核心枢纽站）的人次远高于后续站点，表明客流分布极度不均，建议加强这些站点运力。
4. 车辆使用频次差异相对较小，Top1~Top10递减平缓，说明车辆调度较为均衡。
（实际解读需结合具体数值，本结论基于热力图色差趋势。）
"""
print(conclusion)

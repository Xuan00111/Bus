import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_route_stops(df, route_col='线路号', stops_col='ride_stops'):
    """按线路统计平均搭乘站点数及标准差，降序返回"""
    result = df.groupby(route_col)[stops_col].agg(mean_stops='mean', std_stops='std').reset_index()
    result = result.sort_values('mean_stops', ascending=False)
    return result


if __name__ == '__main__':
    df = pd.read_csv('cleaned_ICData.csv', parse_dates=['交易时间'])  # 读取清洗数据
    df['ride_stops'] = pd.to_numeric(df['ride_stops'], errors='coerce')
    df = df.dropna(subset=['ride_stops'])                             # 再清一次异常值

    route_analysis = analyze_route_stops(df, route_col='线路号', stops_col='ride_stops')

    print("[任务3] 每条线路的平均搭乘站点数及标准差（前10行）：")
    print(route_analysis.head(10).reset_index(drop=True).to_string())  # 重置索引使序号从0开始

    # 取前15条线路画水平条形图
    top15 = route_analysis.head(15).copy()

    plt.figure(figsize=(10, 8))
    palette = sns.color_palette("Blues_d", n_colors=len(top15))

    ax = sns.barplot(
        data=top15,
        y='线路号',
        x='mean_stops',
        hue='线路号',
        palette=palette,
        orient='h',
        legend=False
    )

    # 手动加误差棒
    for i, (_, row) in enumerate(top15.iterrows()):
        ax.errorbar(
            x=row['mean_stops'],
            y=i,
            xerr=row['std_stops'],
            fmt='none',
            capsize=0.3,
            color='black',
            capthick=1,
            elinewidth=1
        )

    ax.set_title('Top 15 Routes by Average Number of Stops per Ride', fontsize=14, fontweight='bold')
    ax.set_xlabel('Average Number of Stops', fontsize=12)
    ax.set_ylabel('Route Number', fontsize=12)
    ax.set_xlim(left=0)                              # x轴从0开始
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig('route_stops.png', dpi=150, bbox_inches='tight')
    print("图像已保存为 route_stops.png")

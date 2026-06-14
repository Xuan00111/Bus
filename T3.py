import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_route_stops(df, route_col='线路号', stops_col='ride_stops'):
    """
    计算各线路乘客的平均搭乘站点数及其标准差。

    Parameters
    ----------
    df : pd.DataFrame
        预处理后的数据集
    route_col : str
        线路号列名
    stops_col : str
        搭乘站点数列名

    Returns
    -------
    pd.DataFrame
        包含列：线路号、mean_stops、std_stops，按 mean_stops 降序排列
    """
    # 按线路分组，计算均值和标准差
    result = df.groupby(route_col)[stops_col].agg(mean_stops='mean', std_stops='std').reset_index()
    # 按 mean_stops 降序排列
    result = result.sort_values('mean_stops', ascending=False)
    return result


# ================= 主程序 =================
if __name__ == '__main__':
    # 1. 读取预处理后的数据
    df = pd.read_csv('cleaned_ICData.csv', parse_dates=['交易时间'])
    # 确保 ride_stops 为数值类型（防止读取时变字符串）
    df['ride_stops'] = pd.to_numeric(df['ride_stops'], errors='coerce')
    # 删除 ride_stops 为 NaN 的记录（若有）
    df = df.dropna(subset=['ride_stops'])

    # 注意：实际数据中线路列名为 '线路'，调用时传入正确的参数
    route_analysis = analyze_route_stops(df, route_col='线路', stops_col='ride_stops')

    # 打印结果（前10行）
    print("===== 各线路平均搭乘站点数（前10名）=====")
    print(route_analysis.head(10))

    # 2. 可视化：取均值最高的前15条线路
    top15 = route_analysis.head(15).copy()

    plt.figure(figsize=(10, 8))

    # 使用 Seaborn 调色板（Blues_d），颜色数量与数据行数一致
    palette = sns.color_palette("Blues_d", n_colors=len(top15))

    # 水平条形图：添加 hue='线路' 和 legend=False 以避免 FutureWarning
    ax = sns.barplot(
        data=top15,
        y='线路',
        x='mean_stops',
        hue='线路',          # 将线路号映射到色调
        palette=palette,
        orient='h',
        legend=False        # 关闭自动生成的图例（不需要）
    )

    # 手动添加误差棒（显示标准差），capsize=0.3
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

    # 设置英文标题和轴标签
    ax.set_title('Top 15 Routes by Average Number of Stops per Ride', fontsize=14, fontweight='bold')
    ax.set_xlabel('Average Number of Stops', fontsize=12)
    ax.set_ylabel('Route Number', fontsize=12)
    # x 轴从 0 起始
    ax.set_xlim(left=0)
    # 添加水平网格线（可选）
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    # 调整布局
    plt.tight_layout()
    # 保存图像，dpi=150
    plt.savefig('route_stops.png', dpi=150, bbox_inches='tight')
    print("图像已保存为 route_stops.png")
    # 如需显示，取消下面一行注释
    # plt.show()
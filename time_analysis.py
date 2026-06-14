import pandas as pd
import numpy as np


def main():
    # 读取预处理后的数据
    df = pd.read_csv('cleaned_ICData.csv', parse_dates=['交易时间'])
    # 确保 hour 列为整数（存储时可能变字符串，转换一下）
    df['hour'] = df['hour'].astype(int)

    # 重要：仅统计刷卡类型 = 0 的记录
    mask_type0 = df['刷卡类型'] == 0
    df_type0 = df[mask_type0]

    # 使用 numpy 数组，便于布尔索引
    hours = df_type0['hour'].to_numpy()

    # 1. 早峰前时段：hour < 7
    early_mask = hours < 7
    early_count = np.sum(early_mask)

    # 2. 深夜时段：hour >= 22
    late_mask = hours >= 22
    late_count = np.sum(late_mask)

    # 全天总刷卡量（刷卡类型=0的总记录数）
    total_count = len(hours)

    # 计算百分比
    early_pct = (early_count / total_count) * 100
    late_pct = (late_count / total_count) * 100

    # 打印结果
    print("===== 时段刷卡量统计（仅刷卡类型=0）=====")
    print(f"早峰前时段 (hour < 7) 刷卡量: {early_count}")
    print(f"占全天总刷卡量百分比: {early_pct:.2f}%")
    print(f"深夜时段 (hour >= 22) 刷卡量: {late_count}")
    print(f"占全天总刷卡量百分比: {late_pct:.2f}%")
    print(f"全天总刷卡量 (刷卡类型=0): {total_count}")


if __name__ == '__main__':
    main()
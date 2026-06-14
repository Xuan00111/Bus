import pandas as pd


def preprocess():
    # 读取原始数据
    df = pd.read_csv('ICData.csv', parse_dates=[1])

    # 提取小时字段
    df['hour'] = df['交易时间'].dt.hour

    # 计算搭乘站点数
    df['ride_stops'] = abs(df['下车站点'] - df['上车站点'])

    # 删除 ride_stops == 0 的记录
    deleted_ride = (df['ride_stops'] == 0).sum()
    df = df[df['ride_stops'] != 0]

    # 删除含有缺失值的记录
    before_dropna = len(df)
    df = df.dropna()
    deleted_missing = before_dropna - len(df)

    # 打印清洗信息
    print(f"预处理完成：")
    print(f" - 删除 ride_stops==0 记录: {deleted_ride}")
    print(f" - 删除缺失值记录: {deleted_missing}")
    print(f" - 最终数据量: {len(df)}")

    # 保存清洗后的数据
    df.to_csv('cleaned_ICData.csv', index=False)
    print("清洗后数据已保存为 cleaned_ICData.csv")

    return df


if __name__ == '__main__':
    preprocess()
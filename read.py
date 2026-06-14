import pandas as pd

# 1. 读取数据：自动使用第一行作为列名，并解析交易时间为 datetime
df = pd.read_csv('ICData.csv', parse_dates=[1])

# 打印原始数据基本信息
print("===== 原始数据 =====")
print(f"数据集形状: {df.shape}")
print(df.head())
print("\n各列数据类型：")
print(df.dtypes)

# 2. 时间解析：提取小时字段
df['hour'] = df['交易时间'].dt.hour

# 3. 构造衍生字段：搭乘站点数 = |下车站点 - 上车站点|
df['ride_stops'] = abs(df['下车站点'] - df['上车站点'])

# 记录删除前的行数
initial_rows = len(df)

# 删除 ride_stops == 0 的异常记录
df = df[df['ride_stops'] != 0]
deleted_rows_ride = initial_rows - len(df)
print(f"\n删除 ride_stops == 0 的记录数: {deleted_rows_ride}")

# 4. 缺失值检查：打印各列缺失值数量
print("\n各列缺失值数量：")
missing_counts = df.isnull().sum()
print(missing_counts[missing_counts > 0] if missing_counts.sum() > 0 else "无缺失值")

# 若存在缺失值，删除对应记录
if missing_counts.sum() > 0:
    before_dropna = len(df)
    df = df.dropna()
    after_dropna = len(df)
    print(f"删除缺失值记录数: {before_dropna - after_dropna}")
else:
    print("没有缺失值，无需删除")

# 最终数据信息
print("\n===== 处理后的数据 =====")
print(f"最终数据集形状: {df.shape}")
print(df.head())
import pandas as pd

# ========== 原有读取和输出（完全保持不变） ==========
df = pd.read_csv('ICData.csv', header=None)

print("数据集前 5 行：")
print(df.head())

print("\n数据集基本信息：")
print(f"行数: {df.shape[0]}")
print(f"列数: {df.shape[1]}")
print("\n各列数据类型：")
print(df.dtypes)

# ========== 新增：数据清洗与保存（不影响上述输出） ==========
# 1. 第0行是列名，去掉这一行，并重置索引
df_clean = df.iloc[1:].reset_index(drop=True)

# 2. 指定列名（根据示例数据字段顺序）
df_clean.columns = [
    '交易类型', '交易时间', '交易卡号', '刷卡类型',
    '线路', '车辆', '上车站点', '下车站点',
    '驾驶员编号', '运营公司编号'
]

# 3. 交易时间转换为 datetime 类型，并提取小时
df_clean['交易时间'] = pd.to_datetime(df_clean['交易时间'])
df_clean['hour'] = df_clean['交易时间'].dt.hour

# 4. 计算搭乘站点数 |下车站点 - 上车站点|
df_clean['ride_stops'] = abs(df_clean['下车站点'].astype(int) - df_clean['上车站点'].astype(int))

# 5. 删除 ride_stops == 0 的记录
initial_rows = len(df_clean)
df_clean = df_clean[df_clean['ride_stops'] != 0]
deleted_ride = initial_rows - len(df_clean)

# 6. 检查并删除缺失值
before_dropna = len(df_clean)
df_clean = df_clean.dropna()
deleted_missing = before_dropna - len(df_clean)

# 7. 可选：打印清洗统计信息（新增输出，但不影响原有输出）
print("\n[新增] 数据清洗统计：")
print(f"删除 ride_stops==0 的记录数: {deleted_ride}")
print(f"删除缺失值记录数: {deleted_missing}")
print(f"清洗后数据行数: {len(df_clean)}")

# 8. 保存清洗后的数据
df_clean.to_csv('cleaned_ICData.csv', index=False)
print("清洗后数据已保存为 cleaned_ICData.csv")
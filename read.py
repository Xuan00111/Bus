import pandas as pd

# 正确读取：自动使用第一行作为列名，并解析第2列（交易时间）为时间类型
df = pd.read_csv('ICData.csv', parse_dates=[1])

# 打印前5行
print("数据集前 5 行：")
print(df.head())

# 打印基本信息
print("\n数据集基本信息：")
print(f"行数: {df.shape[0]}")
print(f"列数: {df.shape[1]}")
print("\n各列数据类型：")
print(df.dtypes)
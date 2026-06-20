import pandas as pd

# 读取CSV，不含表头
df = pd.read_csv('ICData.csv', header=None)

# 第一行是列名，取出后从数据里去掉
col_names = df.iloc[0].tolist()
df_data = df.iloc[1:].copy()
df_data.columns = col_names
df_data = df_data.reset_index(drop=True)

# 批量转数值类型，转不了的（如交易时间）保持原样
for c in df_data.columns:
    try:
        df_data[c] = pd.to_numeric(df_data[c])
    except (ValueError, TypeError):
        pass

# ===== 1. 前5行预览 =====
print("数据集前5行：")
print(df_data.head(5).to_string())

# ===== 2. 基本信息 =====
n_rows, n_cols = df_data.shape
print(f"\n基本信息：")
print(f"行数={n_rows}, 列数={n_cols}")
print(df_data.dtypes)

# ===== 3. 构造 ride_stops 并清洗 =====
df_data['上车站点'] = pd.to_numeric(df_data['上车站点'], errors='coerce')
df_data['下车站点'] = pd.to_numeric(df_data['下车站点'], errors='coerce')

df_data['ride_stops'] = abs(df_data['下车站点'] - df_data['上车站点'])

# 删掉 ride_stops 为0或NaN的记录
before_clean = len(df_data)
df_clean = df_data[df_data['ride_stops'].notna() & (df_data['ride_stops'] != 0)]
after_clean = len(df_clean)
deleted_count = before_clean - after_clean

print(f"\n构造 ride_stops 后删除异常记录（ride_stops==0/无法计算）行数：{deleted_count}")

# ===== 4. 缺失值检查 =====
print("\n各列缺失值数量：")
missing = df_clean.isnull().sum()
if missing.sum() == 0:
    print("无缺失值")
else:
    for col in missing.index:
        if missing[col] > 0:
            print(f"{col}: {missing[col]}")

# ===== 5. 保存清洗结果 =====
df_clean.to_csv('cleaned_ICData.csv', index=False)
print("\n清洗后数据已保存为 cleaned_ICData.csv")

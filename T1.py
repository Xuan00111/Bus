import pandas as pd

# ========== 读取数据 ==========
df = pd.read_csv('ICData.csv', header=None)

# 提取列名（第一行）并设置
col_names = df.iloc[0].tolist()
df_data = df.iloc[1:].copy()
df_data.columns = col_names
df_data = df_data.reset_index(drop=True)

# 转换数据类型：尝试将数值列转为 int/float，时间列保持 object
for c in df_data.columns:
    try:
        df_data[c] = pd.to_numeric(df_data[c])
    except (ValueError, TypeError):
        pass  # 保持原类型（如交易时间）

# ========== 1. 数据集前 5 行 ==========
print("数据集前5行：")
print(df_data.head(5).to_string())

# ========== 2. 基本信息 ==========
n_rows, n_cols = df_data.shape
print(f"\n基本信息：")
print(f"行数={n_rows}, 列数={n_cols}")

# 各列数据类型
print(df_data.dtypes)

# ========== 3. 数据清洗：构造 ride_stops ==========
# 先将相关列转为数值
df_data['上车站点'] = pd.to_numeric(df_data['上车站点'], errors='coerce')
df_data['下车站点'] = pd.to_numeric(df_data['下车站点'], errors='coerce')

# 计算 ride_stops
df_data['ride_stops'] = abs(df_data['下车站点'] - df_data['上车站点'])

# 删除 ride_stops==0 或无法计算（NaN）的记录
before_clean = len(df_data)
df_clean = df_data[df_data['ride_stops'].notna() & (df_data['ride_stops'] != 0)]
after_clean = len(df_clean)
deleted_count = before_clean - after_clean

print(f"\n构造 ride_stops 后删除异常记录（ride_stops==0/无法计算）行数：{deleted_count}")

# ========== 4. 缺失值检查 ==========
print("\n各列缺失值数量：")
missing = df_clean.isnull().sum()
if missing.sum() == 0:
    print("无缺失值")
else:
    for col in missing.index:
        if missing[col] > 0:
            print(f"{col}: {missing[col]}")

# ========== 5. 保存清洗后数据 ==========
df_clean.to_csv('cleaned_ICData.csv', index=False)
print("\n清洗后数据已保存为 cleaned_ICData.csv")

import pandas as pd
import os

# 读取预处理后的数据
df = pd.read_csv('cleaned_ICData.csv', parse_dates=['交易时间'])

# 确保线路列为数值类型（若读取时为字符串则转换）
df['线路'] = pd.to_numeric(df['线路'], errors='coerce')
df = df.dropna(subset=['线路'])

# 1. 筛选线路号在 1101 至 1120 之间的记录
mask = (df['线路'] >= 1101) & (df['线路'] <= 1120)
df_filtered = df[mask].copy()

# 2. 创建文件夹（如果已存在则不报错）
output_dir = '线路驾驶员信息'
os.makedirs(output_dir, exist_ok=True)

# 存储生成的文件路径列表
file_paths = []

# 3. 对每条线路，提取车辆编号与驾驶员编号的去重对，写入文件
for route in range(1101, 1121):
    df_route = df_filtered[df_filtered['线路'] == route]
    # 提取 (车辆, 驾驶员) 去重对
    pairs = df_route[['车辆', '驾驶员编号']].drop_duplicates()
    # 按车辆编号排序（可选，便于查看）
    pairs = pairs.sort_values('车辆')

    # 文件路径
    file_path = os.path.join(output_dir, f'{route}.txt')

    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f'线路号: {route}\n')
        for _, row in pairs.iterrows():
            f.write(f'{int(row["车辆"])}\t{int(row["驾驶员编号"])}\n')

    file_paths.append(file_path)

# 4. 打印20个文件的生成路径
print('已生成以下文件：')
for path in file_paths:
    print(os.path.abspath(path))
print(f'共生成 {len(file_paths)} 个文件。')
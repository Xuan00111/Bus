import pandas as pd
import os

df = pd.read_csv('cleaned_ICData.csv', parse_dates=['交易时间'])  # 读取清洗数据

df['线路号'] = pd.to_numeric(df['线路号'], errors='coerce')      # 确保线路号是数值
df = df.dropna(subset=['线路号'])

# 筛选1101~1120线路
mask = (df['线路号'] >= 1101) & (df['线路号'] <= 1120)
df_filtered = df[mask].copy()

output_dir = '线路驾驶员信息'
os.makedirs(output_dir, exist_ok=True)                # 目标文件夹，已存在不报错

file_paths = []

# 逐线路提取 车辆-驾驶员 去重对
for route in range(1101, 1121):
    df_route = df_filtered[df_filtered['线路号'] == route]
    pairs = df_route[['车辆编号', '驾驶员编号']].drop_duplicates()
    pairs = pairs.sort_values('车辆编号')

    file_path = os.path.join(output_dir, f'{route}.txt')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f'线路号: {route}\n')
        for _, row in pairs.iterrows():
            f.write(f'{int(row["车辆编号"])}\t{int(row["驾驶员编号"])}\n')

    file_paths.append(file_path)

# 打印生成结果
print('已生成以下文件：')
for path in file_paths:
    print(os.path.abspath(path))
print(f'共生成 {len(file_paths)} 个文件。')

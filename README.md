# 李宇轩-25361107-第三次人工智能编程作业
仓库链接：https://github.com/Xuan00111/Bus
## 1. 任务拆解与 AI 协作策略

首先完成数据预处理，让AI在输出符合该任务输出要求的同时再生成一个预处理后的文件cleaned_ICData.csv；

然后完成任务2早晚时段刷卡量统计，读取清洗后的数据进行分析，提取出两个时段的刷卡量数值和计算二者占全天总刷卡量的百分比，接着完成24小时刷卡量分布可视化；

然后完成任务3线路站点分析，定义函数analyze_route_stops，读取清洗后数据实现计算各线路乘客的平均搭乘站点数及其标准差，然后使用seaborn完成可视化；

然后完成任务4高峰小时系数计算，根据全天分小时统计结果，自动找出刷卡量最大的小时作为高峰小时。然后在高峰小时内，按5分钟和15分钟粒度重新统计刷卡量、计算 PHF；

接着按要求完成任务5线路驾驶员信息批量导出功能、任务6服务绩效排名与热力图功能及其可视化；

将六个功能都独立写入脚本中，依次命名为T1、...、T6，作为独立的功能模块；

最后写一个main.py，通过系统菜单调用所需功能。

## 2. 核心 Prompt 迭代记录（示例）

原来的prompt：

首先读取数据：使用 pandas 读取 ICData.csv。打印数据集的前5行和基本信息（行数、列数、各列数据类型）。时间解析：将「交易时间」列转换为 pandas 的 datetime 类型，并从中提取「小时」字段（整数），新增为 hour 列。构造衍生字段：计算每条记录的「搭乘站点数」（即 |下车站点 - 上车站点|），新增为 ride_stops 列。若某行 ride_stops 为 0，视为异常记录，从数据集中删除，并打印删除行数。缺失值检查：打印各列缺失值数量。若存在缺失值，请删除对应记录。

更改后的prompt（使输出格式符合规范）：

首先读取数据：使用 pandas 读取 ICData.csv。打印数据集的前5行和基本信息（行数、列数、各列数据类型），注意ICData.csv有表头，打印时要输出表头，前五行的意思是前五行有效数据，就是一行表头加前五行的数据，总共六行，表头的那一行不用写序号，数据的五行序号是0~4。时间解析：将「交易时间」列转换为 pandas 的 datetime 类型，并从中提取「小时」字段（整数），新增为 hour 列。构造衍生字段：计算每条记录的「搭乘站点数」（即 |下车站点 - 上车站点|），新增为 ride_stops 列。若某行 ride_stops 为 0，视为异常记录，从数据集中删除，并打印删除行数。缺失值检查：打印各列缺失值数量。若存在缺失值，请删除对应记录。

## 3. Debug 记录（已省略一些原因重复的报错记录）

### 报错1：DtypeWarning 混合类型警告

```
D:\anaconda\envs\plane_env\python.exe C:\Users\YX\Desktop\公交IC卡\read.py
C:\Users\YX\Desktop\公交IC卡\read.py:4: DtypeWarning: Columns (0,2,3,4,5,6,7,8,9) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv('ICData.csv', header=None)
```

原因和解决：文件第一行为列名，未告诉AI，将原来代码 `df = pd.read_csv('ICData.csv', header=None)` 改为 `df = pd.read_csv('ICData.csv', parse_dates=[1])` 即可。

### 报错2：FileNotFoundError - 找不到 cleaned_ICData.csv

```
FileNotFoundError: [Errno 2] No such file or directory: 'cleaned_ICData.csv'
```

原因和解决：未运行更改后的preprocess.py，还未产生数据预处理后的cleaned_ICData.csv文件，重新运行preprocess.py后再运行time_analysis.py就可以了。

### 报错3：ModuleNotFoundError - 缺少 seaborn 模块

```
ModuleNotFoundError: No module named 'seaborn'
```

原因和解决：未安装seaborn库，安装后运行即可。

### 报错4：FutureWarning - seaborn barplot palette 参数即将弃用

```
FutureWarning: Passing `palette` without assigning `hue` is deprecated and will be removed in v0.14.0.
```

原因和解决：Seaborn 0.12+ 版本推荐显式使用 hue 来区分颜色映射。当只使用 palette 而不指定 hue 时，未来版本可能会移除这种隐式行为。通过 `hue='线路'`（即按线路号区分颜色）并设置 `legend=False`（避免生成重复的图例），效果与之前完全一致，且不再产生警告。

### 报错5：FileNotFoundError - T6.py 路径错误

```
FileNotFoundError: [Errno 2] No such file or directory: 'cleaned_ICData.csv'
```

原因和解决：不小心将T6.py文件放在任务5产生的线路驾驶员信息文件夹中，导致找不到cleaned_ICData.csv文件，剪切后粘贴在项目文件夹下与T5.py文件同一级就好。

### 报错6：KeyError - 列名 '线路' 不存在

```
KeyError: '线路'
```

原因和解决：cleaned_ICData.csv 中线路列名是线路号，而T3.py 第 41 行写的是 `route_col='线路'`，groupby 找不到这个列就抛了KeyError。将 `route_col='线路'` 改为 `route_col='线路号'` 即可。

### 报错7：KeyError - 列名 'hour' 不存在

```
KeyError: 'hour'
```

原因和解决：cleaned_ICData.csv 里没有 hour 列（清洗时只存了原始字段 + ride_stops），而 T2 第 10 行直接 `df['hour']` 取值，导致KeyError。把 `df['hour'] = df['hour'].astype(int)` 改成从交易时间提取 `df['hour'] = df['交易时间'].dt.hour`。

## 4. 人工代码审查（逐行中文注释）

```python
# ----- 5分钟粒度 -----
# 将高峰小时按5分钟切分为12个窗口（0~11号），统计每个窗口的刷卡量
# 窗口编号 = 记录所在分钟 - 高峰小时起始分钟，再除以5取整
df_peak['win5'] = (df_peak['minute_of_day'] - base_minute) // 5  # 窗口编号0~11
win5_counts = df_peak.groupby('win5').size()     # 每窗口刷卡量
max_win5_count = win5_counts.max()               # 所有窗口中最大的刷卡量
max_win5_idx = win5_counts.idxmax()              # 最大窗口的编号

# 反推最大窗口的实际时间范围（起始分钟 → hh:mm 格式）
win5_start_min = base_minute + max_win5_idx * 5
win5_end_min = win5_start_min + 5
win5_start_time = f"{win5_start_min // 60:02d}:{win5_start_min % 60:02d}"
win5_end_time = f"{win5_end_min // 60:02d}:{win5_end_min % 60:02d}"

# PHF5 = 高峰小时总刷卡量 / (12 × 最大5分钟窗口刷卡量)
# 比值越接近1说明高峰小时内客流越均匀，越小说明集中在某个5分钟
PHF5 = peak_volume / (12 * max_win5_count)

# ----- 15分钟粒度 -----
# 同理，将高峰小时按15分钟切分为4个窗口（0~3号），统计每个窗口的刷卡量
# 窗口编号 = 记录所在分钟 - 高峰小时起始分钟，再除以15取整
df_peak['win15'] = (df_peak['minute_of_day'] - base_minute) // 15  # 窗口编号0~3
win15_counts = df_peak.groupby('win15').size()     # 每窗口刷卡量
max_win15_count = win15_counts.max()               # 所有窗口中最大的刷卡量
max_win15_idx = win15_counts.idxmax()              # 最大窗口的编号

# 反推最大窗口的实际时间范围
win15_start_min = base_minute + max_win15_idx * 15
win15_end_min = win15_start_min + 15
win15_start_time = f"{win15_start_min // 60:02d}:{win15_start_min % 60:02d}"
win15_end_time = f"{win15_end_min // 60:02d}:{win15_end_min % 60:02d}"

# PHF15 = 高峰小时总刷卡量 / (4 × 最大15分钟窗口刷卡量)
PHF15 = peak_volume / (4 * max_win15_count)
```

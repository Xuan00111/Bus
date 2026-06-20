"""
main.py — 公共交通IC刷卡数据分析系统 主菜单
=============================================
通过系统菜单可单独调用 T1~T6 任一功能，也可一键运行全部功能。
"""
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # 脚本所在目录

# 任务注册表：编号 → 脚本文件 + 描述
TASKS = {
    '1': {'file': 'T1.py', 'desc': '数据清洗与预处理'},
    '2': {'file': 'T2.py', 'desc': '早晚时段刷卡量统计与24小时分布可视化'},
    '3': {'file': 'T3.py', 'desc': '线路站点分析（平均搭乘站点数）与可视化'},
    '4': {'file': 'T4.py', 'desc': '高峰小时系数（PHF5/PHF15）计算'},
    '5': {'file': 'T5.py', 'desc': '线路驾驶员信息批量导出'},
    '6': {'file': 'T6.py', 'desc': '服务绩效排名与热力图'},
}


def run_task(task_id: str):
    """读取并执行单个任务脚本"""
    task = TASKS[task_id]
    filepath = os.path.join(SCRIPT_DIR, task['file'])

    print(f"\n{'=' * 60}")
    print(f"  正在执行 [{task_id}] {task['desc']}")
    print(f"  脚本：{task['file']}")
    print(f"{'=' * 60}\n")

    try:
        with open(filepath, encoding='utf-8') as f:
            exec(compile(f.read(), filepath, 'exec'))  # 编译后执行，出错能定位到脚本行号
        print(f"\n✓ [{task_id}] {task['file']} 执行完毕。")
    except Exception as e:
        print(f"\n✗ [{task_id}] {task['file']} 执行出错：{e}")


def run_all():
    """顺序执行 T1 → T6"""
    print("\n" + "=" * 60)
    print("  一键运行全部任务（T1 → T6）")
    print("=" * 60)

    for task_id in ['1', '2', '3', '4', '5', '6']:
        run_task(task_id)

    print("\n" + "=" * 60)
    print("  全部 6 个任务执行完毕！")
    print("=" * 60)


def show_menu():
    """打印系统主菜单"""
    print("\n" + "=" * 60)
    print("   公共交通IC刷卡数据分析系统")
    print("=" * 60)
    print("\n  💡 提示：也可直接在命令行运行 python T1.py ~ python T6.py")
    print("      来单独执行对应任务。\n")
    for key in ['1', '2', '3', '4', '5', '6']:
        print(f"    [{key}]  {TASKS[key]['desc']}")
    print(f"\n    [A]  一键运行全部任务（T1 → T6）")
    print(f"    [Q]  退出系统")
    print("-" * 60)


def main():
    """主循环：显示菜单 → 读取输入 → 执行对应操作"""
    while True:
        show_menu()
        try:
            choice = input("请输入选项（1-6 / A / Q）：").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\n感谢使用，再见！")
            break

        if choice == 'Q':
            print("感谢使用，再见！")
            break
        elif choice == 'A':
            run_all()
        elif choice in TASKS:
            run_task(choice)
        else:
            print(f"⚠ 无效选项 '{choice}'，请重新输入。")


if __name__ == '__main__':
    main()

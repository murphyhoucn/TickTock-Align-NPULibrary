import os
import re
from collections import defaultdict
from datetime import datetime, timedelta
import calendar

def scan_all_photos_in_directory(base_directory):
    """
    扫描基础目录下所有子文件夹中的照片
    返回按日期分组的照片统计
    """
    photo_stats = defaultdict(int)  # key: 'YYYY-MM-DD', value: count
    
    if not os.path.exists(base_directory):
        print(f"错误：目录 {base_directory} 不存在")
        return photo_stats
    
    print(f"正在扫描目录：{base_directory}")
    folder_count = 0
    total_photos = 0
    
    # 遍历所有子文件夹
    for item in os.listdir(base_directory):
        item_path = os.path.join(base_directory, item)
        
        # 只处理文件夹
        if os.path.isdir(item_path):
            folder_count += 1
            folder_photos = 0
            
            # 扫描文件夹中的照片
            try:
                for filename in os.listdir(item_path):
                    if filename.startswith("IMG_") and filename.endswith(".jpg"):
                        try:
                            # 从文件名提取日期：IMG_20230901_114129.jpg
                            date_str = filename[4:12]  # 20230901
                            date_obj = datetime.strptime(date_str, "%Y%m%d")
                            date_key = date_obj.strftime("%Y-%m-%d")
                            
                            photo_stats[date_key] += 1
                            folder_photos += 1
                            total_photos += 1
                            
                        except ValueError:
                            # 如果日期解析失败，跳过这个文件
                            continue
                            
            except PermissionError:
                print(f"警告：无法访问文件夹 {item_path}")
                continue
            
            if folder_photos > 0:
                print(f"  📁 {item}: {folder_photos} 张照片")
    
    print(f"\n扫描完成：")
    print(f"  📁 总文件夹数：{folder_count}")
    print(f"  📸 总照片数：{total_photos}")
    print(f"  📅 拍照天数：{len(photo_stats)}")
    
    return photo_stats

def generate_date_range(start_date, end_date):
    """
    生成指定日期范围内的所有日期
    """
    dates = []
    current_date = start_date
    
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    
    return dates

def validate_date_handling():
    """
    验证日期处理的正确性，特别是月份天数和闰年
    """
    print("\n🔍 验证日期处理...")
    
    test_cases = [
        (2023, 2),  # 2023年2月 - 平年，28天
        (2024, 2),  # 2024年2月 - 闰年，29天
        (2025, 2),  # 2025年2月 - 平年，28天
        (2023, 4),  # 2023年4月 - 30天
        (2023, 12), # 2023年12月 - 31天
    ]
    
    for year, month in test_cases:
        days_in_month = calendar.monthrange(year, month)[1]
        is_leap = calendar.isleap(year)
        
        print(f"  {year}年{month:02d}月：{days_in_month}天", end="")
        if month == 2:
            print(f" ({'闰年' if is_leap else '平年'})", end="")
        print()
    
    print("✅ 日期处理验证完成")

def print_monthly_statistics(photo_stats, start_date, end_date):
    """
    按月度打印统计信息，确保正确处理每月天数
    """
    print("\n" + "=" * 80)
    print("📊 月度统计报告")
    print("=" * 80)
    
    # 按年月分组统计
    monthly_stats = defaultdict(lambda: {'total_photos': 0, 'photo_days': 0, 'total_days': 0})
    
    current_date = start_date
    while current_date <= end_date:
        year_month = f"{current_date.year}-{current_date.month:02d}"
        date_key = current_date.strftime("%Y-%m-%d")
        
        monthly_stats[year_month]['total_days'] += 1
        
        if date_key in photo_stats:
            monthly_stats[year_month]['total_photos'] += photo_stats[date_key]
            monthly_stats[year_month]['photo_days'] += 1
        
        current_date += timedelta(days=1)
    
    # 打印月度统计
    for year_month in sorted(monthly_stats.keys()):
        year, month = year_month.split('-')
        year, month = int(year), int(month)
        stats = monthly_stats[year_month]
        
        # 验证天数是否正确
        expected_days = calendar.monthrange(year, month)[1]
        actual_days = stats['total_days']
        
        photo_rate = (stats['photo_days'] / stats['total_days']) * 100 if stats['total_days'] > 0 else 0
        
        print(f"\n📅 {year}年{month:02d}月：")
        print(f"   总天数：{stats['total_days']} 天", end="")
        if actual_days != expected_days:
            print(f" ⚠️ (期望{expected_days}天)", end="")
        print()
        print(f"   拍照天数：{stats['photo_days']} 天")
        print(f"   未拍天数：{stats['total_days'] - stats['photo_days']} 天")
        print(f"   总照片数：{stats['total_photos']} 张")
        print(f"   拍照率：{photo_rate:.1f}%")

def print_yearly_statistics(photo_stats, start_date, end_date):
    """
    按年度打印统计信息
    """
    print("\n" + "=" * 80)
    print("📊 年度统计报告")
    print("=" * 80)
    
    # 按年份分组统计
    yearly_stats = defaultdict(lambda: {'total_photos': 0, 'photo_days': 0, 'total_days': 0})
    
    current_date = start_date
    while current_date <= end_date:
        year = current_date.year
        date_key = current_date.strftime("%Y-%m-%d")
        
        yearly_stats[year]['total_days'] += 1
        
        if date_key in photo_stats:
            yearly_stats[year]['total_photos'] += photo_stats[date_key]
            yearly_stats[year]['photo_days'] += 1
        
        current_date += timedelta(days=1)
    
    # 打印年度统计
    for year in sorted(yearly_stats.keys()):
        stats = yearly_stats[year]
        photo_rate = (stats['photo_days'] / stats['total_days']) * 100 if stats['total_days'] > 0 else 0
        
        # 验证年度天数
        is_leap = calendar.isleap(year)
        expected_days_in_year = 366 if is_leap else 365
        
        print(f"\n📅 {year}年{'(闰年)' if is_leap else '(平年)'}：")
        print(f"   总天数：{stats['total_days']} 天")
        print(f"   拍照天数：{stats['photo_days']} 天")
        print(f"   未拍天数：{stats['total_days'] - stats['photo_days']} 天")
        print(f"   总照片数：{stats['total_photos']} 张")
        print(f"   拍照率：{photo_rate:.1f}%")

def print_detailed_statistics(photo_stats, start_date, end_date):
    """
    打印详细的每日统计信息
    """
    print("\n" + "=" * 80)
    print("📸 详细每日拍照统计 (2023.09.01 - 2026.04.01)")
    print("=" * 80)
    
    current_date = start_date
    current_year_month = None
    
    while current_date <= end_date:
        year_month = current_date.strftime("%Y年%m月")
        date_key = current_date.strftime("%Y-%m-%d")
        
        # 如果是新的月份，打印月份标题
        if year_month != current_year_month:
            if current_year_month is not None:
                print()  # 月份之间空一行
            print(f"\n🗓️  {year_month}")
            print("-" * 50)
            current_year_month = year_month
        
        # 打印每日情况
        day = current_date.day
        if date_key in photo_stats:
            count = photo_stats[date_key]
            print(f"{day:02d}日：✅ {count} 张照片")
        else:
            print(f"{day:02d}日：❌ 未拍照")
        
        current_date += timedelta(days=1)

def main():
    """
    主函数
    """
    print("=" * 80)
    print("📸 NPU-Everyday 全量照片统计系统")
    print("📅 统计期间：2023.09.01 - 2026.04.01")
    print("=" * 80)
    
    # 获取 NPU-Everyday 目录路径
    # base_directory = input("\n请输入 NPU-Everyday 目录路径: ").strip()

    base_directory = r"D:\\DevProj\\TickTock-Align-NPULibrary\\NPU-Everyday"

    # 去除可能的引号
    if base_directory.startswith('"') and base_directory.endswith('"'):
        base_directory = base_directory[1:-1]
    
    if not base_directory:
        print("❌ 请输入有效的目录路径")
        return
    
    # 定义统计日期范围
    start_date = datetime(2023, 9, 1)
    end_date = datetime(2026, 4, 30)
    
    print(f"开始统计时间范围：{start_date.strftime('%Y年%m月%d日')} - {end_date.strftime('%Y年%m月%d日')}")
    
    # 扫描所有照片
    print("\n🔍 开始扫描照片...")
    photo_stats = scan_all_photos_in_directory(base_directory)
    
    if not photo_stats:
        print("❌ 没有找到任何照片文件")
        return
    
    # 验证日期处理
    validate_date_handling()
    
    # 询问显示模式
    print("\n请选择显示模式：")
    print("1. 年度汇总统计")
    print("2. 月度详细统计")
    print("3. 详细每日统计")
    print("4. 全部显示")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    if choice in ['1', '4']:
        print_yearly_statistics(photo_stats, start_date, end_date)
    
    if choice in ['2', '4']:
        print_monthly_statistics(photo_stats, start_date, end_date)
    
    if choice in ['3', '4']:
        print_detailed_statistics(photo_stats, start_date, end_date)
    
    # 总体统计
    total_days = (end_date - start_date).days + 1
    photo_days = len(photo_stats)
    total_photos = sum(photo_stats.values())
    no_photo_days = total_days - photo_days
    photo_rate = (photo_days / total_days) * 100
    
    print("\n" + "=" * 80)
    print("📊 总体统计汇总")
    print("=" * 80)
    print(f"📅 统计期间：{start_date.strftime('%Y年%m月%d日')} - {end_date.strftime('%Y年%m月%d日')}")
    print(f"📈 总天数：{total_days} 天")
    print(f"✅ 拍照天数：{photo_days} 天")
    print(f"❌ 未拍天数：{no_photo_days} 天")
    print(f"📸 总照片数：{total_photos} 张")
    print(f"📊 拍照率：{photo_rate:.1f}%")
    
    if photo_days > 0:
        avg_photos_per_day = total_photos / photo_days
        print(f"📷 平均每拍照日：{avg_photos_per_day:.1f} 张")

if __name__ == "__main__":
    main()
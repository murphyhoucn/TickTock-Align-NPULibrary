#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TickTock-Align-NPU Library 快速启动脚本

这个脚本提供了一个简单的界面来运行图像对齐和延时摄影功能
"""

import os
import sys
from pathlib import Path

def print_banner():
    """打印横幅"""
    print("████████╗██╗ ██████╗██╗  ██╗████████╗ ██████╗  ██████╗██╗  ██╗")
    print("╚══██╔══╝██║██╔════╝██║ ██╔╝╚══██╔══╝██╔═══██╗██╔════╝██║ ██╔╝")
    print("   ██║   ██║██║     █████╔╝    ██║   ██║   ██║██║     █████╔╝ ")
    print("   ██║   ██║██║     ██╔═██╗    ██║   ██║   ██║██║     ██╔═██╗ ")
    print("   ██║   ██║╚██████╗██║  ██╗   ██║   ╚██████╔╝╚██████╗██║  ██╗")
    print("   ╚═╝   ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝╚═╝  ╚═╝")
    print()
    print("TickTock-Align-NPU Library")
    print("建筑物图像对齐 + 延时摄影制作工具")
    print("=" * 60)

def check_files():
    """检查必要文件是否存在"""
    required_files = [
        "align_lib.py",
        "create_timelapse.py", 
        "demo.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 所有必要文件已存在")
    return True

def check_input_dir():
    """检查输入目录"""
    input_dir = Path("NPU-Lib")
    if not input_dir.exists():
        print("❌ 输入目录 NPU-Lib 不存在")
        return False
    
    image_files = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.jpeg"))
    if len(image_files) < 2:
        print(f"❌ 图像文件不足: 找到 {len(image_files)} 张，至少需要 2 张")
        return False
    
    print(f"✅ 找到 {len(image_files)} 张输入图像")
    return True

def show_menu():
    """显示菜单"""
    print("\n📋 可用功能:")
    print("1. 完整流程 (图像对齐 + 延时摄影)")
    print("2. 仅图像对齐")
    print("3. 仅延时摄影 (需要已对齐的图像)")
    print("4. 查看帮助")
    print("5. 退出")
    print()

def run_command(cmd):
    """运行命令"""
    print(f"🚀 执行命令: {cmd}")
    print("-" * 40)
    return os.system(cmd)

def main():
    """主函数"""
    print_banner()
    
    # 检查文件
    if not check_files():
        input("按回车键退出...")
        return
    
    # 检查输入目录
    if not check_input_dir():
        input("按回车键退出...")
        return
    
    while True:
        show_menu()
        choice = input("请选择功能 (1-5): ").strip()
        
        if choice == "1":
            print("🔄 运行完整流程...")
            result = run_command("python demo.py")
            if result == 0:
                print("✅ 完整流程执行成功!")
            else:
                print("❌ 执行失败，请检查错误信息")
        
        elif choice == "2":
            print("🔄 仅运行图像对齐...")
            result = run_command("python demo.py --align-only")
            if result == 0:
                print("✅ 图像对齐完成!")
            else:
                print("❌ 图像对齐失败，请检查错误信息")
        
        elif choice == "3":
            print("🎬 仅创建延时摄影...")
            result = run_command("python demo.py --video-only")
            if result == 0:
                print("✅ 延时摄影创建完成!")
            else:
                print("❌ 延时摄影创建失败，请检查错误信息")
        
        elif choice == "4":
            print("📖 查看帮助信息:")
            print()
            print("使用方法:")
            print("  python demo.py                    # 完整流程")
            print("  python demo.py --align-only       # 仅图像对齐")
            print("  python demo.py --video-only       # 仅延时摄影")
            print("  python demo.py --reference 2      # 使用第3张图像作为参考")
            print()
            print("分步执行:")
            print("  python align_lib.py               # 图像对齐")
            print("  python create_timelapse.py        # 延时摄影")
            print()
            print("详细文档:")
            print("  USAGE.md - 完整使用指南")
            print("  README.md - 项目介绍")
        
        elif choice == "5":
            print("👋 感谢使用 TickTock-Align-NPU Library!")
            break
        
        else:
            print("❌ 无效选择，请输入 1-5")
        
        print()
        input("按回车键继续...")
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
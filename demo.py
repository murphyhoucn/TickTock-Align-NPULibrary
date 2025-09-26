#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TickTock-Align-NPU Library 完整演示

这个演示脚本整合了图像对齐和延时摄影视频制作功能。

工作流程:
1. 使用 align_lib.py 对齐图像序列
2. 使用 create_timelapse.py 制作延时摄影视频

功能特点:
- 智能图像对齐（基于SIFT特征点匹配）
- 自动延时摄影视频生成
- 多种视频质量选项
- 完整的日志记录
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# 导入自定义模块
from align_lib import TickTockAlign
from create_timelapse import create_file_list, create_timelapse_video

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_banner():
    """打印程序横幅"""
    print("████████╗██╗ ██████╗██╗  ██╗████████╗ ██████╗  ██████╗██╗  ██╗")
    print("╚══██╔══╝██║██╔════╝██║ ██╔╝╚══██╔══╝██╔═══██╗██╔════╝██║ ██╔╝")
    print("   ██║   ██║██║     █████╔╝    ██║   ██║   ██║██║     █████╔╝ ")
    print("   ██║   ██║██║     ██╔═██╗    ██║   ██║   ██║██║     ██╔═██╗ ")
    print("   ██║   ██║╚██████╗██║  ██╗   ██║   ╚██████╔╝╚██████╗██║  ██╗")
    print("   ╚═╝   ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝╚═╝  ╚═╝")
    print()
    print("TickTock-Align-NPU Library 完整演示")
    print("建筑物图像对齐 + 延时摄影视频制作")
    print("=" * 60)

def check_environment():
    """检查运行环境"""
    logger.info("检查运行环境...")
    
    # 检查输入目录
    input_dir = Path("NPU-Lib")
    if not input_dir.exists():
        logger.error("❌ 输入目录 NPU-Lib 不存在")
        return False
    
    # 检查图像文件
    image_files = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.jpeg"))
    if len(image_files) < 2:
        logger.error(f"❌ 图像文件不足：找到 {len(image_files)} 张，至少需要 2 张")
        return False
    
    logger.info(f"✅ 找到 {len(image_files)} 张输入图像")
    
    # 检查输出目录
    output_dir = Path("NPU-Lib-Align")
    output_dir.mkdir(exist_ok=True)
    logger.info(f"✅ 输出目录准备完成：{output_dir}")
    
    # 检查视频输出目录
    video_dir = Path("Video")
    video_dir.mkdir(exist_ok=True)
    logger.info(f"✅ 视频输出目录准备完成：{video_dir}")
    
    return True

def align_images(input_dir="NPU-Lib", output_dir="NPU-Lib-Align", reference_index=0):
    """
    对齐图像序列
    
    Args:
        input_dir (str): 输入图像目录
        output_dir (str): 输出图像目录
        reference_index (int): 参考图像索引
        
    Returns:
        bool: 是否成功完成对齐
    """
    logger.info("🔄 开始图像对齐处理...")
    
    try:
        # 创建对齐器
        aligner = TickTockAlign(
            input_dir=input_dir,
            output_dir=output_dir,
            reference_index=reference_index
        )
        
        # 执行对齐
        aligner.process_images()
        
        # 检查输出结果
        output_path = Path(output_dir)
        aligned_images = list(output_path.glob("*.jpg")) + list(output_path.glob("*.jpeg"))
        
        if len(aligned_images) > 1:
            logger.info(f"✅ 图像对齐完成！生成 {len(aligned_images)} 张对齐图像")
            return True
        else:
            logger.error("❌ 图像对齐失败，输出图像数量不足")
            return False
            
    except Exception as e:
        logger.error(f"❌ 图像对齐过程中发生错误：{e}")
        return False

def create_videos(aligned_dir="NPU-Lib-Align", video_dir="Video"):
    """
    创建延时摄影视频
    
    Args:
        aligned_dir (str): 对齐图像目录
        video_dir (str): 视频输出目录
        
    Returns:
        int: 成功创建的视频数量
    """
    logger.info("🎬 开始创建延时摄影视频...")
    
    # 检查对齐图像
    aligned_path = Path(aligned_dir)
    if not aligned_path.exists():
        logger.error(f"❌ 对齐图像目录不存在：{aligned_dir}")
        return 0
    
    jpg_files = list(aligned_path.glob("*.jpg"))
    if len(jpg_files) < 2:
        logger.error(f"❌ 对齐图像数量不足：{len(jpg_files)} 张")
        return 0
    
    logger.info(f"📷 找到 {len(jpg_files)} 张对齐图像")
    
    # 创建文件列表
    file_list_path = create_file_list()
    if not file_list_path:
        logger.error("❌ 创建文件列表失败")
        return 0
    
    videos_created = 0
    video_configs = [
        ("preview", 30, 23, "快速预览版"),
        ("standard", 15, 20, "标准版"),
        ("hq", 10, 18, "高质量版")
    ]
    
    try:
        for suffix, framerate, quality, description in video_configs:
            output_file = f"{video_dir}/timelapse_{suffix}.mp4"
            logger.info(f"🎬 创建{description}...")
            
            if create_timelapse_video(file_list_path, output_file, framerate, quality):
                videos_created += 1
                
                # 显示文件信息
                if os.path.exists(output_file):
                    file_size = os.path.getsize(output_file) / (1024 * 1024)
                    logger.info(f"✅ {description}创建成功：{output_file} ({file_size:.1f} MB)")
            else:
                logger.warning(f"⚠️ {description}创建失败")
    
    finally:
        # 清理临时文件
        if os.path.exists(file_list_path):
            os.unlink(file_list_path)
            logger.info(f"🧹 清理临时文件：{file_list_path}")
    
    return videos_created

def display_results(output_dir="NPU-Lib-Align", video_dir="Video"):
    """显示处理结果"""
    print("\n" + "=" * 60)
    print("📊 处理结果统计")
    print("=" * 60)
    
    # 对齐图像统计
    aligned_path = Path(output_dir)
    if aligned_path.exists():
        aligned_images = list(aligned_path.glob("*.jpg")) + list(aligned_path.glob("*.jpeg"))
        print(f"📷 对齐图像：{len(aligned_images)} 张")
        print(f"📁 保存位置：{aligned_path.resolve()}")
    
    # 视频文件统计
    video_path = Path(video_dir)
    if video_path.exists():
        video_files = list(video_path.glob("*.mp4"))
        print(f"🎬 视频文件：{len(video_files)} 个")
        
        total_size = 0
        for video_file in video_files:
            if video_file.exists():
                size = os.path.getsize(video_file) / (1024 * 1024)
                total_size += size
                print(f"   • {video_file.name} ({size:.1f} MB)")
        
        if total_size > 0:
            print(f"📦 总大小：{total_size:.1f} MB")
        print(f"📁 保存位置：{video_path.resolve()}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='TickTock-Align-NPU Library 完整演示')
    parser.add_argument('--input', '-i', default='NPU-Lib', 
                       help='输入图像文件夹路径 (默认: NPU-Lib)')
    parser.add_argument('--output', '-o', default='NPU-Lib-Align', 
                       help='输出图像文件夹路径 (默认: NPU-Lib-Align)')
    parser.add_argument('--video', '-v', default='Video',
                       help='视频输出文件夹路径 (默认: Video)')
    parser.add_argument('--reference', '-r', type=int, default=0, 
                       help='参考图像索引 (默认: 0，即第一张图像)')
    parser.add_argument('--align-only', action='store_true',
                       help='仅执行图像对齐，不创建视频')
    parser.add_argument('--video-only', action='store_true',
                       help='仅创建视频，不执行图像对齐')
    
    args = parser.parse_args()
    
    # 打印横幅
    print_banner()
    
    # 检查环境
    if not check_environment():
        logger.error("❌ 环境检查失败，程序退出")
        sys.exit(1)
    
    success_count = 0
    
    # 执行图像对齐
    if not args.video_only:
        if align_images(args.input, args.output, args.reference):
            success_count += 1
        else:
            logger.error("❌ 图像对齐失败")
            if not args.align_only:
                logger.info("⚠️ 继续尝试视频创建...")
    
    # 创建延时摄影视频
    if not args.align_only:
        videos_created = create_videos(args.output, args.video)
        if videos_created > 0:
            success_count += 1
            logger.info(f"✅ 创建了 {videos_created} 个视频文件")
        else:
            logger.error("❌ 视频创建失败")
    
    # 显示结果
    display_results(args.output, args.video)
    
    # 最终状态
    print("\n" + "=" * 60)
    if success_count > 0:
        print("🎉 处理完成！")
        if not args.video_only:
            print(f"✅ 对齐图像保存在：{args.output}")
        if not args.align_only:
            print(f"✅ 视频文件保存在：{args.video}")
    else:
        print("❌ 处理失败，请检查日志信息")
        sys.exit(1)

if __name__ == "__main__":
    main()
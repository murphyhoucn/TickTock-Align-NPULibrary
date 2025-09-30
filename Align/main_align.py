#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TickTock-Main-Align Library

主要图像对齐库，整合了深度学习和增强传统方法。
提供两种对齐策略：
1. 深度学习方法 (superpoint) - 基于LoFTR的现代深度学习对齐
2. 增强传统方法 (enhanced) - 增强的SIFT+模板匹配组合方法

功能特点:
- 智能方法选择和回退
- 保持目录结构的输出
- 统一的处理接口
- 详细的处理报告
"""

import cv2
import numpy as np
from pathlib import Path
import argparse
import logging
import time
import sys
import warnings
warnings.filterwarnings('ignore')

# 导入两个对齐模块
try:
    from .superpoint import DeepLearningAlign
    DL_AVAILABLE = True
except ImportError:
    DL_AVAILABLE = False
    logging.warning("深度学习对齐模块不可用")

try:
    from .enhanced import EnhancedAlign
    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False
    logging.warning("增强对齐模块不可用")

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MainAlign:
    """
    主要图像对齐类 - 整合深度学习和增强传统方法
    """
    
    def __init__(self, input_dir="NPU-Everyday-Sample", output_dir="NPU-Everyday-Sample_Aligned", 
                 reference_index=0, method="auto"):
        """
        初始化主要对齐器
        
        Args:
            input_dir (str): 输入图像文件夹路径
            output_dir (str): 输出对齐图像文件夹路径
            reference_index (int): 参考图像索引
            method (str): 对齐方法选择
                        - "superpoint": 深度学习LoFTR方法
                        - "enhanced": 增强传统SIFT+模板匹配方法
                        - "auto": 自动选择最佳方法
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.reference_index = reference_index
        self.method = method
        
        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查可用的对齐方法
        self.available_methods = []
        if DL_AVAILABLE:
            self.available_methods.append("superpoint")
        if ENHANCED_AVAILABLE:
            self.available_methods.append("enhanced")
            
        if not self.available_methods:
            raise RuntimeError("没有可用的对齐方法！请检查依赖模块。")
        
        logger.info(f"可用的对齐方法: {', '.join(self.available_methods)}")
        
        # 初始化对齐器
        self.aligner = None
        self.selected_method = None
        self._init_aligner()
    
    def _init_aligner(self):
        """初始化具体的对齐器"""
        if self.method == "auto":
            # 自动选择最佳方法
            if "superpoint" in self.available_methods:
                self.selected_method = "superpoint"
                logger.info("🚀 自动选择深度学习方法 (superpoint)")
            else:
                self.selected_method = "enhanced"
                logger.info("🔧 自动选择增强传统方法 (enhanced)")
        else:
            if self.method not in self.available_methods:
                logger.warning(f"请求的方法 '{self.method}' 不可用，回退到可用方法")
                self.selected_method = self.available_methods[0]
            else:
                self.selected_method = self.method
        
        # 创建对应的对齐器
        if self.selected_method == "superpoint":
            self.aligner = DeepLearningAlign(
                input_dir=str(self.input_dir),
                output_dir=str(self.output_dir),
                reference_index=self.reference_index
            )
            logger.info("✅ 深度学习对齐器初始化完成")
            
        elif self.selected_method == "enhanced":
            self.aligner = EnhancedAlign(
                input_dir=str(self.input_dir),
                output_dir=str(self.output_dir),
                reference_index=self.reference_index
            )
            logger.info("✅ 增强传统对齐器初始化完成")
    
    def get_image_files(self):
        """获取所有图像文件"""
        image_files = []
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        
        for ext in image_extensions:
            image_files.extend(list(self.input_dir.rglob(f"*{ext}")))
            image_files.extend(list(self.input_dir.rglob(f"*{ext.upper()}")))
        
        image_files = list(set([str(f) for f in image_files]))
        image_files.sort()
        return image_files
    
    def preserve_directory_structure(self):
        """保持目录结构的对齐处理"""
        logger.info("🔄 开始保持目录结构的图像对齐处理...")
        
        # 获取所有图像文件
        image_files = self.get_image_files()
        if not image_files:
            logger.error(f"❌ 在 {self.input_dir} 中未找到图像文件")
            return False
        
        logger.info(f"📁 找到 {len(image_files)} 张图像")
        
        # 先执行基础对齐到临时目录
        temp_output = self.output_dir / "temp_aligned"
        temp_output.mkdir(exist_ok=True)
        
        # 创建临时对齐器
        if self.selected_method == "superpoint":
            temp_aligner = DeepLearningAlign(
                input_dir=str(self.input_dir),
                output_dir=str(temp_output),
                reference_index=self.reference_index
            )
        else:
            temp_aligner = EnhancedAlign(
                input_dir=str(self.input_dir),
                output_dir=str(temp_output),
                reference_index=self.reference_index
            )
        
        # 执行对齐
        logger.info(f"🎯 使用 {self.selected_method} 方法进行对齐...")
        temp_aligner.process_images()
        
        # 重新组织文件到原有目录结构
        self._reorganize_files(temp_output, image_files)
        
        # 清理临时目录
        import shutil
        shutil.rmtree(temp_output)
        
        # 生成最终报告
        self._generate_main_report(image_files)
        
        logger.info("✅ 保持目录结构的对齐处理完成！")
        return True
    
    def _reorganize_files(self, temp_output, original_files):
        """重新组织文件到原有目录结构"""
        logger.info("📂 重新组织文件到原有目录结构...")
        
        for original_file in original_files:
            original_path = Path(original_file)
            filename = original_path.name
            
            # 在临时输出目录中找到对应的对齐文件
            aligned_file = temp_output / filename
            if aligned_file.exists():
                # 计算相对于输入目录的路径
                relative_path = original_path.relative_to(self.input_dir)
                
                # 创建对应的输出路径
                output_path = self.output_dir / relative_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 复制文件
                import shutil
                shutil.copy2(str(aligned_file), str(output_path))
                logger.debug(f"📄 {filename} -> {relative_path}")
        
        logger.info("✅ 文件重新组织完成")
    
    def _generate_main_report(self, image_files):
        """生成主要处理报告"""
        report_path = self.output_dir / "main_align_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 🎯 Main Align 处理报告\n\n")
            f.write(f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**使用方法**: {self.selected_method}\n")
            f.write(f"**输入目录**: {self.input_dir}\n")
            f.write(f"**输出目录**: {self.output_dir}\n\n")
            
            # 方法说明
            f.write("## 🔧 对齐方法说明\n\n")
            if self.selected_method == "superpoint":
                f.write("### 🚀 深度学习方法 (SuperPoint)\n")
                f.write("- **核心技术**: LoFTR (Local Feature TRansformer)\n")
                f.write("- **特点**: 高精度深度学习特征匹配\n")
                f.write("- **优势**: 对光照、季节变化鲁棒\n")
                f.write("- **适用**: 现代建筑、复杂场景\n\n")
            else:
                f.write("### 🔧 增强传统方法 (Enhanced)\n")
                f.write("- **核心技术**: 增强SIFT + 模板匹配\n")
                f.write("- **特点**: 多层次回退策略\n")
                f.write("- **优势**: 兼容性好、稳定性高\n")
                f.write("- **适用**: 传统场景、兼容性要求高\n\n")
            
            # 统计信息
            f.write("## 📊 处理统计\n\n")
            f.write(f"- **总图像数量**: {len(image_files)}\n")
            
            # 目录结构分析
            dirs = set()
            for img_file in image_files:
                rel_path = Path(img_file).relative_to(self.input_dir)
                if len(rel_path.parts) > 1:
                    dirs.add(rel_path.parent)
            
            if dirs:
                f.write(f"- **目录数量**: {len(dirs)}\n")
                f.write(f"- **目录结构**: 已保持\n\n")
                
                f.write("### 📁 目录分布\n\n")
                for dir_path in sorted(dirs):
                    dir_files = [f for f in image_files if Path(f).relative_to(self.input_dir).parent == dir_path]
                    f.write(f"- `{dir_path}`: {len(dir_files)} 张图像\n")
            else:
                f.write(f"- **目录结构**: 扁平结构\n")
            
            f.write(f"\n## 🎉 处理完成\n\n")
            f.write(f"所有图像已成功对齐并保存到: `{self.output_dir}`\n\n")
            f.write("---\n")
            f.write("*Generated by TickTock Main Align Library*\n")
        
        logger.info(f"📝 主要处理报告已保存: {report_path}")
    
    def process_images(self):
        """主要的图像处理方法"""
        start_time = time.time()
        
        logger.info("=" * 70)
        logger.info("🎯 TickTock Main Align 开始处理")
        logger.info(f"📂 输入: {self.input_dir}")
        logger.info(f"📂 输出: {self.output_dir}")
        logger.info(f"🔧 方法: {self.selected_method}")
        logger.info("=" * 70)
        
        try:
            # 检查输入目录结构
            image_files = self.get_image_files()
            if not image_files:
                logger.error("❌ 未找到图像文件")
                return False
            
            # 检查是否需要保持目录结构
            has_subdirs = any(len(Path(f).relative_to(self.input_dir).parts) > 1 for f in image_files)
            
            if has_subdirs:
                logger.info("📁 检测到子目录结构，将保持目录结构")
                success = self.preserve_directory_structure()
            else:
                logger.info("📄 扁平目录结构，直接处理")
                success = self.aligner.process_images()
            
            end_time = time.time()
            duration = end_time - start_time
            
            if success:
                logger.info("=" * 70)
                logger.info("🎉 Main Align 处理完成!")
                logger.info(f"⏱️  总耗时: {duration:.2f} 秒")
                logger.info(f"📂 结果保存在: {self.output_dir}")
                logger.info("=" * 70)
                return True
            else:
                logger.error("❌ 处理失败")
                return False
                
        except Exception as e:
            logger.error(f"❌ 处理过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='TickTock Main Image Alignment')
    
    parser.add_argument('--input', '-i', default='NPU-Everyday-Sample',
                       help='输入图像文件夹路径 (默认: NPU-Everyday-Sample)')
    
    parser.add_argument('--output', '-o', default='NPU-Everyday-Sample_Aligned',
                       help='输出图像文件夹路径 (默认: NPU-Everyday-Sample_Aligned)')
    
    parser.add_argument('--reference', '-r', type=int, default=0,
                       help='参考图像索引 (默认: 0)')
    
    parser.add_argument('--method', '-m', 
                       choices=['superpoint', 'enhanced', 'auto'],
                       default='auto',
                       help='对齐方法选择 (默认: auto - 自动选择最佳方法)')
    
    args = parser.parse_args()
    
    # 打印启动信息
    print("🎯 TickTock Main Align Library")
    print("=" * 70)
    print(f"📂 输入目录: {args.input}")
    print(f"📂 输出目录: {args.output}")
    print(f"🔧 对齐方法: {args.method}")
    print(f"📍 参考图像: 第 {args.reference + 1} 张")
    print("=" * 70)
    
    try:
        # 创建主要对齐器
        main_aligner = MainAlign(
            input_dir=args.input,
            output_dir=args.output,
            reference_index=args.reference,
            method=args.method
        )
        
        # 执行对齐处理
        success = main_aligner.process_images()
        
        if success:
            print("=" * 70)
            print("✅ 图像对齐处理完成！")
            print(f"📂 结果保存在: {args.output}")
            print("📝 查看详细报告: main_align_report.md")
            print("=" * 70)
        else:
            print("❌ 处理失败，请检查日志信息")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"启动失败: {e}")
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
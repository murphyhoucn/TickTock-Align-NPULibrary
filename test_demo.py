#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TickTock-Align-NPU Library 测试脚本

用于测试demo.py的基本功能
"""

import os
import sys
import cv2
from pathlib import Path

def test_environment():
    """测试运行环境"""
    print("测试运行环境...")
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 6):
        print("❌ Python版本过低，需要3.6+")
        return False
    else:
        print("✅ Python版本满足要求")
    
    # 检查OpenCV
    try:
        cv2_version = cv2.__version__
        print(f"OpenCV版本: {cv2_version}")
        print("✅ OpenCV可用")
    except ImportError:
        print("❌ OpenCV未安装")
        return False
    
    # 检查输入文件夹
    input_dir = Path("NPU-Lib")
    if not input_dir.exists():
        print(f"❌ 输入文件夹不存在: {input_dir}")
        return False
    
    # 检查输入图像
    image_files = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.jpeg"))
    if not image_files:
        print(f"❌ 输入文件夹中没有图像文件: {input_dir}")
        return False
    
    print(f"✅ 找到 {len(image_files)} 张输入图像")
    
    return True

def test_image_loading():
    """测试图像加载"""
    print("\n测试图像加载...")
    
    input_dir = Path("NPU-Lib")
    image_files = sorted(list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.jpeg")))
    
    for i, img_path in enumerate(image_files[:3]):  # 只测试前3张
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"❌ 无法加载图像: {img_path}")
            return False
        else:
            print(f"✅ 成功加载图像: {img_path.name} ({img.shape[1]}x{img.shape[0]})")
    
    return True

def test_feature_detection():
    """测试特征检测"""
    print("\n测试特征检测...")
    
    try:
        # 创建SIFT检测器
        sift = cv2.SIFT_create()
        print("✅ SIFT检测器创建成功")
        
        # 测试特征检测
        input_dir = Path("NPU-Lib")
        image_files = sorted(list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.jpeg")))
        
        if image_files:
            img = cv2.imread(str(image_files[0]))
            if img is not None:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                keypoints, descriptors = sift.detectAndCompute(gray, None)
                
                if descriptors is not None:
                    print(f"✅ 检测到 {len(keypoints)} 个特征点")
                    return True
                else:
                    print("❌ 特征检测失败")
                    return False
    
    except Exception as e:
        print(f"❌ 特征检测测试失败: {e}")
        return False
    
    return False

def test_demo_import():
    """测试demo模块导入"""
    print("\n测试demo模块导入...")
    
    try:
        from align_lib import TickTockAlign
        print("✅ TickTockAlign类导入成功")
        
        # 创建实例
        aligner = TickTockAlign()
        print("✅ TickTockAlign实例创建成功")
        
        return True
    
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 实例创建失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("TickTock-Align-NPU Library 测试")
    print("=" * 50)
    
    tests = [
        ("环境检查", test_environment),
        ("图像加载", test_image_loading),
        ("特征检测", test_feature_detection),
        ("模块导入", test_demo_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                print(f"✅ {test_name} 通过")
                passed += 1
            else:
                print(f"❌ {test_name} 失败")
        except Exception as e:
            print(f"❌ {test_name} 异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！可以运行demo了")
        print("\n运行命令:")
        print("python demo.py")
    else:
        print("⚠️  有测试失败，请检查环境配置")
        print("\n安装依赖:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
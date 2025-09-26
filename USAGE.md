# TickTock-Align-NPU Library 使用指南

## 🚀 快速开始

### 方法1: 一键启动（推荐）
```bash
# Windows用户：双击运行
run_demo.bat

# 或在命令行执行
.\run_demo.bat
```

### 方法2: Python命令行
```bash
# 完整流程（图像对齐 + 延时摄影）
python demo.py

# 仅图像对齐
python demo.py --align-only

# 仅延时摄影（需要已对齐的图像）
python demo.py --video-only

# 自定义参数
python demo.py --input NPU-Lib --output NPU-Lib-Align --video Video --reference 2
```

### 方法3: 分步执行
```bash
# 步骤1：图像对齐
python align_lib.py --input NPU-Lib --output NPU-Lib-Align

# 步骤2：创建延时摄影
python create_timelapse.py
```

## 📋 核心功能

### 🔄 图像对齐 (align_lib.py)
- **智能特征检测**: 使用SIFT算法检测图像特征点
- **快速匹配**: 基于FLANN的特征点匹配
- **鲁棒对齐**: 使用RANSAC算法估计单应性矩阵
- **批量处理**: 自动处理整个文件夹的图像序列
- **错误处理**: 完善的异常处理和日志记录

### 🎬 延时摄影 (create_timelapse.py) 
- **多质量选项**: 自动生成预览版、标准版、高质量版
- **智能编码**: 使用H.264编码确保兼容性
- **自适应分辨率**: 自动调整到合适的输出分辨率
- **FFmpeg集成**: 基于FFmpeg的专业视频处理

## 📊 工作流程

```
输入图像序列 (NPU-Lib)
    ↓
图像对齐处理 (align_lib.py)
    ├── 选择参考图像 (默认第一张)
    ├── SIFT特征点检测
    ├── FLANN特征点匹配  
    ├── RANSAC单应性矩阵估计
    └── 透视变换对齐
    ↓
对齐图像输出 (NPU-Lib-Align)
    ↓
延时摄影制作 (create_timelapse.py)
    ├── 快速预览版 (30fps, 中等质量)
    ├── 标准版 (15fps, 高质量)
    └── 高质量版 (10fps, 最高质量)
    ↓
视频文件输出 (Video)
```

## 🔧 Python API 使用

### 图像对齐API
```python
from align_lib import TickTockAlign

# 创建对齐器实例
aligner = TickTockAlign(
    input_dir="NPU-Lib",           # 输入文件夹
    output_dir="NPU-Lib-Align",   # 输出文件夹
    reference_index=0              # 参考图像索引（0=第一张）
)

# 执行图像对齐
aligner.process_images()
```

### 延时摄影API
```python
from create_timelapse import create_file_list, create_timelapse_video
import os

# 创建文件列表
file_list = create_file_list()

# 创建自定义视频
success = create_timelapse_video(
    file_list_path=file_list,
    output_name="my_timelapse.mp4",
    framerate=20,      # 帧率
    quality=18         # 质量 (18=高质量, 23=中等, 28=低质量)
)

# 清理
if os.path.exists(file_list):
    os.unlink(file_list)
```
# 清理
if os.path.exists(file_list):
    os.unlink(file_list)
```

## ⚙️ 命令行参数

### demo.py 参数
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--input` | `-i` | 输入图像文件夹路径 | NPU-Lib |
| `--output` | `-o` | 输出图像文件夹路径 | NPU-Lib-Align |  
| `--video` | `-v` | 视频输出文件夹路径 | Video |
| `--reference` | `-r` | 参考图像索引 | 0 |
| `--align-only` | - | 仅执行图像对齐 | False |
| `--video-only` | - | 仅创建视频 | False |

### align_lib.py 参数  
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--input` | `-i` | 输入图像文件夹路径 | NPU-Lib |
| `--output` | `-o` | 输出图像文件夹路径 | NPU-Lib-Align |
| `--reference` | `-r` | 参考图像索引 | 0 |

## 📁 文件结构

```
TickTock-Align-NPULibrary/
├── NPU-Lib/                    # 输入：原始图像序列
│   ├── IMG_20250601_114129.jpg
│   ├── IMG_20250602_102318.jpg
│   └── ...
├── NPU-Lib-Align/             # 输出：对齐后的图像
│   ├── IMG_20250601_114129.jpg (参考图像)
│   ├── IMG_20250602_102318.jpg (对齐后)
│   └── ...
├── Video/                      # 输出：延时摄影视频
│   ├── timelapse_preview.mp4   (30fps, 快速预览)
│   ├── timelapse_standard.mp4  (15fps, 标准质量)
│   └── timelapse_hq.mp4        (10fps, 高质量)
├── demo.py                     # 主程序（整合版）
├── align_lib.py               # 图像对齐核心库
├── create_timelapse.py        # 延时摄影制作工具
└── run_demo.bat               # 一键启动脚本
```

## 🎬 视频输出说明

程序会自动生成3个不同质量的延时摄影视频：

1. **快速预览版** (`timelapse_preview.mp4`)
   - 帧率：30fps
   - 质量：中等 (CRF 23)
   - 用途：快速预览效果

2. **标准版** (`timelapse_standard.mp4`)  
   - 帧率：15fps
   - 质量：高 (CRF 20)
   - 用途：日常分享使用

3. **高质量版** (`timelapse_hq.mp4`)
   - 帧率：10fps  
   - 质量：最高 (CRF 18)
   - 用途：专业展示或后期处理

## 💻 系统要求

### 必需软件
- **Python 3.6+**
- **OpenCV 4.0+** 
- **NumPy 1.19+**
- **FFmpeg** (延时摄影功能)

### 推荐硬件
- **内存**: 8GB+ (处理高分辨率图像序列)
- **存储**: 足够空间存储对齐图像和视频文件
- **CPU**: 多核处理器提高处理速度

### 安装方法

#### Python依赖
```bash
pip install -r requirements.txt
```

#### FFmpeg安装
```bash
# Windows (winget)
winget install FFmpeg

# Windows (Chocolatey)  
choco install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg

# macOS (Homebrew)
brew install ffmpeg
```

## 🎯 使用场景

### 适用场景
- ✅ 建筑物延时摄影
- ✅ 固定机位的场景变化记录
- ✅ 景观变化监控
- ✅ 科研观测记录
- ✅ 艺术创作项目

### 图像要求
- 📷 同一场景的不同时间拍摄
- 🎯 相机位置相对固定（允许轻微移动）
- 🏗️ 场景具有丰富的纹理特征
- 📐 图像质量清晰，避免严重模糊
- 🌅 光照变化可以接受

## 🔧 高级配置

### 自定义视频参数
```python
from create_timelapse import create_timelapse_video

# 创建自定义视频
create_timelapse_video(
    file_list_path="file_list.txt",
    output_name="custom.mp4",
    framerate=24,      # 自定义帧率
    quality=15         # 自定义质量 (越小质量越高)
)
```

### 批量处理多个项目
```python
import os
from align_lib import TickTockAlign

projects = ["project1", "project2", "project3"]

for project in projects:
    input_dir = f"{project}/NPU-Lib"
    output_dir = f"{project}/NPU-Lib-Align"
    
    if os.path.exists(input_dir):
        aligner = TickTockAlign(input_dir, output_dir)
        aligner.process_images()
```

## ❗ 故障排除

### 常见问题

**Q: 特征点检测失败**
- 检查图像是否过于模糊
- 确认场景有足够的纹理特征
- 尝试更换参考图像

**Q: 匹配点数量不足**  
- 检查图像之间的重叠度
- 确认图像来自同一场景
- 尝试不同的参考图像

**Q: FFmpeg相关错误**
- 确认FFmpeg已正确安装
- 检查PATH环境变量
- 验证FFmpeg版本兼容性

**Q: 内存不足**
- 减少单次处理的图像数量
- 降低图像分辨率
- 关闭其他占用内存的程序

**Q: 处理速度慢**
- 使用SSD存储
- 确保足够的可用内存
- 考虑使用更快的CPU

### 获取帮助
```bash
# 查看帮助信息
python demo.py --help
python align_lib.py --help

# 运行测试
python test_demo.py
```
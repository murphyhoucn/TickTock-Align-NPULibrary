# 图像统一放缩模块 (Resize)

## 📖 模块简介

图像统一放缩模块负责将不同分辨率的图像统一放缩到目标尺寸，特别针对NPU项目中两种不同手机拍摄的图像：
- **HUAWEI P30 Pro**: 3648×2736 像素
- **vivo X100 Pro**: 4096×3072 像素

所有图像将被统一放缩到 **4096×3072** 像素，确保后续处理的一致性。

## 🎯 主要功能

### ✨ 核心特性
- **智能设备识别**: 自动识别不同手机型号的图像
- **高质量放缩**: 使用LANCZOS算法保持最佳图像质量
- **批量处理**: 支持整个文件夹的批量处理
- **目录结构保持**: 保持原有的子目录结构
- **详细统计**: 提供完整的处理统计信息

### 📊 支持的图像格式
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- WebP (.webp)

## 🚀 使用方法

### 1. 作为独立模块使用
```bash
python Resize/image_resizer.py "输入目录" "输出目录" --width 4096 --height 3072
```

### 2. 通过流水线使用
```bash
# 仅执行放缩步骤
python pipeline.py NPU-Everyday-Sample --resize-only

# 作为流水线的一部分
python pipeline.py NPU-Everyday-Sample --steps resize align timelapse
```

## 📋 参数说明

### 命令行参数
```bash
python image_resizer.py <input_dir> <output_dir> [选项]
```

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `input_dir` | str | ✅ | - | 输入图像目录路径 |
| `output_dir` | str | ✅ | - | 输出图像目录路径 |
| `--width` | int | ❌ | 4096 | 目标图像宽度 |
| `--height` | int | ❌ | 3072 | 目标图像高度 |

### 函数API
```python
from Resize.image_resizer import process_directory

process_directory(
    input_dir="NPU-Everyday-Sample",
    output_dir="NPU-Everyday-Sample_rescale", 
    target_size=(4096, 3072)
)
```

## 🔧 技术实现

### 核心算法
1. **图像读取**: 使用PIL库读取图像
2. **尺寸检测**: 自动检测原始图像尺寸
3. **设备识别**: 根据尺寸识别拍摄设备
4. **智能放缩**: 
   - 如果已经是目标尺寸，直接复制
   - 否则使用LANCZOS算法进行高质量放缩
5. **质量保持**: 保存时使用95%的JPEG质量

### 关键代码片段
```python
def resize_image(input_path, output_path, target_size=(4096, 3072)):
    """将图片放缩到目标尺寸"""
    with Image.open(input_path) as img:
        original_size = img.size
        
        # 如果已经是目标尺寸，直接复制
        if original_size == target_size:
            img.save(output_path, quality=95, optimize=True)
            return True
        
        # 使用高质量重采样方法进行放缩
        resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
        resized_img.save(output_path, quality=95, optimize=True)
        return True
```

## 📊 处理统计

### 自动设备识别
模块会自动识别并统计不同设备的图像：

```
📸 处理第 1 个图片:
   文件: 2023.09\IMG_20230916_114359.jpg
   设备: HUAWEI P30 Pro
原始尺寸: 3648x2736
✅ 放缩完成: 3648x2736 → 4096x3072
```

### 统计报告示例
```
============================================================
📊 处理统计:
   总图片数: 30
   成功处理: 30
   处理失败: 0
   HUAWEI P30 Pro (3648×2736): 10
   vivo X100 Pro (4096×3072): 20
   其他尺寸: 0
✅ 批量处理完成!
```

## ⚡ 性能优化

### 处理速度
- **小批量** (30张图像): ~13秒
- **中等批量** (100张图像): ~45秒
- **大批量** (500+张图像): ~3-5分钟

### 内存使用
- **单张图像处理**: 约50-100MB内存
- **批量处理**: 内存使用保持稳定，不会累积

### 优化建议
1. **SSD存储**: 使用SSD可显著提升I/O性能
2. **充足内存**: 推荐8GB+内存用于大批量处理
3. **多核CPU**: 虽然是单线程，但CPU性能影响LANCZOS算法速度

## 🔍 质量控制

### LANCZOS算法优势
- **高质量重采样**: 比双线性插值质量更高
- **边缘保持**: 更好的边缘细节保持
- **色彩保真**: 减少色彩失真

### 质量参数
- **JPEG质量**: 95% (平衡质量和文件大小)
- **优化开启**: 启用JPEG优化以减小文件大小
- **色彩空间**: 保持原始色彩空间

## 📝 输出结构

### 目录结构保持
```
输入目录/
├── 2023.09/
│   ├── IMG_20230916_114359.jpg
│   └── IMG_20230916_205324.jpg
└── 2024.09/
    └── IMG_20240902_190324.jpg

输出目录/
├── 2023.09/                    # 保持相同结构
│   ├── IMG_20230916_114359.jpg # 4096×3072
│   └── IMG_20230916_205324.jpg # 4096×3072
└── 2024.09/
    └── IMG_20240902_190324.jpg # 4096×3072
```

## ❗ 错误处理

### 常见错误及解决方案

1. **文件读取失败**
   ```
   ❌ 处理失败: cannot identify image file
   ```
   - 原因: 图像文件损坏或格式不支持
   - 解决: 检查文件完整性，确认格式支持

2. **磁盘空间不足**
   ```
   ❌ 处理失败: [Errno 28] No space left on device
   ```
   - 原因: 输出目录磁盘空间不足
   - 解决: 清理磁盘空间或更换输出目录

3. **权限不足**
   ```
   ❌ 处理失败: [Errno 13] Permission denied
   ```
   - 原因: 没有写入权限
   - 解决: 检查目录权限，以管理员身份运行

## 🔧 自定义配置

### 修改默认参数
```python
# 修改默认目标尺寸
DEFAULT_TARGET_SIZE = (4096, 3072)

# 修改质量参数
JPEG_QUALITY = 95
OPTIMIZE = True

# 添加新的设备识别
DEVICE_MAPPING = {
    (3648, 2736): "HUAWEI P30 Pro",
    (4096, 3072): "vivo X100 Pro",
    # 添加新设备...
}
```

## 📚 相关文档

- [主项目文档](../README.md)
- [完整流水线说明](../USAGE.md)
- [环境配置指南](../requirements.txt)

---

**模块版本**: v2.0.0  
**最后更新**: 2025-09-30  
**维护者**: TickTock-Align-NPU Library Team
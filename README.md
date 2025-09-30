# TickTock-Align-NPU Library

████████╗██╗ ██████╗██╗  ██╗████████╗ ██████╗  ██████╗██╗  ██╗
╚══██╔══╝██║██╔════╝██║ ██╔╝╚══██╔══╝██╔═══██╗██╔════╝██║ ██╔╝
   ██║   ██║██║     █████╔╝    ██║   ██║   ██║██║     █████╔╝ 
   ██║   ██║██║     ██╔═██╗    ██║   ██║   ██║██║     ██╔═██╗ 
   ██║   ██║╚██████╗██║  ██╗   ██║   ╚██████╔╝╚██████╗██║  ██╗
   ╚═╝   ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝╚═╝  ╚═╝

**🎯 项目简介**：基于计算机视觉技术的NPU建筑物图像完整处理流水线  
**📥 输入**: NPU-Everyday 或 NPU-Everyday-Sample 文件夹中的建筑物图像序列  
**📤 输出**: {输入文件夹名称}_Output 文件夹中的完整处理结果

包含图像统一放缩、精确对齐、延时摄影制作、马赛克拼图和统计分析。支持两种不同手机拍摄的图像序列自动化处理。

---

## 🚀 快速开始

### 方式1：一键启动脚本（推荐新用户）
```bash
# Windows用户
run_pipeline.bat

# 交互式菜单选择：
# 1. 快速测试 (NPU-Everyday-Sample) - 30张图像，约4分钟
# 2. 完整处理 (NPU-Everyday) - 582+张图像，约1-2小时
# 3-5. 单步处理模式（仅执行特定功能）
# 6. 自定义步骤组合
```

### 方式2：命令行直接运行
```bash
# 安装依赖
pip install -r requirements.txt

# 完整流水线处理（推荐）
python pipeline.py NPU-Everyday-Sample

# 自定义步骤组合
python pipeline.py NPU-Everyday-Sample --steps resize align timelapse mosaic stats

# 单步处理
python pipeline.py NPU-Everyday-Sample --resize-only    # 仅图像放缩
python pipeline.py NPU-Everyday-Sample --align-only     # 仅图像对齐
python pipeline.py NPU-Everyday-Sample --timelapse-only # 仅延时摄影
```

### 环境检查
```bash
# 检查运行环境和依赖
python test_environment.py
```

---

## 🎯 核心功能

### 🔄 步骤1：图像统一放缩 (Resize)
- **多设备支持**: 自动识别HUAWEI P30 Pro (3648×2736) 和 vivo X100 Pro (4096×3072)
- **智能放缩**: 统一放缩到4096×3072像素，保持最佳质量
- **高质量重采样**: 使用LANCZOS算法确保放缩质量
- **批量处理**: 自动处理整个文件夹的图像序列
- **📚 详细文档**: [Resize/README.md](Resize/README.md)

### 🎯 步骤2：智能图像对齐 (Align)
- **SIFT特征检测**: 精确识别图像特征点（208k+特征点）
- **FLANN快速匹配**: 高效的特征点匹配算法
- **RANSAC鲁棒估计**: 抗干扰的单应性矩阵计算
- **递归搜索**: 支持多级目录结构
- **智能错误处理**: 处理特征检测失败等异常情况
- **📚 详细文档**: [Align/README.md](Align/README.md)

### 🎬 步骤3：延时摄影制作 (Timelapse)
- **多质量输出**: 自动生成预览版(30fps)、标准版(15fps)、高质量版(10fps)
- **智能编码**: H.264编码确保广泛兼容性
- **自适应分辨率**: 自动调整到合适的输出分辨率(1920×1080)
- **FFmpeg集成**: 基于业界标准的视频处理工具
- **📚 详细文档**: [Timelapse/README.md](Timelapse/README.md)

### 🧩 步骤4：马赛克拼图生成 (Mosaic)
- **多种布局**: 网格马赛克、时间线马赛克、缩略图概览
- **智能内存管理**: 自动缩放避免内存溢出
- **高质量缩放**: LANCZOS算法保持图像质量
- **自适应布局**: 根据图像数量自动计算最优布局
- **详细报告**: 自动生成马赛克信息报告
- **📚 详细文档**: [Mosaic/README.md](Mosaic/README.md)

### 📊 步骤5：统计分析 (Statistics)
- **GitHub风格图表**: 类似GitHub提交图的拍摄日历
- **详细报告**: Markdown格式的统计报告
- **时间范围分析**: 按日、月、年统计拍摄频率
- **设备分析**: 分析不同设备的拍摄比例
- **可视化输出**: PNG图表和Markdown报告
- **📚 详细文档**: [Stas/README.md](Stas/README.md)

---

## 🎬 工作流程

```
📷 原始图像序列 (NPU-Everyday / NPU-Everyday-Sample)
    ↓
🔄 步骤1：图像统一放缩 (Resize)
    │ 3648×2736 / 4096×3072 → 4096×3072
    │ 输出：{输入目录}_Output/Rescaled/
    ↓
🎯 步骤2：智能图像对齐 (Align)
    │ SIFT特征检测 → FLANN匹配 → RANSAC估计 → 透视变换
    │ 输出：{输入目录}_Output/Aligned/
    ↓
🎬 步骤3：延时摄影制作 (Timelapse)
    │ FFmpeg H.264编码，多质量输出 (30fps/15fps/10fps)
    │ 输出：{输入目录}_Output/Timelapse/
    ↓
🧩 步骤4：马赛克拼图 (Mosaic)
    │ 网格布局 + 时间线布局 + 缩略图概览
    │ 输出：{输入目录}_Output/Mosaic/
    ↓
📊 步骤5：统计分析 (Statistics)
    │ GitHub风格图表 + Markdown报告
    │ 输出：{输入目录}_Output/Statistics/
    ↓
📦 完整结果汇总
    └── {输入目录}_Output/
        ├── processing_report.md  # 完整处理报告
        ├── Rescaled/            # 放缩后图像
        ├── Aligned/             # 对齐后图像
        ├── Timelapse/           # 延时摄影视频
        ├── Mosaic/              # 马赛克拼图
        └── Statistics/          # 统计分析
```

---

## 📁 项目结构

```
TickTock-Align-NPULibrary/
├── 📊 数据集
│   ├── NPU-Everyday/               # 完整数据集：所有月份的图像
│   │   ├── 2023.09/ ... 2025.09/
│   │   └── (582+ 张图像)
│   └── NPU-Everyday-Sample/        # 采样数据集：3个月份用于快速测试
│       ├── 2023.09/ (10张)
│       ├── 2024.09/ (10张)
│       └── 2025.09/ (10张)
│
├── 🔧 核心程序
│   ├── pipeline.py                 # 🚀 完整流水线主程序
│   ├── run_pipeline.bat            # 🖱️ Windows一键启动脚本
│   ├── test_environment.py         # 🔍 环境检查工具
│   └── main.py                     # 📜 原有主程序(兼容性)
│
├── 📦 功能模块
│   ├── Resize/                     # 图像统一放缩
│   │   ├── image_resizer.py        # 核心放缩算法
│   │   └── README.md               # 模块说明文档
│   ├── Align/                      # 智能图像对齐
│   │   ├── align_lib.py            # SIFT特征点对齐
│   │   └── README.md               # 模块说明文档
│   ├── Timelapse/                  # 延时摄影制作
│   │   ├── create_timelapse.py     # FFmpeg视频生成
│   │   └── README.md               # 模块说明文档
│   ├── Mosaic/                     # 马赛克拼图生成
│   │   ├── mosaic_pic.py           # 马赛克拼图算法
│   │   └── README.md               # 模块说明文档
│   └── Stas/                       # 统计分析模块
│       ├── visual_commit_markdown.py  # Markdown报告生成
│       ├── visual_commit_png.py       # PNG图表生成
│       ├── statistics_*.py            # 其他统计工具
│       └── README.md                  # 模块说明文档
│
├── 📋 配置文件
│   ├── requirements.txt            # Python依赖包列表
│   ├── USAGE.md                   # 详细使用指南
│   └── PROJECT_SUMMARY.md          # 项目重构总结
│
└── 📤 输出示例 (自动生成)
    └── {输入目录}_Output/
        ├── Rescaled/               # 🔄 统一放缩后的图像
        ├── Aligned/                # 🎯 SIFT对齐后的图像
        ├── Timelapse/              # 🎬 延时摄影视频
        │   ├── timelapse_preview.mp4   (30fps)
        │   ├── timelapse_standard.mp4  (15fps)
        │   └── timelapse_hq.mp4        (10fps)
        ├── Mosaic/                 # 🧩 马赛克拼图
        │   ├── mosaic_grid.jpg         # 网格布局
        │   ├── mosaic_timeline_*.jpg   # 时间线布局
        │   └── mosaic_info.md          # 拼图报告
        ├── Statistics/             # 📊 统计分析
        │   ├── NPU_Photo_Statistics_Report.md
        │   └── NPU_Photo_Commit_Chart.png
        └── processing_report.md    # 📝 完整处理报告
```

---

## 📱 设备支持

NPU-Everyday的图片使用了两个不同的手机拍摄：
- **HUAWEI P30 Pro**: 3648×2736 像素 → 自动放缩到4096×3072
- **vivo X100 Pro**: 4096×3072 像素 → 保持原尺寸

**技术规格**:
- **统一尺寸**: 4096×3072 像素
- **放缩方法**: 高质量LANCZOS重采样
- **输出质量**: 95% JPEG质量

---

## ⚡ 性能指标

### 处理速度参考 (基于NPU-Everyday-Sample)
| 步骤 | 图像数量 | 耗时 | 主要操作 |
|------|---------|------|----------|
| **图像放缩** | 30张 | ~13秒 | LANCZOS重采样 |
| **图像对齐** | 30张 | ~3分钟 | SIFT特征匹配 |
| **延时摄影** | 30张 | ~6秒 | FFmpeg H.264编码 |
| **马赛克拼图** | 30张 | ~18秒 | 多布局生成 |
| **统计分析** | 30张 | ~1秒 | 图表生成 |
| **总计** | 30张 | **~4分钟** | 完整流水线 |

### 输出文件大小参考
| 输出类型 | 文件大小 | 说明 |
|----------|----------|------|
| 延时摄影视频 | 3.8-6.5MB | 3个不同质量版本 |
| 马赛克拼图 | 各种尺寸 | 从32×32到682×682像素 |
| 统计图表 | <1MB | PNG格式GitHub风格图表 |

---

## 🛠️ 系统要求

### 必需软件
- **Python 3.10+** (推荐3.10-3.12)
- **OpenCV 4.0+** (图像处理)
- **NumPy 2.0+** (数值计算)
- **Pillow** (图像处理)
- **FFmpeg** (延时摄影功能)

### 支持平台
- ✅ **Windows 10/11** (主要测试平台)
- ✅ **Linux (Ubuntu 18.04+)**
- ✅ **macOS 10.14+**

### 推荐硬件配置
- **CPU**: 多核处理器，推荐8核心以上
- **内存**: 16GB+ (处理大量高分辨率图像)
- **存储**: SSD硬盘提升I/O性能
- **显卡**: 可选，OpenCV支持CUDA加速

---

## 📖 详细文档

- 📋 [完整使用指南 (USAGE.md)](USAGE.md) - 详细的使用说明和API文档
- 🔧 [环境配置说明 (requirements.txt)](requirements.txt) - 依赖包安装说明
- 🧪 [环境测试工具 (test_environment.py)](test_environment.py) - 环境和功能测试
- 📊 [项目重构总结 (PROJECT_SUMMARY.md)](PROJECT_SUMMARY.md) - 完整重构过程

### 模块详细文档
- [🔄 图像放缩模块 (Resize/README.md)](Resize/README.md)
- [🎯 图像对齐模块 (Align/README.md)](Align/README.md)
- [🎬 延时摄影模块 (Timelapse/README.md)](Timelapse/README.md)
- [🧩 马赛克拼图模块 (Mosaic/README.md)](Mosaic/README.md)
- [📊 统计分析模块 (Stas/README.md)](Stas/README.md)

---

## 🎯 适用场景

- 🏗️ **建筑物延时摄影** - 建筑施工过程记录
- 🌅 **城市景观变化** - 城市发展变迁记录  
- 🔬 **科研观测** - 长期观测数据可视化
- 🎨 **艺术创作** - 创意延时摄影项目
- 📊 **数据可视化** - 时间序列数据展示
- 🖼️ **图像艺术** - 马赛克拼图艺术创作

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境设置
```bash
# 克隆项目
git clone https://github.com/murphyhoucn/TickTock-Align-NPULibrary.git
cd TickTock-Align-NPULibrary

# 安装开发依赖
pip install -r requirements.txt

# 运行测试
python test_environment.py
```

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 📞 技术支持

如遇到问题，请：
1. 查看 `pipeline.log` 日志文件
2. 检查 `processing_report.md` 处理报告
3. 在GitHub提交Issue，包含错误信息和环境详情

---

**🎉 TickTock-Align-NPU Library v2.0.0**  
*最后更新: 2025-09-30*  
*构建者: 基于计算机视觉技术的完整图像处理流水线*
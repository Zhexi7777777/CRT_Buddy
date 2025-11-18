# 🎮 CRT Buddy

<div align="center">

![Version](https://img.shields.io/badge/version-6.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

**一个充满Y2K复古风格的桌面宠物和表情包生成器** ✨

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [使用指南](#-使用指南) • [截图](#-截图) • [开发](#-开发)

</div>

---

## 📖 简介

CRT Buddy 是一个融合了千禧年（Y2K）美学风格的桌面应用程序，它既是你的电脑桌面宠物，也是一个强大的复古风格表情包生成器。通过 CRT 显示屏效果、像素字体、金属质感按钮和动态扫描线，它完美还原了 2000 年代早期的互联网美学。

### ✨ 主要亮点

- 🖥️ **CRT 显示效果** - 真实的阴极射线管屏幕模拟，包含扫描线和 RGB 偏移
- 🤖 **可爱的桌面吉祥物** - 会眨眼、追踪鼠标、显示不同表情的互动角色
- 🎨 **Y2K 表情包生成器** - 多种复古滤镜效果（VHS、全息、霓虹、像素化等）
- ⌨️ **输入可视化** - 实时显示按键、打字速度和粒子特效
- 💾 **像素字体** - 使用 DinkieBitmap 像素字体，完美还原复古感觉
- 🎭 **丰富表情** - 吉祥物根据你的操作做出不同反应

---

## 🎯 功能特性

### 🎨 表情包生成

#### 文字表情包
- ✨ **多种文字特效**
  - 渐变文字（Rainbow Gradient）
  - 故障效果（RGB Glitch）
  - 霓虹发光（Neon Glow）
  - 金属质感（Chrome）
  - 复古彩虹（Retro Rainbow）

#### 图片处理
- 🖼️ **Y2K 风格滤镜**
  - **CRT 效果** - RGB 偏移 + 扫描线
  - **VHS 磁带** - 横向位移 + 噪点
  - **全息效果** - 彩虹渐变叠加
  - **金属质感** - 边缘增强 + 银色调
  - **霓虹发光** - 边缘检测 + 高亮
  - **像素化** - 8-bit 复古风格

#### 经典短语库
内置 20+ 经典 Y2K 时代短语：
```
UNDER CONSTRUCTION
WELCOME TO MY WEBSITE
BEST VIEWED IN NETSCAPE
POWERED BY GEOCITIES
Y2K AESTHETIC
CYBER DREAMS 2000
404 PAGE NOT FOUND
MILLENNIUM BUG FREE
...更多
```

### ⌨️ 输入可视化系统

#### 实时追踪
- 📺 **大字体按键显示** - 在 CRT 屏幕中央显示当前按键
- 📜 **按键历史** - 显示最近 10 个按键，带渐隐效果
- 📊 **实时统计** - 按键总数和打字速度（CPM）

#### 视觉特效
- ✨ **粒子系统** - 每次按键产生彩色粒子
- 💫 **屏幕脉冲** - 打字时 CRT 屏幕发光
- 😊 **吉祥物反应** - 每 10 个键触发开心表情

### 🤖 桌面吉祥物

#### 互动特性
- 👀 **全局鼠标追踪** - 眼睛跟随你的鼠标移动（即使在其他窗口）
- 😊 **表情系统** - 平静、开心、处理中等多种表情
- 💡 **天线指示灯** - 脉动的发光球，显示运行状态
- ✨ **星星眼效果** - 开心时显示特殊星形眼睛

#### 动画效果
- 👁️ **自然眨眼** - 随机间隔自动眨眼
- 🌟 **发光特效** - 头部和天线的动态光晕
- 📺 **扫描线** - 持续移动的 CRT 扫描线效果

### 🎨 界面设计

#### Y2K 美学元素
- 🖥️ **金属质感机身** - 铝制外壳效果，带高光和阴影
- 🔘 **物理按钮** - 3D 凸起效果的金属按钮
- 💎 **电源 LED** - 脉动的青色指示灯
- 🌈 **Chrome 装饰条** - 底部金属散热孔装饰

#### 可拖动界面
- 📌 **窗口置顶** - 始终显示在最前面
- 🖱️ **自由拖动** - 点击任意位置拖动窗口
- 🎯 **无边框设计** - 透明背景，自定义外观

---

## 🚀 快速开始

### 系统要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows / macOS / Linux
- **内存**: 至少 256MB RAM
- **显示器**: 800x600 或更高分辨率

### 安装步骤

#### 1. 克隆仓库

```bash
git clone https://github.com/Seeglo0052/CRT_Buddy.git
cd CRT_Buddy
```

#### 2. 创建虚拟环境（推荐）

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

#### 3. 安装依赖

```bash
pip install -r CRT_Buddy/requirements.txt
```

或者手动安装：

```bash
pip install PyQt6 Pillow numpy opencv-python pygame requests
```

#### 4. 运行程序

```bash
cd CRT_Buddy
python main.py
```

### 快速测试

启动后，你应该看到：
1. ✅ 带有金属质感的窗口
2. ✅ 中央的 CRT 屏幕和吉祥物
3. ✅ 右侧的控制面板
4. ✅ 吉祥物的眼睛跟随你的鼠标

---

## 📘 使用指南

### 生成文字表情包

1. **输入文字**
   - 在文本框中输入你想要的文字
   - 支持中英文和特殊字符

2. **点击 GENERATE 按钮**
   - 程序会自动应用随机的 Y2K 风格效果
   - 吉祥物会显示"处理中"表情

3. **查看结果**
   - 生成的图片保存在 `output` 文件夹
   - 状态栏会显示文件名

### 处理图片

#### 方法 1：拖放
1. 准备一张图片（支持 PNG, JPG, JPEG, GIF, BMP）
2. 直接拖到窗口上
3. 自动应用随机 Y2K 效果

#### 方法 2：浏览选择
1. 点击 **IMAGE** 按钮
2. 在文件对话框中选择图片
3. 确认后自动处理

#### 方法 3：带文字说明
1. 在文本框输入想要添加的文字
2. 拖入或选择图片
3. 图片会带有你输入的文字叠加

### 生成随机表情包

1. 点击 **RANDOM** 按钮
2. 程序会：
   - 随机选择一个经典 Y2K 短语
   - 随机选择一种文字效果
   - 随机选择画布尺寸
3. 直接生成并保存

### 输入可视化

1. **点击文本框开始输入**
2. **观察 CRT 屏幕**：
   - 中央显示当前按键（大字体）
   - 底部显示按键历史
   - 粒子效果在屏幕上飞舞
3. **查看统计**：
   - 顶部状态栏显示按键数和速度

### 快捷操作

- **拖动窗口**：点击并拖动窗口任意位置
- **关闭程序**：点击右下角的圆形 X 按钮
- **查看输出**：打开 `output` 文件夹查看生成的图片

---

## 📸 截图

### 主界面
```
┌─────────────────────────────────────────────┐
│  CRT BUDDY v6.0            [LED] ●          │
├───────────┬─────────────────────────────────┤
│           │  CRT BUDDY v6.0 - VISUALIZER    │
│           │  KEYS: 42 | SPEED: 180 CPM      │
│    CRT    │                                 │
│  ┌─────┐  │  ┌─────────────────────────┐   │
│  │ 👀  │  │  │ Type here...            │   │
│  │ 😊  │  │  └─────────────────────────┘   │
│  └─────┘  │                                 │
│  [keys]   │  [███ GENERATE ███]            │
│           │  [███  IMAGE   ███]            │
│           │  [███  RANDOM  ███]            │
│           │                    ⦿            │
└───────────┴─────────────────────────────────┘
```

### 效果展示

**文字特效示例：**
- Gradient: 渐变彩虹色文字
- Glitch: RGB 分离故障效果
- Neon: 霓虹发光效果
- Chrome: 金属反光质感
- Retro: 经典彩虹条纹

**图片滤镜示例：**
- CRT: 复古显示器效果
- VHS: 磁带录像带失真
- Holographic: 全息彩虹
- Pixelate: 8-bit 像素化

---

## 🛠️ 开发

### 项目结构

```
CRT_Buddy/
├── CRT_Buddy/
│   ├── main.py                    # 主程序入口
│   ├── config.ini                 # 配置文件
│   ├── requirements.txt           # 依赖列表
│   │
│   ├── core/                      # 核心模块
│   │   ├── __init__.py
│   │   ├── pet_window.py          # 窗口基础类
│   │   ├── pet_window_v5.py       # v5 水平布局
│   │   └── pet_window_v6.py       # v6 输入可视化
│   │
│   ├── effects/                   # 特效模块
│   │   ├── __init__.py
│   │   ├── y2k_styles.py          # Y2K 图片滤镜
│   │   └── text_effects.py        # 文字特效
│   │
│   ├── generators/                # 生成器模块
│   │   ├── __init__.py
│   │   └── meme_engine.py         # 表情包生成引擎
│   │
│   └── output/                    # 输出目录
│       └── (生成的图片)
│
├── DinkieBitmap-v1.5.0-KeDingKeMao/  # 像素字体
│   └── ttf/
│       └── DinkieBitmap-9px.ttf
│
├── README.md                      # 本文件
└── LICENSE                        # 许可证
```

### 技术栈

- **GUI 框架**: PyQt6
- **图像处理**: Pillow (PIL)
- **数值计算**: NumPy
- **计算机视觉**: OpenCV
- **字体**: DinkieBitmap 像素字体

### 核心类说明

#### CRTBuddyWindow
主窗口类，负责 UI 渲染和交互

**主要方法：**
- `paintEvent()` - 自定义绘制 CRT 效果
- `draw_mascot()` - 绘制吉祥物
- `on_keystroke()` - 处理按键输入
- `animate()` - 动画循环

#### MemeEngine
表情包生成引擎

**主要方法：**
- `generate_text_meme()` - 生成文字表情包
- `generate_image_meme()` - 处理图片
- `generate_random_meme()` - 随机生成
- `save_meme()` - 保存到文件

#### Y2KStyles
Y2K 风格滤镜集合

**可用效果：**
- `crt_effect()` - CRT 显示器
- `vhs_effect()` - VHS 磁带
- `holographic_effect()` - 全息效果
- `chrome_effect()` - 金属质感
- `neon_effect()` - 霓虹发光
- `pixelate_effect()` - 像素化

### 自定义配置

你可以修改以下参数来自定义程序：

```python
# 在 pet_window_v6.py 中

# 窗口大小
self.setGeometry(100, 100, 520, 320)

# 按键历史数量
self.key_history = deque(maxlen=10)  # 改为 20 显示更多

# 粒子效果
for _ in range(3):  # 改为 5 产生更多粒子

# 吉祥物反应频率
if self.total_keystrokes % 10 == 0:  # 改为 5 更频繁反应
```

### 添加新的滤镜效果

```python
# 在 effects/y2k_styles.py 中

def my_custom_effect(self, img):
    """我的自定义效果"""
    # 你的图像处理代码
    return img

# 在 apply_effect() 中注册
effects = {
    'crt': self.crt_effect,
    'vhs': self.vhs_effect,
    'my_custom': self.my_custom_effect,  # 添加这行
}
```

---

## 🎨 自定义主题

目前程序使用经典 Y2K 配色。你可以修改颜色常量：

```python
# CRT 屏幕颜色
screen_color = QColor(0, 40, 80)      # 深蓝色
scan_color = QColor(0, 255, 255)      # 青色

# 文字颜色
text_color = QColor(0, 255, 255)      # 青色
glow_color = QColor(255, 0, 255)      # 洋红色

# 金属机身
metal_color = QColor(220, 230, 240)   # 银色
```

---

## 🐛 故障排除

### 字体显示不正确

**问题**: 按钮和文字使用了系统默认字体而非像素字体

**解决方案**:
1. 确认 `DinkieBitmap-v1.5.0-KeDingKeMao/ttf/` 文件夹存在
2. 检查终端输出是否有 "Loaded pixel font" 消息
3. 如果路径错误，手动修改 `load_pixel_font()` 中的路径

### 模块导入错误

**问题**: `ModuleNotFoundError: No module named 'effects'`

**解决方案**:
```bash
# 确保从正确的目录运行
cd CRT_Buddy  # 进入项目子目录
python main.py
```

### 图片处理失败

**问题**: 图片处理时程序崩溃

**解决方案**:
1. 确认图片格式支持（PNG, JPG, JPEG, GIF, BMP）
2. 检查图片是否损坏
3. 尝试将图片转换为 PNG 格式

### 性能问题

**问题**: 程序运行卡顿

**解决方案**:
```python
# 在 setup_animations() 中调整帧率
self.anim_timer.start(100)  # 从 50 改为 100（降低帧率）

# 减少粒子数量
for _ in range(1):  # 从 3 改为 1
```

---

## 📝 更新日志

### v6.0 (2025-11-18)
- ✨ 新增输入可视化系统
- ✨ 新增实时按键显示和历史记录
- ✨ 新增打字速度统计（CPM）
- ✨ 新增粒子特效系统
- 🎨 优化窗口布局（520x320）
- 🐛 修复模块导入路径问题

### v5.1 (2025-11-17)
- ✨ 新增像素字体支持
- 🎨 改进水平布局设计
- 🎨 优化金属按钮样式
- 😊 新增丰富表情系统

### v5.0 (2025-11-16)
- ✨ 全新的 Y2K 桌面 PC 风格设计
- ✨ 金属质感按钮和机身
- ✨ 圆形电源按钮
- 🐛 修复眼睛追踪问题

### v4.0 及更早版本
- 基础功能实现
- 表情包生成引擎
- Y2K 滤镜效果

---

## 🤝 贡献

欢迎贡献！以下是一些可以参与的方式：

1. 🐛 **报告 Bug** - 在 Issues 中提交
2. 💡 **提出新功能** - 在 Issues 中讨论
3. 🔧 **提交 PR** - Fork 后提交你的改进
4. 📖 **改进文档** - 帮助完善文档
5. 🎨 **分享作品** - 展示你用 CRT Buddy 创作的表情包

### 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

## 👨‍💻 作者

**Seeglo0052**

- GitHub: [@Seeglo0052](https://github.com/Seeglo0052)
- 项目链接: [https://github.com/Seeglo0052/CRT_Buddy](https://github.com/Seeglo0052/CRT_Buddy)

---

## 🙏 致谢

- **DinkieBitmap** - 优秀的像素字体
- **PyQt6** - 强大的 GUI 框架
- **Pillow** - 图像处理库
- 所有 Y2K 美学爱好者和复古风格的支持者

---

## 🌟 Star History

如果这个项目对你有帮助，请给它一个 ⭐！

---

<div align="center">

**用 ❤️ 和 Y2K 美学制作**

[回到顶部](#-crt-buddy)

</div>

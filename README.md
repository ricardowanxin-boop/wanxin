

# 魔兽世界自动操作脚本 当前开发分支20251130

## 项目简介

这是一个用尝试自动化操作魔兽世界游戏的Python脚本，主要功能是自动打开地下城查找器并点击"地心之战"下拉框，简化玩家的日常游戏操作。

## 功能特性

- ✅ 自动聚焦魔兽世界窗口
- ✅ 按I键打开副本界面
- ✅ 自动识别"地心之战"下拉框区域
- ✅ 自适应不同游戏窗口分辨率
- ✅ 支持多种模板匹配算法
- ✅ 单次点击操作，提高准确性
- ✅ 详细的调试信息输出
- ✅ 跨平台支持（Mac和Windows）
- ✅ 完善的错误处理机制

## 技术栈

| 技术 | 用途 | 版本要求 |
|------|------|----------|
| Python | 主要开发语言 | 3.7+ |
| pyautogui | 鼠标和键盘操作 | 最新版 |
| OpenCV | 图像识别和模板匹配 | 最新版 |
| numpy | 图像处理 | 最新版 |
| pygetwindow | 窗口管理（可选） | 最新版 |
| AppleScript | Mac系统窗口管理 | 内置 |

## 安装说明

### 1. 克隆项目

```bash
git clone <repository-url>
cd xOne
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 准备模板图像

1. 启动魔兽世界游戏
2. 打开地下城查找器（按I键）
3. 截图"地心之战"下拉框区域
4. 将截图保存为 `resources/underground_dungeon_template.png`
5. 确保模板基于1920x1080分辨率创建
6. 裁剪模板为最小必要尺寸，只包含下拉框区域

## 使用方法

### 1. 启动游戏

确保魔兽世界游戏已启动并在前台运行。

### 2. 运行脚本

```bash
python src/main.py
```

### 3. 观察执行过程

脚本将自动执行以下操作：
1. 聚焦魔兽世界窗口
2. 按I键打开副本界面
3. 检查鼠标位置
4. 识别"地心之战"下拉框区域
5. 移动鼠标到目标位置
6. 执行单次点击

## 配置说明

### 模板图像

- 文件名：`underground_dungeon_template.png`
- 位置：`resources/underground_dungeon_template.png`
- 要求：基于1920x1080分辨率，只包含下拉框区域

### 参考分辨率

脚本使用1920x1080作为参考分辨率，模板图像应基于此分辨率创建。

### 匹配阈值

默认匹配阈值为0.4，可以在`src/image_recognition.py`中调整：

```python
threshold = 0.4  # 匹配阈值，0.4表示40%以上匹配度
```

## 项目结构

```
xOne/
├── src/
│   ├── main.py              # 主程序入口
│   ├── window_manager.py    # 窗口管理模块
│   ├── image_recognition.py # 图像识别模块
│   ├── keyboard_mouse.py    # 鼠标键盘操作模块
│   └── dungeon_automator.py # 自动化流程控制
├── resources/
│   └── underground_dungeon_template.png # 模板图像
├── requirements.txt         # 依赖列表
└── README.md               # 项目文档
```

## 技术原理

### 1. 自适应分辨率

脚本使用相对比例计算模板大小，适应不同游戏窗口分辨率：

```python
# 计算模板与参考分辨率的比例
template_ratio_w = template_width / 1920
template_ratio_h = template_height / 1080

# 根据游戏窗口实际大小调整模板尺寸
new_template_width = int(game_width * template_ratio_w)
new_template_height = int(game_height * template_ratio_h)
```

### 2. 模板匹配

使用多种模板匹配算法，自动选择最佳匹配：

```python
# 支持的匹配方法
match_methods = [
    (cv2.TM_CCOEFF_NORMED, "TM_CCOEFF_NORMED"),
    (cv2.TM_CCORR_NORMED, "TM_CCORR_NORMED"),
    (cv2.TM_SQDIFF_NORMED, "TM_SQDIFF_NORMED")
]
```

### 3. 窗口管理

- **Mac系统**：使用AppleScript查找并激活游戏窗口
- **Windows系统**：使用Alt+Tab切换窗口

### 4. 鼠标键盘操作

使用pyautogui进行鼠标和键盘操作：

```python
# 按I键打开副本界面
pyautogui.press('i')

# 移动鼠标到目标位置
pyautogui.moveTo(x, y, duration=0.2)

# 执行点击
pyautogui.click(x, y)
```

## 常见问题

### 1. 无法获取游戏窗口坐标

**解决方案**：
- 检查系统权限，确保Python和终端被允许控制电脑
- 确认游戏进程名称正确
- 尝试重启游戏和脚本

### 2. 模板匹配失败

**解决方案**：
- 重新截图模板，确保基于1920x1080分辨率
- 裁剪模板为最小必要尺寸
- 调整匹配阈值

### 3. 点击位置不准确

**解决方案**：
- 重新截图模板，确保只包含下拉框区域
- 调整模板相对比例
- 检查游戏窗口分辨率

## 后续计划

1. 添加配置文件支持
2. 支持多语言游戏界面
3. 实现更多自动化操作
4. 添加图形界面
5. 支持更多游戏版本

## 贡献

欢迎提交Issue和Pull Request，共同改进项目。

## 许可证

MIT License

## 免责声明

本脚本仅用于学习和研究目的，请勿用于商业用途。使用本脚本可能违反游戏的服务条款，请谨慎使用。

---

**最后更新**：2025-11-30
**作者**：TraeAI
**版本**：v1.0.0
import pyautogui

# 参考分辨率
REFERENCE_WIDTH = 1920
REFERENCE_HEIGHT = 1080

# 参考坐标
REFERENCE_X = 800
REFERENCE_Y = 300

print(f"参考分辨率: {REFERENCE_WIDTH}x{REFERENCE_HEIGHT}")
print(f"参考坐标: ({REFERENCE_X}, {REFERENCE_Y})")

# 获取当前屏幕分辨率
screen_width, screen_height = pyautogui.size()
print(f"当前屏幕分辨率: {screen_width}x{screen_height}")

# 计算缩放比例
scale_x = screen_width / REFERENCE_WIDTH
scale_y = screen_height / REFERENCE_HEIGHT
print(f"缩放比例: x={scale_x:.2f}, y={scale_y:.2f}")

# 转换为当前分辨率下的坐标
target_x = int(REFERENCE_X * scale_x)
target_y = int(REFERENCE_Y * scale_y)
print(f"转换后坐标: ({target_x}, {target_y})")

# 验证坐标是否在合理范围内
window_width = screen_width // 2
print(f"估算地下城查找器窗口宽度: {window_width}px")

if target_x < window_width and target_y < screen_height:
    print(f"✓ 坐标计算成功: ({target_x}, {target_y})")
else:
    print(f"✗ 坐标计算失败: ({target_x}, {target_y})")

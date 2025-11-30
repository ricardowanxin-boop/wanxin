#!/usr/bin/env python3
"""测试坐标计算逻辑，验证不同游戏窗口分辨率下的坐标准确性"""

import pyautogui

# 参考分辨率和坐标
REFERENCE_WIDTH = 1920
REFERENCE_HEIGHT = 1080
REFERENCE_X = 600  # 下拉框中心x坐标
REFERENCE_Y = 350  # 下拉框中心y坐标

print("=== 测试坐标计算逻辑 ===")
print(f"参考分辨率: {REFERENCE_WIDTH}x{REFERENCE_HEIGHT}")
print(f"参考坐标: ({REFERENCE_X}, {REFERENCE_Y})")

# 测试不同游戏窗口分辨率
# 模拟不同的游戏窗口大小和位置
window_test_cases = [
    # (game_x, game_y, game_width, game_height)
    (0, 0, 1920, 1080),  # 全屏1920x1080
    (100, 50, 1280, 720),  # 窗口模式1280x720
    (200, 100, 1600, 900),  # 窗口模式1600x900
    (50, 50, 2560, 1440),  # 全屏2560x1440
    (150, 150, 1366, 768),  # 旧显示器分辨率
]

for i, (game_x, game_y, game_width, game_height) in enumerate(window_test_cases, 1):
    print(f"\n=== 测试用例 {i}: 游戏窗口 {game_width}x{game_height} at ({game_x}, {game_y})")
    
    # 计算缩放比例
    scale_x = game_width / REFERENCE_WIDTH
    scale_y = game_height / REFERENCE_HEIGHT
    print(f"缩放比例: x={scale_x:.2f}, y={scale_y:.2f}")
    
    # 转换为相对于游戏窗口的坐标
    relative_x = int(REFERENCE_X * scale_x)
    relative_y = int(REFERENCE_Y * scale_y)
    print(f"相对于游戏窗口的坐标: ({relative_x}, {relative_y})")
    
    # 转换为屏幕坐标
    target_x = game_x + relative_x
    target_y = game_y + relative_y
    print(f"转换为屏幕坐标: ({target_x}, {target_y})")
    
    # 验证坐标是否在合理范围内
    if game_x <= target_x <= game_x + game_width and game_y <= target_y <= game_y + game_height:
        print("✓ 坐标验证通过：计算出的坐标在游戏窗口内")
    else:
        print("✗ 坐标验证失败：计算出的坐标超出游戏窗口范围")
    
    # 计算相对位置百分比，验证是否保持一致
    ref_percent_x = REFERENCE_X / REFERENCE_WIDTH
    ref_percent_y = REFERENCE_Y / REFERENCE_HEIGHT
    calc_percent_x = relative_x / game_width
    calc_percent_y = relative_y / game_height
    print(f"参考位置百分比: ({ref_percent_x:.2f}, {ref_percent_y:.2f})")
    print(f"计算位置百分比: ({calc_percent_x:.2f}, {calc_percent_y:.2f})")
    
    if abs(ref_percent_x - calc_percent_x) < 0.01 and abs(ref_percent_y - calc_percent_y) < 0.01:
        print("✓ 位置百分比验证通过：相对位置保持一致")
    else:
        print("✗ 位置百分比验证失败：相对位置不一致")

print("\n=== 测试完成 ===")

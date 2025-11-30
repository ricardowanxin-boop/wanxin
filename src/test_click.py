#!/usr/bin/env python3
"""测试点击逻辑"""

import pyautogui
import time

print("=== 测试点击逻辑 ===")

# 1. 获取当前鼠标位置
current_x, current_y = pyautogui.position()
print(f"当前鼠标位置: ({current_x}, {current_y})")

# 2. 测试连续点击3次，再双击一次
print("\n2. 测试连续点击3次，再双击一次")
print("点击位置: ({current_x}, {current_y})")

# 连续点击3次
print("执行连续点击3次")
for i in range(3):
    pyautogui.click(current_x, current_y)
    time.sleep(0.1)

# 再双击一次
print("执行双击一次")
pyautogui.doubleClick(current_x, current_y, interval=0.1)

print("\n=== 测试完成 ===")

import pyautogui
import time

class KeyboardMouse:
    def __init__(self):
        # 设置pyautogui的延迟，避免操作过快
        pyautogui.PAUSE = 0.1
        # 记录初始鼠标位置
        self.initial_mouse_pos = pyautogui.position()
    
    def press_key(self, key):
        """按下并释放单个按键"""
        print(f"按下按键: {key}")
        pyautogui.press(key)
    
    def move_mouse(self, x, y, duration=0.5):
        """移动鼠标到指定位置"""
        print(f"移动鼠标到: ({x}, {y})")
        pyautogui.moveTo(x, y, duration=duration)
    
    def click_mouse(self, x=None, y=None, button='left'):
        """点击鼠标，点击一次"""
        if x is not None and y is not None:
            print(f"点击位置: ({x}, {y})")
            # 先移动鼠标到目标位置
            pyautogui.moveTo(x, y, duration=0.2)
            # 输出当前实际鼠标位置，用于调试
            current_pos = pyautogui.position()
            print(f"实际鼠标位置: ({current_pos[0]}, {current_pos[1]})")
            # 点击一次
            print("执行点击一次")
            pyautogui.click(x, y, button=button)
        else:
            print("点击当前位置")
            # 点击一次
            print("执行点击一次")
            pyautogui.click(button=button)
    
    def wait(self, seconds):
        """等待指定秒数"""
        print(f"等待 {seconds} 秒")
        time.sleep(seconds)
    
    def open_dungeon_interface(self):
        """打开副本界面（按I键）"""
        self.press_key('i')
    
    def save_mouse_pos(self):
        """保存当前鼠标位置"""
        self.initial_mouse_pos = pyautogui.position()
    
    def has_mouse_moved(self, threshold=5):
        """检测鼠标是否移动
        Args:
            threshold: 鼠标移动的阈值，单位像素
        Returns:
            bool: 如果鼠标移动超过阈值，返回True，否则返回False
        """
        current_pos = pyautogui.position()
        dx = abs(current_pos[0] - self.initial_mouse_pos[0])
        dy = abs(current_pos[1] - self.initial_mouse_pos[1])
        return dx > threshold or dy > threshold
    
    def wait_for_mouse_stable(self, check_interval=0.5, stable_duration=2, threshold=5):
        """等待鼠标稳定
        Args:
            check_interval: 检测间隔，单位秒
            stable_duration: 稳定持续时间，单位秒
            threshold: 鼠标移动的阈值，单位像素
        Returns:
            bool: 如果鼠标稳定，返回True
        """
        print("等待鼠标稳定...")
        stable_start = None
        while True:
            if self.has_mouse_moved(threshold):
                # 鼠标移动了，重置稳定开始时间
                stable_start = None
                self.save_mouse_pos()
            else:
                # 鼠标没有移动
                if stable_start is None:
                    stable_start = time.time()
                elif time.time() - stable_start >= stable_duration:
                    # 鼠标稳定了指定时间
                    print("鼠标已稳定")
                    return True
            time.sleep(check_interval)

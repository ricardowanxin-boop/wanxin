import time

class DungeonAutomator:
    def __init__(self, window_manager, image_recognition, keyboard_mouse):
        self.window_manager = window_manager
        self.image_recognition = image_recognition
        self.keyboard_mouse = keyboard_mouse
    
    def start_automation(self):
        """开始自动化流程"""
        print("开始魔兽世界自动操作...")
        
        max_retries = 3  # 减少最大重试次数，提高运行效率
        retry_count = 0
        
        while retry_count < max_retries:
            retry_count += 1
            
            try:
                # 1. 自动聚焦魔兽世界窗口
                print(f"\n第 {retry_count} 次尝试 - 1. 自动聚焦魔兽世界窗口")
                if not self.window_manager.focus_game_window():
                    print("无法聚焦游戏窗口，请确保游戏已启动并在前台")
                    return False
                
                # 2. 按I键打开副本界面
                print(f"第 {retry_count} 次尝试 - 2. 按I键打开副本界面")
                self.keyboard_mouse.open_dungeon_interface()
                self.keyboard_mouse.wait(2)  # 等待界面加载
                
                # 3. 检查鼠标是否在游戏窗口内
                print(f"第 {retry_count} 次尝试 - 3. 检查鼠标位置")
                if not self.window_manager.is_mouse_in_game_window():
                    print("鼠标不在游戏窗口内，正在将鼠标移动到游戏窗口")
                    if not self.window_manager.move_mouse_to_game_window():
                        print("无法将鼠标移动到游戏窗口，等待5秒后重试")
                        self.keyboard_mouse.wait(5)
                        continue
                
                # 4. 识别当前窗口中'地心之'字样区域并点击
                print(f"第 {retry_count} 次尝试 - 4. 识别'地心之'字样区域并点击")
                # 传递游戏窗口坐标给识别方法，支持自适应分辨率
                found, position, reason = self.image_recognition.find_underground_dungeon(self.window_manager.game_window_rect)
                
                if found and position:
                    # 记录并输出当前坐标
                    click_x, click_y = position
                    print(f"\n📌 识别结果：")
                    print(f"   状态：成功")
                    print(f"   原因：{reason}")
                    print(f"   坐标：({click_x}, {click_y})")
                    print(f"   正在执行点击操作...")
                    
                    # 移动鼠标到指定位置并点击
                    self.keyboard_mouse.move_mouse(click_x, click_y)
                    self.keyboard_mouse.click_mouse()
                    self.keyboard_mouse.wait(1)
                    print("✅ 操作完成")
                    return True
                else:
                    print(f"\n❌ 识别结果：")
                    print(f"   状态：失败")
                    print(f"   原因：{reason}")
                    print(f"   坐标：无")
                    
                    # 如果是识别问题，等待5秒后重试
                    print("识别失败，等待5秒后重试")
                    self.keyboard_mouse.wait(5)
                    continue
                    
            except Exception as e:
                print(f"操作过程中出错: {e}")
                # 其他错误，等待5秒后重试
                print("发生错误，等待5秒后重试")
                self.keyboard_mouse.wait(5)
                continue
        
        print(f"已达到最大重试次数 {max_retries}，操作失败")
        return False

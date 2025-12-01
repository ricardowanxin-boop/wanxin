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
                
                # 4. 识别"地心之战"下拉框区域
                print(f"第 {retry_count} 次尝试 - 4. 识别'地心之战'下拉框区域")
                success, center_pos, msg = self.image_recognition.find_underground_dungeon(self.window_manager.game_window_rect)
                
                if success:
                    print(f"识别成功: {msg}")
                    # 5. 移动鼠标到目标位置并点击
                    print(f"第 {retry_count} 次尝试 - 5. 移动鼠标到目标位置并点击")
                    
                    # 调整Y坐标，稍微向下偏移，避免点到文字边缘
                    click_x = center_pos[0]
                    click_y = center_pos[1] + 5 # 向下偏移5像素
                    
                    # 直接传入坐标给click_mouse，确保移动和点击的原子性
                    self.keyboard_mouse.click_mouse(click_x, click_y)
                    
                    # 等待下拉框展开
                    self.keyboard_mouse.wait(1.0)
                    
                    # 6. 识别并点击"追随者地下城"
                    print(f"第 {retry_count} 次尝试 - 6. 识别'追随者地下城'选项")
                    success_follower, center_pos_follower, msg_follower = self.image_recognition.find_template('follower_dungeon_template.png', self.window_manager.game_window_rect)
                    
                    if success_follower:
                        print(f"识别成功: {msg_follower}")
                        # 直接传入坐标给click_mouse
                        self.keyboard_mouse.click_mouse(center_pos_follower[0], center_pos_follower[1])
                        
                        # 等待界面响应
                        self.keyboard_mouse.wait(1.0)
                        
                        # 7. 识别并点击"暗焰裂口"（点击左侧复选框）
                        print(f"第 {retry_count} 次尝试 - 7. 识别'暗焰裂口'并点击左侧复选框")
                        success_cleft, pos_info_cleft, msg_cleft = self.image_recognition.find_template('darkflame_cleft_template.png', self.window_manager.game_window_rect, threshold=0.8)
                        
                        if success_cleft:
                            print(f"识别成功: {msg_cleft}")
                            # pos_info_cleft 包含 (center_x, center_y, width, height)
                            center_x, center_y, width, height = pos_info_cleft
                            
                            # 计算左侧复选框位置
                            # 假设复选框在整个模板的最左侧，宽度大约为高度或者是固定的一个小范围
                            # 我们点击模板左边缘向右偏移一点的位置
                            click_x = int(center_x - (width / 2) + 15) # 左边缘 + 15像素
                            click_y = center_y
                            
                            print(f"计算点击位置: 中心({center_x}, {center_y}), 宽{width} -> 点击({click_x}, {click_y})")
                            self.keyboard_mouse.click_mouse(click_x, click_y)
                            
                            # 等待界面响应
                            self.keyboard_mouse.wait(1.0)
                            
                            # 8. 识别并点击"寻找组队"按钮
                            print(f"第 {retry_count} 次尝试 - 8. 识别'寻找组队'按钮")
                            success_group, pos_info_group, msg_group = self.image_recognition.find_template('find_group_template.png', self.window_manager.game_window_rect, threshold=0.8)
                            
                            if success_group:
                                print(f"识别成功: {msg_group}")
                                center_x, center_y, _, _ = pos_info_group
                                self.keyboard_mouse.click_mouse(center_x, center_y)
                                
                                # 等待界面响应，可能需要排队或加载，稍微多等待一会
                                print("等待8秒以进行匹配...")
                                self.keyboard_mouse.wait(8.0)
                                
                                # 9. 识别并点击"进入"按钮
                                print(f"第 {retry_count} 次尝试 - 9. 识别'进入'按钮")
                                success_enter, pos_info_enter, msg_enter = self.image_recognition.find_template('enter_dungeon_template.png', self.window_manager.game_window_rect, threshold=0.68)
                                
                                if success_enter:
                                    print(f"识别成功: {msg_enter}")
                                    center_x, center_y, _, _ = pos_info_enter
                                    self.keyboard_mouse.click_mouse(center_x, center_y)
                                    return True
                                else:
                                    print(f"识别'进入'失败: {msg_enter}")
                                    print("请确保已将'进入'的截图保存为 resources/enter_dungeon_template.png")
                                    # 这里不强制返回False，因为可能已经进入排队状态
                                    # self.keyboard_mouse.wait(2)
                                    # continue
                                    return True # 暂时认为前面的步骤成功即可
                                
                                return True
                            else:
                                print(f"识别'寻找组队'失败: {msg_group}")
                                print("请确保已将'寻找组队'的截图保存为 resources/find_group_template.png")
                                self.keyboard_mouse.wait(2)
                                continue
                            
                            return True
                        else:
                             print(f"识别'暗焰裂口'失败: {msg_cleft}")
                             print("请确保已将'暗焰裂口'的截图保存为 resources/darkflame_cleft_template.png")
                             self.keyboard_mouse.wait(2)
                             continue
                        
                        return True
                    else:
                        print(f"识别'追随者地下城'失败: {msg_follower}")
                        # 如果第二步识别失败，不要立即重试，给用户反馈
                        print("请确保已将'追随者地下城'的截图保存为 resources/follower_dungeon_template.png")
                        self.keyboard_mouse.wait(2)
                        continue
                        
                else:
                    print(f"识别失败: {msg}")
                    
            except Exception as e:
                print(f"操作过程中出错: {e}")
                # 其他错误，等待5秒后重试
                print("发生错误，等待5秒后重试")
                self.keyboard_mouse.wait(5)
                continue
        
        print(f"已达到最大重试次数 {max_retries}，操作失败")
        return False

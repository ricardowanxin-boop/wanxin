import pyautogui
import platform
import subprocess

# 尝试导入pygetwindow库，如果失败则使用默认实现
try:
    import pygetwindow as gw
    has_pygetwindow = True
    print("已成功导入pygetwindow库")
except ImportError:
    has_pygetwindow = False
    print("未安装pygetwindow库，使用默认实现")

class WindowManager:
    def __init__(self):
        # 魔兽世界应用名称列表，用于查找
        self.game_app_names = ["魔兽世界", "World of Warcraft", "Wow", "wow"]
        # 存储游戏窗口对象
        self.game_window = None
        # 存储游戏窗口的坐标范围
        self.game_window_rect = None
    
    def focus_game_window(self):
        """自动聚焦魔兽世界窗口（跨平台）"""
        print("正在聚焦魔兽世界窗口...")
        
        try:
            # 优先使用pygetwindow库（如果可用）
            if has_pygetwindow:
                print("使用pygetwindow库查找游戏窗口")
                if self._focus_with_pygetwindow():
                    return True
                
            # 跨平台聚焦逻辑
            if platform.system() == 'Darwin':  # Mac系统
                return self._focus_mac_window()
            else:  # Windows系统
                return self._focus_windows_window()
            
        except Exception as e:
            print(f"窗口聚焦失败: {e}")
            return False
    
    def _focus_with_pygetwindow(self):
        """使用pygetwindow库聚焦游戏窗口"""
        try:
            # 获取所有窗口
            windows = gw.getAllWindows()
            print(f"找到 {len(windows)} 个窗口")
            
            # 打印所有可见窗口的标题，帮助调试
            visible_windows = [w.title for w in windows if w.title]
            print(f"当前可见窗口列表: {visible_windows}")
            
            # 查找包含游戏名称的窗口
            for window in windows:
                try:
                    window_title = window.title
                    if window_title:
                        for app_name in self.game_app_names:
                            if app_name.lower() in window_title.lower():
                                print(f"找到游戏窗口: {window_title}")
                                # 如果窗口最小化，先还原
                                if window.isMinimized:
                                    print("窗口已最小化，正在还原...")
                                    window.restore()
                                
                                # 激活窗口
                                try:
                                    window.activate()
                                except Exception as activate_error:
                                    print(f"直接激活窗口失败: {activate_error}，尝试最小化后还原")
                                    # 有些情况下直接activate无效，可以尝试先最小化再还原
                                    window.minimize()
                                    pyautogui.sleep(0.2)
                                    window.restore()
                                
                                # 等待窗口激活
                                pyautogui.sleep(1)
                                # 保存窗口对象和坐标
                                self.game_window = window
                                self.game_window_rect = (window.left, window.top, window.right, window.bottom)
                                print(f"游戏窗口坐标: ({window.left}, {window.top}) - ({window.right}, {window.bottom})")
                                return True
                except Exception as e:
                    print(f"处理窗口 '{window.title}' 失败: {e}")
            
            print("使用pygetwindow库未找到游戏窗口")
            return False
            
        except Exception as e:
            print(f"使用pygetwindow库聚焦窗口失败: {e}")
            return False
    
    def _focus_mac_window(self):
        """在Mac系统上聚焦魔兽世界窗口"""
        print("Mac系统：使用AppleScript查找并激活魔兽世界窗口")
        
        # 使用AppleScript查找并激活魔兽世界应用
        for app_name in self.game_app_names:
            try:
                # 构建AppleScript命令
                applescript = f'''
                tell application "System Events"
                    set processList to every process whose name contains "{app_name}"
                    if processList is not {{}} then
                        set frontmost of item 1 of processList to true
                        return true
                    end if
                end tell
                return false
                '''
                
                # 执行AppleScript命令
                result = subprocess.run(
                    ['osascript', '-e', applescript],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                if result.stdout.strip() == "true":
                    print(f"成功激活应用: {app_name}")
                    # 等待窗口激活
                    pyautogui.sleep(1)
                    # 获取游戏窗口坐标范围
                    self._get_mac_window_rect(app_name)
                    return True
                    
            except subprocess.CalledProcessError as e:
                print(f"执行AppleScript失败: {e}")
            except Exception as e:
                print(f"处理Mac窗口失败: {e}")
        
        # 如果通过应用名称没有找到，尝试通过Dock图标激活
        print("尝试通过Dock图标激活魔兽世界")
        try:
            # 使用AppleScript点击Dock上的魔兽世界图标
            applescript = f'''
            tell application "System Events"
                tell process "Dock"
                    # 查找魔兽世界图标
                    set dockItems to UI elements of list 1
                    repeat with dockItem in dockItems
                        try
                            set itemDescription to description of dockItem
                            if itemDescription contains "World of Warcraft" or itemDescription contains "魔兽世界" then
                                click dockItem
                                return true
                            end if
                        end try
                    end repeat
                end tell
            end tell
            return false
            '''
            
            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout.strip() == "true":
                print("成功通过Dock图标激活魔兽世界")
                pyautogui.sleep(1)
                # 尝试获取游戏窗口坐标范围
                for app_name in self.game_app_names:
                    self._get_mac_window_rect(app_name)
                    if self.game_window_rect:
                        break
                return True
                
        except Exception as e:
            print(f"通过Dock图标激活失败: {e}")
        
        print("无法找到或激活魔兽世界窗口，请确保游戏已启动")
        return False
    
    def _get_mac_window_rect(self, app_name):
        """在Mac系统上获取游戏窗口坐标范围"""
        try:
            # 构建AppleScript命令获取窗口坐标
            applescript = f'''
            tell application "System Events"
                set processList to every process whose name contains "{app_name}"
                if processList is not {{}} then
                    set targetProcess to item 1 of processList
                    set windowList to every window of targetProcess
                    if windowList is not {{}} then
                        set targetWindow to item 1 of windowList
                        set {{x, y, width, height}} to bounds of targetWindow
                        return "" & x & "," & y & "," & width & "," & height
                    end if
                end if
            end tell
            return ""
            '''
            
            # 执行AppleScript命令
            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                check=True
            )
            
            output = result.stdout.strip()
            if output:
                # 解析窗口坐标
                x, y, width, height = map(int, output.split(','))
                # 计算窗口的右下角坐标
                x2 = x + width
                y2 = y + height
                self.game_window_rect = (x, y, x2, y2)
                print(f"获取到游戏窗口信息: 位置({x}, {y}), 大小({width}x{height})")
                return True
            
        except Exception as e:
            # 尝试使用另一种AppleScript命令
            try:
                # 构建简化的AppleScript命令
                applescript = f'''
                tell application "System Events"
                    set processList to every process whose name contains "{app_name}"
                    if processList is not {{}} then
                        set targetProcess to item 1 of processList
                        set frontmost of targetProcess to true
                        delay 0.5
                        return "success"
                    end if
                end tell
                return ""
                '''
                
                subprocess.run(
                    ['osascript', '-e', applescript],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # 如果激活成功，假设窗口是全屏或占据整个屏幕
                screen_width, screen_height = pyautogui.size()
                self.game_window_rect = (0, 0, screen_width, screen_height)
                print(f"假设游戏窗口为全屏: {screen_width}x{screen_height}")
                return True
                
            except Exception as e2:
                print(f"简化AppleScript命令执行失败: {e2}")
        
        return False
    
    def _focus_windows_window(self):
        """在Windows系统上聚焦魔兽世界窗口"""
        print("Windows系统：尝试使用Alt+Tab切换窗口")
        # Windows：尝试使用Alt+Tab切换窗口
        pyautogui.hotkey('alt', 'tab')
        pyautogui.hotkey('alt', 'shift', 'tab')
        print("窗口聚焦成功")
        # 对于Windows系统，我们假设整个屏幕都是游戏窗口
        screen_width, screen_height = pyautogui.size()
        self.game_window_rect = (0, 0, screen_width, screen_height)
        print(f"假设Windows游戏窗口坐标范围: (0, 0) - ({screen_width}, {screen_height})")
        return True
    
    def is_mouse_in_game_window(self):
        """判断鼠标是否在游戏窗口内"""
        # 获取当前鼠标位置
        current_mouse_pos = pyautogui.position()
        print(f"当前鼠标位置: {current_mouse_pos}")
        
        # 如果没有获取到游戏窗口坐标，假设鼠标在窗口内
        if not self.game_window_rect:
            print("未获取到游戏窗口坐标，假设鼠标在窗口内")
            return True
        
        # 判断鼠标是否在窗口内
        x1, y1, x2, y2 = self.game_window_rect
        if x1 <= current_mouse_pos[0] <= x2 and y1 <= current_mouse_pos[1] <= y2:
            print(f"鼠标在游戏窗口内: {current_mouse_pos}")
            return True
        else:
            print(f"鼠标在游戏窗口外: {current_mouse_pos}，窗口范围: ({x1}, {y1}) - ({x2}, {y2})")
            return False
    
    def move_mouse_to_game_window(self):
        """将鼠标移动到游戏窗口内"""
        if not self.game_window_rect:
            print("未获取到游戏窗口坐标，无法移动鼠标")
            return False
        
        # 计算窗口中心位置
        x1, y1, x2, y2 = self.game_window_rect
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        
        # 移动鼠标到窗口中心
        print(f"将鼠标移动到游戏窗口中心: ({center_x}, {center_y})")
        pyautogui.moveTo(center_x, center_y, duration=0.5)
        
        # 验证鼠标是否已移动到窗口内
        if self.is_mouse_in_game_window():
            print("鼠标已成功移动到游戏窗口内")
            return True
        else:
            print("鼠标移动失败，仍在游戏窗口外")
            return False

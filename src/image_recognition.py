import cv2
import numpy as np
import pyautogui
import os

class ImageRecognition:
    def __init__(self):
        # 初始化资源目录路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        self.template_dir = os.path.join(project_root, 'resources')
        print(f"资源目录路径: {self.template_dir}")
    
    def capture_screen(self):
        """捕获当前屏幕"""
        screenshot = pyautogui.screenshot()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def find_underground_dungeon(self, game_window_rect=None):
        """使用自适应分辨率的模板匹配查找'地心之战'下拉框区域"""
        print("正在使用自适应分辨率的模板匹配查找'地心之战'下拉框区域...")
        
        try:
            # 模板图像路径
            template_name = 'underground_dungeon_template.png'
            template_path = os.path.join(self.template_dir, template_name)
            
            # 检查模板图像是否存在
            if not os.path.exists(template_path):
                error_msg = f"模板图像不存在: {template_path}"
                print(f"✗ 识别失败：{error_msg}")
                print("  请在游戏中截图'地心之战'下拉框区域，并保存为：")
                print(f"  {template_path}")
                return False, None, error_msg
            
            # 加载模板图像
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                error_msg = f"无法加载模板图像: {template_path}"
                print(f"✗ 识别失败：{error_msg}")
                return False, None, error_msg
            
            # 捕获当前屏幕
            screen = self.capture_screen()
            
            # 获取屏幕尺寸
            screen_height, screen_width = screen.shape[:2]
            print(f"当前屏幕分辨率: {screen_width}x{screen_height}")
            
            # 计算游戏窗口的实际大小和位置
            game_x, game_y, game_width, game_height = 0, 0, screen_width, screen_height
            
            if game_window_rect:
                print(f"使用提供的游戏窗口坐标: {game_window_rect}")
                game_x, game_y, game_right, game_bottom = game_window_rect
                game_width = game_right - game_x
                game_height = game_bottom - game_y
                print(f"游戏窗口实际大小: {game_width}x{game_height}")
            
            # 裁剪游戏窗口区域，只处理游戏窗口内的内容
            game_screen = screen[game_y:game_y+game_height, game_x:game_x+game_width]
            
            # 转换为灰度图像，提高匹配效率
            gray_screen = cv2.cvtColor(game_screen, cv2.COLOR_BGR2GRAY)
            gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            
            # 获取模板尺寸
            template_height, template_width = gray_template.shape
            print(f"原始模板尺寸: {template_width}x{template_height}")
            
            # 计算模板与游戏窗口的比例
            template_ratio_w = template_width / 1920  # 假设模板基于1920x1080分辨率
            template_ratio_h = template_height / 1080
            print(f"模板相对比例: w={template_ratio_w:.4f}, h={template_ratio_h:.4f}")
            
            # 根据游戏窗口实际大小动态调整模板大小
            new_template_width = int(game_width * template_ratio_w)
            new_template_height = int(game_height * template_ratio_h)
            print(f"根据游戏窗口调整后的模板尺寸: {new_template_width}x{new_template_height}")
            
            # 调整模板大小
            gray_template_resized = cv2.resize(gray_template, (new_template_width, new_template_height), interpolation=cv2.INTER_AREA)
            
            # 使用多种模板匹配方法
            match_methods = [
                (cv2.TM_CCOEFF_NORMED, "TM_CCOEFF_NORMED"),
                (cv2.TM_CCORR_NORMED, "TM_CCORR_NORMED"),
                (cv2.TM_SQDIFF_NORMED, "TM_SQDIFF_NORMED")
            ]
            
            best_match = None
            best_score = -1
            best_method = ""
            
            for method, method_name in match_methods:
                result = cv2.matchTemplate(gray_screen, gray_template_resized, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                # 对于不同的匹配方法，最佳匹配值的位置不同
                if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                    current_score = 1 - min_val  # 转换为相似度
                    current_loc = min_loc
                else:
                    current_score = max_val
                    current_loc = max_loc
                
                print(f"  {method_name}: {current_score:.2f}")
                
                if current_score > best_score:
                    best_score = current_score
                    best_match = current_loc
                    best_method = method_name
            
            # 设置匹配阈值（0.4表示40%以上匹配度，降低阈值提高匹配成功率）
            threshold = 0.4
            print(f"最佳匹配方法: {best_method}, 最佳匹配度: {best_score:.2f} (阈值: {threshold})")
            
            if best_score >= threshold:
                # 计算匹配区域的中心坐标（相对于游戏窗口）
                center_x_relative = best_match[0] + new_template_width // 2
                center_y_relative = best_match[1] + new_template_height // 2
                
                # 转换为屏幕坐标
                center_x = game_x + center_x_relative
                center_y = game_y + center_y_relative
                
                print(f"✓ 识别成功：找到'地心之战'下拉框区域")
                print(f"  匹配方法: {best_method}")
                print(f"  匹配度: {best_score:.2f}")
                print(f"  游戏窗口大小: {game_width}x{game_height}")
                print(f"  相对于游戏窗口坐标: ({center_x_relative}, {center_y_relative})")
                print(f"  屏幕坐标: ({center_x}, {center_y})")
                return True, (center_x, center_y), f"{best_method}匹配度: {best_score:.2f}"
            else:
                error_msg = f"未找到匹配区域，最佳匹配度: {best_score:.2f} < 阈值: {threshold}"
                print(f"✗ 识别失败：{error_msg}")
                print("  可能原因：")
                print("  1. 游戏界面未显示'地心之战'下拉框")
                print("  2. 模板图像与当前游戏界面不匹配")
                print("  3. 游戏分辨率或窗口大小变化过大")
                print("  解决方法：重新截图'地心之战'下拉框区域并替换模板图像")
                return False, None, error_msg
                
        except cv2.error as e:
            error_msg = f"OpenCV错误: {e}"
            print(f"✗ 识别失败：{error_msg}")
            return False, None, error_msg
        except Exception as e:
            error_msg = f"系统错误: {e}"
            print(f"✗ 识别失败：{error_msg}")
            import traceback
            traceback.print_exc()
            return False, None, error_msg

from window_manager import WindowManager
from image_recognition import ImageRecognition
from keyboard_mouse import KeyboardMouse
from dungeon_automator import DungeonAutomator


def main():
    """主程序入口"""
    print("=" * 60)
    print("魔兽世界自动操作脚本")
    print("=" * 60)
    print("说明：")
    print("1. 确保游戏已启动并在前台运行")
    print("2. 游戏分辨率推荐1920x1080")
    print("=" * 60)
    
    try:
        # 初始化各个组件
        window_manager = WindowManager()
        image_recognition = ImageRecognition()
        keyboard_mouse = KeyboardMouse()
        
        # 创建自动化实例
        automator = DungeonAutomator(
            window_manager,
            image_recognition,
            keyboard_mouse
        )
        
        # 开始自动化
        automator.start_automation()
        
    except KeyboardInterrupt:
        print("\n\n脚本已被用户中断")
    except Exception as e:
        print(f"\n\n脚本运行出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n脚本已结束运行")


if __name__ == "__main__":
    main()

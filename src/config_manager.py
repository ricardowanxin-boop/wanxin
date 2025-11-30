import json
import os

class ConfigManager:
    def __init__(self, config_path=None):
        if config_path is None:
            # 默认配置文件路径
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.config_path = os.path.join(current_dir, 'config', 'config.json')
        else:
            self.config_path = config_path
        
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件不存在: {self.config_path}")
            return self.get_default_config()
        except json.JSONDecodeError:
            print(f"配置文件格式错误: {self.config_path}")
            return self.get_default_config()
    
    def get_default_config(self):
        """获取默认配置"""
        return {
            "window_title_keywords": ["魔兽世界", "World of Warcraft"],
            "dungeon_name": "追随者地下城-暗焰裂口"
        }
    
    def get_window_title_keywords(self):
        """获取窗口标题关键词"""
        return self.config.get("window_title_keywords", ["魔兽世界", "World of Warcraft"])
    
    def get_dungeon_name(self):
        """获取副本名称"""
        return self.config.get("dungeon_name", "追随者地下城-暗焰裂口")
    
    def update_config(self, new_config):
        """更新配置"""
        self.config.update(new_config)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

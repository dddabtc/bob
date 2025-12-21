"""
语言系统模块
"""

import json
import os
from data.languages import TRANSLATIONS, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, LANGUAGE_NAMES


class LanguageSystem:
    """多语言系统"""

    _instance = None

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self.current_language = DEFAULT_LANGUAGE
        self.config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "saves",
            "settings.json"
        )
        self._load_settings()

    def _load_settings(self):
        """从文件加载语言设置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    lang = settings.get("language", DEFAULT_LANGUAGE)
                    if lang in SUPPORTED_LANGUAGES:
                        self.current_language = lang
        except (json.JSONDecodeError, IOError):
            pass

    def _save_settings(self):
        """保存语言设置到文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

            # 读取现有设置
            settings = {}
            if os.path.exists(self.config_path):
                try:
                    with open(self.config_path, 'r', encoding='utf-8') as f:
                        settings = json.load(f)
                except (json.JSONDecodeError, IOError):
                    pass

            # 更新语言设置
            settings["language"] = self.current_language

            # 保存
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def set_language(self, language_code):
        """设置当前语言"""
        if language_code in SUPPORTED_LANGUAGES:
            self.current_language = language_code
            self._save_settings()
            return True
        return False

    def get_language(self):
        """获取当前语言代码"""
        return self.current_language

    def get_language_name(self):
        """获取当前语言的显示名称"""
        return LANGUAGE_NAMES.get(self.current_language, self.current_language)

    def get_supported_languages(self):
        """获取所有支持的语言"""
        return [(code, LANGUAGE_NAMES.get(code, code)) for code in SUPPORTED_LANGUAGES]

    def next_language(self):
        """切换到下一个语言"""
        idx = SUPPORTED_LANGUAGES.index(self.current_language)
        next_idx = (idx + 1) % len(SUPPORTED_LANGUAGES)
        self.set_language(SUPPORTED_LANGUAGES[next_idx])
        return self.current_language

    def get(self, key, **kwargs):
        """获取翻译文本

        Args:
            key: 翻译键名
            **kwargs: 用于格式化的变量

        Returns:
            翻译后的文本，如果找不到则返回键名
        """
        translation = TRANSLATIONS.get(key, {})
        text = translation.get(self.current_language)

        if text is None:
            # 尝试回退到默认语言
            text = translation.get(DEFAULT_LANGUAGE)

        if text is None:
            # 如果还是找不到，返回键名
            return f"[{key}]"

        # 格式化文本
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass

        return text

    def t(self, key, **kwargs):
        """get 的简写"""
        return self.get(key, **kwargs)


# 全局语言系统实例
_lang_system = None


def get_lang():
    """获取全局语言系统实例"""
    global _lang_system
    if _lang_system is None:
        _lang_system = LanguageSystem()
    return _lang_system


def t(key, **kwargs):
    """快捷翻译函数

    用法:
        from systems.language import t
        print(t("menu_new_game"))  # 输出: "新游戏" 或 "New Game"
        print(t("welcome_message", name="克莱恩"))  # 输出: "欢迎，克莱恩！"
    """
    return get_lang().get(key, **kwargs)


def set_language(language_code):
    """快捷设置语言函数"""
    return get_lang().set_language(language_code)


def get_language():
    """快捷获取当前语言函数"""
    return get_lang().get_language()

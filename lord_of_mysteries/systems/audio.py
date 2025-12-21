"""
音频系统模块
"""

import pygame
import json
import os


class AudioSystem:
    """音频系统 - 管理音效和音乐"""

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

        # 初始化混音器
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.mixer_available = True
        except pygame.error:
            self.mixer_available = False
            print("警告: 音频系统初始化失败")

        # 音量设置 (0.0 - 1.0)
        self.sound_volume = 0.7
        self.music_volume = 0.5
        self.sound_enabled = True
        self.music_enabled = True

        # 音效缓存
        self.sounds = {}

        # 配置文件路径
        self.config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "saves",
            "settings.json"
        )

        # 音频文件目录
        self.audio_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "audio"
        )

        # 加载设置
        self._load_settings()

        # 预加载音效
        self._preload_sounds()

    def _load_settings(self):
        """从文件加载音频设置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.sound_enabled = settings.get("sound_enabled", True)
                    self.music_enabled = settings.get("music_enabled", True)
                    self.sound_volume = settings.get("sound_volume", 0.7)
                    self.music_volume = settings.get("music_volume", 0.5)
        except (json.JSONDecodeError, IOError):
            pass

    def _save_settings(self):
        """保存音频设置到文件"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

            settings = {}
            if os.path.exists(self.config_path):
                try:
                    with open(self.config_path, 'r', encoding='utf-8') as f:
                        settings = json.load(f)
                except (json.JSONDecodeError, IOError):
                    pass

            settings["sound_enabled"] = self.sound_enabled
            settings["music_enabled"] = self.music_enabled
            settings["sound_volume"] = self.sound_volume
            settings["music_volume"] = self.music_volume

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def _preload_sounds(self):
        """预加载常用音效"""
        if not self.mixer_available:
            return

        # 音效文件映射 (如果有音频文件的话)
        sound_files = {
            "attack": "attack.wav",
            "hit": "hit.wav",
            "enemy_death": "enemy_death.wav",
            "player_hurt": "player_hurt.wav",
            "dodge": "dodge.wav",
            "pickup": "pickup.wav",
            "level_up": "level_up.wav",
            "skill": "skill.wav",
            "menu_click": "menu_click.wav",
            "menu_hover": "menu_hover.wav",
            "boss_appear": "boss_appear.wav",
            "wave_complete": "wave_complete.wav",
            "potion_craft": "potion_craft.wav",
            "save": "save.wav",
        }

        for name, filename in sound_files.items():
            path = os.path.join(self.audio_dir, "sounds", filename)
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(self.sound_volume)
                except pygame.error:
                    pass

    def play_sound(self, name):
        """播放音效"""
        if not self.mixer_available or not self.sound_enabled:
            return

        if name in self.sounds:
            self.sounds[name].set_volume(self.sound_volume)
            self.sounds[name].play()

    def play_music(self, filename, loops=-1):
        """播放背景音乐"""
        if not self.mixer_available or not self.music_enabled:
            return

        path = os.path.join(self.audio_dir, "music", filename)
        if os.path.exists(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops)
            except pygame.error:
                pass

    def stop_music(self):
        """停止背景音乐"""
        if self.mixer_available:
            pygame.mixer.music.stop()

    def pause_music(self):
        """暂停背景音乐"""
        if self.mixer_available:
            pygame.mixer.music.pause()

    def resume_music(self):
        """恢复背景音乐"""
        if self.mixer_available and self.music_enabled:
            pygame.mixer.music.unpause()

    def set_sound_enabled(self, enabled):
        """设置音效开关"""
        self.sound_enabled = enabled
        self._save_settings()

    def set_music_enabled(self, enabled):
        """设置音乐开关"""
        self.music_enabled = enabled
        if not enabled:
            self.stop_music()
        self._save_settings()

    def set_sound_volume(self, volume):
        """设置音效音量 (0.0 - 1.0)"""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
        self._save_settings()

    def set_music_volume(self, volume):
        """设置音乐音量 (0.0 - 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.mixer_available:
            pygame.mixer.music.set_volume(self.music_volume)
        self._save_settings()

    def toggle_sound(self):
        """切换音效开关"""
        self.set_sound_enabled(not self.sound_enabled)
        return self.sound_enabled

    def toggle_music(self):
        """切换音乐开关"""
        self.set_music_enabled(not self.music_enabled)
        return self.music_enabled

    def is_sound_enabled(self):
        """获取音效开关状态"""
        return self.sound_enabled

    def is_music_enabled(self):
        """获取音乐开关状态"""
        return self.music_enabled


# 全局音频系统实例
_audio_system = None


def get_audio():
    """获取全局音频系统实例"""
    global _audio_system
    if _audio_system is None:
        _audio_system = AudioSystem()
    return _audio_system


def play_sound(name):
    """快捷播放音效"""
    get_audio().play_sound(name)


def play_music(filename, loops=-1):
    """快捷播放音乐"""
    get_audio().play_music(filename, loops)

#!/usr/bin/env python3
"""
Minecraft 2D - 一个用Python和Pygame制作的2D Minecraft风格游戏

控制方式:
    WASD / 方向键: 移动
    空格: 跳跃
    鼠标左键: 挖掘方块
    鼠标右键: 放置方块
    1-9: 选择快捷栏物品
    E: 打开/关闭背包
    ESC: 暂停游戏
    F3: 显示调试信息

作者: AI Assistant
"""

import os
import sys

# 确保能找到模块
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 检查依赖
try:
    import pygame
except ImportError:
    print("错误: 需要安装 pygame 库")
    print("请运行: pip install pygame")
    sys.exit(1)

from game import Game, main

if __name__ == "__main__":
    print("=" * 50)
    print("  Minecraft 2D")
    print("=" * 50)
    print()
    print("控制方式:")
    print("  WASD / 方向键: 移动")
    print("  空格: 跳跃")
    print("  鼠标左键: 挖掘方块")
    print("  鼠标右键: 放置方块")
    print("  1-9: 选择快捷栏物品")
    print("  E: 打开/关闭背包")
    print("  ESC: 暂停游戏")
    print("  F3: 显示调试信息")
    print()
    print("正在启动游戏...")
    print()

    main()

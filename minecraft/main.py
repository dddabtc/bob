#!/usr/bin/env python3
"""
Minecraft 3D - 一个用Python、Pygame和OpenGL制作的3D Minecraft风格游戏

控制方式:
    WASD: 移动
    空格: 跳跃
    Shift: 冲刺
    Ctrl: 潜行
    鼠标移动: 视角
    左键: 挖掘方块
    右键: 放置方块
    滚轮/1-9: 选择物品
    ESC: 暂停/菜单
    F3: 调试信息
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

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError:
    print("错误: 需要安装 PyOpenGL 库")
    print("请运行: pip install PyOpenGL PyOpenGL_accelerate")
    sys.exit(1)

try:
    import numpy
except ImportError:
    print("错误: 需要安装 numpy 库")
    print("请运行: pip install numpy")
    sys.exit(1)

# 导入3D游戏
from game3d import Game, main

if __name__ == "__main__":
    print("=" * 50)
    print("  Minecraft 3D")
    print("=" * 50)
    print()
    print("控制方式:")
    print("  WASD: 移动")
    print("  空格: 跳跃")
    print("  Shift: 冲刺")
    print("  鼠标: 视角")
    print("  左键: 挖掘")
    print("  右键: 放置")
    print("  滚轮/1-9: 选择物品")
    print("  ESC: 暂停")
    print("  F3: 调试信息")
    print()
    print("正在启动游戏...")
    print()

    main()

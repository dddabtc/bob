#!/usr/bin/env python3
"""
诡秘之主 - Lord of Mysteries
实时动作RPG游戏

基于《诡秘之主》世界观
玩家选择途径，打怪收集材料，炮制魔药晋升序列
"""

from game import Game


def main():
    """游戏入口"""
    print("=" * 50)
    print("       诡秘之主 - Lord of Mysteries")
    print("            实时动作RPG游戏")
    print("=" * 50)
    print()
    print("操作说明:")
    print("  WASD / 方向键  - 移动")
    print("  J / 鼠标左键   - 攻击")
    print("  K / 鼠标右键   - 闪避")
    print("  1-4 数字键     - 释放技能")
    print("  I              - 打开背包")
    print("  ESC            - 暂停菜单")
    print()
    print("游戏目标: 选择途径，收集材料，晋升序列！")
    print("-" * 50)
    print()

    game = Game()
    game.run()


if __name__ == "__main__":
    main()

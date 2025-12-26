# 昼夜循环系统
import math
from settings3d import (
    DAY_LENGTH, DAWN_START, DAY_START, DUSK_START, NIGHT_START, NIGHT_END
)


class DayNightCycle:
    """昼夜循环系统"""

    def __init__(self, start_time=0.2):
        """
        初始化昼夜循环
        start_time: 初始时间 (0.0-1.0, 0.2=早晨)
        """
        self.time = start_time  # 0.0-1.0 表示一天中的时间
        self.day_count = 1

    def update(self, dt):
        """更新时间"""
        self.time += dt / DAY_LENGTH
        if self.time >= 1.0:
            self.time -= 1.0
            self.day_count += 1

    def get_time_of_day(self):
        """获取当前时段"""
        if self.time < DAY_START:
            return 'dawn'      # 黎明
        elif self.time < DUSK_START:
            return 'day'       # 白天
        elif self.time < NIGHT_START:
            return 'dusk'      # 黄昏
        elif self.time < NIGHT_END:
            return 'night'     # 夜晚
        else:
            return 'dawn'      # 黎明（循环）

    def is_night(self):
        """是否为夜晚（僵尸生成时间）"""
        return NIGHT_START <= self.time < NIGHT_END

    def is_dangerous_time(self):
        """是否为危险时间（黄昏到黎明）"""
        return self.time >= DUSK_START or self.time < DAY_START

    def get_sky_color(self):
        """获取天空颜色"""
        # 基础颜色
        day_sky = (0.53, 0.81, 0.92)      # 蓝天
        dawn_sky = (0.9, 0.6, 0.4)         # 橙红色黎明
        dusk_sky = (0.85, 0.5, 0.3)        # 橙色黄昏
        night_sky = (0.05, 0.05, 0.15)     # 深蓝夜空

        time_of_day = self.get_time_of_day()

        if time_of_day == 'day':
            return day_sky
        elif time_of_day == 'night':
            return night_sky
        elif time_of_day == 'dawn':
            # 从夜晚过渡到白天
            if self.time >= NIGHT_END:
                # NIGHT_END 到 1.0 的过渡
                t = (self.time - NIGHT_END) / (1.0 - NIGHT_END)
            else:
                # 0.0 到 DAY_START 的过渡
                t = (self.time + (1.0 - NIGHT_END)) / (DAY_START + (1.0 - NIGHT_END))
            return self._lerp_color(night_sky, dawn_sky, min(t * 2, 1.0))
        else:  # dusk
            # 从白天过渡到夜晚
            t = (self.time - DUSK_START) / (NIGHT_START - DUSK_START)
            return self._lerp_color(dusk_sky, night_sky, t)

    def get_fog_color(self):
        """获取雾颜色（与天空相关但更淡）"""
        sky = self.get_sky_color()
        # 雾比天空颜色更淡
        return (
            min(sky[0] + 0.15, 1.0),
            min(sky[1] + 0.15, 1.0),
            min(sky[2] + 0.15, 1.0),
            1.0
        )

    def get_ambient_light(self):
        """获取环境光强度 (0.0-1.0)"""
        time_of_day = self.get_time_of_day()

        if time_of_day == 'day':
            return 1.0
        elif time_of_day == 'night':
            return 0.2  # 夜晚较暗但不是完全黑
        elif time_of_day == 'dawn':
            if self.time >= NIGHT_END:
                t = (self.time - NIGHT_END) / (1.0 - NIGHT_END)
            else:
                t = (self.time + (1.0 - NIGHT_END)) / (DAY_START + (1.0 - NIGHT_END))
            return 0.2 + 0.8 * t
        else:  # dusk
            t = (self.time - DUSK_START) / (NIGHT_START - DUSK_START)
            return 1.0 - 0.8 * t

    def get_time_string(self):
        """获取时间字符串（24小时制）"""
        hours = int(self.time * 24)
        minutes = int((self.time * 24 - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"

    def get_display_info(self):
        """获取显示信息"""
        time_names = {
            'dawn': '黎明',
            'day': '白天',
            'dusk': '黄昏',
            'night': '夜晚'
        }
        return {
            'time': self.get_time_string(),
            'period': time_names[self.get_time_of_day()],
            'day': self.day_count,
            'is_night': self.is_night()
        }

    def _lerp_color(self, c1, c2, t):
        """线性插值颜色"""
        return (
            c1[0] + (c2[0] - c1[0]) * t,
            c1[1] + (c2[1] - c1[1]) * t,
            c1[2] + (c2[2] - c1[2]) * t
        )

    def set_time(self, time):
        """设置时间 (用于调试)"""
        self.time = time % 1.0

    def skip_to_day(self):
        """跳到白天"""
        self.time = DAY_START + 0.01

    def skip_to_night(self):
        """跳到夜晚"""
        self.time = NIGHT_START + 0.01

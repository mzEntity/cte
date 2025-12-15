import sys
import atexit
import os

# ANSI 转义序列
ALT_SCREEN_ON = "\033[?1049h\033[H"   # 启用替代屏幕 + 清屏 + 光标归位
ALT_SCREEN_OFF = "\033[?1049l"        # 切回主屏幕

class BufferSwitcher:
    def __init__(self):
        self._active = False

    def enter(self):
        """进入替代屏幕（干净缓冲区）"""
        if not self._active:
            sys.stdout.write(ALT_SCREEN_ON)
            sys.stdout.flush()
            self._active = True
            # 注册自动退出（防止异常退出后卡在替代屏）
            atexit.register(self.exit)

    def exit(self):
        """退出替代屏幕，恢复原终端"""
        if self._active:
            sys.stdout.write(ALT_SCREEN_OFF)
            sys.stdout.flush()
            self._active = False

    def __enter__(self):
        self.enter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit()

# 全局便捷函数（可选）
def use_alternate_screen():
    """返回一个上下文管理器，用于 with 语句"""
    return BufferSwitcher()


with use_alternate_screen():
    print("这是干净的全屏缓冲区！")
    input("按回车退出...")
# 自动恢复原终端
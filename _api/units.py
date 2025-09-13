import win32api
import win32con
import win32gui
import win32process

from .window import  Window


def _get_windows_by_pid(target_pid: int) -> list[Window]:
    windows = []

    def enum_windows_callback(hwnd, _):
        # 获取窗口的进程ID
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        if pid == target_pid:
            class_name = win32gui.GetClassName(hwnd)
            title = win32gui.GetWindowText(hwnd)
            windows.append(Window(hwnd, pid, class_name, title))
        return True

    # 枚举所有顶级窗口
    win32gui.EnumWindows(enum_windows_callback, None)

    return windows


def _get_potplayer_window_by_pid(target_pid: int) -> Window:
    windows = _get_windows_by_pid(target_pid)

    # 筛选出类名为PotPlayer的窗口
    potplayer_windows = [window for window in windows if window.class_name == "PotPlayer"]

    if not potplayer_windows:
        raise ValueError(f"进程ID {target_pid} 中没有找到PotPlayer窗口")

    # 返回第一个PotPlayer窗口
    return potplayer_windows[0]

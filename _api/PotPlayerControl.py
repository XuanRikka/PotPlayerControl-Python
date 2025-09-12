import win32gui
import win32con

from .MessageTypeConst import MessageTypeConst

COMMAND_TYPE = win32con.WM_COMMAND
REQUEST_TYPE = win32con.WM_USER

class PlayStatus:
    Stopped = -1
    Paused = 1
    Running = 2
    Undefined = 0

class PotPlayerControl:
    def __init__(self, hwnd: int):
        """
        参数：
            hwnd (int): PotPlayer播放器的窗口句柄
        """
        self.hwnd = hwnd
        try:
            win32gui.GetWindow(hwnd, 5)
        except Exception as error:
            if error.args[2] == "无效的窗口句柄。":
                raise ValueError("hwnd无效")

    def play(self):
        """开始播放"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.PLAY, 0)

    def pause(self):
        """暂停播放"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.PAUSE, 0)

    def stop(self):
        """停止播放"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.STOP, 0)

    def previous(self):
        """播放上一个视频"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.PREVIOUS, 0)

    def next(self):
        """播放下一个视频"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.NEXT, 0)

    def play_pause(self):
        """切换播放/暂停状态"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.PLAY_PAUSE, 0)

    def volume_up(self):
        """音量增加"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.VOLUME_UP, 0)

    def volume_down(self):
        """音量减少"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.VOLUME_DOWN, 0)

    def mute(self):
        """静音切换"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.TOGGLE_MUTE, 0)

    def toggle_sub(self):
        """切换字幕显示"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.TOGGLE_SUBS, 0)

    def toggle_osd(self):
        """切换OSD"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.TOGGLE_OSD, 0)

    def fullscreen(self):
        """切换全屏"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.FULLSCREEN, 0)

    def five_sec_back(self):
        """后退5秒"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.FIVE_SEC_BACK, 0)

    def five_sec_forward(self):
        """前进5秒"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.FIVE_SEC_FORWARD, 0)

    def thirty_sec_forward(self):
        """前进30秒"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.THIRTY_SEC_FORWARD, 0)

    def thirty_sec_back(self):
        """后退30秒"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.THIRTY_SEC_BACK, 0)

    def one_minute_back(self):
        """后退1分钟"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.ONE_MIN_BACK, 0)

    def one_minute_forward(self):
        """前进1分钟"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.ONE_MIN_FORWARD, 0)

    def five_minute_back(self):
        """后退5分钟"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.FIVE_MIN_BACK, 0)

    def five_minute_forward(self):
        """前进5分钟"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.FIVE_MIN_FORWARD, 0)

    def speed_up(self):
        """播放加速"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.SPEED_UP, 0)

    def speed_down(self):
        """播放江苏"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.SPEED_DOWN, 0)

    def speed_normal(self):
        """恢复正常速度"""
        win32gui.PostMessage(self.hwnd, COMMAND_TYPE, MessageTypeConst.SPEED_NORMAL, 0)

    def get_volume(self):
        """
        获取当前音量

        返回：
            int: 当前音量值（0-100）
        """
        return win32gui.SendMessage(self.hwnd, REQUEST_TYPE, MessageTypeConst.GET_VOLUME, 0)

    def set_volume(self, volume: int):
        """
        设置音量

        参数：
            volume (int): 音量值（0-100）
        """
        win32gui.PostMessage(self.hwnd, REQUEST_TYPE, MessageTypeConst.SET_VOLUME, volume)

    def get_total_time(self):
        """
        获取媒体总时长（毫秒）

        返回：
            int: 总时长（毫秒）
        """
        return win32gui.SendMessage(self.hwnd, REQUEST_TYPE, MessageTypeConst.GET_TOTAL_TIME, 0)

    def get_progress_time(self):
        """
        获取播放进度（毫秒）

        返回：
            int: 进度（毫秒）
        """
        return win32gui.SendMessage(self.hwnd, REQUEST_TYPE, MessageTypeConst.GET_PROGRESS_TIME, 0)

    def get_current_time(self):
        """
        获取当前播放（毫秒）

        返回：
            int: 当前（毫秒）
        """
        return win32gui.SendMessage(self.hwnd, REQUEST_TYPE, MessageTypeConst.GET_CURRENT_TIME, 0)

    def set_current_time(self, time: int):
        """
        设置当前播放时间

        参数：
            time (int): 要设置的进度位置（毫秒）
        """
        win32gui.PostMessage(self.hwnd, REQUEST_TYPE, MessageTypeConst.SET_CURRENT_TIME, time)

    def get_play_status(self) -> int:
        """
        获取播放状态

        返回：
            PlayStatus: 播放状态枚举值
        """
        status_code = win32gui.SendMessage(self.hwnd, REQUEST_TYPE, MessageTypeConst.GET_PLAY_STATUS, 0)
        if status_code == -1:
            return PlayStatus.Stopped
        elif status_code == 1:
            return PlayStatus.Paused
        elif status_code == 2:
            return PlayStatus.Running
        else:
            return PlayStatus.Undefined

    def send_virtual_key(self, key_code: int):
        """
        发送虚拟按键

        参数：
            key_code (int): 按键代码
        """
        win32gui.SendMessage(self.hwnd, REQUEST_TYPE, MessageTypeConst.SEND_VIRTUAL_KEY, key_code)

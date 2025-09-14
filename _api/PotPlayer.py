from time import sleep
from typing import Iterable
from pathlib import Path
from functools import wraps
import subprocess
import psutil

from .units import _get_windows_by_pid, _get_potplayer_window_by_pid
from .PotPlayerControl import PotPlayerControl, PlayStatus
from .window import Window

PathLike = str | Path


def to_path(path: PathLike | Iterable[PathLike]) -> list[Path] | None:
    """
    把Iterable[str | Path]统一转换为list[Path]

    参数：
        path (PathLike | Iterable[PathLike]): 需要转换的对象/列表
    返回：
        list[Path]: 转换完成的对象/列表
    """
    if isinstance(path, (str, Path)):
        return [Path(path).resolve()]
    elif isinstance(path, Iterable):
        return [Path(i).resolve() for i in path]
    else:
        return None


def check_pid_wraps(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._check_pid():
            raise RuntimeError(f"PotPlayer进程未启动或者被关闭")
        return func(self, *args, **kwargs)

    return wrapper


class PotPlayer:
    def __init__(self, player_path: Path | str):
        if isinstance(player_path, str):
            player_path = Path(player_path)
            if not player_path.exists():
                raise ValueError("播放器路径无效")
        self.player_path: Path = player_path
        self.video_files: list[Path] | None = None
        self.running: bool = False
        self.pid: int | None = None
        self._window: Window | None = None
        self._control: PotPlayerControl | None = None

    def run(self, video_files: PathLike | Iterable[PathLike] | None = None):
        """
        运行PotPlayer播放器并初始化播放器控制器

        参数：
            video_files: 视频文件路径或路径列表。可以是以下类型之一：
                         - 单个视频文件路径（字符串或Path对象）
                         - 视频文件路径的可迭代对象（列表、元组等）
                         - None（不指定文件，启动空播放器）
        行为：
            当传入单个视频文件路径时PotPlayer会自动使用视频文件所在路径创建播放列表
            当传入多个视频文件路径时会采用这些视频文件路径作为播放列表
        """
        if video_files is None:
            command = f"{self.player_path}"
            process = subprocess.Popen(command)
        else:
            video_files = to_path(video_files)
            video_files = " ".join([str(i) for i in video_files])
            command = f"{self.player_path} {video_files}"
            process = subprocess.Popen(command)
        self.pid = process.pid
        while True:
            try:
                window_info = _get_potplayer_window_by_pid(self.pid)
            except ValueError as error:
                pass
            except Exception as error:
                raise error
            else:
                break

        self._window = window_info
        self._control = PotPlayerControl(hwnd=window_info.hwnd)
        self.running = True

    @check_pid_wraps
    def close(self, timeout: int) -> bool:
        try:
            process = psutil.Process(self.pid)
            process.terminate()
            process.wait(timeout=timeout)
            print(f"PotPlayer进程已正常关闭")
        except psutil.NoSuchProcess:
            print(f"播放器进程不存在")
        except psutil.TimeoutExpired:
            print(f"播放器进程关闭超时，尝试强制终止")
            try:
                process.kill()
                process.wait(timeout=2)
                print(f"播放器进程已强制终止")
            except:
                print(f"无法终止播放器进程")
                return False
        except psutil.AccessDenied:
            print(f"权限不足，无法终止播放器进程")
            return False
        except Exception as e:
            print(f"关闭进程时发生错误: {e}")
            return False
        finally:
            self.running = False
            self.pid = None
            self.video_files = None
            self._control = None
        return True

    @check_pid_wraps
    def restart(self, video_files: Iterable[PathLike] | None = None):
        video_files = to_path(video_files)
        self.close()
        self.run(video_files)

    def _check_pid(self) -> bool:
        """
        检查播放器进程是否存在
        """
        try:
            if self.pid is None:
                raise ValueError("播放器没有启动")
            elif psutil.pid_exists(self.pid):
                self.running = True
                return True
            else:
                return False
        except (psutil.NoSuchProcess, ValueError):
            self.running = False
            self.pid = None
            self._window = None
            self._control = None
            self.video_files = None
            return False

    @check_pid_wraps
    def wait_play(self):
        """
        阻塞等待到播放开始
        行为：当没有在播放/存在更新提示窗口时阻塞
        应在使用run函数后使用这个函数等待到播放正式开始
        """
        while True:
            if self._control.get_play_status() == PlayStatus.Running:
                break
            if not self._check_pid():
                break
            sleep(0.5)

    @check_pid_wraps
    def get_control(self):
        return self._control

from time import sleep
from typing import Iterable
from pathlib import Path
import subprocess

from .units import _get_windows_by_pid, _get_potplayer_window_by_pid
from .PotPlayerControl import PotPlayerControl
from .window import Window

PathLike = str | Path


def to_path(path: PathLike | Iterable[PathLike]) -> list[Path]:
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
        self.window: Window | None = None
        self.control: PotPlayerControl | None = None

    def run(self, video_files: PathLike | Iterable[PathLike] | None = None):
        if video_files is None:
            process = subprocess.Popen(f"{self.player_path}")
        else:
            video_files = to_path(video_files)
            video_files = " ".join([str(i) for i in video_files])
            process = subprocess.Popen(f"{self.player_path} {video_files}")
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

        self.window = window_info
        self.control = PotPlayerControl(hwnd=window_info.hwnd)
        self.running = True




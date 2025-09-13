from dataclasses import dataclass

@dataclass
class Window:
    hwnd: int  # 窗口句柄
    pid: int  # 进程ID
    class_name: str  # 窗口类名
    title: str  # 窗口标题

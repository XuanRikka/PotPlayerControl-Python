import win32api
import win32con
import win32gui
import win32process


def find_potplayer():
    """
    查找PotPlayer窗口

    返回：
        list: 包含窗口信息的字典列表，每个字典包含hwnd、pid、title等信息
    """
    windows = []
    target_processes = ["PotPlayerMini.exe", "PotPlayerMini64.exe"]

    def enum_windows_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            try:
                process_handle = win32api.OpenProcess(
                    win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
                    False, pid
                )

                process_exe = win32process.GetModuleFileNameEx(process_handle, 0)
                process_name = process_exe.split('\\')[-1].lower()

                if any(target_process.lower() == process_name for target_process in target_processes):
                    title = win32gui.GetWindowText(hwnd)
                    if title:
                        windows.append({
                            'hwnd': hwnd,
                            'pid': pid,
                            'title': title,
                            'class_name': win32gui.GetClassName(hwnd),
                            'process_path': process_exe,
                            'process_name': process_name
                        })

                win32api.CloseHandle(process_handle)

            except Exception as e:
                pass

        return True

    win32gui.EnumWindows(enum_windows_callback, None)
    return windows
import win32gui
import win32con

def get_windows():
    def sort_windows(windows):
        sorted_windows = []

        # Find the first entry
        [print(n) for n in windows]
        for window in windows:
            if window["hwnd_above"] == 0:
                sorted_windows.append(window)
                break
            else:
                raise(IndexError("Could not find first entry"))

        # Follow the trail
        while True:
            for window in windows:
                if sorted_windows[-1]["hwnd"] == window["hwnd_above"]:
                    sorted_windows.append(window)
                    break
            else:
                break

        # Remove hwnd_above
        for window in windows:
            del(window["hwnd_above"])

        return sorted_windows

    def enum_handler(hwnd, results):
        window_placement = win32gui.GetWindowPlacement(hwnd)
        results.append({"hwnd":hwnd, \
                "hwnd_above":win32gui.GetWindow(hwnd, win32con.GW_HWNDPREV), \
                "title":win32gui.GetWindowText(hwnd), \
                "visible":win32gui.IsWindowVisible(hwnd) == 1, \
                "minimized":window_placement[1] == win32con.SW_SHOWMINIMIZED, \
                "maximized":window_placement[1] == win32con.SW_SHOWMAXIMIZED, \
                "rectangle":win32gui.GetWindowRect(hwnd) \
                })

    enumerated_windows = []
    win32gui.EnumWindows(enum_handler,enumerated_windows)
    return sort_windows(enumerated_windows)

if __name__ == "__main__":
    windows = get_windows()
    
    for window in windows:
        print(window)
    print()

    # Pretty print
    for window in windows:
        if window["title"] == "" or not window["visible"]:
            continue
        print(window)

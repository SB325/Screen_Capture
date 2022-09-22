import win32gui
import win32con
import sys

def get_windows(screenname):
    def sort_windows(windows,screenname):
        sorted_windows = []
        
        for window in windows:
            if screenname in window['title'] and 'Command Prompt' not \
            in window['title']:
                sorted_windows.append(window)
        
        if sorted_windows:
            return sorted_windows
        else:
            raise(IndexError(f"No window matching name: {screenname}"))

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
    return sort_windows(enumerated_windows,screenname)

if __name__ == "__main__":
   if len(sys.argv)>1:
        sname = sys.argv[1]
        windows = get_windows(sname)
    

import win32gui
import win32api
classname = "MozillaWindowClass"
titlename = "百度一下，你就知道"
#获取句柄
hwnd = win32gui.FindWindow(classname, titlename)
#获取窗口左上角和右下角坐标
left, top, right, bottom = win32gui.GetWindowRect(hwnd)


print(left, top, right, bottom)
import random
import win32api, win32gui, win32ui, win32com, win32con
import PIL
import cv2
from PIL import Image


def func_im_grab(hwnd, zooming=1):
    '''
    截图函数，输入句柄，返回PIL格式的im对象。
    '''
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = int((right - left)*zooming)
    height = int((bot - top)*zooming)
    #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hwndDC = win32gui.GetWindowDC(hwnd)
    #创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)  ### 1个
    #创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()  ###2个
    #创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()  ###3
    #为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
    #将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    #保存bitmap到内存设备描述表
    saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)

    ##方法二(第一部分)：PIL保存
    ###获取位图信息
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    ###生成图像
    ### 内存释放。清除两个dc，十分十分重要，不然会造成内存溢出。
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd,hwndDC)
    ### opencv格式转PIL
    im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
    return im_PIL


def click(clickpos):
    '''
    窗口点击
    
    '''
    win32api.SetCursorPos(clickpos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP|win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    return

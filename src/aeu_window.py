import random
import win32api, win32gui, win32ui, win32com, win32con
import PIL
import cv2
import time
from PIL import Image

class aeu_window:
    '''
    模拟器窗口类
    '''
    def __init__(
        self, 
        instant_name, 
        emu_type="nox",
        zooming="auto"
        ):
        self.name=instant_name
        #截图
        self.capture=0
        self.dict_init={
            #夜神模拟器载入类
            "nox":self.init_nox
        }
        self.dict_init.get(emu_type)(self.name)
        #临时日志函数
        self.info=print
        return

    def init_nox(self,name):
        '''
        夜神模拟器的初始化类。
        根据实例名称确定父窗、子窗、截图窗、操作窗、操作窗偏移。
        '''


    def set_zooming(self, zooming_arg):
        '''
        设置系统缩放
        '''
        if zooming_arg=="auto":
            #自动获取系统缩放，目前暂时默认1
            self.zooming=1
        else:
            self.zooming=float(zooming_arg)

    def find_emuwindow(self, hwnd):
        win32gui.FindWindow(None, "andro2")


    def click(self, rel_pos):
        '''
        点击准备按钮。写死了位置，假如改了分辨率，这个要重新改。后续将变成算的
        '''
        pos_center = (500,500)
        long_target = win32api.MAKELONG(*pos_center)
        win32api.SendMessage(hwnd,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,long_target)
        time.sleep(0.02+ 0.03*random.random())
        win32api.SendMessage(hwnd,win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,long_target)
        return



    hwnd=0xC05AC



    hwnd=0x16076E

    
    hwnd=0x220730

    hwnd=0xC05AC
    hwnd=0x20AC0

    c=func_im_grab(hwnd,zooming=1.25)
    c.show()


win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
time.sleep(0.02+ 0.03*random.random())
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)



def doo(hwnd):
    '''
    找到hwnd是否为sub
    '''

    class_name= win32gui.GetClassName(hwnd)
    print(hwnd,class_name)
    if class_name ==  "subWin":
        print('yes!',hwnd, class_name)
    return


def demo_child_windows(parent):
    '''
    演示如何列出所有的子窗口
    :return:
    '''

    hWndChildList = []
    win32gui.EnumChildWindows(parent, doo,  hWndChildList)
    return hWndChildList
 

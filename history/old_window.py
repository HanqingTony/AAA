import win32com
import win32api
import win32con
import win32gui
import win32ui
import pymysql
import math
import time
from PIL import Image
import logging
import numpy as np
import cv2
import aircv as ac
import random
import datetime



class window:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.pos
        self.
        return

    def grabScreen(self):
        '''
        截图函数，返回PIL格式的im对象。
        '''
        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        width = right - left
        height = bot - top
        #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        hwndDC = win32gui.GetWindowDC(self.hwnd)
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
        win32gui.DeleteObject(saveBitMap.GetHandle())

        ### 清除两个dc，十分十分重要，不然会造成内存溢出。
        saveDC.DeleteDC()
        mfcDC.DeleteDC()

        ### opencv格式转PIL
        im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
        return im_PIL


    def click(self, tuple_pos):
        '''
        点击准备按钮。写死了位置，假如改了分辨率，这个要重新改。后续将变成算的
        '''
        pos_center = (633,332)
        pos_rand = (633+ random.randint(-20, 20), 332+random.randint(-20, 20))
        logger.info(
            '点击:位置'+ str(pos_rand)
        )
        long_target = win32api.MAKELONG(*pos_rand)
        win32api.SendMessage(hwnd_child,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,long_target)
        time.sleep(0.02+ 0.03*random.random())
        win32api.SendMessage(hwnd_child,win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,long_target)
        return
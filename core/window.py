import win32gui
import win32api
import win32ui
import win32con
from PIL import Image
import random
import aircv as ac
import cv2
import numpy as np

class window:
    '''
    window类，写一些基本的窗口相关的方法
    '''
    def __init__(self, window_name, zooming=1.25):
        '''
        输入窗口名，创建类
        '''
        self.hwnd=win32gui.FindWindow(None, window_name)
        self.zooming=zooming
        self.update_position()
        return

    def grab(self):
        '''
        截图函数，返回PIL格式的im对象。
        '''
        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        width = int((right - left)*self.zooming)
        height = int((bot - top)*self.zooming)
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
        ### 内存释放。清除两个dc，十分十分重要，不然会造成内存溢出。
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd,hwndDC)
        ### opencv格式转PIL
        im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
        return im_PIL

    def grab_ndarray(self):
        '''
        return numpy.ndarray img object
        '''
        #截图,返回ndarray格式
        img_capt=self.grab()
        ndarray_capt = cv2.cvtColor(np.asarray(img_capt), cv2.COLOR_RGB2BGR)
        return ndarray_capt

    def click(self, tuple_pos):
        '''
        点击,兼容坐标和百分比
        '''
        if tuple_pos[0]>1 and tuple_pos[1]>1:
            self.click_byxy(tuple_pos)
        else:
            self.click_byprop(tuple_pos)
        return

    def click_byprop(self,tuple_pos):
        '''
        根据坐标百分比
        '''        
        self.update_position()
        click_x=int(tuple_pos[0]*self.width)
        click_y=int(tuple_pos[1]*self.height)
        clickpos=(click_x+self.zero_x,click_y+self.zero_y)
        self.click_abs(clickpos) 
        return

    def click_byxy(self, tuple_pos):
        '''
        根据xy坐标点击
        '''
        self.update_position()
        click_x=int(tuple_pos[0])
        click_y=int(tuple_pos[1])
        clickpos=(click_x+self.zero_x,click_y+self.zero_y)
        self.click_abs(clickpos) 
        return

    def click_abs(self, tuple_pos):
        '''
        绝对坐标点击
        '''
        win32api.SetCursorPos(tuple_pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP|win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        return

    def click_byxy_rand(self, tuple_pos, r=0):
        '''
        传入点击位置，随机半径，随机点击半径内的位置。
        使用标准正态分布
        '''
        #加入随机
        random_x=random.normalvariate()
        if abs(random_x)>3:
            random_x=0
        offset_x=int(r*random_x/3)
        random_y=random.normalvariate()
        if abs(random_y)>3:
            random_y=0
        offset_y=int(r*random_y/3)
        self.click_byxy((tuple_pos[0]+offset_x, tuple_pos[1]+offset_y))
        return

    def update_position(self):
        '''
        获取窗口位置
        '''
        self.position=win32gui.GetWindowRect(self.hwnd)
        self.zero_x=self.position[0]
        self.zero_y=self.position[1]
        self.zero_pos=(self.zero_x,self.zero_y)
        self.width=self.position[2]-self.position[0]
        self.height=self.position[3]-self.position[1]
        return

    def find(self, ndarray_template, confidence=0.95):
        '''
        输入一个ndarray_template图片，找到所在位置，否则返回Null
        只返回找到的第一个。
        返回值为一个字典，第一个是成功与否，第二个是经过缩放修正的位置坐标
        '''
        ndarray_capt=self.grab_ndarray()
        judge = ac.find_template(ndarray_capt, ndarray_template)
        if judge==None:
            out = {
                "found":False,
                "position":(-1,-1)
            }
        elif judge['confidence']>confidence:
            out = {
                "found":True,
                "position":(
                    int(judge['result'][0]/self.zooming),
                    int(judge['result'][1]/self.zooming)
                )
            }
        else:
            out = {
                "found":False,
                "position":(-1,-1)
            }
        return out

if __name__=="__main__":
    path_coins="assets/coins.bmp"
    path_challenge="assets/challenge.bmp"
    path_pos1="assets/teaming_position1.bmp"
    
    ndarray_coins=ac.imread(path_coins)
    ndarray_challenge=ac.imread(path_challenge)
    npimg_barrier=ac.imread("assets/barrier_not_attacked.bmp")
    ndarray_pos1=ac.imread(path_pos1)
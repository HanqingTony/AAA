import win32com
import win32api
import win32con
import win32gui
import win32ui
import math
import time
from PIL import Image
import logging
import numpy as np
import cv2
import aircv as ac
import random
import datetime

#日志路径,每日生成新的
path_log = 'log/mitama_{date}.log'.format(date=datetime.datetime.now().strftime(r"%Y-%m-%d"))

#要开的模拟器名。
list_str_hwndOfEmu=[
    'BlueStacks',
    'BlueStacks 2',
    #'BlueStacks 3',
]
#标准大小
resolution_standard=(701,409)

#opencv格式的准备、获胜结算、战利品结算、挑战按钮图片的读入。
imcv_prepare = ac.imread("./asset/prepare.bmp")
imcv_evaluate_win = ac.imread("./src/evaluate_win.bmp")
imcv_evaluate_opened = ac.imread("./src/evaluate_opened.bmp")
imcv_challenge = ac.imread("./src/challenge.bmp")


'''
#日志模块初始化。
logging.basicConfig(
    level=logging.INFO
    ,filename=path_log
    ,format='%(asctime)s(%(filename)s:L%(lineno)d)[%(levelname)s]:%(message)s'
    ,datefmt='%Y-%m-%d %H:%M:%S'
    ,filemode='a'
    #,encoding='utf-8'
    #不能写在初始设置里，吐了,初始设置就是个大坑
    )
'''
logger=logging.getLogger('log')
'''
#删除所有的文件管理handler
for i in logger.handlers:
    logger.removeHandler(i)
'''
#创建utf-8的文件输出流, 后面发现可以直接写在初始化设置里
handler_utf8= logging.FileHandler(
    filename=path_log
    , mode='a'
    , encoding='utf-8'
    , delay=False
    )
#格式管理
formatter = logging.Formatter('%(asctime)s(%(filename)s:L%(lineno)d)[%(levelname)s]:%(message)s')
handler_utf8.setFormatter(formatter)
#把utf8的文件handler附加到logger上，新的格式管理模块附加上，新的
logger.addHandler(handler_utf8)
logger.setLevel(logging.INFO)

def get_child_windows(parent):  
    '''  
    获得parent的所有子窗口句柄
    返回子窗口句柄列表
    '''  
    if not parent:   
        return  
    hwndChildList = []  
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)   
    return hwndChildList 


def func_hwnd_subwindow(str_hwnd_parent):
    '''
    直接获得子窗口句柄，原理是取第一个子窗口句柄
    '''
    return get_child_windows(str_hwnd_parent)[0]

def adjust_windowSize(hwnd_in):
    '''
    调节窗口大小至标准尺寸，通过父窗口来判断
    '''
    tuple_Rect = win32gui.GetWindowRect(hwnd_in)
    tuple_curentSize = (tuple_Rect[2]-tuple_Rect[0],tuple_Rect[3]-tuple_Rect[1])
    #如果分辨率不为标准大小，则调节至标准大小
    if tuple_curentSize != resolution_standard:
        win32gui.MoveWindow(hwnd_in, 1000, 0, 700, 500, True)
        logger.info("窗口"+str(hwnd_in)+":已调节至:"+str(resolution_standard))
    return


def func_im_grab(hwnd):
    '''
    截图函数，输入句柄，返回PIL格式的im对象。
    '''
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
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
    win32gui.ReleaseDC(hWnd,hWndDC)

    ### opencv格式转PIL
    im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
    return im_PIL

def clickPrepare(hwnd_child):
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

def clickEveryWhere(hwnd_child):
    '''
    点击过结算，比较宽松。目前点击屏幕右侧一小条随机位置。后面可以和上面的一起做一个新函数。
    '''
    pos_center = (633,332)
    pos_rand = (random.randint(570, 660), random.randint(70, 250))
    logger.info(
        '点击:位置'+ str(pos_rand)
    )
    long_target = win32api.MAKELONG(*pos_rand)
    win32api.SendMessage(hwnd_child,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,long_target)
    time.sleep(0.02+ 0.03*random.random())
    win32api.SendMessage(hwnd_child,win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,long_target)
    return


def func_mainloop(list_str_hwndOfEmu):
    '''
    主循环。
    '''
    #构建子窗口的句柄列表。
    list_hwnd_child = []
    for str_emuName in list_str_hwndOfEmu:
        hwnd_emu = win32gui.FindWindow(None, str_emuName)
        #调节窗口大小至标准
        adjust_windowSize(hwnd_emu)
        list_hwnd_child.append(func_hwnd_subwindow(hwnd_emu))
        
    while True:
        for hwnd_child in list_hwnd_child:
            #截屏
            im_capt = func_im_grab(hwnd_child)
            #转成cv格式的图片
            imcv_capt = cv2.cvtColor(np.asarray(im_capt), cv2.COLOR_RGB2BGR)

            #判断挑战按钮
            judge = ac.find_template(imcv_capt,imcv_challenge)
            if judge is not None:
                if judge.get("confidence")>0.95:
                    str_log = "识别:挑战按钮" + "，相似度" + str(round(judge['confidence'],2)) + '，句柄：' + str(hwnd_child)
                    logger.info(str_log)
                    clickPrepare(hwnd_child)
            #判断挑战按钮
            judge = ac.find_template(imcv_capt,imcv_prepare)
            if judge is not None:
                if judge.get("confidence")>0.95:
                    str_log = "识别:准备按钮" + "，相似度" + str(round(judge['confidence'],2)) + '，句柄：' + str(hwnd_child)
                    logger.info(str_log)
                    #print("imcv_prepare",hwnd_child,judge['confidence'])
            #判断挑战按钮
            judge = ac.find_template(imcv_capt,imcv_evaluate_win)
            if judge is not None:
                if judge.get("confidence")>0.95:
                    str_log = "识别:胜利界面" + "，相似度" + str(round(judge['confidence'],2)) + '，句柄：' + str(hwnd_child)
                    logger.info(str_log)
                    clickEveryWhere(hwnd_child)
            #判断挑战按钮
            judge = ac.find_template(imcv_capt,imcv_evaluate_opened)
            if judge is not None:
                if judge.get("confidence")>0.95:
                    str_log = "识别:开箱界面" + "，相似度" + str(round(judge['confidence'],2)) + '，句柄：' + str(hwnd_child)
                    logger.info(str_log)
                    clickEveryWhere(hwnd_child)
        #休眠几秒钟。休眠时间由固定时长+随机时长组成。
        time.sleep(0.3+0.7*random.random())
    return

if "__main__" == __name__:
    '''
    程序入口
    '''
    func_mainloop(list_str_hwndOfEmu)
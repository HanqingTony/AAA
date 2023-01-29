from time import *
import win32api
import win32gui
import win32ui
import logging
import aircv as ac
import cv2
import numpy as np
import win32con
from PIL import Image
import random
from utils import *


class mainloop:
    '''
    主循环，包含日志输出，循环间隔等参数，传入不同的task_controller
    改进方向：支持多个task
    '''
    def __init__(self, tasks):
        self.sleep_interval=0.3
        self.debug=print
        self.info=print
        self.error=print
        self.fatel=print
        self.tasks=tasks
        return

    def do(self):
        '''
        主循环，包含跳出机制
        '''
        while not self.check_finish():
            self.debug(win32api.GetCursorPos())
            for task in self.tasks:
                #执行task对象的update方法
                task.update()
            #睡指定的时间
            sleep(self.sleep_interval)
            
    def check_finish(self):
        '''
        检查是否结束
        '''
        if win32api.GetCursorPos() == (0, 0):
            self.info('结束主循环')
            return True
        else:
            return False


if __name__=="__main__":
    
    pass
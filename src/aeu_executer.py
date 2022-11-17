from time import *
import win32api
import logging

class aeu_executer:
    '''
    执行器
    '''
    def __init__(self):
        self.list_registed_policy=[]
        self.sleep_interval=0.3
        self.debug=print
        self.info=print
        self.error=print
        self.fatel=print
        return

    def do(self):
        '''
        主循环，包含跳出机制
        '''
        while not self.check_finish():
            self.debug(win32api.GetCursorPos())
            for policy in self.list_registed_policy:
                policy.check()
            #睡指定的时间
            sleep(self.sleep_interval)
            


    def clean_rutine(self):
        '''
        
        '''
        self.list_routine_check=[]
        return

    def check_finish(self):
        '''
        检查是否结束
        '''
        if win32api.GetCursorPos() == (0, 0):
            self.info('结束主循环')
            return True
        else:
            return False



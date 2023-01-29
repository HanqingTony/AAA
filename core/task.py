import time
import aircv as ac

class task:
    '''
    task类，可以成批输入mainloop类中
    有一个update方法，执行状态转移
    '''
    def __init__(self, window):
        '''
        输入一个window对象。
        '''
        self.window=window
        self.click=self.window.click_byxy_rand
        self.init_dict_state()
        self.debug=print
        self.fresh_capture()
        self.timers={}
        return

    def update(self):
        '''
        主循环，包含多个状态，每个状态有一个条件判断函数
        '''
        #截图
        #self.current_capt=self.window.grab()
        self.fresh_capture()
        #打印日志
        self.debug(self.state)
        #执行全局状态更新,如拒绝协同任务
        self.globle_operate()
        #执行当前状态的更新函数。
        self.dict_state[self.state]()
        return

    def globle_operate(self):
        '''
        所有状态下都执行的操作，应该由子类重写
        '''
        self.debug('task.globle_operate')
        return

    def init_dict_state(self):
        '''
        初始化设置状态字典及默认状态，子类重写
        '''
        self.dict_state={
            "default":print
        }
        self.state="default"
        return
    
    def set_timer(self, str_name, interval):
        '''
        简单的设置计时
        '''
        self.timers[str_name]=time.time()+interval
        return

    def timer_left(self,str_name):
        '''
        查看剩余定时器时间
        '''
        return self.timers[str_name]-time.time()

    def timeup(self,str_timerName):
        '''
        查看计时器是否到时间的函数
        '''
        flag_time=self.timers.get(str_timerName)
        if flag_time is None:
            return True
        elif time.time()>flag_time:
            return True
        else:
            return False

    def check_and_click(self, npimg_in, r=2, offset=(0,0)):
        '''
        检查指定样本的位置，有就点, 范围为r,默认2
        '''
        check_result=self.find(npimg_in)
        if check_result['found']:
            click_pos=(check_result['position'][0]+offset[0],check_result['position'][1]+offset[1])
            self.click(click_pos, r)

    def fresh_capture(self):
        '''
        刷新当前截图
        '''
        self.current_capture=self.window.grab_ndarray()
        return

    def operate_node(self, list_npimg_click, npimg_end, new_state_name, mode="exist"):
        '''
        一般的操作树节点，从一个状态转移到另一个状态
        有两个模式，存在模式和消失模式，存在模式出现下一个状态的标记就转移状态，消失模式某个标记不见了就转移状态
        '''
        #如果没有计时器：
        if self.timeup(new_state_name):
            #存在模式
            if mode=="exist":
                #未达到状态转移条件
                if not self.find(npimg_end, 0.85)['found']:
                    #检查并点击
                    for i in list_npimg_click:
                        self.check_and_click(i)
                    #设置1秒的计时器
                    self.set_timer(new_state_name, 1)
                #达到状态转移条件
                else:
                    #设置状态为新状态
                    self.state=new_state_name
            #消失模式
            elif mode=="disappear":
                #未达到状态转移条件
                if self.find(npimg_end, 0.85)['found']:
                    #检查并点击
                    for i in list_npimg_click:
                        self.check_and_click(i)
                    #设置1秒的计时器
                    self.set_timer(new_state_name, 1)
                #达到状态转移条件
                else:
                    #设置状态为新状态
                    self.state=new_state_name
        return

    def found(self,ndarray_template, confidence=0.95):
        ans=self.find(ndarray_template, confidence)
        if ans['found']:
            return True
        else:
            return False

    def find(self, ndarray_template, confidence=0.95):
        '''
        输入一个ndarray_template图片，找到所在位置，否则返回Null

        '''
        ndarray_capt=self.current_capture
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
                    int(judge['result'][0]/self.window.zooming),
                    int(judge['result'][1]/self.window.zooming)
                )
            }
        else:
            out = {
                "found":False,
                "position":(-1,-1)
            }
        return out

from window import window
from task_onmyoji import task_onmyoji
from mainloop import mainloop
import aircv as ac


class task_mitama_guest(task_onmyoji):
    '''
    被邀请的任务，或者两人组的task
    '''
    def __init__(self, window, timeup):
        super().__init__(window)
        self.set_timer("mitama_end", timeup*60)
        return

    def init_dict_state(self):
        self.dict_state={
            'teaming':self.state_teaming,
            'battle_farming':self.state_battle_farming,
            'stop_buff':self.state_stop_buff
        }
        self.state="teaming"
        return
    def state_battle_farming(self):
        '''
        战斗
        '''
        self.base_battle()
        if self.found(self.npimg_teaming_main):
            self.set_timer('teaming_sleep', 2)
            self.state='teaming'
        return

    def state_teaming(self):
        '''
        如果到了结束时间，就点
        '''
        if self.timeup("mitama_end"):
            self.operate_node([self.npimg_buff], self.npimg_buff_mitama_running,"stop_buff")
        else:
            self.debug(self.timer_left("mitama_end")/60)
            if self.timeup("teaming_sleep"):
                self.state='battle_farming'

    def state_stop_buff(self):
        if self.timeup('buffstop_mark'):
            self.check_and_click(self.npimg_buff_mitama_running, 2, (40,0))
            self.set_timer('buffstop_mark', 1)
        return

class task_mitama_host(task_onmyoji):
    '''
    三人房主task
    '''
    def __init__(self, window, timeup):
        super().__init__(window)
        self.set_timer("mitama_end", timeup*60)
        return
    def init_dict_state(self):
        '''
        重写类字典
        '''
        self.dict_state={
            'teaming':self.state_teaming,
            'battle':self.state_battle,
            'stop_buff':self.state_stop_buff
        }
        self.state="teaming"
        return

    def state_teaming(self):
        '''
        组队中
        '''
        self.check_and_click(self.npimg_win_2)
        check_pos1=self.find(self.npimg_pos1)
        check_pos2=self.find(self.npimg_pos2)
        check_challenge=self.find(self.npimg_challenge)
        if (not (check_pos1['found'] or check_pos2['found'])) and check_challenge['found']:
            #如果不是一二号坑任意一个无人，也即两个都有人，且存在挑战按钮
            if self.timeup("mitama_end"):
                self.operate_node([self.npimg_buff], self.npimg_buff_mitama_running,"stop_buff")
            else:
                self.click(check_challenge['position'], 25)
                self.state="battle"

    def state_stop_buff(self):
        if self.timeup('buffstop_mark'):
            self.check_and_click(self.npimg_buff_mitama_running, 2, (40,0))
            self.set_timer('buffstop_mark', 1)
        return

    def state_battle(self):
        '''
        战斗中
        '''
        self.base_battle()
        check_result=self.find(self.npimg_win_2)
        if check_result['found']:
            self.click(check_result['position'], 25)
            self.state="teaming"



if __name__=="__main__":
    andro0 = window("andro0")
    andro1 = window("andro1")
    andro2 = window("andro2")
    task0=task_mitama_guest(andro0,60)
    task1=task_mitama_host(andro2,60)
    task2=task_mitama_guest(andro1,60)

    a=mainloop([task0, task1, task2])

    a.do()
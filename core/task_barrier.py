from window import window
from task_onmyoji import task_onmyoji
from mainloop import mainloop
import aircv as ac

class task_barrier(task_onmyoji):
    '''
    结界突破
    '''
    def __init__(self, window):
        super().__init__(window)
        #失败计数器
        self.lose_quant=0
        return

    def init_dict_state(self):
        self.dict_state={
            'nine_grid':self.state_nine_grid,
            'click_attack':self.state_click_attack,
            'click_attack_autolose':self.state_click_attack_autolose,
            'click_attack_final':self.state_click_attack_final,
            'battle':self.state_battle,
            'battle_autolose':self.state_battle_autolose,
            'autolose_quit':self.state_autolose_quit
        }
        self.state="nine_grid"
        return
    def state_nine_grid_old(self):
        '''
        九宫格界面逻辑
        如果不是打完了八个，且突破卷不为0，
        优先打未打过的
        已经废弃
        '''
        if self.timeup("nine_grid"):
            check_1left=self.find(self.npimg_1left)['found']
            check_0ticket=self.find(self.npimg_0ticket)['found']
            #if (not check_0ticket) and (not check_1left):
            if (not check_1left):
                #点击
                if not self.find(self.npimg_barrier_attack,0.85)["found"]:
                    self.check_and_click(self.npimg_not_attacked,2)
                    self.set_timer("nine_grid", 1)
                else:
                    self.state="click_attack"
            else:
                '''
                只剩一个，进入四输流程
                '''
                self.state="click_attack_autolose"
        return

    def state_nine_grid(self):
        '''
        新版九宫格界面逻辑，使用task中的新函数operate_node
        '''
        check_1left=self.find(self.npimg_1left)['found']
        check_0ticket=self.find(self.npimg_0ticket)['found']
        #如果没票了
        if check_0ticket:
            #打印 ticket out
            self.debug("ticket out")
        #如果还有票：
        else:
            #如果不是只剩一个，进行小状态转移
            if not check_1left:
                self.operate_node([self.npimg_not_attacked], self.npimg_barrier_attack, "click_attack")
            else:
                #如果输计时器小于等于4
                if self.lose_quant<4:
                    self.operate_node([self.npimg_attacked, self.npimg_not_attacked], self.npimg_barrier_attack, "click_attack_autolose")
                #否则正常赢
                else:
                    self.operate_node([self.npimg_attacked,self.npimg_not_attacked], self.npimg_barrier_attack, "click_attack_final")
        return

    def state_click_attack(self):
        '''
        小状态，用于点击进攻按钮
        '''
        check_attack=self.find(self.npimg_barrier_attack,0.85)
        if check_attack['found']:
            self.click((check_attack['position'][0]+30, check_attack['position'][1]))
        if self.find(self.npimg_prepare)['found']:
            self.state="battle"
        return

    def state_battle(self):
        '''
        结界突破的战斗，此状态需要处理失败情况
        '''
        self.base_battle()
        self.check_and_click(self.npimg_lose)
        if self.find(self.npimg_barrier_assult)['found'] and (not self.find(self.npimg_win_2)['found']):
            #状态更新, 有结界突破字样并且没有结算球
            self.state="nine_grid"
        return

    def state_click_attack_autolose(self):
        '''
        小状态，用于点击自动输的进攻按钮
        '''
        check_attack=self.find(self.npimg_barrier_attack,0.85)
        self.debug(check_attack)
        if check_attack['found']:
            self.click((check_attack['position'][0]+30, check_attack['position'][1]))
        if self.find(self.npimg_prepare)['found']:
            #失败次数加一
            self.lose_quant+=1
            self.debug(self.lose_quant)
            self.state="battle_autolose"
        return

    def state_click_attack_final(self):
        '''
        最后一胜，点击
        '''
        self.lose_quant=0
        check_attack=self.find(self.npimg_barrier_attack,0.85)
        self.debug(check_attack)
        if check_attack['found']:
            self.click((check_attack['position'][0]+30, check_attack['position'][1]))
        if self.find(self.npimg_prepare)['found']:
            #失败次数加一
            self.lose_quant+=1
            self.debug(self.lose_quant)
            self.state="battle"
        return

    def state_battle_autolose(self):
        '''
        进入自动输的战斗了，点击退出按钮
        '''
        self.operate_node([self.npimg_barrier_quit], self.npimg_barrier_confirm,"autolose_quit")
        return

    def state_autolose_quit(self):
        '''
        点了退出了，该点确认了,确认之后用战斗结算逻辑回到九宫
        '''
        self.operate_node([self.npimg_barrier_confirm], self.npimg_lose,"battle")


if __name__ == "__main__":
    andro0 = window("andro0")
    task_0=task_barrier(andro0)
    andro2 = window("andro2")
    task_2=task_barrier(andro2)
    andro1 = window("andro1")
    task_1=task_barrier(andro1)
    a=mainloop([task_0,task_1,task_2])
    a.do()
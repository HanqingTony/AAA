from window import window
from task import task
from mainloop import mainloop
import aircv as ac

class task_onmyoji(task):
    '''
    阴阳师通用
    '''
    def __init__(self, window):
        super().__init__(window)
        self.npimg_challenge=ac.imread("assets/challenge.bmp")
        self.npimg_prepare=ac.imread("assets/prepare.bmp")
        self.npimg_refuse=ac.imread("assets/refuse.bmp")
        self.npimg_win_1=ac.imread("assets/win_1.bmp")
        self.npimg_win_2=ac.imread("assets/win_2.bmp")
        self.npimg_pos1=ac.imread("assets/teaming_position1.bmp")
        self.npimg_pos2=ac.imread("assets/teaming_position2.bmp")
        self.npimg_lose=ac.imread("assets/lose.bmp")
        self.npimg_not_attacked=ac.imread("assets/barrier_not_attacked.bmp")
        self.npimg_1left=ac.imread("assets/barrier_1left.bmp")
        self.npimg_0ticket=ac.imread("assets/barrier_0ticket.png")
        self.npimg_barrier_attackmark=ac.imread("assets/attack_mark.png")
        self.npimg_barrier_assult=ac.imread("assets/barrier_assult.png")
        self.npimg_barrier_attack=ac.imread("assets/barrier_attack.png")
        self.npimg_barrier_confirm=ac.imread("assets/barrier_confirm.png")
        self.npimg_attacked=ac.imread("assets/barrier_attacked.png")
        self.npimg_barrier_quit=ac.imread("assets/barrier_quit.png")
        self.npimg_teaming_main=ac.imread("assets/teaming_main.png")
        self.npimg_buff=ac.imread("assets/buff.png")
        self.npimg_buff_mitama_running=ac.imread("assets/buff_mitama_running.png")
        return

    def globle_operate(self):
        '''
        重写通用操作，自动点拒绝
        '''
        #随时点击拒绝
        self.check_and_click(self.npimg_refuse)
        return

    def base_battle(self):
        '''
        基础战斗逻辑,自动点准备、两个结算画面
        '''
        self.check_and_click(self.npimg_prepare)
        self.check_and_click(self.npimg_win_1, 30)
        self.check_and_click(self.npimg_win_2, 60)
        return
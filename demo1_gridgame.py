from demo1_init import *
from pygarios import *
from random import random, randint, shuffle
from collections import deque
import pygame


fps_clock = pygame.time.Clock()


def get_input_arrows():
    global key_pressed_limit_t
    key_pressed_limit_t += 1
    if key_pressed_limit_t < 10:
        return 0, 0
    else:
        left = pygame.key.get_pressed()[pygame.K_LEFT]
        up = pygame.key.get_pressed()[pygame.K_UP]
        down = pygame.key.get_pressed()[pygame.K_DOWN]
        right = pygame.key.get_pressed()[pygame.K_RIGHT]
        dx, dy = right - left, down - up
        if dx != 0 or dy != 0:
            key_pressed_limit_t = 0
            return dx, dy
        else:
            return 0, 0


def pygame_process_events(events):
    global mousePressed, mouseX, mouseY
    mousePressed, mouseX, mouseY = update_mouse_state_from_pygame_events(events)

    for event in events:
        if event.type == game.BLOCK_UPDATE:
            game.blocks_update()


FPS_MAX = 40
width, height = 900, 900
key_pressed_limit_t = 0

class Game():
    def __init__(self, k):
        self.k = k
        self.xgrid_len = width/k
        self.ygrid_len = height/k
        self.playerxy = [k//2, 0]
        self.playerlivetime = 0
        self.block_data = deque([[] for _ in range(self.k)])
        self.block_make_flag = 0
        self.block_make_T = 3
        self.BLOCK_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.BLOCK_UPDATE, 1300)

    def grid_rect(self, i, k):
        rect(self.xgrid_len*i, self.ygrid_len *
             k, self.xgrid_len, self.ygrid_len)

    def disp(self):

        # back grid
        fill(*BackColor)
        stroke(1, 1, 1)
        for i in range(self.k):
            for k in range(self.k):
                self.grid_rect(i, k)

        # block
        fill(*BlockColor)
        stroke(1, 1, 1)
        for i in range(self.k):
            if self.block_data[i] != []:
                s, l = self.block_data[i]
                for k in range(s, s+l):
                    self.grid_rect(k, i)

        # player
        fill(*PlayerColor)
        noStroke()
        px, py = self.playerxy
        self.grid_rect(px, py)

        # scores
        fill(*BlockColor)
        PfontSize(50)
        Ptext("Scores: "+str(self.playerlivetime), 100, 100)

    def player_mouse_update(self, mx, my):
        gridmousex = mx // self.xgrid_len
        gridmousey = my // self.ygrid_len
        px, py = self.playerxy
        if abs(px - gridmousex) <= 1:
            px = gridmousex
        if abs(py - gridmousey) <= 1:
            py = gridmousey
        self.playerxy = [px, py]

    def player_key_update(self):
        dx, dy = get_input_arrows()
        if dx != 0 or dy != 0:
            # print("get_key:", dx, dy)
            px, py = self.playerxy
            px = Pconstrain(px+dx, 0, self.k-1)
            py = Pconstrain(py+dy, 0, self.k-1)
            self.playerxy = [px, py]

    def generate_random_block(self, add_block_flag):
        if add_block_flag:
            pblock = (randint(0, self.k-4), randint(3, 7))
            self.block_data.append(pblock)
        else:
            self.block_data.append([])
        self.block_data.popleft()

    def blocks_update(self):
        self.playerlivetime += 1
        self.block_make_flag += 1
        self.block_make_flag = self.block_make_flag % self.block_make_T
        if self.block_make_flag == 0:
            self.generate_random_block(True)
        else:
            self.generate_random_block(False)

    def detect_collision(self):
        collision = False
        px, py = self.playerxy
        for blocky, (blocks_blockl) in enumerate(self.block_data):
            if blocks_blockl:
                blocks, blockl = blocks_blockl
                if blocky==py and blocks <= px < blocks+blockl:
                    collision = True
                    break
        return collision

    def update(self):
        self.player_key_update()
        if self.detect_collision():
            print("COLLISION")
            self.__init__(self.k)


def start():
    global game
    game = Game(10)


def update():
    pygame_process_events(pygame.event.get())  # pyplay 特殊语法

    background(*BackColor)
    stroke(1, 0, 0)
    strokeWeight(3.0)

    game.disp()
    game.update()
    

    if mousePressed:
        stroke(0, .5, 1)
        circle(mouseX, mouseY, 20)

        game.player_mouse_update(mouseX, mouseY)

    passed_time = fps_clock.tick(FPS_MAX)




if __name__ == "__main__":  # pyplay 特殊语法
    main(start, update, width, height)

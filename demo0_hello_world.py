from demo1_init import *
from pygarios import *
from random import random, randint, shuffle
from collections import deque
import pygame




def pygame_process_events(events):
    global mousePressed, mouseX, mouseY
    mousePressed, mouseX, mouseY = update_mouse_state_from_pygame_events(events)




width, height = 900, 900




def start():
    pass
    


def update():
    pygame_process_events(pygame.event.get())  # pyplay 特殊语法

    background(*BackColor)
    stroke(1, 0, 0)
    strokeWeight(3.0)


    

    if mousePressed:
        stroke(0, .5, 1)
        circle(mouseX, mouseY, 20)

        game.player_mouse_update(mouseX, mouseY)

    passed_time = fps_clock.tick(FPS_MAX)




if __name__ == "__main__":  # pyplay 特殊语法
    main(start, update, width, height)

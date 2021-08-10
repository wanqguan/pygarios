from pygarios import *
import pygame

width, height = 900, 900


def pygame_process_events(events):
    global mousePressed, mouseX, mouseY
    mousePressed, mouseX, mouseY = update_mouse_state_from_pygame_events(events)


def start():
    background(1, 1, 1)
    

def update():
    pygame_process_events(pygame.event.get())  # pyplay 特殊语法

    background(1, 1, 1)
    
    strokeWeight(3.0)

    PfontSize(50)

    for xi in range(8):
        for yi in range(6):
            stroke(1, 0, 0)
            noFill()
            rect(xi*100, yi*100, 70, 50)

            fill(0, 1, 0)
            Ptext(str(max(xi, yi)), xi*100, yi*100+40)


    if mousePressed:
        stroke(0, .5, 1)
        circle(mouseX, mouseY, 20)


if __name__ == "__main__":  # pyplay 特殊语法
    main(start, update, width, height)

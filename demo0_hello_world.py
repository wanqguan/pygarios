from pygarios import *
import pygame

# 定义窗口的长度和宽度，单位是像素
width, height = 900, 900

# 处理Pygame事件（包括键盘鼠标的输入等），开头两行是必须加的
def pygame_process_events(events):
    global mousePressed, mouseX, mouseY
    mousePressed, mouseX, mouseY = update_mouse_state_from_pygame_events(events)

# 项目初始化时候，执行一次
def start():
    background(1, 1, 1)
    
# 项目初始化后，循环执行本函数
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


# 固定写法
if __name__ == "__main__":  
    main(start, update, width, height)
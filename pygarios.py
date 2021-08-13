import cairo
import pygame
from math import pi
from pygame.math import Vector2
from copy import deepcopy
from random import random
from PIL import Image
import sys


def hex_to_rgb(value):
    """将十六进制的颜色转换为RGB表示

    Args:
        value (str): 十六进制的颜色的字符串表示，如：“#FF00FF”

    Returns:
        (float, float, float): [颜色的RGB表示]
    """
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16)/255.0 for i in range(0, lv, lv // 3))


def bgra_surf_to_rgba_string(cairo_surface):
    """ pygarios 内置函数
    """
    # We use PIL to do this
    img = Image.frombuffer(
        'RGBA', (cairo_surface.get_width(),
                 cairo_surface.get_height()),
        cairo_surface.get_data().tobytes(), 'raw', 'BGRA', 0, 1)
    return img.tobytes('raw', 'RGBA', 0, 1)


def Prandom(*arg):
    """Processing风格实用函数， 随机数：生成指定范围内的随机数

    Returns:
        float: 生成的随机数
    """
    if len(arg) == 1:
        return random() * arg[0]
    else:
        a, b = arg
        return a + random() * (b - a)


def Pconstrain(amt, low, high):
    """Processing风格实用函数，限制：将一个数amt限制在指定范围（low, high）内。

    Returns:
        float: 应用限制后的数
    """
    if amt < low:
        return low
    if amt > high:
        return high
    return amt


def Pmap(value, start1, stop1, start2, stop2):
    """Processing风格实用函数，映射：将一个数amt从指定范围（start1, stop1）线性映射到范围（start2, stop2）内对应位置。

    Returns:
        float: 应用映射后的数
    """
    k = (stop2 - start2) / (stop1 - start1)
    return start2 + (value - start1) * k


ctx = None
width, height = None, None
mouseX, mouseY = 0, 0
mousePressed = False

Pfill = True
Pfillcolor = (0, 0, 0)
Pstroke = True
Pstrokecolor = (0, 0, 0)


def init_ctx(ctx2, w, h):
    global ctx, width, height
    ctx = ctx2
    width = w
    height = h
    ctx.scale(w//4*3, h//4*3)


def main(start, update, w, h):
    """pygarios 的主函数

    Args:
        start (func): 程序开始时运行该函
        update (func): 程序开始后自动重复运行该函数
        w (int): 窗口宽度设置
        h (int): 窗口高度设置
    """
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    pygame.init()
    pygame.display.set_mode((w//4*3, h//4*3))
    pygame.display.set_caption('Pygarios demo')  # 窗口标题
    pygame.key.set_repeat(1, 10)
    screen = pygame.display.get_surface()

    ctx = cairo.Context(surface)
    init_ctx(ctx, w, h)

    start()
    while True:
        update()
        # Create PyGame surface from Cairo Surface
        data_string = bgra_surf_to_rgba_string(surface)
        image = pygame.image.frombuffer(data_string, (width, height), 'RGBA')
        # Tranfer to Screen
        screen.blit(image, (0, 0))
        pygame.display.flip()


def update_mouse_state_from_pygame_events(events):
    mousePressed = False
    mouseX, mouseY = 0, 0
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            mouseX = mouseX / 3*4
            mouseY = mouseY / 3*4
            mousePressed = True
        else:
            mousePressed = False
    return mousePressed, mouseX, mouseY


def PfontSize(k):
    """Processing风格画图设置函数，设置字体显示时的大小"""
    ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(k/width)


def Ptext(text, x, y):
    """画出指定文字

    Args:
        text (str): 指定文字
        x (float): x方向位置
        y (float): y方向位置
    """
    if len(Pfillcolor) == 3:
        ctx.set_source_rgb(*Pfillcolor)
    elif len(Pfillcolor) == 4:
        ctx.set_source_rgba(*Pfillcolor)
    ctx.move_to(x/width, y/height)
    ctx.show_text(text)


def translate(x, y):
    """Processing风格渲染设置函数，位移"""
    ctx.translate(x/width, y/height)


def rotate(angle):
    """Processing风格渲染设置函数，旋转"""
    ctx.rotate(angle)


def pushMatrix():
    """Processing风格渲染设置函数，压入上下文？怎么解释合适"""
    ctx.save()


def popMatrix():
    """Processing风格渲染设置函数，弹出上下文？怎么解释合适"""
    ctx.restore()


def strokeWeight(k):
    """Processing风格绘图函数，指定轮廓宽度"""
    ctx.set_line_width(k/width)


def noStroke():
    """Processing风格绘图函数，设置填充色为空。
    """
    global Pstroke
    Pstroke = False


def stroke(*arg):
    """Processing风格绘图函数，指定轮廓色
    Args:
        arg (r, g, b): 颜色的RGB表示，范围从0-1。
    """
    global Pstroke, Pstrokecolor
    Pstroke = True
    Pstrokecolor = arg


def noFill():
    """Processing风格绘图函数，设置填充色为空。
    """
    global Pfill
    Pfill = False


def fill(*arg):
    """Processing风格绘图函数，指定填充色
    Args:
        arg (r, g, b): 颜色的RGB表示，范围从0-1。
    """
    global Pfill, Pfillcolor
    Pfill = True
    Pfillcolor = arg
    # print("fill", Pfillcolor)


def circle(x, y, r):
    """Processing风格绘图函数, 画一个圆

    Args:
        x (float): x 方向位置
        y (float): y 方向位置
        r (float): 圆的半径
    """
    if Pfill:
        if len(Pfillcolor) == 3:
            ctx.set_source_rgb(*Pfillcolor)
        elif len(Pfillcolor) == 4:
            ctx.set_source_rgba(*Pfillcolor)
        ctx.arc(x/width, y/height, r/width, 0.0, 2.0 * pi)
        ctx.fill()
    if Pstroke:
        if len(Pstrokecolor) == 3:
            ctx.set_source_rgb(*Pstrokecolor)
        elif len(Pstrokecolor) == 4:
            ctx.set_source_rgba(*Pstrokecolor)
        ctx.arc(x/width, y/height, r/width, 0.0, 2.0 * pi)
        ctx.stroke()


def rect(x, y, a, b):
    """Processing风格绘图函数, 画一个方形

    Args:
        x (float): x 方向位置
        y (float): y 方向位置
        a (float): 方形的 x方向长度
        b (float): 方形的 y方向长度
    """
    x /= width
    y /= height
    a /= width
    b /= height

    if Pfill:
        if len(Pfillcolor) == 3:
            ctx.set_source_rgb(*Pfillcolor)
        elif len(Pfillcolor) == 4:
            ctx.set_source_rgba(*Pfillcolor)
        ctx.rectangle(x, y, a, b)
        ctx.fill()
    if Pstroke:
        if len(Pstrokecolor) == 3:
            ctx.set_source_rgb(*Pstrokecolor)
        elif len(Pstrokecolor) == 4:
            ctx.set_source_rgba(*Pstrokecolor)
        ctx.rectangle(x, y, a, b)
        ctx.stroke()


def line(x1, y1, x2, y2):
    """Processing风格绘图函数, 画一个线段

    Args:
        x1 (float): x from
        y1 (float): y from
        x2 (float): x to
        y2 (float): y to
    """
    if Pstroke:
        if len(Pstrokecolor) == 3:
            ctx.set_source_rgb(*Pstrokecolor)
        elif len(Pstrokecolor) == 4:
            ctx.set_source_rgba(*Pstrokecolor)
            ctx.move_to(x1/width, y1/height)
            ctx.line_to(x2/width, y2/height)
        ctx.stroke()


def background(*c):
    """Processing风格绘图函数, 使用颜色c绘制背景
    """
    if len(c) == 3:
        ctx.set_source_rgb(*c)
    elif len(c) == 4:
        ctx.set_source_rgba(*c)
    ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
    ctx.fill()


def load_image(fpath):
    """Processing风格渲染函数, 从指定路径fpath加载图片
    """
    return cairo.ImageSurface.create_from_png(fpath)


def draw_image(image, x, y, w, h):
    """Draw a scaled image on a given context.
    Args:
        image (image): 加载过的图片
        x (float): x 方向位置
        y (float): y 方向位置
        a (float): 图片的 x方向长度
        b (float): 图片的 y方向长度
    """
    x /= width
    y /= height
    w /= width
    h /= height
    img_height = image.get_height()
    img_width = image.get_width()
    width_ratio = float(w) / float(img_width)
    height_ratio = float(h) / float(img_height)
    scale_xy = min(height_ratio, width_ratio)
    # scale image and add it
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale_xy, scale_xy)
    ctx.set_source_surface(image)

    ctx.paint()
    ctx.restore()


class PVector(Vector2):
    """Processing风格实用函数, 封装二维向量的表示和计算
    """
    def __init__(self, x, y):
        super().__init__(x, y)

    def mult(self, k):
        self.__imul__(k)

    def get(self):
        return deepcopy(self)

    def limit(self, k):
        if self.length() > k:
            self.scale_to_length(k)

    def mag(self):
        return self.magnitude()

    def heading2D(self):
        return self.angle_to(PVector(0, 1))

    def add(self, *arg):
        if len(arg) == 1:
            self.__iadd__(arg[0])  # 这里对self赋值失败
            return self.get()
        elif len(arg) == 2:
            tmp = arg[0] + arg[1]
            return PVector(tmp.x, tmp.y)

    def sub(self, *arg):
        if len(arg) == 1:
            self -= arg[0]
            return self.get()
        elif len(arg) == 2:
            tmp = arg[0] - arg[1]
            return PVector(tmp.x, tmp.y)

    def copy(self):
        return deepcopy(self)


def gradient_cricle(x, y, r):
    "实验功能，绘制渐近色填充的圆形，可尝试使用"
    pat = cairo.RadialGradient(x/width+r/width/10, y/height+r/width/10, r/width/5,
                               x/width+r/width/3, y/height+r/width/3, r/width)
    pat.add_color_stop_rgba(0, 1, 1, 1, 1)

    if Pfill:
        if len(Pfillcolor) == 3:
            pat.add_color_stop_rgb(*([1] + list(Pfillcolor)))
        elif len(Pfillcolor) == 4:
            pat.add_color_stop_rgba(*([1] + list(Pfillcolor)))
        ctx.arc(x/width, y/height, r/width, 0.0, 2.0 * pi)
        ctx.set_source(pat)
        ctx.fill()
    # if Pstroke:
    #     if len(Pstrokecolor) == 3:
    #         ctx.set_source_rgb(*Pstrokecolor)
    #     elif len(Pstrokecolor) == 4:
    #         ctx.set_source_rgba(*Pstrokecolor)
    #     ctx.arc(x/width, y/height, r/width, 0.0, 2.0 * pi)
    #     ctx.stroke()


def gradient_rect(x, y, a, b, GradientDarkColor):
    "实验功能，绘制渐近色填充的方形，可尝试使用"
    x /= width
    y /= height
    a /= width
    b /= height

    pat = cairo.RadialGradient(x+a/10, y+b/10, (a+b)/10,
                               x+a/3, y+b/3, (a+b)/2)
    # pat = cairo.LinearGradient(x/width, y/height, x/width+r/width/3, y/height+r/width/3)
    pat.add_color_stop_rgba(1.5, *GradientDarkColor, 1)

    if Pfill:
        if len(Pfillcolor) == 3:
            pat.add_color_stop_rgb(*([.2] + list(Pfillcolor)))
        elif len(Pfillcolor) == 4:
            pat.add_color_stop_rgba(*([.2] + list(Pfillcolor)))
        ctx.rectangle(x, y, a, b)
        ctx.set_source(pat)
        ctx.fill()
    if Pstroke:
        if len(Pstrokecolor) == 3:
            pat.add_color_stop_rgb(*([.2] + list(Pstrokecolor)))
        elif len(Pstrokecolor) == 4:
            pat.add_color_stop_rgba(*([.2] + list(Pstrokecolor)))
        ctx.rectangle(x, y, a, b)
        ctx.set_source(pat)
        ctx.stroke()


def two_border_Ptext(text, x, y, TextBorderColor):
    "实验功能，绘制带轮廓的文字，可尝试使用"
    ctx.move_to(x/width, y/height)
    ctx.text_path(text)
    if len(Pfillcolor) == 3:
        ctx.set_source_rgb(*Pfillcolor)
    elif len(Pfillcolor) == 4:
        ctx.set_source_rgba(*Pfillcolor)
    ctx.fill_preserve()
    ctx.set_source_rgb(*TextBorderColor)
    ctx.set_line_width(2/width)
    ctx.stroke()



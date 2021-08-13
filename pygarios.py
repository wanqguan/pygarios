import cairo
import pygame
from math import pi
from pygame.math import Vector2
from copy import deepcopy
from random import random
from PIL import Image
import sys


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16)/255.0 for i in range(0, lv, lv // 3))


def bgra_surf_to_rgba_string(cairo_surface):
    # We use PIL to do this
    img = Image.frombuffer(
        'RGBA', (cairo_surface.get_width(),
                 cairo_surface.get_height()),
        cairo_surface.get_data().tobytes(), 'raw', 'BGRA', 0, 1)
    return img.tobytes('raw', 'RGBA', 0, 1)


def Prandom(*arg):
    if len(arg) == 1:
        return random() * arg[0]
    else:
        a, b = arg
        return a + random() * (b - a)


def Pconstrain(amt, low, high):
    if amt < low:
        return low
    if amt > high:
        return high
    return amt


def Pmap(value, start1, stop1, start2, stop2):
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
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    pygame.init()
    pygame.display.set_mode((w//4*3, h//4*3))
    pygame.display.set_caption('Pygarios demo')
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
    ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(k/width)


def Ptext(text, x, y):
    if len(Pfillcolor) == 3:
        ctx.set_source_rgb(*Pfillcolor)
    elif len(Pfillcolor) == 4:
        ctx.set_source_rgba(*Pfillcolor)
    ctx.move_to(x/width, y/height)
    ctx.show_text(text)


def translate(x, y):
    ctx.translate(x/width, y/height)


def rotate(angle):
    ctx.rotate(angle)


def pushMatrix():
    ctx.save()


def popMatrix():
    ctx.restore()


def strokeWeight(k):
    ctx.set_line_width(k/width)


def noStroke():
    global Pstroke
    Pstroke = False


def stroke(*arg):
    global Pstroke, Pstrokecolor
    Pstroke = True
    Pstrokecolor = arg


def noFill():
    global Pfill
    Pfill = False


def fill(*arg):
    global Pfill, Pfillcolor
    Pfill = True
    Pfillcolor = arg
    # print("fill", Pfillcolor)


def circle(x, y, r):
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
    if Pstroke:
        if len(Pstrokecolor) == 3:
            ctx.set_source_rgb(*Pstrokecolor)
        elif len(Pstrokecolor) == 4:
            ctx.set_source_rgba(*Pstrokecolor)
            ctx.move_to(x1/width, y1/height)
            ctx.line_to(x2/width, y2/height)
        ctx.stroke()


def background(*c):
    if len(c) == 3:
        ctx.set_source_rgb(*c)
    elif len(c) == 4:
        ctx.set_source_rgba(*c)
    ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
    ctx.fill()


def load_image(fpath):
    return cairo.ImageSurface.create_from_png(fpath)


def draw_image(image, x, y, w, h):
    """Draw a scaled image on a given context."""
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



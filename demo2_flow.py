from pygarios import *
import pygame
from noise import pnoise2 as noise
from collections import deque
from math import sin, cos

fps_clock = pygame.time.Clock()



def pygame_process_events(events):
    global mousePressed, mouseX, mouseY
    mousePressed, mouseX, mouseY = update_mouse_state_from_pygame_events(events)



FPS_MAX = 40
width, height = 900, 900


class FlowField():
    def __init__(self, r):
        self.resolution = r
        # Determine the number of columns and rows based on sketch's width and height
        self.cols = width // r  # Attention
        self.rows = height // r
        self.field = []
        self.init()

    def init(self):
        self.field = []
        xoff = 0
        xrand = Prandom(0, 1)
        yrand = Prandom(0, 1)
        for i in range(self.cols):
            yoff = 0
            tmp = []
            for j in range(self.rows):
                theta = Pmap(noise(xoff+xrand, yoff+yrand), 0, 1, 0, 2 * pi)
                assert theta < 2 * pi
                # Polar to cartesian coordinate transformation to get x and y components of the vector
                tmp.append(PVector(cos(theta), sin(theta)))
                yoff += 0.01
            self.field.append(tmp)
            xoff += 0.01

    def display(self):
        # fill(0, 1, 0)
        for i in range(self.cols):
            for j in range(self.rows):
                self.drawVector(
                    self.field[i][j], i * self.resolution, j * self.resolution, self.resolution - 2)

    def drawVector(self, v, x, y, scayl):
        pushMatrix()
        translate(x, y)
        rotate(v.heading2D())
        leg = v.mag()*scayl
        line(0, 0, leg, 0)
        arrowsize = 4
        line(leg, 0, leg-arrowsize, +arrowsize/2)
        line(leg, 0, leg-arrowsize, -arrowsize/2)
        popMatrix()

    def lookup(self, lookup):
        column = int(Pconstrain(lookup.x / self.resolution, 0, self.cols - 1))
        row = int(Pconstrain(lookup.y / self.resolution, 0, self.rows - 1))
        return self.field[column][row].get()


class Vehicle(object):
    """ generated source for class Vehicle """

    def __init__(self, l, ms, mf):
        """ generated source for method __init__ """
        self.location = l.get()
        self.history_loc = deque()
        self.r = 3.0
        self.color = (Prandom(1), Prandom(1), Prandom(1))
        self.maxspeed = ms
        self.maxforce = mf
        self.acceleration = PVector(0, 0)
        self.velocity = PVector(0, 0)

    def run(self):
        """ generated source for method run """
        self.update()
        self.borders()
        self.display()

    #  Implementing Reynolds' flow field following algorithm
    #  http://www.red3d.com/cwr/steer/FlowFollow.html
    def follow(self, flow):
        """ generated source for method follow """
        #  What is the vector at that spot in the flow field?
        desired = flow.lookup(self.location)
        #  Scale it up by maxspeed
        desired.mult(self.maxspeed)
        #  Steering is desired minus velocity
        steer = PVector.sub(desired, self.velocity)
        steer.limit(self.maxforce)
        #  Limit to maximum steering force
        self.applyForce(steer)

    def applyForce(self, force):
        """ generated source for method applyForce """
        #  We could add mass here if we want A = F / M
        self.acceleration.add(force)

    #  Method to update location
    def update(self):
        """ generated source for method update """
        #  Update velocity
        self.velocity.add(self.acceleration)
        #  Limit speed
        self.velocity.limit(self.maxspeed)
        self.location.add(self.velocity)
        #  Reset accelertion to 0 each cycle
        self.acceleration.mult(0)
        self.history_loc.append(self.location.copy())
        if len(self.history_loc) > 10:
            self.history_loc.popleft()

    def display(self):
        """ generated source for method display """
        #  Draw a triangle rotated in the direction of velocity
        m = 0.0
        for loc in self.history_loc:
            fill(*self.color, m)
            circle(loc.x, loc.y, 3)
            m += 0.1

    #  Wraparound

    def borders(self):
        """ generated source for method borders """
        if self.location.x < -self.r:
            self.location.x = width + self.r
        if self.location.y < -self.r:
            self.location.y = height + self.r
        if self.location.x > width + self.r:
            self.location.x = -self.r
        if self.location.y > height + self.r:
            self.location.y = -self.r


def start():
    global flowfield, vehicles
    flowfield = FlowField(20)
    vehicles = []
    for i in range(120):
        vehicles.append(Vehicle(PVector(Prandom(width), Prandom(
            height)), Prandom(2, 5), Prandom(0.1, 0.5)))


def update():
    pygame_process_events(pygame.event.get())
    background(1, 1, 1)
    fill(1, 0, 0)
    strokeWeight(0.003)
    # flowfield.display()
    for v in vehicles:
        v.follow(flowfield)
        v.run()
    if mousePressed:
        flowfield.init()
        circle(mouseX, mouseY, 20)
    
    passed_time = fps_clock.tick(FPS_MAX)


if __name__ == "__main__":
    main(start, update, width, height)




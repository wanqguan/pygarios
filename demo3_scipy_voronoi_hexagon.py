import numpy as np
from scipy import spatial
from pygarios import *

def pygame_process_events(events):
    global mousePressed, mouseX, mouseY
    mousePressed, mouseX, mouseY = update_mouse_state_from_pygame_events(events)


def generate_points(n_iter, n_points, radius, theta0):
    """Creates a mandala figure using Voronoi tesselations.

    Parameters
    ----------
    n_iter : int
        Number of iterations, i.e. how many times the equidistant points will
        be generated.
    n_points : int
        Number of points to draw per iteration.
    radius : scalar
        The radial expansion factor.

    Returns
    -------
    fig : matplotlib.Figure instance

    Notes
    -----
    This code is adapted from the work of Audrey Roy Greenfeld [1]_ and Carlos
    Focil-Espinosa [2]_, who created beautiful mandalas with Python code.  That
    code in turn was based on Antonio Sánchez Chinchón's R code [3]_.

    References
    ----------
    .. [1] https://www.codemakesmehappy.com/2019/09/voronoi-mandalas.html

    .. [2] https://github.com/CarlosFocil/mandalapy

    .. [3] https://github.com/aschinchon/mandalas

    """


    angles = np.linspace(0, 2*np.pi * (1 - 1/n_points), num=n_points) + np.pi/2
    # Starting from a single center point, add points iteratively
    xy = np.array([[0, 0]])
    for k in range(n_iter):
        angles += theta0
        t1 = np.array([])
        t2 = np.array([])
        # Add `n_points` new points around each existing point in this iteration
        for i in range(xy.shape[0]):
            t1 = np.append(t1, xy[i, 0] + radius**k * np.cos(angles))
            t2 = np.append(t2, xy[i, 1] + radius**k * np.sin(angles))

        xy = np.column_stack((t1, t2))

    return xy
    
fps_clock = pygame.time.Clock()
FPS_MAX = 2
width, height = 600, 600

n_iter = 2
n_points = 6
radius = 4
scale_k = 30





def start():
    global theta0
    theta0 = 0



def update():
    global theta0
    theta0 += 0.002
    pygame_process_events(pygame.event.get())  # pyplay 特殊语法

    points = generate_points(n_iter, n_points, radius, theta0)
    points *= scale_k
    # print(points.shape)  # (216, 2)
    vor = spatial.Voronoi(points)

    background(1, 1, 1)
    pushMatrix()
    translate(width/2, height/2)

    fill(0, 0, 0)
    noStroke()
    for px, py in points:
        circle(px, py, 2)



    fill(.3, .8, .5)
    for px, py in vor.vertices:
        circle(px, py, 2)

    
    fill(0, 0, 0)
    stroke(0, 0, 0)
    strokeWeight(1)


    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            
            p0x, p0y = vor.vertices[simplex, 0]
            p1x, p1y = vor.vertices[simplex, 1]
            line(p0x, p1x, p0y, p1y)
    
    popMatrix()




if __name__ == "__main__":  # pyplay 特殊语法
    main(start, update, width, height)

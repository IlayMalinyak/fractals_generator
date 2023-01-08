import sdl2.ext

from fractal import FractalApp, Recursor
from geometry import Line, Transform
from math import pi
import numpy as np
from tqdm import tqdm

BLACK = sdl2.ext.Color(50, 50, 50)


def fractal_tree(copies, scale, rot_angle, idx):
    base_diagram = [Line((0, 0), 1, pi / 2, BLACK), ]

    angle = 2*pi/(copies + 1)
    recrule = [Transform((0,1), -pi+i*angle) for i in range(1,copies+1)]

    rec = Recursor(base_diagram,recrule,scale,'add')

    arrangement = [Transform((0,0),rot_angle)]

    my_app = FractalApp()
    renderer = my_app.renderer

    lines = rec.generate(7)
    for a in arrangement:
        renderer.lines.extend(a.modify_lines(lines,1))
    fd = np.log(copies)/np.log(1/scale)
    renderer.save_matrix((50,50), "images/tree_{:.2f}_{}.bmp".format(fd, idx),1)
    # my_app.run()


def koch(rot_angle):
    base_diagram = [Line((0, 0), 1, 0, BLACK),
                    Line((1, 0), 1, pi / 3, BLACK),
                    Line((1.5, np.sqrt(3) / 2), 1, -pi / 3, BLACK),
                    Line((2, 0), 1, 0, BLACK)]

    recrule = [Transform((0, 0), 0),
               Transform((1, 0), pi / 3),
               Transform((1.5, np.sqrt(3) / 2), -pi / 3),
               Transform((2, 0), 0)]

    rec = Recursor(base_diagram, recrule, 1. / 3)

    # arrangement = [Transform((0, 3 * np.sqrt(3) / 2), 0),
    #                Transform((1.5, 0), 2 * pi / 3),
    #                Transform((3, 3 * np.sqrt(3) / 2), -2 * pi / 3)]
    arrangement = [Transform((-1.5,0), rot_angle)]
    my_app = FractalApp()
    renderer = my_app.renderer


    # renderer.save_svg('tree.svg',1000)
    lines = rec.generate(7)
    for a in arrangement:
        renderer.lines.extend(a.modify_lines(lines, 1))
    my_app.run()

def cantor(scale, rot_angle, idx):
    base_diagram = [Line((0, 0), 1, 0, BLACK), ]
    recrule = [Transform((i*1/scale, 1), 0) for i in range(0, scale, 2)]

    rec = Recursor(base_diagram, recrule, 1/scale, 'add')

    arrangement = [Transform((0, 0),rot_angle)]

    my_app = FractalApp()
    renderer = my_app.renderer

    lines = rec.generate(7)
    for a in arrangement:
        renderer.lines.extend(a.modify_lines(lines, 1))
    fd = np.log(scale - 1) / np.log(scale)
    renderer.save_matrix((50,50), "images/cantor_{:.2f}_{}.bmp".format(fd, idx),1)


def random_fractal(idx,base_size, base_angle, base_copies, copies, scale, rot_angle, base_flip=0, flip=0):
    BLACK = sdl2.ext.Color(0, 0, 0)
    start = (0,0)
    base_diagram = []
    for i in range(1,base_copies):
        angle = i*base_angle + base_flip
        base_diagram.append(Line(start, base_size, angle, BLACK))
        addition = base_size * np.cos(angle), base_size * np.sin(angle)
        start = (start[0] +addition[0], start[1] + addition[1])
    angle = 2 * pi / (copies + 1)
    recrule = [Transform(start, -pi + i * angle + flip) for i in range(1, copies + 1)]
    rec = Recursor(base_diagram,recrule,scale,'add')

    arrangement = [Transform((0, 0), rot_angle)]

    my_app = FractalApp()
    renderer = my_app.renderer

    lines = rec.generate(7)
    for a in arrangement:
        renderer.lines.extend(a.modify_lines(lines, 1))
    # my_app.run()
    fd = np.log(copies) / np.log(1 / scale)
    try:
        renderer.save_matrix((50, 50), "images/random_{:.2f}_{}.bmp".format(fd, idx), 1)
    except ValueError:
        pass


def generate_random_fractals(scales, num_bases, num_copies):
    for i, base_scale in enumerate(scales):
        for j in range(num_bases):
            base_angle = np.random.rand() * pi / 4
            base_copies = np.random.randint(2, 7)
            for k in range(num_copies):
                copies = np.random.randint(2, 7)
                scale = np.random.rand() * 0.5
                base_flip = 0 if np.random.rand() > 0.5 else pi / 2
                flip = 0 if np.random.rand() > 0.5 else pi / 2
                rot_angle = np.random.rand() * pi / 4 +flip
                idx = i * 9 + j * 3 + k
                print(idx, "fd=", np.log(copies) / np.log(1 / scale))
                random_fractal(idx, base_scale, base_angle, base_copies, copies, scale, rot_angle,
                               base_flip=base_flip, flip=flip)


# create fractal trees in different dimensions
for c in [3,4,5,6]:
    for s in [1/3,1/2]:
        for i in tqdm(range(10)):
            rot_angle = np.random.rand() * np.pi - np.pi/2
            fractal_tree(c,s, rot_angle, i)
# create Cantor sets in different dimensions
for c in [3,5,7]:
    for i in tqdm(range(10)):
        rot_angle = np.random.rand()*2*np.pi
        cantor(c, rot_angle, i)
#  create random fractals
generate_random_fractals([0.3,0.4,0.5], 3, 3)


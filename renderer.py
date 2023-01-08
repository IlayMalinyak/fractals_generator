import sdl2
import sdl2.ext
from geometry import Grid
import svgwrite
import numpy as np
from matplotlib import pyplot as plt



class Renderer(sdl2.ext.SoftwareSpriteRenderSystem):

    def __init__(self, window):
        wx, wy = window.size
        self.grid = Grid((int(wx/2),int(5*wy/6)), 200, window.size)
        self.lines = []


        super(Renderer, self).__init__(window)

    @staticmethod
    def draw_line(mat, x0, y0, x1, y1, inplace=False):
        if not (0 <= x0 < mat.shape[0] and 0 <= x1 < mat.shape[0] and
                0 <= y0 < mat.shape[1] and 0 <= y1 < mat.shape[1]):
            raise ValueError('Invalid coordinates.')
        if not inplace:
            mat = mat.copy()
        if (x0, y0) == (x1, y1):
            mat[x0, y0] = 2
            return mat if not inplace else None
        # Swap axes if Y slope is smaller than X slope
        transpose = abs(x1 - x0) < abs(y1 - y0)
        if transpose:
            mat = mat.T
            x0, y0, x1, y1 = y0, x0, y1, x1
        # Swap line direction to go left-to-right if necessary
        if x0 > x1:
            x0, y0, x1, y1 = x1, y1, x0, y0
        # Write line ends
        mat[x0, y0] = 2
        mat[x1, y1] = 2
        # Compute intermediate coordinates using line equation
        x = np.arange(x0 + 1, x1)
        y = np.round(((y1 - y0) / (x1 - x0)) * (x - x0) + y0).astype(x.dtype)
        # Write intermediate coordinates
        mat[x, y] = 1
        if not inplace:
            return mat if not transpose else mat.T


    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(255,255,255))

        # self.grid.plot(self.surface)

        for l in self.lines:
            l.plot(self.surface, self.grid)

        super(Renderer, self).render(components)

    def save_svg(self, filename, scale):
        dwg = svgwrite.Drawing(filename, profile='tiny')

        for l in self.lines:
            p1 = l.p1
            p2 = l.p2

            p1 = (p1[0]*scale, p1[1]*scale)
            p2 = (p2[0]*scale, p2[1]*scale)

            dwg.add(dwg.line(p1,p2,stroke=svgwrite.rgb(l.color.r,l.color.g,l.color.b)))

    def save_matrix(self, size, filename, scale):
        # p1s = np.array([(l.p1[0], l.p1[1]) for l in self.lines])
        p2s = np.array([(l.p2[1], l.p2[0]) for l in self.lines])
        range = np.max(p2s) - np.min(p2s)
        size = int(size[0]*range)*4, int(size[0]*range)*4
        mat = np.zeros(size)
        center = size[0]//2, size[1]//2
        for i,l in enumerate(self.lines):
            p1 = -1*np.array([l.p1[1],l.p1[0]])
            p2 = -1*p2s[i]
            p1 = (p1*size[0]//4 + center).astype(np.int16)
            p2 = (p2*size[0]//4 + center).astype(np.int16)
            mat = self.draw_line(mat, p1[0], p1[1], p2[0], p2[1])
        max_coords = np.max(np.where(mat), axis=1)
        min_coords = np.min(np.where(mat), axis=1)
        new_shape = (max_coords - min_coords)*3
        new_mat = np.zeros(new_shape)
        new_mat[new_shape[0]//3:2*new_shape[0]//3, new_shape[1]//3:2*new_shape[1]//3] = mat[min_coords[0]:max_coords[0],
                                                                                        min_coords[1]:max_coords[1]]
        plt.imsave(filename, mat, cmap='gray')
        return mat





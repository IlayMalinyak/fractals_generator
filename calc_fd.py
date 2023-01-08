import numpy as np
import pylab as pl
from skimage.filters import threshold_otsu
from matplotlib import pyplot as plt
import os
import cv2
import imageio

import cairosvg
import io
from PIL import Image
import re

def svgRead(filename):
   """Load an SVG file and return image in Numpy array"""
   # Make memory buffer
   mem = io.BytesIO()
   # Convert SVG to PNG in memory
   cairosvg.svg2png(url=filename, write_to=mem, scale=2.0)
   # Convert PNG to Numpy array
   return np.array(Image.open(mem))

# Read SVG file into Numpy array

def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def calc_fd(path):
    image = plt.imread(path)[...,0]
    pixels = np.array(np.where(image > 0)).T
    # plt.imshow(image,cmap="gray")
    # plt.show()
    Lx = image.shape[1]
    Ly = image.shape[0]
    scales = np.logspace(0.01, 1, num=10, endpoint=False, base=2)
    Ns = []
    for scale in scales:
        H, edges = np.histogramdd(pixels, bins=(np.arange(0, Lx, scale), np.arange(0, Ly, scale)))
        Ns.append(np.sum(H > 0))

    coeffs = np.polyfit(np.log(scales), np.log(Ns), 1)

    # print("The Hausdorff dimension is", -coeffs[0])
    return -coeffs[0]



gt = []
error =[]
print(len(os.listdir('./images')))
for p in os.listdir('./images'):
    true_fd = float(re.findall(r'[0-9].[0-9]+', p)[0])
    # print("GT - ", true_fd, end='-')
    fd = calc_fd(f'images/{p}')
    gt.append([true_fd])
    error.append(abs(fd - true_fd))
plt.plot(gt, error, 'o')
plt.title("box counting")
plt.xlabel("$FD_{True}$")
plt.ylabel(r"$|FD_{box}-FD_{True}|$")
plt.savefig("box_error.png")
plt.show()

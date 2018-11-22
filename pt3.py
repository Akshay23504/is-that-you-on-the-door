import numpy as np
from scipy import ndimage

a = np.asarray([[], [], [], []])
gx = ndimage.sobel(a, 0)
gy = ndimage.sobel(a, 1)
magnitude = np.hypot(gx, gy)
print(magnitude)
magnitude += 255.0 / np.max(magnitude)
print("After normalizing\n", magnitude)


f = np.asarray([[], []])
x, y = np.linalg.eig(f)
print(x, y)

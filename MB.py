import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(re_min, re_max, im_min, im_max, width, height, max_iter):
    # Create a grid of complex numbers
    real = np.linspace(re_min, re_max, width)
    imag = np.linspace(im_min, im_max, height)
    c = real[:, None] + imag[None, :] * 1j

    # Initialize z and iteration count
    z = np.zeros_like(c, dtype=np.complex128)
    div_time = np.zeros_like(c, dtype=int)

    # Iterate
    for i in range(max_iter):
        mask = np.abs(z) <= 2
        z[mask] = z[mask]**2 + c[mask]
        div_time[mask & (div_time == 0)] = i

    return div_time

# Parameters
re_min, re_max = -2.0, 1.0
im_min, im_max = -1.5, 1.5
width, height = 1000, 1000
max_iter = 100

# Generate Mandelbrot set
mandelbrot_set = mandelbrot(re_min, re_max, im_min, im_max, width, height, max_iter)

# Plot
plt.figure(figsize=(10, 10))
plt.imshow(mandelbrot_set, extent=(re_min, re_max, im_min, im_max), cmap="inferno")
plt.colorbar()
plt.title("Mandelbrot Set")
plt.xlabel("Re(c)")
plt.ylabel("Im(c)")
plt.show()

import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Set backend for matplotlib
matplotlib.use("MacOSX")
# matplotlib.use("Qt5Agg")


def get_datapoint(n_points):
    dx = 2 * np.pi / n_points

    x = 0
    while True:
        yield x, np.sin(x)
        x += dx


xl = []
yl = []

# Number of data points to show in the figure
n_points = 100

# Draw empty figure
fig, ax = plt.subplots()

# Get an initial line object that we will modify
(line,) = ax.plot([], [])

# We can now set the axes properties outside of loop as we won't clear it
ax.set_xlim(-0.1, 2 * np.pi)
ax.set_xticks(
    [0, 0.5 * np.pi, np.pi, 1.5 * np.pi, 2 * np.pi],
    labels=[0, "$\\dfrac{\\pi}{2}$", "$\\pi$", "$\\dfrac{3\\pi}{2}$", "$2\\pi$"],
)
ax.set_ylim(-1.1, 1.1)
ax.set_title("y = sin(x)")

t0 = time.time()
n = 0
for x, y in get_datapoint(n_points):
    # Exit loop if figure is closed
    if not plt.get_fignums():
        break

    # # Get new data points, keep last n_points
    xl.append(x)
    yl.append(y)
    if len(xl) > n_points:
        xl = xl[-n_points:]
        yl = yl[-n_points:]

    # Instead of calling clear + plot, just set the new x and y data
    line.set_data([x - xl[0] for x in xl], yl)

    # Calculate average framerate
    n += 1
    print(f"FPS: {n / (time.time() - t0)}")

    # Need to add pause - otherwise no plot shows
    plt.pause(1e-6)

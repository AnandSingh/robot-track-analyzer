import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import numpy as np

# Simulated log data
num_points = 30
yaw_deg = np.linspace(0, 90, num_points) + np.random.normal(0, 2, num_points)
dist_l = np.linspace(0, 300, num_points) + np.random.normal(0, 5, num_points)
dist_r = np.linspace(0, 310, num_points) + np.random.normal(0, 5, num_points)

# Prepare position lists
X_path, Y_path = [0.0], [0.0]
x, y = 0.0, 0.0

for i in range(1, num_points):
    dist_delta = ((dist_l[i] - dist_l[i-1]) + (dist_r[i] - dist_r[i-1])) / 2
    yaw_rad = math.radians(yaw_deg[i])
    dx = dist_delta * math.cos(yaw_rad)
    dy = dist_delta * math.sin(yaw_rad)
    x += dx
    y += dy
    X_path.append(x)
    Y_path.append(y)

# Animation setup
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_aspect('equal')
ax.set_title("Robot Path Playback (Bird’s Eye View)")
ax.set_xlabel("X Position (mm)")
ax.set_ylabel("Y Position (mm)")
ax.grid(True)

line, = ax.plot([], [], lw=2, color='blue')
dot, = ax.plot([], [], 'ro', label='Current Position')

def init():
    ax.set_xlim(min(X_path)-50, max(X_path)+50)
    ax.set_ylim(min(Y_path)-50, max(Y_path)+50)
    line.set_data([], [])
    dot.set_data([], [])
    return line, dot

def update(frame):
    line.set_data(X_path[:frame], Y_path[:frame])
    dot.set_data(X_path[frame-1], Y_path[frame-1])
    return line, dot

ani = animation.FuncAnimation(fig, update, frames=len(X_path), init_func=init,
                              interval=300, blit=True, repeat=False)

plt.legend()
plt.tight_layout()
plt.show()

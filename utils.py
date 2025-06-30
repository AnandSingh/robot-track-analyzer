import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def degrees_to_meters(deg, wheel_radius=0.03):
    return (np.deg2rad(deg) * wheel_radius)

def process_csv_and_plot(csv_path, plot_folder):
    df = pd.read_csv(csv_path)

    x, y = 0.0, 0.0
    positions = [(0, 0)]

    for i in range(1, len(df)):
        l_prev, r_prev = df.loc[i - 1, ['angle_l', 'angle_r']]
        l_curr, r_curr, yaw = df.loc[i, ['angle_l', 'angle_r', 'yaw']]

        dl = degrees_to_meters(l_curr - l_prev)
        dr = degrees_to_meters(r_curr - r_prev)
        d = (dl + dr) / 2.0

        theta_rad = np.deg2rad(yaw)
        x += d * np.cos(theta_rad)
        y += d * np.sin(theta_rad)
        positions.append((x, y))

    xs, ys = zip(*positions)

    plot_filename = os.path.basename(csv_path).replace('.csv', '.png')
    plot_path = os.path.join(plot_folder, plot_filename)

    plt.figure(figsize=(8, 6))
    plt.plot(xs, ys, marker='o')
    plt.title('Robot Trajectory')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    return plot_path

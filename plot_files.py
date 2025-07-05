import matplotlib.pyplot as plt
import math
import re
import os
import glob

# Constants
WHEEL_DIAMETER = 56  # mm
DEGREE_TO_MM = (math.pi * WHEEL_DIAMETER) / 360  # mm per degree

# Function to parse a log file into X and Y path
def parse_log_csv(filepath):
    x, y = 0.0, 0.0
    X_path, Y_path = [x], [y]
    last_l, last_r = None, None

    with open(filepath, 'r') as f:
        lines = f.readlines()
    print(filepath)
    print(lines)
    for line in lines:
        match = re.search(r"(\d*),? L: ([\-0-9.]+)°.*, R: ([\-0-9.]+)°.*, Yaw: ([\-0-9.e]+)", line)
        if match:
            _, l_angle, r_angle, yaw_deg = match.groups()
            l_angle = float(l_angle)
            r_angle = float(r_angle)
            yaw_rad = math.radians(float(yaw_deg))

            if last_l is not None and last_r is not None:
                delta_l = (l_angle - last_l) * DEGREE_TO_MM
                delta_r = (r_angle - last_r) * DEGREE_TO_MM
                dist = (delta_l + delta_r) / 2

                dx = dist * math.cos(yaw_rad)
                dy = dist * math.sin(yaw_rad)
                x += dx
                y += dy
                X_path.append(x)
                Y_path.append(y)

            last_l, last_r = l_angle, r_angle

    return X_path, Y_path

# Directory containing run CSV logs
log_dir = "robot_logs"  # change this to your actual folder name
log_files = sorted(glob.glob(os.path.join(log_dir, "run*.csv")))

# Plot setup
plt.figure(figsize=(12, 10))
colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'cyan', 'magenta']
markers = ['o-', 's--', '^--', 'd-.', 'x-', '*-', 'v--', '<-.']

# Loop through each log file and plot
for idx, file in enumerate(log_files):
    X, Y = parse_log_csv(file)
    label = os.path.splitext(os.path.basename(file))[0]
    plt.plot(X, Y, markers[idx % len(markers)], label=label, color=colors[idx % len(colors)])

plt.title("Overlay of Robot Runs from CSV Logs")
plt.xlabel("X Position (mm)")
plt.ylabel("Y Position (mm)")
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

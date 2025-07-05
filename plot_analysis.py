import matplotlib.pyplot as plt
import math
import re
import os
import glob

# Constants
WHEEL_DIAMETER = 56  # mm
DEGREE_TO_MM = (math.pi * WHEEL_DIAMETER) / 360  # mm per degree

# Analysis results storage
analysis_results = []

# Function to parse a log file and extract X/Y path and analysis
def parse_log_csv(filepath):
    x, y = 0.0, 0.0
    X_path, Y_path = [x], [y]
    last_l, last_r = None, None
    total_dist = 0
    turn_count = 0
    symmetry_error_accum = 0
    lines = open(filepath, 'r').readlines()

    for i, line in enumerate(lines):
        match = re.search(r"(\d*),? L: ([\-0-9.]+)°.*, R: ([\-0-9.]+)°.*, Yaw: ([\-0-9.e]+), Rate: ([\-0-9.e]+)", line)
        if match:
            _, l_angle, r_angle, yaw_deg, yaw_rate = match.groups()
            l_angle = float(l_angle)
            r_angle = float(r_angle)
            yaw_rad = math.radians(float(yaw_deg))
            yaw_rate = float(yaw_rate)

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

                total_dist += abs(dist)
                symmetry_error_accum += abs(delta_l - delta_r)

                if abs(yaw_rate) > 1.0:
                    turn_count += 1

            last_l, last_r = l_angle, r_angle

    if total_dist > 0:
        symmetry_error = (symmetry_error_accum / total_dist) * 100
    else:
        symmetry_error = 0

    confidence = 100
    confidence -= min(symmetry_error, 20)
    confidence -= max(0, (turn_count - 4) * 5)
    confidence = max(0, round(confidence))

    analysis_results.append({
        'run': os.path.basename(filepath),
        'distance': round(total_dist),
        'symmetry_error': round(symmetry_error, 2),
        'turns': turn_count,
        'confidence': confidence
    })

    return X_path, Y_path

# Directory containing run CSV logs
log_dir = "walle_logs"  # Change as needed
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

# Print analysis summary
print("\n=== Run Summary ===")
for result in analysis_results:
    print(f"Run: {result['run']}")
    print(f"- Total Distance: {result['distance']} mm")
    print(f"- Wheel Symmetry Error: {result['symmetry_error']}%")
    print(f"- Turn Events Detected: {result['turns']}")
    print(f"- Confidence Score: {result['confidence']}%\n")

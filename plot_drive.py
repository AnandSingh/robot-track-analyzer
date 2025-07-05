import matplotlib.pyplot as plt
import math
import re

# Constants
WHEEL_DIAMETER = 56  # mm
DEGREE_TO_MM = (math.pi * WHEEL_DIAMETER) / 360  # mm per degree

# Function to parse log into X and Y coordinates
def parse_log_to_path(log_text):
    x, y = 0.0, 0.0
    X_path, Y_path = [x], [y]
    lines = log_text.strip().split('\n')
    last_l, last_r = None, None

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

log_run1 = """
L: -112.0°, R: 133.0°, Yaw: 0.0, Rate: 0.05944281, Note: Init Done
3, L: -112.0°, R: 133.0°, Yaw: 3.051758e-05, Rate: -0.08055719, Note: drive 250mm
994, L: 249.0°, R: 494.0°, Yaw: 0.1638794, Rate: -0.2205572, Note: drive 250mm
1980, L: 386.0°, R: 356.0°, Yaw: 94.82266, Rate: -1.060557, Note: drive 250mm
2955, L: 740.0°, R: 722.0°, Yaw: 90.74838, Rate: 1.179443, Note: drive 250mm
3945, L: 878.0°, R: 582.0°, Yaw: 185.2661, Rate: 3.909443, Note: drive 250mm
4920, L: 1235.0°, R: 950.0°, Yaw: 181.7995, Rate: 3.979443, Note: drive 250mm
5915, L: 1370.0°, R: 809.0°, Yaw: 275.1749, Rate: 2.159443, Note: drive 250mm
6890, L: 1726.0°, R: 1177.0°, Yaw: 270.8669, Rate: -0.5005572, Note: drive 250mm 
"""

# Second run log
log_run2 = """
0, L: 67.0°, R: 1.0°, Yaw: 0.0, Rate: -0.03469862, Note: Init Done
2, L: 67.0°, R: 1.0°, Yaw: -0.0001220703, Rate: 0.03530139, Note: drive 250mm
994, L: 429.0°, R: 363.0°, Yaw: 0.19104, Rate: 2.065301, Note: drive 250mm
1984, L: 567.0°, R: 223.0°, Yaw: 94.6333, Rate: -0.8746986, Note: drive 250mm
2958, L: 924.0°, R: 591.0°, Yaw: 91.22205, Rate: 2.205302, Note: drive 250mm
3949, L: 1063.0°, R: 449.0°, Yaw: 186.5015, Rate: 0.5253014, Note: drive 250mm
4924, L: 1415.0°, R: 818.0°, Yaw: 181.1576, Rate: 0.8753014, Note: drive 250mm
5909, L: 1553.0°, R: 678.0°, Yaw: 274.5451, Rate: -1.574699, Note: drive 250mm
6884, L: 1909.0°, R: 1047.0°, Yaw: 270.3685, Rate: 2.765301, Note: drive 250mm
"""

# Paste your five logs here
log_run3 = """
0, L: -159.0°, R: 152.0°, Yaw: 0.0, Rate: 0.07841856, Note: Init Done
2, L: -159.0°, R: 152.0°, Yaw: 0.0001220703, Rate: -0.06158143, Note: drive 250mm
1045, L: 201.0°, R: 513.0°, Yaw: -0.08581543, Rate: 2.108418, Note: drive 250mm
2035, L: 337.0°, R: 374.0°, Yaw: 93.24329, Rate: -0.8315814, Note: drive 250mm
3010, L: 693.0°, R: 741.0°, Yaw: 89.47571, Rate: -2.231581, Note: drive 250mm
3990, L: 832.0°, R: 602.0°, Yaw: 184.0475, Rate: -1.531581, Note: drive 250mm
4965, L: 1189.0°, R: 969.0°, Yaw: 181.1858, Rate: 0.008418575, Note: drive 250mm
5950, L: 1326.0°, R: 829.0°, Yaw: 274.6189, Rate: 1.128419, Note: drive 250mm
6925, L: 1681.0°, R: 1196.0°, Yaw: 270.9994, Rate: 2.388418, Note: drive 250mm
"""

log_run4 = """
1, L: -9.0°, R: -26.0°, Yaw: 0.0, Rate: 0.04039412, Note: Init Done
3, L: -9.0°, R: -25.0°, Yaw: 0.0, Rate: 0.04039412, Note: drive 250mm
1045, L: 352.0°, R: 337.0°, Yaw: -0.0078125, Rate: 2.490394, Note: drive 250mm
2034, L: 489.0°, R: 196.0°, Yaw: 94.80457, Rate: 0.3903941, Note: drive 250mm
3010, L: 846.0°, R: 565.0°, Yaw: 90.81775, Rate: 0.3203941, Note: drive 250mm
3995, L: 986.0°, R: 425.0°, Yaw: 185.5226, Rate: -1.149606, Note: drive 250mm
4970, L: 1339.0°, R: 792.0°, Yaw: 180.9788, Rate: 0.5303941, Note: drive 250mm
5954, L: 1477.0°, R: 654.0°, Yaw: 275.0571, Rate: 0.1803942, Note: drive 250mm
6930, L: 1831.0°, R: 1022.0°, Yaw: 270.6875, Rate: 1.510394, Note: drive 250mm
"""

log_run5 = """
1, L: 178.0°, R: -176.0°, Yaw: 0.0, Rate: -0.03266166, Note: Init Done
3, L: 178.0°, R: -176.0°, Yaw: -0.0001220703, Rate: 0.1073383, Note: drive 250mm
996, L: 541.0°, R: 185.0°, Yaw: 0.743042, Rate: 1.297338, Note: drive 250mm
1986, L: 679.0°, R: 44.0°, Yaw: 95.37598, Rate: -0.3126617, Note: drive 250mm
2961, L: 1033.0°, R: 412.0°, Yaw: 90.72083, Rate: 1.577338, Note: drive 250mm
3951, L: 1174.0°, R: 271.0°, Yaw: 184.8198, Rate: -0.5926617, Note: drive 250mm
4926, L: 1530.0°, R: 638.0°, Yaw: 181.8707, Rate: 0.8773383, Note: drive 250mm
5916, L: 1667.0°, R: 499.0°, Yaw: 274.9087, Rate: -0.4526617, Note: drive 250mm
6891, L: 2021.0°, R: 865.0°, Yaw: 271.5386, Rate: 1.647338, Note: drive 250mm
"""

# Parse logs
X1, Y1 = parse_log_to_path(log_run1)
X2, Y2 = parse_log_to_path(log_run2)
X3, Y3 = parse_log_to_path(log_run3)
X4, Y4 = parse_log_to_path(log_run4)
X5, Y5 = parse_log_to_path(log_run5)

# Plot all runs
plt.figure(figsize=(12, 10))
plt.plot(X1, Y1, 'o-', label='Run 1', color='blue')
plt.plot(X2, Y2, 's--', label='Run 2', color='green')
plt.plot(X3, Y3, '^--', label='Run 3', color='red')
plt.plot(X4, Y4, 'd-.', label='Run 4', color='purple')
plt.plot(X5, Y5, 'x-', label='Run 5', color='orange')

plt.title("Overlay of Multiple Robot Runs (Path Comparison)")
plt.xlabel("X Position (mm)")
plt.ylabel("Y Position (mm)")
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

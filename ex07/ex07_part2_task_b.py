import numpy as np
import matplotlib.pyplot as plt

def simulate_robot(num_runs, velocity, time_step, total_time, sigma_right, sigma_left, circular=False):
    b = 1.0  # axis length
    radius = 5.0  # Radius for circular path
    positions = np.zeros((num_runs, 2))  # x, y positions
    odometries = np.zeros((num_runs, 2))  # x, y odometry

    for i in range(num_runs):
        x, y, theta = 0, 0, 0  # initial pose
        odom_x, odom_y = 0, 0  # initial odometry readings

        for t in np.arange(0, total_time, time_step):
            if circular:
                vr = velocity  # constant right velocity
                vl = velocity * (1 - b / radius)  # reduced left velocity for turning
            else:
                vr = velocity  # constant right velocity
                vl = velocity  # constant left velocity

            # Add noise to velocities
            vr += np.random.normal(0, sigma_right)
            vl += np.random.normal(0, sigma_left)

            # Kinematic model for actual movement
            delta_x = 0.5 * (vr + vl) * np.cos(theta) * time_step
            delta_y = 0.5 * (vr + vl) * np.sin(theta) * time_step
            delta_theta = (1/b) * (vr - vl) * time_step

            x += delta_x
            y += delta_y
            theta += delta_theta

            # Perfect odometry (no error model here)
            odom_x += delta_x
            odom_y += delta_y

        positions[i] = [x, y]
        odometries[i] = [odom_x, odom_y]

    return positions, odometries

# Simulation parameters
num_runs = 100
velocity = 1.0  # constant velocity
time_step = 0.1
total_time = 5.0  # simulate for 5 seconds
sigma_right = 0.1  # Standard deviation of noise for right wheel
sigma_left = 0.1  # Standard deviation of noise for left wheel

# Simulate straight line movement
straight_positions, straight_odometries = simulate_robot(num_runs, velocity, time_step, total_time, sigma_right, sigma_left)

# Simulate circular movement
circular_positions, circular_odometries = simulate_robot(num_runs, velocity, time_step, total_time, sigma_right, sigma_left, circular=True)

# Plotting results for straight line and circular movements
plt.figure(figsize=(12, 12))

# Actual positions for straight line movement
plt.subplot(2, 2, 1)
plt.hist2d(straight_positions[:, 0], straight_positions[:, 1], bins=(50, 50), cmap='viridis')
plt.colorbar(label='Counts in bin')
plt.title('Actual Positions (Straight Line)')
plt.xlabel('X Position')
plt.ylabel('Y Position')

# Odometry readings for straight line movement
plt.subplot(2, 2, 2)
plt.hist2d(straight_odometries[:, 0], straight_odometries[:, 1], bins=(50, 50), cmap='viridis')
plt.colorbar(label='Counts in bin')
plt.title('Odometry Readings (Straight Line)')
plt.xlabel('X Position')
plt.ylabel('Y Position')

# Actual positions for circular movement
plt.subplot(2, 2, 3)
plt.hist2d(circular_positions[:, 0], circular_positions[:, 1], bins=(50, 50), cmap='viridis')
plt.colorbar(label='Counts in bin')
plt.title('Actual Positions (Circular Path)')
plt.xlabel('X Position')
plt.ylabel('Y Position')

# Odometry readings for circular movement
plt.subplot(2, 2, 4)
plt.hist2d(circular_odometries[:, 0], circular_odometries[:, 1], bins=(50, 50), cmap='viridis')
plt.colorbar(label='Counts in bin')
plt.title('Odometry Readings (Circular Path)')
plt.xlabel('X Position')
plt.ylabel('Y Position')

plt.tight_layout()
plt.savefig("ex07/ex07_b.png")
plt.show()

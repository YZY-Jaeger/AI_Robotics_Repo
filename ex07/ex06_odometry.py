import numpy as np
import matplotlib.pyplot as plt

def simulate_robot(num_runs, velocity, time_step, total_time):
    b = 1.0  # axis length
    positions = np.zeros((num_runs, 2))  # x, y positions
    odometries = np.zeros((num_runs, 2))  # x, y from odometry

    for i in range(num_runs):
        x, y, theta = 0, 0, 0  # initial pose
        odom_x, odom_y = 0, 0  # initial odometry readings

        for t in np.arange(0, total_time, time_step):
            # Simulate some noise in velocity measurements
            vr = velocity + np.random.normal(0, 0.05)  # velocity noise
            vl = velocity + np.random.normal(0, 0.05)

            # Kinematic model
            delta_x = 0.5 * (vr + vl) * np.cos(theta) * time_step
            delta_y = 0.5 * (vr + vl) * np.sin(theta) * time_step
            delta_theta = (1/b) * (vr - vl) * time_step

            x += delta_x
            y += delta_y
            theta += delta_theta

            odom_x += delta_x  # simplistic odometry (no error model here)
            odom_y += delta_y

        positions[i] = [x, y]
        odometries[i] = [odom_x, odom_y]

    return positions, odometries

# Simulation parameters
num_runs = 100
velocity = 1.0  # constant velocity for both wheels
time_step = 0.1
total_time = 5.0  # simulate for 5 seconds

# Run simulation
positions, odometries = simulate_robot(num_runs, velocity, time_step, total_time)

# Generate a combined 2-dimensional histogram
plt.figure(figsize=(8, 6))

# Plot the actual positions and odometry readings on the same histogram
plt.hist2d(np.concatenate((positions[:, 0], odometries[:, 0])),
           np.concatenate((positions[:, 1], odometries[:, 1])),
           bins=(50, 50), cmap='viridis')
plt.colorbar(label='Counts in bin')
plt.title('Combined Histogram of Actual Positions and Odometry Readings')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.grid(True)
plt.show()

import numpy as np
import matplotlib.pyplot as plt

def simulate_robot(num_runs, velocity, time_step, total_time, sigma_right, sigma_left, sigma_o_right, sigma_o_left):
    b = 1.0  # axis length
    radius = 5.0  # Radius for circular path
    results = []

    for scenario in range(3):  # Loop over scenarios
        positions = np.zeros((num_runs, 2))  # x, y positions
        odometries = np.zeros((num_runs, 2))  # x, y odometry
        
        for i in range(num_runs):
            x, y, theta = 0, 0, 0  # initial pose
            odom_x, odom_y = 0, 0  # initial odometry readings
            prev_odo_x, prev_odo_y = 0, 0  # previous odometry for correction

            for t in np.arange(0, total_time, time_step):
                vr = velocity  # constant right velocity
                vl = velocity * (1 - b / radius)  # reduced left velocity for turning

                # Add movement noise
                noisy_vr = vr + np.random.normal(0, sigma_right)
                noisy_vl = vl + np.random.normal(0, sigma_left)

                # Kinematic model for actual movement
                delta_x = 0.5 * (noisy_vr + noisy_vl) * np.cos(theta) * time_step
                delta_y = 0.5 * (noisy_vr + noisy_vl) * np.sin(theta) * time_step
                delta_theta = (1/b) * (noisy_vr - noisy_vl) * time_step

                x += delta_x
                y += delta_y
                theta += delta_theta

                # Odometry with noise
                odom_vr = vr + np.random.normal(0, sigma_o_right)
                odom_vl = vl + np.random.normal(0, sigma_o_left)
                odo_delta_x = 0.5 * (odom_vr + odom_vl)  * np.cos(theta) * time_step
                odo_delta_y = 0.5 * (odom_vr + odom_vl)  * np.sin(theta) * time_step

                odom_x += odo_delta_x
                odom_y += odo_delta_y

                if scenario == 1:  # Perfect odometry correction
                    odom_x, odom_y  = x, y
                elif scenario == 2:  # Noisy odometry correction
                    correction_factor = 0.1
                    x += correction_factor * (odom_x - prev_odo_x)
                    y += correction_factor * (odom_y - prev_odo_y)
                    prev_odo_x, prev_odo_y = odom_x, odom_y

            positions[i] = [x, y]
            odometries[i] = [odom_x, odom_y]

        results.append((positions, odometries))

    return results

# Simulation parameters
num_runs = 100
velocity = 1.0  # constant velocity
time_step = 0.1
total_time = 10.0  # simulate for 10 seconds
sigma_right = 0.1  # Movement noise right wheel
sigma_left = 0.1  # Movement noise left wheel
sigma_o_right = 0.2  # Odometry noise right wheel
sigma_o_left = 0.2  # Odometry noise left wheel

# Run simulation
results = simulate_robot(num_runs, velocity, time_step, total_time, sigma_right, sigma_left, sigma_o_right, sigma_o_left)

# Plotting results
titles = ['No Odometry Correction', 'Perfect Odometry Correction', 'Noisy Odometry Correction']
plt.figure(figsize=(18, 12))

for i in range(3):
    positions, odometries = results[i]
    # Plot actual positions
    plt.subplot(3, 2, 2*i+1)
    plt.hist2d(positions[:, 0], positions[:, 1], bins=(50, 50), cmap='viridis')
    plt.colorbar(label='Counts in bin')
    plt.title(f'Actual Positions ({titles[i]})')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')

    # Plot odometry readings
    plt.subplot(3, 2, 2*i+2)
    plt.hist2d(odometries[:, 0], odometries[:, 1], bins=(50, 50), cmap='viridis')
    plt.colorbar(label='Counts in bin')
    plt.title(f'Odometry Positions ({titles[i]})')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')

plt.tight_layout()
plt.savefig("ex07/c.png")
plt.show()

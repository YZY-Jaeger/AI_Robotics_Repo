import numpy as np
import matplotlib.pyplot as plt

VELOCITY = 1.0
TIME_STEP = 0.1
TOTAL_TIME = 10.0
SIGMA_RIGHT = 0.1
SIGMA_LEFT = 0.1
SIGMA_O_RIGHT = 0.2
SIGMA_O_LEFT = 0.2
RADIUS = 5.0
B = 1.0

def kinematic_model(vr, vl, theta, time_step):
    delta_x = 0.5 * (vr + vl) * np.cos(theta) * time_step
    delta_y = 0.5 * (vr + vl) * np.sin(theta) * time_step
    delta_theta = (1/B) * (vr - vl) * time_step
    return delta_x, delta_y, delta_theta

def odometry(vr, vl, theta, time_step):
    odo_dx = 0.5 * (vr + vl) * np.cos(theta) * time_step
    odo_dy = 0.5 * (vr + vl) * np.sin(theta) * time_step
    return odo_dx, odo_dy

def simulate_robot(num_runs, velocity, time_step, total_time, sigma_right, sigma_left, sigma_o_right, sigma_o_left):
    results = []

    # Task a) and b) - Straight line motion with and without errors
    positions_straight = np.zeros((num_runs, 2))
    odometries_straight = np.zeros((num_runs, 2))
    
    positions_straight_error = np.zeros((num_runs, 2))
    odometries_straight_error = np.zeros((num_runs, 2))

    for i in range(num_runs):
        x, y, theta = 0, 0, 0
        odom_x, odom_y = 0, 0

        for t in np.arange(0, total_time, time_step):
            vr = velocity
            vl = velocity

            noisy_vr = vr + np.random.normal(0, sigma_right)
            noisy_vl = vl + np.random.normal(0, sigma_left)

            delta_x, delta_y, delta_theta = kinematic_model(vr, vl, theta, time_step)
            x += delta_x
            y += delta_y
            theta += delta_theta

            odom_vr = vr + np.random.normal(0, sigma_o_right)
            odom_vl = vl + np.random.normal(0, sigma_o_left)
            odo_dx, odo_dy = odometry(odom_vr, odom_vl, theta, time_step)
            odom_x += odo_dx
            odom_y += odo_dy

        positions_straight[i] = [x, y]
        odometries_straight[i] = [odom_x, odom_y]

        x, y, theta = 0, 0, 0
        odom_x, odom_y = 0, 0

        for t in np.arange(0, total_time, time_step):
            vr = velocity
            vl = velocity

            noisy_vr = vr + np.random.normal(0, sigma_right)
            noisy_vl = vl + np.random.normal(0, sigma_left)

            delta_x, delta_y, delta_theta = kinematic_model(noisy_vr, noisy_vl, theta, time_step)
            x += delta_x
            y += delta_y
            theta += delta_theta

            odom_vr = vr + np.random.normal(0, sigma_o_right)
            odom_vl = vl + np.random.normal(0, sigma_o_left)
            odo_dx, odo_dy = odometry(odom_vr, odom_vl, theta, time_step)
            odom_x += odo_dx
            odom_y += odo_dy

        positions_straight_error[i] = [x, y]
        odometries_straight_error[i] = [odom_x, odom_y]

    results.append((positions_straight, odometries_straight))
    results.append((positions_straight_error, odometries_straight_error))

    # Task b) - Circular motion with and without odometry correction
    positions = np.zeros((num_runs, 2))
    odometries = np.zeros((num_runs, 2))

    for scenario in range(3):
        positions_scenario = np.zeros((num_runs, 2))
        odometries_scenario = np.zeros((num_runs, 2))

        for i in range(num_runs):
            x, y, theta = 0, 0, 0
            odom_x, odom_y= 0, 0

            for t in np.arange(0, total_time, time_step):
                vr = velocity
                vl = velocity * (1 - B / RADIUS)

                noisy_vr = vr + np.random.normal(0, sigma_right)
                noisy_vl = vl + np.random.normal(0, sigma_left)

                delta_x, delta_y, delta_theta = kinematic_model(noisy_vr, noisy_vl, theta, time_step)
                x += delta_x
                y += delta_y
                theta += delta_theta

                if scenario == 0:  # No odometry correction
                    odom_vr = vr + np.random.normal(0, sigma_o_right)
                    odom_vl = vl + np.random.normal(0, sigma_o_left)
                elif scenario == 1:  # Perfect odometry correction
                    odom_vr = vr
                    odom_vl = vl
                else:  # Noisy odometry correction
                    odom_vr = vr + np.random.normal(0, sigma_o_right)
                    odom_vl = vl + np.random.normal(0, sigma_o_left)

                odo_dx, odo_dy = odometry(odom_vr, odom_vl, theta, time_step)
                odom_x += odo_dx
                odom_y += odo_dy

            positions_scenario[i] = [x, y]
            odometries_scenario[i] = [odom_x, odom_y]

        positions = positions_scenario
        odometries = odometries_scenario

        results.append((positions, odometries))

    return results

def plot_results(results):
    fig, axs = plt.subplots(3, 2, figsize=(18, 12))

    axs[0, 0].hist2d(results[0][0][:, 0], results[0][0][:, 1], bins=50)
    axs[0, 0].set_title('Actual Position (Straight Line)')
    axs[0, 0].set_xlabel('X Position')
    axs[0, 0].set_ylabel('Y Position')

    axs[0, 1].hist2d(results[0][1][:, 0], results[0][1][:, 1], bins=50)
    axs[0, 1].set_title('Odometry (Straight Line)')
    axs[0, 1].set_xlabel('X Position')
    axs[0, 1].set_ylabel('Y Position')

    axs[1, 0].hist2d(results[1][0][:, 0], results[1][0][:, 1], bins=50)
    axs[1, 0].set_title('Actual Position (Straight Line with Errors)')
    axs[1, 0].set_xlabel('X Position')
    axs[1, 0].set_ylabel('Y Position')

    axs[1, 1].hist2d(results[1][1][:, 0], results[1][1][:, 1], bins=50)
    axs[1, 1].set_title('Odometry (Straight Line with Errors)')
    axs[1, 1].set_xlabel('X Position')
    axs[1, 1].set_ylabel('Y Position')

    axs[2, 0].hist2d(results[2][0][:, 0], results[2][0][:, 1], bins=50)
    axs[2, 0].set_title('Actual Position (Circular Motion)')
    axs[2, 0].set_xlabel('X Position')
    axs[2, 0].set_ylabel('Y Position')

    axs[2, 1].hist2d(results[2][1][:, 0], results[2][1][:, 1], bins=50)
    axs[2, 1].set_title('Odometry (Circular Motion)')
    axs[2, 1].set_xlabel('X Position')
    axs[2, 1].set_ylabel('Y Position')

    plt.subplots_adjust(hspace=0.6)
    plt.savefig('ex07/ex07_a&b.png')
    plt.show()

num_runs = 1000
results = simulate_robot(num_runs, VELOCITY, TIME_STEP, TOTAL_TIME, SIGMA_RIGHT, SIGMA_LEFT, SIGMA_O_RIGHT, SIGMA_O_LEFT)
plot_results(results)
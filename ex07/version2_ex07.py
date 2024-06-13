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

    # Task a) and b) - Straight line motion without velocity errors (a) and with (b)
    positions = np.zeros((num_runs, 2))
    odometries = np.zeros((num_runs, 2))
    
    for error in [False, True]:
        for i in range(num_runs):
            x, y, theta = 0, 0, 0
            odom_x, odom_y = 0, 0

            for t in np.arange(0, total_time, time_step):

                if error: #b.1
                    noisy_vr = velocity + np.random.normal(0, sigma_right)
                    noisy_vl = velocity + np.random.normal(0, sigma_left)
                else: #a
                    noisy_vr = velocity 
                    noisy_vl = velocity 

                delta_x, delta_y, delta_theta = kinematic_model(noisy_vr, noisy_vl, theta, time_step)
                x += delta_x
                y += delta_y
                theta += delta_theta

                odom_vr = velocity + np.random.normal(0, sigma_o_right)
                odom_vl = velocity + np.random.normal(0, sigma_o_left)
                odo_dx, odo_dy = odometry(odom_vr, odom_vl, theta, time_step)
                odom_x += odo_dx
                odom_y += odo_dy

            positions[i] = [x, y]
            odometries[i] = [odom_x, odom_y]

        results.append((positions, odometries))

    # Task b) - Circular motion with and without velocity errors
    positions = np.zeros((num_runs, 2))
    odometries = np.zeros((num_runs, 2))

    for i in range(num_runs):
        x, y, theta = 0, 0, 0
        odom_x, odom_y= 0, 0

        for t in np.arange(0, total_time, time_step):
            vr = velocity
            vl = velocity * (1 - B / RADIUS)
            #random velocity noice
            noisy_vr = vr + np.random.normal(0, sigma_right)
            noisy_vl = vl + np.random.normal(0, sigma_left)
            #kinematic_model with velocity noise
            delta_x, delta_y, delta_theta = kinematic_model(noisy_vr, noisy_vl, theta, time_step)
            x += delta_x
            y += delta_y
            theta += delta_theta
            #without velocity noise
            odo_dx, odo_dy = odometry(vr, vl, theta, time_step)
            odom_x += odo_dx
            odom_y += odo_dy

        positions[i] = [x, y]
        odometries[i] = [odom_x, odom_y]

    results.append((positions, odometries))

    #Task c) Circular motion with velocities errors and odometry errors
    # i. drive without taking odometry into consideration
    # ii. make correlations based on the perfect odometry estimation
    # iii. make correlations based on the noisy odometry estimation 
    cases = [
        {'name': 'no_odom', 'odom_noise': False, 'odom_error': False},
        {'name': 'perfect_odom', 'odom_noise': False, 'odom_error': False},
        {'name': 'noisy_odom', 'odom_noise': True, 'odom_error': True}
    ]

    for case in cases:
        positions = np.zeros((num_runs, 2))
        odometries = np.zeros((num_runs, 2))
        for i in range(num_runs):
            x, y, theta = 0, 0, 0
            odom_x, odom_y = 0, 0

            for t in np.arange(0, total_time, time_step):
                vr = velocity
                vl = velocity * (1 - B / RADIUS)

                noisy_vr = vr + np.random.normal(0, sigma_right)
                noisy_vl = vl + np.random.normal(0, sigma_left)

                delta_x, delta_y, delta_theta = kinematic_model(noisy_vr, noisy_vl, theta, time_step)
                x += delta_x
                y += delta_y
                theta += delta_theta

                if case['odom_noise']:
                    odom_vr = vr + np.random.normal(0, sigma_o_right)
                    odom_vl = vl + np.random.normal(0, sigma_o_left)
                else:
                    odom_vr = vr
                    odom_vl = vl

                odo_dx, odo_dy = odometry(odom_vr, odom_vl, theta, time_step)
                odom_x += odo_dx
                odom_y += odo_dy

            positions[i] = [x, y]
            odometries[i] = [odom_x, odom_y]

        results.append((positions, odometries))

    return results

def plot_results(results):
    # First 6 histograms
    fig1, axs1 = plt.subplots(3, 2, figsize=(18, 18))

    axs1[0, 0].hist2d(results[0][0][:, 0], results[0][0][:, 1], bins=50)
    axs1[0, 0].set_title('Actual Position (Straight Line)')
    axs1[0, 0].set_xlabel('X Position')
    axs1[0, 0].set_ylabel('Y Position')

    axs1[0, 1].hist2d(results[0][1][:, 0], results[0][1][:, 1], bins=50)
    axs1[0, 1].set_title('Estimated Position (Straight Line)')
    axs1[0, 1].set_xlabel('X Position')
    axs1[0, 1].set_ylabel('Y Position')

    axs1[1, 0].hist2d(results[1][0][:, 0], results[1][0][:, 1], bins=50)
    axs1[1, 0].set_title('Actual Position (Straight Line with Velocity Errors)')
    axs1[1, 0].set_xlabel('X Position')
    axs1[1, 0].set_ylabel('Y Position')

    axs1[1, 1].hist2d(results[1][1][:, 0], results[1][1][:, 1], bins=50)
    axs1[1, 1].set_title('Estimated Position (Straight Line with Velocity Errors)')
    axs1[1, 1].set_xlabel('X Position')
    axs1[1, 1].set_ylabel('Y Position')

    axs1[2, 0].hist2d(results[2][0][:, 0], results[2][0][:, 1], bins=50)
    axs1[2, 0].set_title('Actual Position (Circular Motion with Velocity Errors)')
    axs1[2, 0].set_xlabel('X Position')
    axs1[2, 0].set_ylabel('Y Position')

    axs1[2, 1].hist2d(results[2][1][:, 0], results[2][1][:, 1], bins=50)
    axs1[2, 1].set_title('Estimated Position (Circular Motion with Velocity Errors)')
    axs1[2, 1].set_xlabel('X Position')
    axs1[2, 1].set_ylabel('Y Position')

    axs1[0, 0].set_ylabel('Y Position')
    axs1[1, 0].set_ylabel('Y Position')
    axs1[2, 0].set_ylabel('Y Position')

    plt1 = plt.gcf()
    plt.subplots_adjust(hspace=0.6)
    plt.savefig('ex07/ex07_a&b.png')
    plt.show()

    # Last 6 histograms
    fig2, axs2 = plt.subplots(3, 2, figsize=(18, 18))

    axs2[0, 0].hist2d(results[3][0][:, 0], results[3][0][:, 1], bins=50)
    axs2[0, 0].set_title('Actual Position (Circular Motion with Velocity Errors, No Odometry)')
    axs2[0, 0].set_xlabel('X Position')
    axs2[0, 0].set_ylabel('Y Position')

    axs2[0, 1].hist2d(results[3][1][:, 0], results[3][1][:, 1], bins=50)
    axs2[0, 1].set_title('Estimated Position (Circular Motion with Velocity Errors, Perfect Odometry)')
    axs2[0, 1].set_xlabel('X Position')
    axs2[0, 1].set_ylabel('Y Position')

    axs2[1, 0].hist2d(results[4][0][:, 0], results[4][0][:, 1], bins=50)
    axs2[1, 0].set_title('Actual Position (Circular Motion with Velocity Errors, Perfect Odometry)')
    axs2[1, 0].set_xlabel('X Position')
    axs2[1, 0].set_ylabel('Y Position')

    axs2[1, 1].hist2d(results[4][1][:, 0], results[4][1][:, 1], bins=50)
    axs2[1, 1].set_title('Estimated Position (Circular Motion with Velocity Errors, Perfect Odometry)')
    axs2[1, 1].set_xlabel('X Position')
    axs2[1, 1].set_ylabel('Y Position')

    axs2[2, 0].hist2d(results[5][0][:, 0], results[5][0][:, 1], bins=50)
    axs2[2, 0].set_title('Actual Position (Circular Motion with Velocity Errors, Noisy Odometry)')
    axs2[2, 0].set_xlabel('X Position')
    axs2[2, 0].set_ylabel('Y Position')

    axs2[2, 1].hist2d(results[5][1][:, 0], results[5][1][:, 1], bins=50)
    axs2[2, 1].set_title('Estimated Position (Circular Motion with Velocity Errors, Noisy Odometry)')
    axs2[2, 1].set_xlabel('X Position')
    axs2[2, 1].set_ylabel('Y Position')

    axs2[0, 0].set_ylabel('Y Position')
    axs2[1, 0].set_ylabel('Y Position')
    axs2[2, 0].set_ylabel('Y Position')

    plt2 = plt.gcf()
    plt.subplots_adjust(hspace=0.6, wspace=0.8)
    plt.show()

num_runs = 1000
results = simulate_robot(num_runs, VELOCITY, TIME_STEP, TOTAL_TIME, SIGMA_RIGHT, SIGMA_LEFT, SIGMA_O_RIGHT, SIGMA_O_LEFT)
plot_results(results)
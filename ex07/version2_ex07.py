import numpy as np
import matplotlib.pyplot as plt

# Constants
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
    delta_theta = (1 / B) * (vr - vl) * time_step
    return delta_x, delta_y, delta_theta

def odometry(vr, vl, theta, time_step):
    odo_dx = 0.5 * (vr + vl) * np.cos(theta) * time_step
    odo_dy = 0.5 * (vr + vl) * np.sin(theta) * time_step
    return odo_dx, odo_dy

def simulate_robot(num_runs, velocity, time_step, total_time, sigma_right, sigma_left, sigma_o_right, sigma_o_left):
    results = []
    cases = [
        {'name': 'no_errors', 'circular_path': False, 'v_noise': False, 'odom_noise': False},
        {'name': 'v_error_linear', 'circular_path': False, 'v_noise': True, 'odom_noise': False},
        {'name': 'v_error_circular', 'circular_path': True, 'v_noise': True, 'odom_noise': False},
        {'name': 'v_error_no_odom', 'circular_path': True, 'v_noise': True, 'odom_noise': False},
        {'name': 'v_error_perfect_odom', 'circular_path': True, 'v_noise': True, 'odom_noise': False},
        {'name': 'v_error_noisy_odom', 'circular_path': True, 'v_noise': True, 'odom_noise': True},
    ]

    for case in cases:
        positions = np.zeros((num_runs, 2))
        odometries = np.zeros((num_runs, 2))
        for i in range(num_runs):
            x, y, theta = 0, 0, 0
            odom_x, odom_y = 0, 0

            for t in np.arange(0, total_time, time_step):
                vr = velocity
                vl = velocity * (1 - B / RADIUS) if case['circular_path'] else velocity

                noisy_vr = vr + np.random.normal(0, sigma_right) if case['v_noise'] else vr
                noisy_vl = vl + np.random.normal(0, sigma_left) if case['v_noise'] else vl

                delta_x, delta_y, delta_theta = kinematic_model(noisy_vr, noisy_vl, theta, time_step)
                x += delta_x
                y += delta_y
                theta += delta_theta

                odom_vr = vr + np.random.normal(0, sigma_o_right) if case['odom_noise'] else vr
                odom_vl = vl + np.random.normal(0, sigma_o_left) if case['odom_noise'] else vl

                odo_dx, odo_dy = odometry(odom_vr, odom_vl, theta, time_step)
                odom_x += odo_dx
                odom_y += odo_dy

            positions[i] = [x, y]
            odometries[i] = [odom_x, odom_y]

        results.append((positions, odometries))

    return results

def plot_results(results, case_names):
    num_cases = len(results)
    fig, axs = plt.subplots(num_cases, 2, figsize=(12, 3 * num_cases))

    for i, result in enumerate(results):
        axs[i, 0].hist2d(result[0][:, 0], result[0][:, 1], bins=50, cmap='viridis')
        axs[i, 0].set_title(f'Actual Position - {case_names[i]}')

        axs[i, 1].hist2d(result[1][:, 0], result[1][:, 1], bins=50,  cmap='viridis')
        axs[i, 1].set_title(f'Estimated Position - {case_names[i]}')

    plt.tight_layout(pad=6.0)
    plt.show()

num_runs = 1000
results = simulate_robot(num_runs, VELOCITY, TIME_STEP, TOTAL_TIME, SIGMA_RIGHT, SIGMA_LEFT, SIGMA_O_RIGHT, SIGMA_O_LEFT)
case_names = ['no_errors', 'v_error_linear', 'v_error_circular', 'v_error_no_odom', 'v_error_perfect_odom', 'v_error_noisy_odom']
plot_results(results, case_names)

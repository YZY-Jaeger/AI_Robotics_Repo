import numpy as np
import matplotlib.pyplot as plt

## Free Parameters:
# k - learning rate
k = 0.3
# pi_x - inverse of the variance 
pi_zc = pi_zm = pi_wm = 1.0
# speed is a scaling factor
speed = 0.01

# Initial conditions
believe_ground = 0.0
believe_motor = 0.0
action = 0.0
# x - the number of units the robot will move
x = 0.0

# Inintialize all the necessary arrays
positions = np.zeros(6000)
free_energies = np.zeros(6000)
sensor_ground_values = np.zeros(6000)
believe_ground_values = np.zeros(6000)
sensor_motor_values = np.zeros(6000)
believe_motor_values = np.zeros(6000)

# Simulation
for t in range(6000):
    # Sensor readings
    # Gradient enviroment:
    # sensor_ground = 10 - x
    # Periodic enviroment:
    sensor_ground = np.cos(x) + 1.1 
    # Sensor reading is the underlying belief and some zero-mean Gaussian noise
    sensor_motor = believe_motor + np.random.normal(0, 1.0)

    # Compute free energy with the formula
    F = 0.5 * (pi_zc * (sensor_ground - believe_ground) ** 2 + pi_zm * (sensor_motor - believe_motor) ** 2 + pi_wm * (believe_motor - believe_ground) ** 2)

    # Update rules for belief (Perception Step)
    believe_ground_dot = -k * (pi_zc * (believe_ground - sensor_ground) + pi_wm * (believe_ground - believe_motor))
    believe_ground += believe_ground_dot
    believe_motor_dot = -k * (pi_zm * (believe_motor - sensor_motor) + pi_wm * (believe_motor - believe_ground))
    believe_motor += believe_motor_dot

    # Update rule for action (Action step)
    action_dot = -k * (pi_zm * (sensor_motor - believe_motor))
    action += action_dot

    # Move the robot x units in the world 
    x += speed * action

    # Save values
    positions[t] = x
    free_energies[t] = F
    sensor_ground_values[t] = sensor_ground
    believe_ground_values[t] = believe_ground
    sensor_motor_values[t] = sensor_motor
    believe_motor_values[t] = believe_motor

# Plotting
plt.figure(figsize=(12, 6))
plt.suptitle("Exercise 10.2 2nd part")

plt.subplot(2, 3, 1)
plt.plot(positions)
plt.title("Position in periodic enviroment")
plt.xlabel("Time step")
plt.ylabel("Position")

plt.subplot(2, 3, 2)
plt.plot(free_energies)
plt.title("Free Energy")
plt.xlabel("Time step")
plt.ylabel("Free Energy")

plt.subplot(2, 3, 3)
plt.plot(sensor_ground_values)
plt.title("Sensor reading of the ground")
plt.xlabel("Time step")
plt.ylabel("s_c")

plt.subplot(2, 3, 4)
plt.plot(believe_ground_values)
plt.title("Belief about the cause of ground sensing")
plt.xlabel("Time step")
plt.ylabel("µ_c")

plt.subplot(2, 3, 5)
plt.plot(sensor_motor_values)
plt.title("Sensor reading of the motor")
plt.xlabel("Time step")
plt.ylabel("s_m")

plt.subplot(2, 3, 6)
plt.plot(believe_motor_values)
plt.title("Belief about the cause of motor sensing")
plt.xlabel("Time step")
plt.ylabel("µ_m")

plt.tight_layout()
plt.show()
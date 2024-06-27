import random
from collections import defaultdict
from scipy.stats import beta

class Robot:
    def __init__(self, platform,action_noise=0.0,sensor_noise=0.0):
        self.platform = platform
        self.position = 0  # Start on the left side of the platform
        # Alpha is for 'black', Beta is for 'white'
        self.alpha = defaultdict(int, {i: 1 for i in range(len(platform))})  # Pseudo-counts
        self.beta = defaultdict(int, {i: 1 for i in range(len(platform))})  # Pseudo-counts
        self.noise_action =action_noise
        self.noise_sensor =sensor_noise

    def move(self, direction):
        intended_position = self.position + (1 if direction == 'right' else -1)
        if random.random() <= self.noise_action:  # Random noise affects the movement
            intended_position = self.position - (1 if direction == 'right' else -1)
        # Ensure the robot stays within bounds
        intended_position = max(0, min(intended_position, len(self.platform) - 1))
        self.position = intended_position
        self.update_histogram()

    def sensing_color(self):
        actual_color = self.platform[self.position]
        if random.random() <= self.noise_sensor:  # Noise in color sensing
            actual_color = 'white' if actual_color == 'black' else 'black'
        return actual_color

    def update_histogram(self):
        perceived_color = self.sensing_color()
        if perceived_color == 'black':
            self.alpha[self.position] += 1
        else:
            self.beta[self.position] += 1
        self.report_position()

    def report_position(self):
        print(f"The robot is on the {self.platform[self.position]} tile at position {self.position}.")
        print(f"Histogram for position {self.position}:")
        print(f"  Black: alpha = {self.alpha[self.position]}")
        print(f"  White: beta = {self.beta[self.position]}")

    def predict_color(self, position):
        if position < 0 or position >= len(self.platform):
            return 'unknown'
        # Use beta distribution to predict the most likely color
        prob_black = self.alpha[position] / (self.alpha[position] + self.beta[position])
        return 'black' if prob_black > 0.5 else 'white'

    def choose_action(self, strategy='cautious'):
        left_position = max(0, self.position - 1)
        right_position = min(len(self.platform) - 1, self.position + 1)

        # Calculate the predictive uncertainty
        delta_left = self.calculate_delta(left_position)
        delta_right = self.calculate_delta(right_position)

        if strategy == 'cautious':
            return 'left' if delta_left < delta_right else 'right'
        else:
            return 'left' if delta_left > delta_right else 'right'

    def calculate_delta(self, position):
        if position < 0 or position >= len(self.platform):
            return float('inf')  # High uncertainty for out-of-bounds positions
        a = self.alpha[position]
        b = self.beta[position]
        variance = beta.var(a, b)
        mean = beta.mean(a, b)
        last_measurement = 0 if self.platform[self.position] == 'white' else 1
        return variance * abs(last_measurement - mean)

    def simulate(self, steps, strategy='cautious',action_noise=0.0,sensor_noise=0.0):
        error = 0
        self.noise_action = action_noise
        self.noise_sensor = sensor_noise
        for _ in range(steps):
            print("\n------------------------------------")
            print("step: ", _)  
            action = self.choose_action(strategy)
            next_position = self.position - 1 if action == 'left' else self.position + 1
            predicted_color = self.predict_color(next_position)
            print(f"Predicted color for current position: {predicted_color}")

            self.move(action)

            actual_color = self.platform[self.position]
            if predicted_color != actual_color:
                print("The prediction was incorrect.")
                error += 1

        print(f"\nError: {error}  Steps: {steps}")
        print(f"Total error rate: {error / steps}")

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("Cautious strategy: with action noise=0.0 and sensor noise=0.0")
platform = ['white', 'black', 'white', 'white']
robot = Robot(platform)
robot.simulate(20, strategy='cautious',action_noise=0.0,sensor_noise=0.0) 
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("Adventurous strategy with action noise=0.0 and sensor noise=0.0:")
platform = ['white', 'black', 'white', 'white']
robot = Robot(platform)
robot.simulate(20, strategy='adventurous',action_noise=0.0,sensor_noise=0.0) 

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("Cautious strategy: with action noise=0.1 and sensor noise=0.1")
platform = ['white', 'black', 'white', 'white']
robot = Robot(platform)
robot.simulate(20, strategy='cautious',action_noise=0.1,sensor_noise=0.1) 
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("Adventurous strategy with action noise=0.1 and sensor noise=0.1:")
platform = ['white', 'black', 'white', 'white']
robot = Robot(platform)
robot.simulate(20, strategy='adventurous',action_noise=0.1,sensor_noise=0.1) 

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("Cautious strategy: with action noise=0.4 and sensor noise=0.4")
platform = ['white', 'black', 'white', 'white']
robot = Robot(platform)
robot.simulate(20, strategy='cautious',action_noise=0.4,sensor_noise=0.4) 
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("Adventurous strategy with action noise=0.4 and sensor noise=0.4:")
platform = ['white', 'black', 'white', 'white']
robot = Robot(platform)
robot.simulate(20, strategy='adventurous',action_noise=0.4,sensor_noise=0.4) 
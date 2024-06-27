import random
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

class Robot:
    def __init__(self, platform):
        self.platform = platform
        self.position = 0  # Start on the left side of the platform
        self.histograms = defaultdict(lambda: {'white': 1, 'black': 1})
        self.read_color = "default"
        self.positions = []
        self.errors = []

        
    def move_left(self):
        if self.position > 0 and random.random() > 0.1:
            self.position -= 1
        elif self.position < len(self.platform) - 1 and random.random() <= 0.1:
            self.position += 1
        self.update_histogram()

    def move_right(self):
        if self.position < len(self.platform) - 1 and random.random() > 0.1:
            self.position += 1
        elif self.position > 0 and random.random() <= 0.1:
            self.position -= 1
        self.update_histogram()

    def update_histogram(self):
        perceived_color = self.sensing_color()
        self.histograms[self.position][perceived_color] += 1
        self.report_position()

    def sensing_color(self, noise=0.1):
        perceived_color = self.platform[self.position]
        if random.random() <= noise:
            perceived_color = 'white' if perceived_color == 'black' else 'black'
        self.read_color = perceived_color
        return perceived_color

    def report_position(self):
        print(f"The robot is on the {self.platform[self.position]} tile at position {self.position}.")
        self.positions.append(self.position)
        self.print_histogram(self.position)
        self.print_platform()

    def print_histogram(self, position):
        histogram = self.histograms[position]
        print(f"Histogram for position {position}:")
        for color, count in histogram.items():
            print(f"  {color}: {count}")

    def print_platform(self):
        position_representation = [' ']*len(self.platform)
        position_representation[self.position] = 'ROB'
        
        platform_representation = ' | '.join([f' {p} ' for p in self.platform])
        robot_representation = ' | '.join([f'{r:^3}' for r in position_representation])
        
        print(f"|{robot_representation}|")
        print(f"|{platform_representation}|")

    def predict_color(self, position):
        if position < 0 or position >= len(self.platform):
            return 'unknown'
        histogram = self.histograms[position]
        total = histogram['white'] + histogram['black']
        probability_white = histogram['white'] / total
        probability_black = histogram['black'] / total
        return 'white' if probability_white > probability_black else 'black'

    def choose_action_cautious(self):
        left_position = self.position - 1
        right_position = self.position + 1

        delta_left = self.calculate_delta(left_position)
        delta_right = self.calculate_delta(right_position)

        if delta_left < delta_right:
            return 'left'
        elif delta_right < delta_left:
            return 'right'
        else:
            return random.choice(['left', 'right'])

    def choose_action_adventurous(self):
        left_position = self.position - 1
        right_position = self.position + 1

        delta_left = self.calculate_delta(left_position)
        delta_right = self.calculate_delta(right_position)

        if delta_left > delta_right:
            return 'left'
        elif delta_right > delta_left:
            return 'right'
        else:
            return random.choice(['left', 'right'])

    def calculate_delta(self, position):
        if position < 0:
            position = 0
        elif position >= len(self.platform):
            position = len(self.platform) - 1
            
        histogram = self.histograms[position]
        total = histogram['white'] + histogram['black']
        p_white = histogram['white'] / total
        p_black = histogram['black'] / total
        mean = p_white  # Mean is the probability of observing white
        variance = (p_white * (1 - p_white)) / (total + 1)  # Variance for binomial distribution
        color = 0 if self.read_color == 'white' else 1
        return variance*(color - mean)

    def simulate(self, steps, strategy='cautious'):
        error = 0
        self.errors = []
        self.sensing_color()
        for _ in range(steps):
            print("\n------------------------------------")

            if strategy == 'cautious':
                action = self.choose_action_cautious()
            else:
                action = self.choose_action_adventurous()

            next_position = self.position - 1 if action == 'left' else self.position + 1
            predicted_color = self.predict_color(next_position)
            print(f"Predicted color for position {next_position}: {predicted_color}")

            if action == 'left':
                self.move_left()
            else:
                self.move_right()

            if next_position < 0 or next_position >= len(self.platform):
                print("Prediction was for out-of-bounds position.")
                continue

            if predicted_color != self.platform[self.position]:
                print("The prediction was incorrect.")
                error += 1

            self.errors.append(error / (len(self.positions) + 1))

        print(f"\nError: {error}  Steps: {steps}")
        print(f"Total error rate: {error / steps}")
        return error / steps
    
# Test the Robot class with a platform of more than two tiles
platform = ['white', 'black', 'white', 'white']
robot = Robot(platform)
# Simulate for cautious robot
cautious_error_rate = robot.simulate(20, strategy='cautious')
cautious_positions = robot.positions
cautious_errors = robot.errors

# Reset for adventurous robot
robot = Robot(platform)

# Simulate for adventurous robot
adventurous_error_rate = robot.simulate(20, strategy='adventurous')
adventurous_positions = robot.positions
adventurous_errors = robot.errors

# Plot the positions over time
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(cautious_positions, label='Cautious Robot')
plt.plot(adventurous_positions, label='Adventurous Robot', linestyle='--')
plt.title('Robot Positions Over Time')
plt.xticks(range(21))
plt.xlabel('Time Steps')
plt.ylabel('Position')
plt.legend()

# Plot the error rates over time
plt.subplot(2, 1, 2)
plt.plot(cautious_errors, label='Cautious Robot')
plt.plot(adventurous_errors, label='Adventurous Robot', linestyle='--')
plt.title('Error Rates Over Time')
plt.xticks(range(21))
plt.xlabel('Time Steps')
plt.ylabel('Error Rate')
plt.legend()

plt.tight_layout()
plt.show()

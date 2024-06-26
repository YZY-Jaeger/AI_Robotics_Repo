import random
from collections import defaultdict
import numpy as np

class Robot:
    def __init__(self, platform):
        self.platform = platform
        self.position = 0  # Start on the left side of the platform
        self.histograms = defaultdict(lambda: {'white': 1, 'black': 1})

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
        perceived_color = self.platform[self.position]
        if random.random() <= 0.1:
            perceived_color = 'white' if perceived_color == 'black' else 'black'
        self.histograms[self.position][perceived_color] += 1
        self.report_position()

    def report_position(self):
        print(f"The robot is on the {self.platform[self.position]} tile at position {self.position}.")
        self.print_histogram(self.position)

    def print_histogram(self, position):
        histogram = self.histograms[position]
        print(f"Histogram for position {position}:")
        for color, count in histogram.items():
            print(f"  {color}: {count}")

    def predict_color(self, position):
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
        if position < 0 or position >= len(self.platform):
            return float('inf')
        histogram = self.histograms[position]
        total = histogram['white'] + histogram['black']
        p_white = histogram['white'] / total
        p_black = histogram['black'] / total
        mean = p_white  # Mean is the probability of observing white
        variance = (p_white * (1 - p_white)) / (total + 1)  # Variance for binomial distribution
        return mean + variance

    def simulate(self, steps, strategy='cautious'):
        error = 0
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

            if predicted_color != self.platform[self.position]:
                print("The prediction was incorrect.")
                error += 1

        print(f"\nError: {error}  Steps: {steps}")
        print(f"Total error rate: {error / steps}")

# Test the Robot class with a platform of more than two tiles
platform = ['white', 'black', 'white', 'white']
robot = Robot(platform)
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("Cautious Robot Simulation")
robot.simulate(20, strategy='cautious')

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("\nAdventurous Robot Simulation")
robot.simulate(20, strategy='adventurous')


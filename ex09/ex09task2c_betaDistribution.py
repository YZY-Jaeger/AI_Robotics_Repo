import random
from collections import defaultdict

class Robot:
    def __init__(self, platform):
        self.platform = platform
        self.position = 0  # Start on the left side of the platform
        self.alpha = defaultdict(lambda: {'white': 1, 'black': 1})
        self.beta = defaultdict(lambda: {'white': 1, 'black': 1})

    def move_left(self):
        if random.random() <= self.noise_prob:  # Noise in execution
            self.move_right()  # Move in the opposite direction
        else:
            if self.position > 0:
                self.position -= 1
            self.update_histogram()

    def move_right(self):
        if random.random() <= self.noise_prob:  # Noise in execution
            self.move_left()  # Move in the opposite direction
        else:
            if self.position < len(self.platform) - 1:
                self.position += 1
            self.update_histogram()

    def update_histogram(self):
        # Noise in perception
        perceived_color = self.platform[self.position]
        if random.random() <= self.noise_prob:
            perceived_color = 'white' if perceived_color == 'black' else 'black'

        if perceived_color == 'white':
            self.beta[self.position]['white'] += 1
        else:
            self.alpha[self.position]['black'] += 1
        
        self.report_position()

    def report_position(self):
        print(f"The robot is on the {self.platform[self.position]} tile at position {self.position}.")
        self.print_histogram(self.position)

    def print_histogram(self, position):
        alpha_histogram = self.alpha[position]
        beta_histogram = self.beta[position]
        print(f"Histogram for position {position}:")
        for color in alpha_histogram:
            print(f"  {color}: alpha = {alpha_histogram[color]}, beta = {beta_histogram[color]}")

    def predict_color(self, position):
        alpha_histogram = self.alpha[position]
        beta_histogram = self.beta[position]
        total_white = alpha_histogram['white'] + beta_histogram['white']
        total_black = alpha_histogram['black'] + beta_histogram['black']
        probability_white = alpha_histogram['white'] / total_white
        probability_black = alpha_histogram['black'] / total_black
        return 'white' if probability_white > probability_black else 'black'

    def beta_mean_variance(self, position):
        alpha_histogram = self.alpha[position]
        beta_histogram = self.beta[position]
        mean_white = alpha_histogram['white'] / (alpha_histogram['white'] + beta_histogram['white'])
        variance_white = (alpha_histogram['white'] * beta_histogram['white']) / ((alpha_histogram['white'] + beta_histogram['white'])**2 * (alpha_histogram['white'] + beta_histogram['white'] + 1))
        mean_black = alpha_histogram['black'] / (alpha_histogram['black'] + beta_histogram['black'])
        variance_black = (alpha_histogram['black'] * beta_histogram['black']) / ((alpha_histogram['black'] + beta_histogram['black'])**2 * (alpha_histogram['black'] + beta_histogram['black'] + 1))
        return mean_white, variance_white, mean_black, variance_black

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
        mean_white, variance_white, mean_black, variance_black = self.beta_mean_variance(position)
        return min(variance_white, variance_black)

    def simulate(self, steps, strategy='cautious', noise_prob=0):
        self.noise_prob = noise_prob
        error = 0
        for _ in range(steps):
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

print("Cautious Robot Simulation - No Noise")
robot.simulate(20, strategy='cautious', noise_prob=0)

print("\n------------------------------------")


print("\nCautious Robot Simulation - 10% Noise")
robot.simulate(20, strategy='cautious', noise_prob=0.1)

print("\n------------------------------------")


print("\nCautious Robot Simulation - 40% Noise")
robot.simulate(20, strategy='cautious', noise_prob=0.4)

print("\n------------------------------------")


print("\nAdventurous Robot Simulation - No Noise")
robot.simulate(20, strategy='adventurous', noise_prob=0)

print("\n------------------------------------")


print("\nAdventurous Robot Simulation - 10% Noise")
robot.simulate(20, strategy='adventurous', noise_prob=0.1)

print("\n------------------------------------")


print("\nAdventurous Robot Simulation - 40% Noise")
robot.simulate(20, strategy='adventurous', noise_prob=0.4)

print("\n------------------------------------")


import random
from collections import defaultdict
from scipy.stats import beta

class Robot:
    def __init__(self, platform):
        self.platform = platform
        self.position = 0  # Start on the left side of the platform
        self.alpha = defaultdict(lambda: {'white': 1, 'black': 1})
        self.beta = defaultdict(lambda: {'white': 1, 'black': 1})
        self.read_color = "default"
        self.noise_prob = 0

    def move_left(self,noise=0.1):
        randnum = 1
        if self.position > 0 and randnum > noise:
            self.position -= 1
        elif self.position < len(self.platform) - 1 and randnum <= noise:
            self.position += 1
        else:
            self.position = max(0, self.position) 
        self.update_histogram()

    def move_right(self,noise=0.1):
        randnum = 1
        if self.position < len(self.platform) - 1 and randnum > noise:
            self.position += 1
        elif self.position > 0 and randnum <= noise:
            self.position -= 1
        else:
            self.position = min(len(self.platform) - 1, self.position)
        self.update_histogram()

    def sensing_color(self, noise=0.1):
        perceived_color = self.platform[self.position]
        if random.random() <= noise:
            perceived_color = 'white' if perceived_color == 'black' else 'black'
        self.read_color = perceived_color
        return perceived_color

    def update_histogram(self):
        # Noise in perception
        perceived_color = self.sensing_color()

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
        
        mean_white = beta.mean(alpha_histogram['white'], beta_histogram['white'])
        mean_black = beta.mean(alpha_histogram['black'], beta_histogram['black'])
        
        return 'white' if mean_white > mean_black else 'black'

    def beta_mean_variance(self, position):

        
        a = self.alpha[position]['black']
        b = self.beta[position]['black']
        mean = beta.mean(a, b)
        variance = beta.var(a, b)
        
        last_measurement = 0 if self.read_color == 'white' else 1  # Assuming last color read affects decision
        
        return variance * abs(last_measurement - mean)

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
            return 0
        elif position >= len(self.platform):
            return 0

        #mean_white, variance_white, mean_black, variance_black = self.beta_mean_variance(position)
        color = 0 if self.read_color == 'white' else 1
        return self.beta_mean_variance(position)

    def simulate(self, steps, strategy='cautious', noise_prob=0):
        self.noise_prob = noise_prob
        error = 0
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

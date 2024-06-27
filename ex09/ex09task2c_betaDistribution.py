import random
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from scipy.stats import beta as beta_dist

class Robot:
    def __init__(self, platform, action_noise=0.0, sensor_noise=0.0):
        self.platform = platform
        self.position = 0  
        # Alpha is for 'black', Beta is for 'white'
        self.alpha = defaultdict(int, {i: 1 for i in range(len(platform))})  
        self.beta = defaultdict(int, {i: 1 for i in range(len(platform))})  
        self.noise_action = action_noise
        self.noise_sensor = sensor_noise
        self.visit_count = defaultdict(int) 

    def move(self, direction):
        intended_position = self.position + (1 if direction == 'right' else -1)
        if random.random() <= self.noise_action:  # Random noise affects the movement
            intended_position = self.position - (1 if direction == 'right' else -1)
        intended_position = max(0, min(intended_position, len(self.platform) - 1))
        self.position = intended_position
        self.update_histogram()
        self.visit_count[self.position] += 1  

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

    def predict_color(self, position):
        if position < 0 or position >= len(self.platform):
            return 'unknown'
        #beta distribution to predict the most likely color
        prob_black = self.alpha[position] / (self.alpha[position] + self.beta[position])
        return 'black' if prob_black > 0.5 else 'white'

    def choose_action(self, strategy='cautious'):
        left_position = max(0, self.position - 1)
        right_position = min(len(self.platform) - 1, self.position + 1)

        delta_left = self.calculate_delta(left_position)
        delta_right = self.calculate_delta(right_position)

        if strategy == 'cautious':
            action = 'left' if delta_left < delta_right else 'right'
        else:
            action = 'left' if delta_left > delta_right else 'right'

        return action

    def calculate_delta(self, position):
        if position < 0 or position >= len(self.platform):
            return float('inf')  
        a = self.alpha[position]
        b = self.beta[position]
        variance = beta_dist.var(a, b)
        mean = beta_dist.mean(a, b)
        last_measurement = 0 if self.platform[self.position] == 'white' else 1
        return variance * abs(last_measurement - mean)

    def simulate(self, steps, strategy='cautious'):
        all_positions = []
        all_errors = []
        for step in range(steps):
            action = self.choose_action(strategy)
            self.move(action)
            all_positions.append(self.position)

            actual_color = self.platform[self.position]
            predicted_color = self.predict_color(self.position)
            error = 1 if predicted_color != actual_color else 0
            all_errors.append(error)

            print("------------------------------------")
            print(f"Step {step + 1}")
            print(f"Current position: {self.position}, Predicted color: {predicted_color}, Actual color: {actual_color}")
            if predicted_color != actual_color:
                print("Prediction was incorrect!")
            else:
                print("Prediction was correct.")
            print(f"The robot is on the {actual_color} tile at position {self.position}.")
            print(f"Histogram for position {self.position}:")
            print(f"  Black: alpha = {self.alpha[self.position]}")
            print(f"  White: beta = {self.beta[self.position]}")
            print("------------------------------------")

        return all_positions, all_errors

def plot_beta_and_visit_patterns(alpha, beta, visit_counts, platform, title, ax1, ax2):
    visited_positions = [pos for pos in range(len(alpha)) if visit_counts[pos] > 0]
    x = np.linspace(0, 1, 100)
    
    for pos in visited_positions:
        a = alpha[pos]
        b = beta[pos]
        y = beta_dist.pdf(x, a, b)
        ax1.plot(x, y, label=f'Position {pos} (α={a}, β={b})')

    ax1.set_xlabel('Probability')
    ax1.set_ylabel('Density')
    ax1.set_title(title)
    ax1.legend(loc='upper right')
    ax1.grid(True)

    colors = ['black' if platform[pos] == 'black' else 'lightgrey' for pos in range(len(platform))]
    ax2.bar(range(len(visit_counts)), visit_counts, align='center', color=colors)
    ax2.set_xlabel('Position')
    ax2.set_ylabel('Visit Count')
    ax2.set_title('Visitation Pattern')
    ax2.set_xticks(range(len(visit_counts)))
    ax2.grid(True, axis='y')

def compare_strategies(platform, steps, noise_levels):
    strategies = ['cautious', 'adventurous']
    
    for strategy in strategies:
        print(f"Running simulation for {strategy.capitalize()} strategy...")
        fig, axs = plt.subplots(len(noise_levels), 2, figsize=(15, 7 * len(noise_levels)))
        fig.suptitle(f'{strategy.capitalize()} Strategy: Beta Distributions and Visitation Patterns')

        for i, noise_level in enumerate(noise_levels):
            print(f"Simulating with noise level: {noise_level}")
            robot = Robot(platform, action_noise=noise_level, sensor_noise=noise_level)
            positions, errors = robot.simulate(steps, strategy=strategy)
            alpha, beta = robot.alpha, robot.beta
            visit_counts = [robot.visit_count[pos] for pos in range(len(platform))]
            
            plot_beta_and_visit_patterns(alpha, beta, visit_counts, platform, f"Noise Level: {int(noise_level*100)}%", axs[i, 0], axs[i, 1])
            axs[i, 0].legend(loc='upper right', bbox_to_anchor=(-0.1, 1))

        plt.subplots_adjust(left=0.2, right=0.9, bottom=0.1, top=0.9, hspace=0.6, wspace=0.3)
        plt.show()

platform = ['white', 'black', 'white', 'white']
steps = 20
noise_levels = [0.0, 0.1, 0.4]

compare_strategies(platform, steps, noise_levels)

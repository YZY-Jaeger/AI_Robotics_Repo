import random
from collections import defaultdict
import matplotlib.pyplot as plt

class Robot:
    def __init__(self, platform):
        self.platform = platform
        self.position = 0 
        self.histograms = defaultdict(lambda: {'white': 1, 'black': 1})
        self.positions = []
        self.errors = []

    def move_left(self):
        if self.position > 0:
            self.position -= 1
        self.update_histogram()

    def move_right(self):
        if self.position < len(self.platform) - 1:
            self.position += 1
        self.update_histogram()

    def update_histogram(self):
        self.histograms[self.position][self.platform[self.position]] += 1
        self.report_position()

    def report_position(self):
        print(f"The robot is on the {self.platform[self.position]} tile at position {self.position}.")
        self.positions.append(self.position)
        self.print_histogram(self.position)

    def print_histogram(self, position):
        histogram = self.histograms[position]
        print(f"Histogram for position {position}:")
        for color, count in histogram.items():
            print(f"  {color}: {count}")

    def sensing_color(self, noise=0.1):
        perceived_color = self.platform[self.position]
        if random.random() <= noise:
            perceived_color = 'white' if perceived_color == 'black' else 'black'
        self.read_color = perceived_color
        return perceived_color

    def predict_color(self, position):
        histogram = self.histograms[position]
        total = histogram['white'] + histogram['black']
        probability_white = histogram['white'] / total
        probability_black = histogram['black'] / total
        return 'white' if probability_white > probability_black else 'black'

    def choose_action(self):
        if self.position == 0:
            return 'right'
        elif self.position == len(self.platform) - 1:
            return 'left'
        else:
            return random.choice(['left', 'right'])

    def simulate(self, steps):
        error = 0
        for _ in range(steps):
            action = self.choose_action()
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
            self.errors.append(error / (len(self.positions) + 1))
        print(f"\nerror: {error}  step: {steps}")
        print(f"Total error rate: {error / steps}")
        return error / steps

# Test the Robot class with a platform of more than two tiles
platform = ['white', 'black', 'white', 'white']
robot = Robot(platform)

error_rates = robot.simulate(20)
positions = robot.positions
errors = robot.errors
print("\n------------------------------------")
print("\nFinal histograms:")
for position in range(len(platform)):
    robot.print_histogram(position)

plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(positions, label='Robot')
plt.title('Robot Positions Over Time')
plt.xticks(range(len(positions)))
plt.xlabel('Time Steps')
plt.ylabel('Position')

plt.subplot(3, 1, 2)
plt.plot(errors, label='Robot')
plt.title('Error Rate Over Time')
plt.xticks(range(len(errors)))
plt.xlabel('Time Steps')
plt.ylabel('Error Rate')

colors = {'white': 'lightgrey', 'black': 'black'}
for i in range(len(platform)):
    plt.subplot(3, len(platform), len(platform)*2 + i + 1)
    color_list = [colors[c] for c in robot.histograms[i].keys()]
    plt.bar(robot.histograms[i].keys(), robot.histograms[i].values(), color=color_list, edgecolor='black')
    plt.title(f'Position {i} Histogram')
    plt.xlabel('Color')
    plt.ylabel('Count')

plt.tight_layout()
plt.show()

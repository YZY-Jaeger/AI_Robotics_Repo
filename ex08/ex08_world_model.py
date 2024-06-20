import numpy as np
import matplotlib.pyplot as plt
from rosbags.rosbag2 import Reader
from rosbags.typesys import Stores, get_typestore

# Create a typestore and get the string class.
typestore = get_typestore(Stores.LATEST)

def extract_lidar_data(bag_path):
    lidar_data = []
    with Reader(bag_path) as reader:
        connections = [x for x in reader.connections if x.topic == '/scan']
        for connection, timestamp, rawdata in reader.messages(connections=connections):
            msg = typestore.deserialize_cdr(rawdata, connection.msgtype)
            #get the data from the LiDAR: 
            # ranges: A list or array of distance measurements.
            #angle_min: The starting angle of the LiDAR scan.
            #angle_max: The ending angle of the LiDAR scan.
            #angle_increment: The angular distance between measurements.
            return msg.ranges, msg.angle_min, msg.angle_max, msg.angle_increment

# Convert polar coordinates to Cartesian coordinates 
def polar_to_cartesian(ranges, angle_min, angle_increment):
    points = []
    #iterate over each range measurement:
    for i, r in enumerate(ranges):
        #Check if the range measurement is valid:
        if r < float('inf'):
            angle = angle_min + i * angle_increment
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            points.append(np.array([x, y]))
    return np.array(points)

# Calculate distance from a point to a line for the split-and-merge algorithm 
# so we can use it to find the max_distance of a point which will be out splitting point (p')
def point_distance_to_line(point, line_start, line_end):
    if np.all(line_start == line_end):
        return np.linalg.norm(point - line_start)
    else:
        return np.linalg.norm(np.cross(line_end - line_start, line_start - point)) / np.linalg.norm(line_end - line_start)

# Split-and-Merge algorithm
def split_and_merge_algorithm(points, threshold):
    if len(points) < 2:
        return [points]

    line_start, line_end = points[0], points[-1]
    distances = [point_distance_to_line(p, line_start, line_end) for p in points]
    max_distance = max(distances)
    max_index = distances.index(max_distance)
    #if max_distance is below the threshold we terminate the algorithm
    if max_distance < threshold:
        return [points]
    else:
        #else we split the point set by the max_distance point (p')
        #and do a recursion for both subsets
        left_points = split_and_merge_algorithm(points[:max_index+1], threshold)
        right_points = split_and_merge_algorithm(points[max_index:], threshold)
        return left_points + right_points

def main():
    ranges, angle_min, angle_max, angle_increment = extract_lidar_data('ex08')
    cartesian_points = polar_to_cartesian(ranges, angle_min, angle_increment)

    threshold = 0.5 
    segments = split_and_merge_algorithm(cartesian_points, threshold)

    plt.figure(figsize=(8, 6))
    plt.scatter(cartesian_points[:, 0], cartesian_points[:, 1], c='black', marker='o', s=15, label='LiDAR Points')
    plt.legend()

    for segment in segments:
        segment = np.array(segment)
        plt.plot(segment[:, 0], segment[:, 1])

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Line map from LiDAR data using Split-and-Merge algorithm')
    plt.gca().invert_yaxis()  # This line flips the y-axis
    plt.gca().invert_xaxis()  # This line flips the x-axis
    plt.show()

# Run the main process
if __name__ == "__main__":
    main()

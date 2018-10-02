import csv
import datetime

path = "../Dataset/Sample/Sample_6/53/"
filename = "HandPhoneGyrUser53S1.csv"
filename_checkpoint = "HandPhoneCheckpointsUser53S1.csv"
door_entry_checkpoints = []
door_exit_checkpoints = []
stair_entry_checkpoints = []
stair_exit_checkpoints = []
center_points = []
entries = {}
window_size = 6  # In seconds


def convert_string_to_time(time_in_str):
    return datetime.datetime.strptime(time_in_str, '%Y-%m-%d %H:%M:%S.%f')


def calculate_center_point(entry_time, exit_time):
    return datetime.datetime.fromtimestamp((entry_time.timestamp() + exit_time.timestamp()) / 2)


with open(path + filename_checkpoint) as input_file:
    next(input_file)  # Skip the first line
    read_input = csv.reader(input_file, delimiter=',')
    for row in read_input:
        checkpoint_time = convert_string_to_time(row[2])
        if row[1] == "DoorEntry":
            door_entry_checkpoints.append(checkpoint_time)
        elif row[1] == "DoorExit":
            door_exit_checkpoints.append(checkpoint_time)
        elif row[1] == "StairEntry":
            stair_entry_checkpoints.append(checkpoint_time)
        elif row[1] == "StairExit":
            stair_exit_checkpoints.append(checkpoint_time)

for i in range(len(door_entry_checkpoints)):
    center_points.append(calculate_center_point(door_entry_checkpoints[i], door_exit_checkpoints[i]))


with open(path + filename) as input_file:
    next(input_file)  # Skip the first line
    read_input = csv.reader(input_file, delimiter=',')
    for row in read_input:
        time = convert_string_to_time(row[4])
        for i in range(len(center_points)):
            if (center_points[i] - datetime.timedelta(seconds=window_size)) <= time <= \
                    (center_points[i] + datetime.timedelta(seconds=window_size)):
                if entries.get(i + 1) is None:
                    entries[i + 1] = []
                entries[i + 1].append([row[1], row[2], row[3], row[4]])

# Code to put the results into CSV
# counter = 1
# for d in entries:
#     with open("../Dataset/Sample/Sample_6_small/53/HandPhoneGyrUser53S1_door" + str(counter) + ".csv", "w+") as o_file:
#         csv.writer(o_file).writerows(entries.get(counter))
#         counter += 1


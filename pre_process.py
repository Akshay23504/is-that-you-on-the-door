import csv
import datetime
import pandas as pd


def convert_string_to_time(time_in_str):
    """
    As the name says, converts 'time_in_str' from the string format to python
    datetime format. Reason: Using the datetime object, we can add, subtract
    and play freely with time.

    :param time_in_str: String format of time to be converted to datetime
    :return: The datetime format of the parameter

    """

    return datetime.datetime.strptime(time_in_str, '%Y-%m-%d %H:%M:%S.%f')


def convert_epoch_to_datetime(time_in_epoch):
    """
    As the name says, converts 'time_in_epoch' from the epoch format to python
    datetime format. Reason: Using the datetime object, we can add, subtract
    and play freely with time.

    :param time_in_epoch: Floating epoch variable
    :return: The datetime format of the parameter

    """

    return datetime.datetime.fromtimestamp(time_in_epoch / 1000)  # 1000 is for milliseconds


class PreProcess:
    """
    This class contains all the ingredients for pre-processing. From the initial
    step soon after the raw data is obtained, this class takes care of all the
    things that are necessary for the raw data to nourish and look pretty.

    All the pre-processing steps defined here can be run from the
    feature_extraction file or can also be run stand-alone. To run in
    stand-alone mode, uncomment the last couple of lines in this file. But,
    there is no need to run this file alone.

    """

    def __init__(self):
        """
        Initialization stuff. Different sensors, devices and users need to be
        configured here. And also the file names, file checkpoints and window
        size. In addition, there are also some dictionaries and lists
        initialized which are required for pre-processing.

        Once, the parameters like the sensor and user are set, just
        run the file and it should achieve the outcome. There is no need to
        touch other parts of the code.

        """

        self.user_id = "998"  # User id
        self.sensor_name = "gyroscope"  # accelerometer or gyroscope
        self.path = "../Dataset/Sample/watchtrial/" + self.user_id + "/"  # File path
        self.filename = self.user_id + "_" + self.sensor_name + ".xlsx"  # Filename
        self.filename_checkpoint = "Events" + self.user_id + ".txt"
        self.door_open_checkpoints = {}
        self.entries = {}
        self.window_size = 3  # In seconds
        self.door_instance_dimension = {}

    def store_checkpoints(self):
        """
        Just storing the checkpoints in a list here. There is also some extent
        of cleaning done.

        """

        # Open the checkpoint file
        with open(self.path + self.filename_checkpoint) as input_file:
            read_input = csv.reader(input_file, delimiter=',')
            door_counter = 1
            for row in read_input:
                if row[0] == 'door open':
                    if self.door_open_checkpoints.get(door_counter) is None:
                        self.door_open_checkpoints[door_counter] = []
                        # Convert the timestamp to datetime and store in a list
                    self.door_open_checkpoints[door_counter].append(convert_epoch_to_datetime(float(row[1])))
                if row[0] == 'event1':  # Just making sure we consider only the events
                    door_counter += 1

    def store_door_opening_instances(self):
        """
        Get the raw data values from the excel file. Note that the values from
        data frame is considered which is numpy array. Some additional
        pre-processing is also done.

        Then comes the core part. The data from the checkpoint instance to a
        certain window size (3 seconds) is considered. Because the sensors from
        the smartwatch continuously record the values, we only need 3 second of
        the data for every instance.

        The code in this method is not really optimized for time complexity!
        Pfff
        Maybe there is a better way...hmmm...

        """

        input_file = pd.ExcelFile(self.path + self.filename).parse('Sheet1').get_values()  # Sheet 1 only
        for row in input_file:
            time = convert_epoch_to_datetime(float(row[4]))
            for i in range(len(self.door_open_checkpoints)):
                for j in range(len(self.door_open_checkpoints[i + 1])):  # Ewwww....3 loops
                    if (self.door_open_checkpoints[i + 1][j] - datetime.timedelta(seconds=self.window_size)) \
                            <= time <= \
                            (self.door_open_checkpoints[i + 1][j] + datetime.timedelta(seconds=self.window_size)):
                        if self.entries.get(i + 1) is None:
                            self.entries[i + 1] = {}
                            self.entries[i + 1][j] = []
                        if self.entries.get(i + 1).get(j) is None:
                            self.entries.get(i + 1)[j] = []
                        self.entries[i + 1][j].append([j, row[1], row[2], row[3], row[4]])

    def get_door_opening_instances(self):
        """
        All the data is in the entries dictionary. But, sometimes, we need the
        data to be in a different format. Here, the format is, we need separate
        x, y and z values. Reason: We can extract features from this, if we
        have x, y and z as separate columns.

        door_instance_dimension is for each door, for each instance, there are
        x, y and z values

        Example: door_instance_dimension[1][1]['x'] = -0.005
        Door 1, instance 1, x value

        """

        for k, v in self.entries.items():
            if self.door_instance_dimension.get(k) is None:
                # Create empty dictionaries for each instance
                self.door_instance_dimension[k] = {}
            for ks, vs in self.entries.get(k).items():
                if self.door_instance_dimension.get(k).get(ks) is None:
                    self.door_instance_dimension[k][ks] = {}
                    # Create empty lists for each dimension
                    self.door_instance_dimension[k][ks]['x'] = []
                    self.door_instance_dimension[k][ks]['y'] = []
                    self.door_instance_dimension[k][ks]['z'] = []
                for vss in self.entries.get(k).get(ks):
                    self.door_instance_dimension[k][ks]['x'].append(vss[1])
                    self.door_instance_dimension[k][ks]['y'].append(vss[2])
                    self.door_instance_dimension[k][ks]['z'].append(vss[3])

    def write_entries_to_file(self):
        """
        This method is used to write the entries (the big dictionary) to a file,
        so that it can be used for later easy retrieval.

        """

        # Code to put the results (entries) into CSV
        for entry in self.entries:
            with open(self.path + self.user_id + "_" + self.sensor_name + "_door" + str(entry) + ".csv", "w+") as o_file:
                for e in self.entries[entry]:
                    csv.writer(o_file).writerows(self.entries[entry][e])

    def get_door_instance_dimension(self):
        """
        Just a getter method

        :return: fall_instance_dimension

        """

        return self.door_instance_dimension


# Uncomment the below lines if this file needs to be run separately
# pre_process = PreProcess()
#
# pre_process.store_checkpoints()
# pre_process.store_door_opening_instances()
# pre_process.write_entries_to_file()
# pre_process.get_door_opening_instances()


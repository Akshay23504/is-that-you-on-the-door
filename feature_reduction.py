import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class FeatureReduction:
    """
    This class is used after feature extraction and selection. The dataset
    begins with 36 features (columns). The methods (correlation)
    explained in this class reduce these 36 features to
    around 10-18 features. This reduction is a manual process and we have to
    analyze and identify the features to remove based on the results obtained
    from the reduction techniques described here.

    """

    def __init__(self):
        """
        As usual, lot of initialization stuff here.
        Filenames and directory names vary on the problem (door 1 or door 2)

        """

        # Refer to this link for why 0.6 was chosen as the threshold
        # https://www.researchgate.net/post/What_is_the_minimum_value_of_correlation_coefficient_to_prove_the_existence_of_the_accepted_relationship_between_scores_of_two_of_more_tests
        self.threshold = 0.6
        self.features_data_frame = pd.DataFrame()  # Initialize panda data frames
        self.user_id = "995"  # Not needed here
        self.sensor_name = "gyroscope"  # gyroscope or accelerometer
        self.door_number = str(2)  # 1 or 2
        self.path = "../Dataset/Sample/watchtrial/"
        self.filename = "door_" + self.door_number + "_" + self.sensor_name + ".xlsx"

    def correlation(self):
        """
        Perform correlation between every pair of features. For example,
        feature 1 is compared with all the other 35 features. Feature 2
        is compared with all the other 34 features and so on. The
        correlation gives a matrix of 36 x 36 dimensions. The diagonal values
        are 1.0.

        """

        # We can also do a zip and check...but ehhh
        column_correlation = set()
        # Just call corr(). Cannot get easier than this!
        correlation_matrix = self.features_data_frame.corr()
        plt.figure(figsize=(10, 10))
        plt.pcolor(correlation_matrix, edgecolors='k', cmap='hot')
        plt.xticks(np.arange(0.5, len(correlation_matrix.columns), 1), correlation_matrix.columns, rotation=90)
        plt.yticks(np.arange(0.5, len(correlation_matrix.index), 1), correlation_matrix.index)
        # Uncomment this for the heat map
        # plt.show()
        for i in range(len(correlation_matrix.columns)):
            for j in range(i):
                if correlation_matrix.iloc[i, j] >= self.threshold:
                    column_to_remove = correlation_matrix.columns[i]
                    column_correlation.add(column_to_remove)
        print(len(column_correlation))
        print(column_correlation)

    def get_the_features(self):
        """
        Get the data from the excel files using panda data frames.

        """

        self.features_data_frame = pd.ExcelFile(self.path + self.filename).parse('Sheet1')  # Sheet 1 only
        self.correlation()


feature_reduction = FeatureReduction()
feature_reduction.get_the_features()

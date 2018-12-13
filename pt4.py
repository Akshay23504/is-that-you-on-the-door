import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class FeatureReduction:
    def __init__(self):
        self.threshold = 0.6
        self.features_data_frame = pd.DataFrame()
        self.user_id = "995"  # Not needed here
        self.sensor_name = "gyroscope"  # gyroscope or accelerometer
        self.door_number = str(2)  # 1 or 2
        self.path = "../Dataset/Sample/watchtrial/"
        self.filename = "door_" + self.door_number + "_" + self.sensor_name + ".xlsx"

    def correlation(self):
        # We can also do a zip and check...but ehhh
        column_correlation = set()
        correlation_matrix = self.features_data_frame.corr()
        plt.figure(figsize=(10, 10))
        plt.pcolor(correlation_matrix, edgecolors='k', cmap='hot')
        plt.xticks(np.arange(0.5, len(correlation_matrix.columns), 1), correlation_matrix.columns, rotation=90)
        plt.yticks(np.arange(0.5, len(correlation_matrix.index), 1), correlation_matrix.index)
        plt.show()
        for i in range(len(correlation_matrix.columns)):
            for j in range(i):
                if correlation_matrix.iloc[i, j] >= self.threshold:
                    column_to_remove = correlation_matrix.columns[i]
                    column_correlation.add(column_to_remove)
                    # if column_to_remove in self.data.columns:
                    #     del self.data[column_to_remove]
        print(len(column_correlation))
        print(column_correlation)

    def get_the_features(self):
        self.features_data_frame = pd.ExcelFile(self.path + self.filename).parse('Sheet1')  # Sheet 1 only
        self.correlation()


feature_reduction = FeatureReduction()
feature_reduction.get_the_features()


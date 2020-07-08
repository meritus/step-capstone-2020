# Created by Tedi Mitiku 07/07/20
# This script is for verifying our euclidean distance assumption on
# the 7D user attribute vector space.

import math
import random
import numpy as np
import pandas as pd
import normalizing_data

#Take in user attribute data as DataFrame
user_data = pd.read_csv("data/googler_attribute_table.csv")
user_data = user_data.fillna(0) #Replace null values with 0

#Variable to adjust features to include (b/c sample data missing a column)
num_col = 6

#Normalize Data
normalizing_data.normalize(user_data, num_col+1)
print(user_data.head())

# Create distance function to measure euclidean aka l2 norm distance between two users
#(Probably want to wrap into a Googler/user class down the line)
def l2_distance(user_one, user_two):
    """Return the distance of two users in 7D vector space.
    Args:
        @user_one(1D array): user attribute values in 1x7 array. ex. [3, 5, 6, 6, 9, 10, 0]
        @user_two(1D array): user attribute values in 1x7 array.

    Returns:
        int: Euclidean distance between users.
    """
    attr_one = np.array(user_one)
    attr_two = np.array(user_two)
    return np.linalg.norm(attr_one-attr_two)

# insert other distance functions we create


#Calculate distances between several pairs of randomly sampled users
def sample(num, low, high, distance):
    """Creates a dataframe that contains sample user pairs and their euclidean distances from.

    Args:
        num(int): Number of pairs to sample.
        low(int): Lower bound of range of user ids. Ex: To sample user_id's in range from 0-50, low = 0, high = 50.
        high(int): Upper bound of range of user ids.
        distance(function): A function

    Returns:
        random_sample(DataFrame): A table with user pairs and their l2 distances.
    """
    random_sample = pd.DataFrame(columns = ["user_one_id", "user_two_id", "l2"])
    for i in range(num):
        user_one_id = random.randint(low, high)
        user_two_id = random.randint(low, high)

        user_one_attributes = user_data.iloc[user_one_id].values[1:num_col+1] #should be [1:8] but sample data is missing a column
        user_two_attributes = user_data.iloc[user_two_id].values[1:num_col+1]
        l2 = distance(user_one_attributes, user_two_attributes)

        random_sample = random_sample.append({"user_one_id": user_one_id,
                                            "user_two_id": user_two_id,
                                            "l2": l2 },
                                            ignore_index=True)
    return random_sample


test_data = sample(10, 0, 10, l2_distance)
test_data.to_csv(path_or_buf="data/test_data.csv", index=False)

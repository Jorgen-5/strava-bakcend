import numpy as np
import json
#import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter
import math

import matplotlib.pyplot as plt

def edit_distance_features(features, predicted_distances):
    for i, distance in enumerate(features[:, 0]):
        d = min(predicted_distances, key=lambda x: abs(x - distance))
        features[i, 0] = d

    return features


def predict_distances(features):
    true_distance = [50, 60, 80, 100, 150, 200, 250, 300, 350, 400, 500, 600, 800, 1000, 1200, 1400, 1600, 1609, 2000,
                     2500, 3000]

    # Runs k-means 10 times to find the optimal number of clusters
    K = range(1,10)
    dist = []
    for i in K:
        kmeans = KMeans(n_clusters=i).fit(features[:, 0].reshape(-1, 1))
        dist.append(kmeans.inertia_)

    a = dist[0] - dist[8]
    b = K[8] - K[0]
    c1 = K[0] * dist[8]
    c2 = K[8] * dist[0]
    c = c1 - c2

    # Calulates the distance from the line connecting the furthest poins and all points equating to cluster centers
    dist_from_line = []
    for i in range(9):
        dist_from_line.append(calc_distance(K[i], dist[i], a, b, c))

    # Finds the point with the furthest distance, that should be our cluster center
    num_clusters = np.argmax(dist_from_line) + 1

    kmeans = KMeans(n_clusters=num_clusters).fit(features[:, 0].reshape(-1, 1))

    num_distances = len(set(kmeans.labels_))
    distance_sum = np.zeros(shape=num_distances)
    predicted_distance = np.zeros(shape=num_distances)
    number_of_laps = np.zeros(shape=num_distances)
    counts = Counter(kmeans.labels_)
    for i in counts:
        number_of_laps[i] = counts[i]

    for i, data in enumerate(features[:, 0]):
        distance_sum[kmeans.labels_[i]] += data

    for i, data in enumerate(distance_sum):
        distance_sum[i] = distance_sum[i] / number_of_laps[i]

    for i, distance in enumerate(distance_sum):
        predicted_distance[i] = min(true_distance, key=lambda x: abs(x - distance))

    return predicted_distance


def setup_data(data):
    distance = []
    cadence = []
    speed = []
    timestamp = []
    for lap in data:
        # Removes the laps that dont have enough speed
        if lap["average_speed"] < 3:
            continue
        distance.append(lap["distance"])
        cadence.append(lap["average_cadence"])
        speed.append(lap["elapsed_time"])
        timestamp.append(lap["start_date"])

    npdistance = np.asarray(distance)
    npcadence = np.asarray(cadence)
    npspeed = np.asarray(speed)

    npdistance = npdistance.reshape(npdistance.shape[0], 1)
    npcadence = npcadence.reshape(npcadence.shape[0], 1)
    npspeed = npspeed.reshape(npspeed.shape[0], 1)

    features = np.concatenate((npdistance, npcadence, npspeed), axis=1)


    #np.save('test_data/test_features.npy', features)

    return features, timestamp, distance


def calc_distance(x1, y1, a, b, c):
  d = abs((a * x1 + b * y1 + c)) / (math.sqrt(a * a + b * b))
  return d


def normalize_array(array):
    norm = np.linalg.norm(array)
    return array / norm

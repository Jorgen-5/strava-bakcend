import numpy as np
import json
#import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter
from calculations import calculate_avg_time


#Main funciton used for testing
def main():
    # analisys()
    plt.show()


def edit_distance_features(features, predicted_distances):
    for i, distance in enumerate(features[:, 0]):
        d = min(predicted_distances, key=lambda x: abs(x - distance))
        features[i, 0] = d
    return features


def predict_distances(features):
    true_distance = [50, 60, 80, 100, 150, 200, 250, 300, 350, 400, 500, 600, 800, 1000, 1200, 1400, 1600, 1609, 2000,
                     2500, 3000]

    kmeans = KMeans(n_clusters=3).fit(features[:, 0].reshape(-1, 1))

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
    #print("Data: ", data)
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

    return features, timestamp, distance


def normalize_array(array):
    norm = np.linalg.norm(array)
    return array / norm

#Analysis used for testing
def analisys():
    with open('strava_laps_2.json') as json_file:
        r = json.load(json_file)

    features = setup_data(r)
    predicted_distances = predict_distances(features)
    new_features = edit_distance_features(features, predicted_distances)

    for i in range(5):
        j = new_features.shape[0] - 1
        new_features = np.delete(new_features, j, axis=0)

    plt.scatter(new_features[:, 1], new_features[:, 2])

    print(new_features)
    return calculate_avg_time(new_features)


if __name__ == "__main__":
    main()

import json

from Set import Set
from data_analysis import setup_data, edit_distance_features, predict_distances


class Workout:
    def __init__(self, workout_data):
        self.workout_data = None
        self.distance_ready = None
        self.laps = []
        self.different_distances = 0
        self.sets = {}
        self.predict_distances = []
        self.workout_avg = {}
        self.setLaps = {}
        self.timestamp = []

        self.workout_data = workout_data

        self.workout_data, self.timestamp, self.laps = setup_data(
            self.workout_data)
        self.predicted_distances = predict_distances(self.workout_data)
        self.different_distances = len(self.predicted_distances)
        self.distance_ready = edit_distance_features(
            self.workout_data, self.predicted_distances)

    def setup_sets(self):
        for distance in self.predicted_distances:
            self.sets[str(int(distance))] = Set(distance, str(distance))
            self.workout_avg[str(int(distance))] = 0

        for lap in self.distance_ready:
            set_object = self.sets[str(int(lap[0]))]
            set_object.set_new_lap(lap)

    def do_workout_analisys(self):
        for key, workout_set in self.sets.items():
            workout_set.calculate_set_data()
            self.workout_avg[key] = workout_set.get_set_avg()

    def make_json(self):
        data = []
        for key, avg in self.workout_avg.items():
            line = {'workout': key, 'avg': avg}
            data.append(line)

        json_data = json.dumps(data)
        return json_data

    def get_workout_avg(self):
        return self.workout_avg

    def get_laps(self):
        for i, j in enumerate(self.laps):
            self.laps[i] = min(self.predicted_distances,
                               key=lambda x: abs(x - j))

        exists = []
        new_laps = []
        for i in self.laps:
            if i not in exists:
                new_laps.append(i)
                exists.append(i)

        for i in self.sets:
            self.setLaps[i] = self.sets[i].get_lap_times()

        data = []
        for key, time_list in self.setLaps.items():
            line = {'set': key, 'times': time_list}
            data.append(line)

        data_final = []
        for i in new_laps:
            for j in data:
                if str(int(i)) == j['set']:
                    line = {'set': j['set'], 'times': j['times']}
                    data_final.append(line)

        json_data = json.dumps(data_final)

        return json_data

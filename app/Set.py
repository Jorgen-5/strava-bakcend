from Lap import Lap


class Set:
    def __init__(self, set_distance, set_name):
        self.set_distance = set_distance
        self.set_name = set_name
        self.set_distance = 0
        self.reps = 0
        self.laps = []
        self.lap_times = []
        self.avg_time = 0
        self.set_name = ""
        self.start_time = ""

    def set_new_lap(self, lap):
        self.laps.append(Lap(lap[0], lap[1], lap[2]))

    def calculate_set_data(self):
        time = 0
        for lap in self.laps:
            time += lap.get_time()
        self.avg_time = time / len(self.laps)

    def get_set_avg(self):
        return self.avg_time

    def get_lap_times(self):
        for i in self.laps:
            self.lap_times.append(i.get_time())
        return self.lap_times

    def set_start_time(self, start_time):
        self.start_time = start_time

# Takes a nparray of lap features
def calculate_avg_time(laps):
    lap_times = laps[:, 2]
    sum_avg = 0
    for lap in lap_times:
        sum_avg += lap
    avg = sum_avg / len(lap_times)

    return avg


def calculate_avg_hr():
    pass

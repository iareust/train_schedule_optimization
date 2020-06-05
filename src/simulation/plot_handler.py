import numpy as np
import matplotlib.pyplot as plt


def plot_trains(env, stations, tracks, trains, intervall=50):
    plt.figure(1)
    while True:

        plt.figure(1)
        plt.clf()

        for station in stations.values():
            station.plot()

        for track in tracks.values():
            track.plot()

        for train in trains.values():
            train.plot()

        plt.axis('off')
        plt.plot()
        yield env.timeout(1)


def plot_avg_wait_time(env, stations, window_size=10):
    i = 1
    time = []
    waiting_at_t = []

    result = []

    for _ in range(window_size):

        waiting = 0
        for station in stations.values():
            waiting += station.get_passenger_level()

        waiting_at_t.append(waiting)

        i += 1
        yield env.timeout(1)

    while True:

        time.append(i * 1)
        waiting = 0
        for station in stations.values():
            waiting += station.get_passenger_level()

        waiting_at_t.append(waiting)

        plt.figure(3)
        plt.clf()

        waited_slice = waiting_at_t[-window_size:]

        minutes_waited_in_interval = 0

        n = window_size
        for k in range(len(waited_slice)):
            minutes_waited_in_interval += k * waited_slice[k]
            n -= 1

        avg_num_of_passengers = sum(waited_slice) / float(window_size)
        result.append((minutes_waited_in_interval / (avg_num_of_passengers) - window_size))

        plt.plot(time, result, label="Avg Waited")

        i += 1
        yield env.timeout(1)


def plot_passengers(env, stations, trains, intervall=50, passenger_per_intervall=60):
    time_steps = 1

    time = []
    total_served = [0]
    bar_scale = [0]
    current_waiting = []
    current_transfer = []
    total = []

    i = 1
    while True:
        time.append(i * time_steps)

        served = 0
        waiting = 0
        for station in stations.values():
            served += station.handled_passengers
            waiting += station.get_passenger_level()

        transfer = 0
        for train in trains.values():
            transfer += train.get_passenger_level()

        if i % passenger_per_intervall == 0:
            bar_scale.append(env.now)
            total_served.append(served - sum(total_served))

        current_transfer.append(transfer)
        current_waiting.append(waiting)
        total.append(served + waiting + transfer)

        if i % intervall == 0:
            plt.figure(2)
            plt.clf()

            coef = np.polyfit(time, current_waiting, 1)
            poly_fn = np.poly1d(coef)

            plt.bar(bar_scale, total_served, align='center', width=passenger_per_intervall, color='')
            plt.plot(time, current_transfer, label="Current Transfers")
            plt.plot(time, current_waiting, label="Current Waiting")
            plt.bar(bar_scale, total_served, align='center', width=passenger_per_intervall)
            plt.plot(time, poly_fn(time), '--k')
            plt.legend()
            plt.xlabel('Time Slots')
            plt.ylabel('Passengers')
            plt.plot()

        i += 1
        yield env.timeout(time_steps)


def count(env):
    i = 1
    while True:
        print('{} - Delay: {} - Early: {} - Passengers({}/{})'.format(i, env.total_delay, env.total_early, env.total_handled, env.total_passengers))
        i += 1
        yield env.timeout(1)


def plot_pause(env):
    while True:
        plt.pause(0.01)
        yield env.timeout(1)
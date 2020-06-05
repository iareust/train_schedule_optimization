from src.model.interfaces import PassengerHandling, Locatable, Speedable
from src.model.track import Track
from typing import Union
import math


def get_distance_for_accel(terminal_speed, acceleration):
    return 0.5*(acceleration*(terminal_speed/acceleration)**2)


def get_time_to_accel(terminal_speed, acceleration):
    return terminal_speed/acceleration


def get_time_to_accel_distance(distance, acceleration):
    return math.sqrt(2*distance/acceleration)


def sim_transfer_passengers(env, station: PassengerHandling, train: PassengerHandling, section, ignore_early=False):
    """
    Simulating the transfer of passengers between station and train

    :param env: SimPy Simulation environment
    :param station: The stations with which passengers are exchanged
    :param train: The train with which passengers are exchanged
    :param section: The current schedule sections to read the arrival time
    :param ignore_early: Option weather early arrivals should be logged. This is normally activated when the last
    schedule section was a turnaround
    """
    # Wait defined amount of time
    if section.entry_planed > env.now:
        if not ignore_early:
            env.add_early(train.train_line.id, section.entry_planed - env.now)

        yield env.timeout(section.entry_planed - env.now)
    elif section.entry_planed == env.now:
        pass
    else:
        env.add_delay(train.train_line.id, (env.now - section.entry_planed))

    yield env.timeout(section.min_stopping_time)

    amount_unload = max(0, int(train.get_passenger_level() * section.unloading_factor))

    if station.get_passenger_level() > 0:

        if station.get_passenger_level() >= train.get_passenger_capacity_left()+amount_unload:
            amount_load = train.get_passenger_capacity_left()+amount_unload

        else:
            amount_load = station.get_passenger_level()
    else:
        amount_load = 0

    if int(amount_load) > 0:
        yield station.pop_passengers(amount_load)

    if amount_unload > 0:
        yield train.pop_passengers(amount_unload)

    if int(amount_load) > 0:
        yield train.put_passengers(amount_load)

    if amount_unload > 0:
        yield station.put_passengers(amount_unload)


def sim_travel(env, train: Union[Speedable, Locatable], track: Track, destination_id: str):
    """
    Simulate the movement of a train on a track
    :param env: SimPy Environment
    :param train: Train which is simulated
    :param track: Track on which train drives
    :param destination_id: The next hop of the train
    """
    speed = min(train.max_speed, track.get_max_speed(train))

    if 2 * get_distance_for_accel(speed, train.acceleration) > track.length:
        drive_duration_min = (get_time_to_accel_distance(track.length/2, train.acceleration)*2)/60.0
    else:
        accel_time_min = 2*(get_time_to_accel(speed, train.acceleration)/60.0)
        drive_duration_min = ((track.length - 2*get_distance_for_accel(speed, train.acceleration))/speed)/60.0+accel_time_min
    drive_duration_min = math.ceil(drive_duration_min)

    for i in range(drive_duration_min):
        yield env.timeout(1)
        train.position = track.get_current_position(destination_id, int(
            i * (track.length / drive_duration_min)
        ))

        if train.sim_force_stop_time > 0:
            track.direction_blocked[destination_id] = True
            yield env.timeout(train.sim_force_stop_time)
            track.direction_blocked[destination_id] = False
            train.sim_force_stop_time = 0

        while track.direction_blocked[destination_id]:
            yield env.timeout(1)


def sim_turnaround(env, section):
    yield env.timeout(section.min_stopping_time)


def sim_force_stop_random_train(env, train, time: int, duration: int):
    yield env.timeout(time)
    train.sim_force_stop_time = duration





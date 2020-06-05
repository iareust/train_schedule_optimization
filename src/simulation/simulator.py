from src.simulation.utils import generate_network, populate_network_with_trains_from_schedule
from src.simulation.environment import TrainEnvironment
from src.simulation.handlers import sim_force_stop_random_train
from src.simulation.plot_handler import count, plot_trains, plot_pause
from src.simulation import settings
from src.model.schedule import Schedule, ScheduleSection, SectionTypes

import random
import numpy as np


class Simulator:
    """
    Simulator which is used by the optimizer to evaluate timetables
    """

    def __init__(self, network_settings, seed=None, reward_weight=(1.0, 1.0, 1.0)):
        self.network_settings = network_settings
        self.reward_weight = reward_weight
        if seed is not None:
            random.seed = seed
            np.random.seed(seed=seed)

    def simulate(self, time_tables: [], connections_per_h=1, passenger_increase_factor=1,
                 force_train_stop_time=0, plot=False):
        return self.__simulate(time_tables, connections_per_h, passenger_increase_factor, force_train_stop_time,
                               plot)

    def __simulate(self, time_tables: [], connections_per_h=1, passenger_increase_factor=1,
                   force_train_stop_time=0, plot=False):

        if len(time_tables) != len(self.network_settings.LINES):
            raise ValueError("Number of Timetables ({}) is not equal to num of routes in the given network ({})".format(
                len(time_tables), len(self.network_settings.LINES)))

        env = TrainEnvironment()

        if isinstance(self.network_settings.MAX_PASSENGERS_PER_H, list):
            passenger_increment = [i * passenger_increase_factor for i in self.network_settings.MAX_PASSENGERS_PER_H]
        else:
            passenger_increment = self.network_settings.MAX_PASSENGERS_PER_H * passenger_increase_factor

        stations, tracks = generate_network(env, self.network_settings.NETWORK_CAPACITY,
                                            self.network_settings.NETWORK_DISTANCE,
                                            self.network_settings.NETWORK_ID, self.network_settings.STATION_DEST_FACTOR,
                                            self.network_settings.STATION_POSITION,
                                            max_passengers_per_h=passenger_increment)

        schedules = {}
        trains = {}

        for line, timetable in zip(self.network_settings.LINES, time_tables):
            line_sceleton = self.__generate_sceleton_schedule(line[0], line[1])
            line_sceleton.connections_per_h = connections_per_h
            schedules[line[0]] = line_sceleton.set_schedule(timetable)

            temp_trains = populate_network_with_trains_from_schedule(train_prefix='t{}'.format(line[0]),
                                                                     base_schedule=schedules[line[0]],
                                                                     stations=stations,
                                                                     connections_per_h=connections_per_h,
                                                                     env=env, max_speed=self.network_settings.TRAIN_MAX_SPEED,
                                                                     capacity_per_train=self.network_settings.TRAIN_CAPACITY)

            trains = {**trains, **temp_trains}

        for station in stations.values():
            env.process(station.simulate())

        for train in trains.values():
            env.process(train.simulate())

        if force_train_stop_time > 0:
            train = random.choice(list(trains.values()))
            time = np.random.randint(low=settings.TRAIN_BREAKDOWN_TIMESLOT[0],
                                     high=settings.TRAIN_BREAKDOWN_TIMESLOT[1])
            env.process(sim_force_stop_random_train(env, train, time=time, duration=force_train_stop_time))

        if plot:
            env.process(plot_trains(env, stations, tracks, trains))
            env.process(count(env))
            env.process(plot_pause(env))

        env.run(24 * 60)

        last_item = []

        for train in trains.values():
            timetable = train.train_line.get_schedule()
            last_item.append(timetable[-1])
            if timetable[-1] < env.now:
                env.add_delay(train.train_line.id, int(env.now - timetable[-1]))

        env.total_drive_h = len(trains) * (24 * 60)

        return env

    def __get_total_reward(self, env, tolerance_min_per_line, num_lines):
        rew_handled = env.get_reward_handled()
        rew_delay = env.get_reward_delay(tolarance_per_line=tolerance_min_per_line, num_lines=num_lines)
        rew_early = env.get_reward_early_arrival()

        reward_total = self.reward_weight[0]*rew_handled + self.reward_weight[1]*rew_delay + self.reward_weight[2]*rew_early

        return reward_total

    def evaluate_timetable(self, timetables):

        results = {
            'passenger_increase': {},
            'trains_increase': {},
            'trains_delay': {},
        }

        ######################
        #
        # Increasing Amount of Trains
        # (Num of Trains per Station per Hour)
        #
        ######################

        for i in [1, 2, 3, 4]:
            env = self.__simulate(timetables, passenger_increase_factor=1, connections_per_h=i)

            results['trains_increase'][str(i)] = self.__get_total_reward(env,
                                                                         tolerance_min_per_line=settings.ACCEPTED_DELAY_PER_LINE_PER_DAY_MIN,
                                                                         num_lines=len(timetables)
                                                                         )

        accum_reward = sum(results['trains_increase'].values())
        results['trains_increase'].update({
            'reward_total': accum_reward
        })

        ######################
        #
        # Increasing Amount of Passengers
        #
        ######################

        for i in [1, 2, 4, 8]:
            env = self.__simulate(timetables, passenger_increase_factor=i, connections_per_h=1)
            results['passenger_increase'][str(i)] = self.__get_total_reward(env,
                                                                         tolerance_min_per_line=settings.ACCEPTED_DELAY_PER_LINE_PER_DAY_MIN,
                                                                         num_lines=len(timetables)
                                                                         )

        accum_reward = sum(results['passenger_increase'].values())
        results['passenger_increase'].update({
            'reward_total': accum_reward
        })

        ######################
        #
        # Force Train Delay
        #
        ######################

        for i in [5, 30, 60, 120]:
            env = self.__simulate(timetables, force_train_stop_time=i, passenger_increase_factor=1, connections_per_h=1)
            results['trains_delay'][str(i)] = self.__get_total_reward(env,
                                                                         tolerance_min_per_line=settings.ACCEPTED_DELAY_PER_LINE_PER_DAY_MIN,
                                                                         num_lines=len(timetables)
                                                                         )

        accum_reward = sum(results['trains_delay'].values())
        results['trains_delay'].update({
            'reward_total': accum_reward
        })

        results['timetables'] = timetables

        return results

    @staticmethod
    def __generate_sceleton_schedule(id, node_list: []):

        LINE = Schedule(id=id)
        LINE.add_section(ScheduleSection(object_id=node_list[0][0], section_type=SectionTypes.START))

        for node in node_list:
            if node[0].startswith('s'):
                LINE.add_section(
                    ScheduleSection(object_id=node[0], section_type=SectionTypes.PASSENGER_STOP,
                                    unloading_factor=node[1], min_stopping_time=settings.MIN_WAIT_TIME))
            elif node[0].startswith('t'):
                LINE.add_section(ScheduleSection(object_id=node[0], section_type=SectionTypes.TRAVEL))

            elif node[0].startswith('_ta'):
                LINE.add_section(ScheduleSection(object_id=node[1], section_type=SectionTypes.TURNAROUND,
                                                 min_stopping_time=settings.TRAIN_DIRECTION_CHANGE_TIME))

            elif node[0].startswith('_tr'):
                LINE.add_section(ScheduleSection(object_id=node[1], section_type=SectionTypes.TRAVEL))
            else:
                raise ValueError

        LINE.add_section(ScheduleSection(object_id=node_list[-2][0], section_type=SectionTypes.END))

        return LINE

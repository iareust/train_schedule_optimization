import copy
from src.simulation.example_states import RL_Network

import gym
from gym import spaces
import numpy as np
import math


class TrainEnvTF(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Discrete(360)
        # self.observation_space = spaces.Dict({
        #     'capacity_matrix': spaces.Box(low=0, high=10, shape=(4, 4, 1), dtype=np.int32),
        #     'distance_matrix': spaces.Box(low=0, high=10000, shape=(4, 4, 1), dtype=np.int32),
        #     'time_tables': spaces.Box(low=0, high=1440, shape=(3, 6, 1), dtype=np.int32),
        #     # 'max_passengers_per_h': spaces.Discrete(500)
        # })
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(1, 4 * 4 + 4 * 4 + 3 * 6 + 1), dtype=np.float64)
        self.state_0 = RL_Network()
        self.timetables = copy.deepcopy(self.state_0.TIME_TABLES)
        self.zero_element_pointer = (0, -1)
        self.zero_element_pointer = self._get_pointer_to_next_zero_element()
        self.all_timetables_set = False

        self._last_action = None
        self._reward = 0

    def step(self, action: int):

        self._last_action = action
        self.timetables[self.zero_element_pointer[0]][self.zero_element_pointer[1]] = action
        obs = self._next_observation()

        if self.zero_element_pointer[1] > 0:
            if self.timetables[self.zero_element_pointer[0]][self.zero_element_pointer[1] - 1] >= action:
                done = True
                # self._reward += -10

                return obs, self._reward, done, {}

            else:
                self._reward += (1440-(action - self.timetables[self.zero_element_pointer[0]][self.zero_element_pointer[1] - 1]))/1440

        else:
            self._reward += (1440 - action) / 1440

        self.zero_element_pointer = self._get_pointer_to_next_zero_element()

        if self.all_timetables_set:
            # ToDo implement Simulation of Network with given timetables
            done = True
            self._reward += 10
        else:
            done = False

        #self._reward += 1

        return obs, self._reward, done, {}

    def reset(self):
        self.timetables = copy.deepcopy(self.state_0.TIME_TABLES)
        self.zero_element_pointer = (0, -1)
        self.zero_element_pointer = self._get_pointer_to_next_zero_element()
        self.all_timetables_set = False
        self._last_action = None
        self._reward = 0

        return self._next_observation()

    def render(self, mode='human'):
        #print('Last Action: {} - Reward: {}'.format(self._last_action, self._reward))
        #if self.all_timetables_set:
        #    print('Timetable: {}'.format(self.timetables))

        for element in self.timetables:
            for time in element:
                h = math.floor(time/60)
                min = time - (math.floor(time/60)*60)
                print('{:2}:{:2} - '.format(h, min), end='')
            print('')
    def close(self):
        pass

    def _next_observation(self):
        capacity_mat = (np.array(self.state_0.NETWORK_CAPACITY) / 100).flatten()
        distance_mat = (np.array(self.state_0.NETWORK_DISTANCE) / 10000).flatten()
        time_tables = (np.array(self.timetables) / 1440).flatten()
        max_passenger = 100 / 1000

        obs = np.append(capacity_mat, distance_mat, axis=0)
        obs = np.append(obs, time_tables)
        obs = np.append(obs, max_passenger)

        return obs

    def _get_pointer_to_next_zero_element(self):
        i = self.zero_element_pointer[0]
        j = self.zero_element_pointer[1] + 1
        for i in range(i, len(self.timetables)):
            for j in range(j, len(self.timetables[0])):
                if self.timetables[i][j] == 0:
                    return tuple((i, j))
            j = 0

        self.all_timetables_set = True
        return tuple((len(self.timetables) - 1, len(self.timetables[0]) - 1))

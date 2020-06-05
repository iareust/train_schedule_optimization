import copy
from src.simulation.example_states import RL_Network
import gym
from gym import spaces
import numpy as np
import math

from simulation.simulator import Simulator
from simulation.utils import DemoNetwork1


class TrainEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, state_0):
        self.action_space = spaces.Discrete(360)
        # self.observation_space = spaces.Dict({
        #     'capacity_matrix': spaces.Box(low=0, high=10, shape=(4, 4, 1), dtype=np.int32),
        #     'distance_matrix': spaces.Box(low=0, high=10000, shape=(4, 4, 1), dtype=np.int32),
        #     'time_tables': spaces.Box(low=0, high=1440, shape=(3, 6, 1), dtype=np.int32),
        #     # 'max_passengers_per_h': spaces.Discrete(500)
        # })
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(4 * 4 + 4 * 4 + 3 * 6 + 1,), dtype=np.float64)
        self.state_0 = state_0
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

                return obs, self._reward, done, {}

            else:
                self._reward += 1
                # self._reward += (1440 - (action - self.timetables[self.zero_element_pointer[0]][
                #     self.zero_element_pointer[1] - 1])) / 1440

        else:
            self._reward += 1

        self.zero_element_pointer = self._get_pointer_to_next_zero_element()

        if self.all_timetables_set:
            # ToDo implement Simulation of Network with given timetables
            done = True
            self._reward += 10
        else:
            done = False

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
        # print('Last Action: {} - Reward: {}'.format(self._last_action, self._reward))
        # if self.all_timetables_set:
        #    print('Timetable: {}'.format(self.timetables))

        for element in self.timetables:
            for time in element:
                h = math.floor(time / 60)
                min = time - (math.floor(time / 60) * 60)
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


class TrainEnvTF(TrainEnv):

    def __init__(self):
        super().__init__(RL_Network())
    #     self.observation_space = spaces.Dict({
    #         'capacity_matrix': spaces.Box(low=0, high=10, shape=(4, 4, 1), dtype=np.int32),
    #         'distance_matrix': spaces.Box(low=0, high=10000, shape=(4, 4, 1), dtype=np.int32),
    #         'time_tables': spaces.Box(low=0, high=1440, shape=(3, 6, 1), dtype=np.int32),
    #         'max_passengers_per_h': spaces.Discrete(500)
    #     })

    # def _next_observation(self):
    #     obs = {
    #         'capacity_matrix': np.array(self.state_0.NETWORK_CAPACITY),
    #         'distance_matrix': np.array(self.state_0.NETWORK_DISTANCE),
    #         'time_tables': np.array(self.timetables),
    #         'max_passengers_per_h': 100
    #     }

    #     return obs


class TrainEnvTFv1(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Box(np.array([0, 1, 2, 3, 4, 5]), np.array([355, 356, 357, 358, 359, 360]))
        # self.observation_space = spaces.Dict({
        #     'capacity_matrix': spaces.Box(low=0, high=10, shape=(4, 4, 1), dtype=np.int32),
        #     'distance_matrix': spaces.Box(low=0, high=10000, shape=(4, 4, 1), dtype=np.int32),
        #     'time_tables': spaces.Box(low=0, high=1440, shape=(3, 6, 1), dtype=np.int32),
        #     # 'max_passengers_per_h': spaces.Discrete(500)
        # })
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(4 * 4 + 4 * 4 + 3 * 6 + 1,), dtype=np.float64)
        self.state_0 = RL_Network()
        self.timetables = copy.deepcopy(self.state_0.TIME_TABLES)
        self.current_schedule_pointer = 0
        self._reward = 0
        self._simulator = Simulator(DemoNetwork1)

    def step(self, action):

        action = list(map(int, action))
        self.timetables[self.current_schedule_pointer] = list(action)

        obs = self._next_observation()

        for i in range(1, len(self.timetables[self.current_schedule_pointer])):

            if self.timetables[self.current_schedule_pointer][i - 1] >= self.timetables[self.current_schedule_pointer][
                i]:
                return obs, self._reward, True, {}  # Environment, Reward, done?, comment

            self._reward += 1

        self.current_schedule_pointer += 1

        if self.current_schedule_pointer >= len(self.timetables):
            results = self._simulator.evaluate_timetable(self.timetables)
            total_reward = results['passenger_increase']['reward_total'] + \
                           results['trains_delay']['reward_total'] + \
                           results['trains_increase']['reward_total']

            self._reward += int(total_reward * 10)
            return obs, self._reward, True, {}

        return obs, self._reward, False, {}

    def reset(self):
        self.timetables = copy.deepcopy(self.state_0.TIME_TABLES)
        self.current_schedule_pointer = 0
        self._reward = 0
        return self._next_observation()

    def render(self, mode='human'):
        # print('Last Action: {} - Reward: {}'.format(self._last_action, self._reward))
        # if self.all_timetables_set:
        #    print('Timetable: {}'.format(self.timetables))
        for element in self.timetables:
            for time in element:
                h = math.floor(time / 60)
                min = time - (math.floor(time / 60) * 60)
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


class SubStateDecisionTree:
    def __init__(self, tree_depth: int = 9, max_reward: float = 1.0):
        self.tree_depth = tree_depth
        self.current_level = 1
        self.max_reachable_value = 2 ** self.tree_depth
        self.max_reward = max_reward

    def reset_tree(self):
        self.current_level = 1
        self.max_reachable_value = 2 ** self.tree_depth

    def rollout_decision_and_get_reward(self, action: int, min_value: int) -> (int, float, bool):
        """

        Args:
            action: Action to take on the current level (0 or 1)
            min_value: The Minimum Value that must be reached. If Value not reachable with the given action, the reward will be 0

        Returns:
            Tuple of form (Max reachable value from current state, reward, finial_state) with types (int, float, bool)
        """
        self.max_reachable_value = self.max_reachable_value - action * 2 ** (self.tree_depth - self.current_level)
        # print('{} > {}'.format(self.max_reachable_value, min_value))
        self.current_level += 1
        if self.max_reachable_value < min_value:
            return self.max_reachable_value, 0.0, True
        elif self.current_level > self.tree_depth:
            return self.max_reachable_value, self.max_reward / self.tree_depth, True
        else:
            return self.max_reachable_value, self.max_reward / self.tree_depth, False


class TrainEnvTFv2(TrainEnv):

    def __init__(self):
        super().__init__(RL_Network())
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(4 * 4 + 4 * 4 + 3 * 6 + 1,), dtype=np.float64)
        self.subset_tree = SubStateDecisionTree(tree_depth=9, max_reward=1.0)

    def reset(self):
        _ = super().reset()
        self.timetables = copy.deepcopy(self.state_0.TIME_TABLES)
        self.current_schedule_pointer = 0
        self._reward = 0.0
        return self._next_observation()

    def step(self, action: int):

        if self.zero_element_pointer[1] == 0:
            max_reachable_value, reward, subdone = self.subset_tree.rollout_decision_and_get_reward(action=action,
                                                                                                    min_value=1)
        else:
            min_value = self.timetables[self.zero_element_pointer[0]][self.zero_element_pointer[1] - 1] + 1
            max_reachable_value, reward, subdone = self.subset_tree.rollout_decision_and_get_reward(action=action,
                                                                                                    min_value=min_value)

        self.timetables[self.zero_element_pointer[0]][self.zero_element_pointer[1]] = max_reachable_value
        self._reward += reward

        done = False

        if subdone:
            self.subset_tree.reset_tree()
            self.zero_element_pointer = self._get_pointer_to_next_zero_element()

            if not reward > 0:
                done = True

        if self.all_timetables_set and not done:
            # Todo Insert Simulation Step and Test
            self._reward += 10
            done = True

        obs = self._next_observation()
        return obs, self._reward, done, {}

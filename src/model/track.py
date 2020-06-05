import typing
import scipy.spatial
import simpy
from matplotlib import pyplot as plt
from src.model.interfaces import Plotable, Identifiable, Driveable, Locatable, Speedable
from src.simulation.settings import MIN_DISTANCE_BETWEEN_TRAINS_METERS


class Track(Plotable, Driveable, Identifiable):
    """
    A track is used by trains to drive between stations. It has no simulated behaviour of its own.

    """

    def __init__(self, track_id: str, endpoints: typing.Dict[str, Driveable and Locatable], env: simpy.core.Environment,
                 num_parallel_tracks: int = 1,
                 length: int = 0,
                 avg_speed: int = 70):

        if len(endpoints) != 2:
            raise ValueError("Invalid number of stations. A track needs to connect 2 endpoints")

        if length < 0:
            raise ValueError("Length of track cannot be lower than 0")

        if avg_speed < 1:
            raise ValueError("Avarage Speed cannot be lower than 1")

        # noinspection PyCallByClass
        Driveable.__init__(self, env, num_parallel_tracks, track_id)

        self._adjacent_nodes = endpoints

        self._avg_speed = avg_speed
        self._avg_speed_per_train = {}
        self._num_parallel_tracks = num_parallel_tracks
        self._capacity_per_track = max(1, int(length / MIN_DISTANCE_BETWEEN_TRAINS_METERS))
        self._capacity = {}

        endpoint_ids = list(endpoints.keys())
        self._capacity[endpoint_ids[0]] = simpy.PriorityResource(env,
                                                                 capacity=self._num_parallel_tracks * self._capacity_per_track)
        self._capacity[endpoint_ids[1]] = simpy.PriorityResource(env,
                                                                 capacity=self._num_parallel_tracks * self._capacity_per_track)

        self.direction_blocked = {endpoint_ids[0]: False,
                                  endpoint_ids[1]: False}

        """ Initialize List for Storing Requests """
        self._req = {endpoint_ids[0]: [], endpoint_ids[1]: []}

        if length == 0:
            self.length = self._distance_from_station_coord(endpoints)
        else:
            self.length = length

    @staticmethod
    def _distance_from_station_coord(stations: typing.Dict[str, Locatable]):

        stations = list(stations.values())
        stations: typing.List[Locatable]
        p = stations[0].position
        q = stations[1].position

        return scipy.spatial.distance.euclidean(p, q)

    def get_current_position(self, destination_id: str, meter_driven: int) -> tuple:
        """
        Helper function with which trains can get their current positon by the amount of meters they have driven on the track.
        :param destination_id: Destination of the train
        :param meter_driven: Meters driven so far
        :return: (x/y) position the train is currently in
        """
        if meter_driven > self.length:
            meter_driven = self.length

        if destination_id not in self._adjacent_nodes:
            raise ValueError("Destination ID not a valid endpoint of the Track")

        fac = meter_driven / self.length

        dest_station: Locatable = self._adjacent_nodes[destination_id]
        indexes = list(self._adjacent_nodes.keys())
        indexes.remove(destination_id)

        source_station: Locatable = self._adjacent_nodes[indexes[0]]
        x_len = dest_station.position[0] - source_station.position[0]
        y_len = dest_station.position[1] - source_station.position[1]

        x_pos = source_station.position[0] + (x_len * fac)
        y_pos = source_station.position[1] + (y_len * fac)

        return (int(x_pos), int(y_pos))

    def plot(self):
        stations = list(self._adjacent_nodes.values())
        plt.plot([stations[0].position[0], stations[1].position[0]],
                 [stations[0].position[1], stations[1].position[1]],
                 '-', zorder=1, color='grey', linewidth=self.capacity)

    def get_max_speed(self, train: Identifiable and Speedable) -> int:
        """
        Called by the train to get the maximum allowed speed it can drive on the track.
        :param train: Referenc on the train which is calling the function (self)
        :return: Maximum speed in m/s
        """
        if len(self._avg_speed_per_train) == 0:
            self._avg_speed_per_train[train.id] = min(self._avg_speed, train.max_speed)
            return self._avg_speed

        else:
            if train.id in self._avg_speed_per_train:
                return self._avg_speed_per_train[train.id]

            else:

                key_of_min_val = min(self._avg_speed_per_train.keys(), key=(lambda k: self._avg_speed_per_train[k]))
                self._avg_speed_per_train[train.id] = min(train.max_speed, self._avg_speed_per_train[key_of_min_val])
                return self._avg_speed_per_train[train.id]

    @property
    def capacity(self):
        return self._num_parallel_tracks

    @property
    def count(self):
        cap_list = list(self._capacity.values())
        count = cap_list[0].count + cap_list[1].count

        return count

    def request(self, train=None, direction=None):
        if train is None or direction is None:
            raise ValueError("Request has to contain a requesting train instance and a direction")

        if isinstance(direction, str):
            direction_id = direction

        else:
            direction_id = direction.id

        if self._capacity[direction_id].count != self._capacity[direction_id].capacity and \
                self._capacity[direction_id].count % self._capacity_per_track == 0:

            oposit_direction = list(self._capacity.keys())
            oposit_direction.remove(direction_id)

            for _ in range(self._capacity_per_track):
                self._req[direction_id].append(self._capacity[oposit_direction[0]].request())

            return self._capacity[direction_id].request()

        else:
            return self._capacity[direction_id].request()

    def release(self, req=None, train=None, direction=None):
        if train is None or direction is None:
            raise ValueError("Request has to contain a requesting train instance and a direction")

        if type(direction) is str:
            direction_id = direction

        else:
            direction_id = direction.id

        self._avg_speed_per_train.pop(train.id)

        if (self._capacity[direction_id].count-1) % self._capacity_per_track == 0 and \
                self._capacity[direction_id].count != 0:

            oposit_direction = list(self._capacity.keys())
            oposit_direction.remove(direction_id)

            for r in self._req[direction_id][:self._capacity_per_track]:
                self._capacity[oposit_direction[0]].release(r)
                self._req[direction_id].remove(r)

            return self._capacity[direction_id].release(req)

        else:
            return self._capacity[direction_id].release(req)

    def get_state(self) -> {}:
        """
        Generates a Pandas Series with the Object Id in the Id column

        Returns: pd.Series

        """

        stations = list(self._adjacent_nodes.values())

        data_series = {'Id': self.id,
                       'Capacity': int(self.capacity),
                       'AvgSpeed': int(self._avg_speed),
                       'PositionA': [stations[0].position[0], stations[1].position[0]],
                       'PositionB': [stations[0].position[1], stations[1].position[1]]}

        return data_series


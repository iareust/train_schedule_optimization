import logging
import simpy


from matplotlib import pyplot as plt
from typing import Tuple
from src.model.interfaces import Locatable, Plotable, Identifiable, PassengerHandling, Driveable

logger = logging.getLogger(__name__)


class Station(Locatable, Plotable, Driveable, Identifiable, PassengerHandling):
    """
    A station generates and removes passengers from the network and enables trains stop and load/disembark passengers.

    """

    def __init__(self, station_id: str, num_platforms: int, position: Tuple[int, int], env: simpy.core.Environment,
                 max_passengers_per_h: int = 200, factor_destination: float = 1.0):

        # noinspection PyCallByClass
        Locatable.__init__(self, position)
        # noinspection PyCallByClass
        Driveable.__init__(self, env, num_platforms, station_id)

        self._env = env
        self._passengers = simpy.Container(self._env)

        self.factor_destination = factor_destination

        if max_passengers_per_h > 1:
            self._max_passengers_per_h = max(1, max_passengers_per_h)

        self._handled_passengers: int = 0
        self._num_passengers_last_h = 0

    @property
    def handled_passengers(self) -> int:
        return self._handled_passengers

    @property
    def passengers_waiting(self) -> int:
        return self.get_passenger_level()

    def put_passengers(self, amount: int):

        if amount <= 0:
            raise ValueError("Amount cannot be negative or null")

        if amount == 1:
            at_destination = 1
        else:
            at_destination = max(0, int(self.factor_destination * amount))

        self._handled_passengers += at_destination
        self._env.total_handled += at_destination

        if amount - at_destination > 0:
            return self._passengers.put(amount - at_destination)
        else:
            return self._env.timeout(0)

    def pop_passengers(self, amount: int):

        if amount <= 0:
            raise ValueError("Amount cannot be negativ or null")

        if amount > self.get_passenger_level() > 0:
            print('ammount: {}, Level: {}'.format(amount, self.get_passenger_level()))
            return self._passengers.get(self.get_passenger_level())

        else:
            return self._passengers.get(amount)

    def get_passenger_capacity_left(self) -> int:
        return self._passengers.capacity - self._passengers.level

    def get_passenger_level(self) -> int:
        return self._passengers.level

    def simulate(self):

        while True:
            yield self._env.timeout(1)
            x = self._env.now / (24 * 60)
            new_passengers = int(max(0, min(1, (0.8 - 0.3*(1.704*x - 0.354) + 1.5*(-1.1 + 2.2*(1.704*x - 0.354))**2 - 2.2*(-1.1 + 2.2*(1.704*x - 0.354))**4))) * (self._max_passengers_per_h / 60))

            self._env.total_passengers += new_passengers
            if new_passengers > 0:
                yield self._passengers.put(new_passengers)

    def get_state(self) -> {}:
        """
        Generates a Pandas Series with the Object Id in the Id column

        Returns: pd.Series

        """
        data_series = {'Id': self.id,
                       'PassengersWaiting': int(self.passengers_waiting),
                       'PassengersHandled': int(self.handled_passengers),
                       'MaxPassengersPerH': int(self._max_passengers_per_h),
                       'Location': self.position,
                       'NumPlatforms': self.capacity}

        return data_series

    def plot(self):
        plt.scatter(self.position[0], self.position[1], marker="s", zorder=15)
        plt.text(self.position[0], self.position[1] + 240, self.id, fontsize=9, zorder=21)
        plt.text(self.position[0], self.position[1] + 120,
                 '{} | {}'.format(self._passengers.level, self._handled_passengers), fontsize=9, zorder=21)

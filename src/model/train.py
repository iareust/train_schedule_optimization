import math
import threading
from typing import Union

import simpy
from matplotlib import pyplot as plt

from src.simulation.handlers import sim_transfer_passengers, sim_travel, sim_turnaround
from src.model.interfaces import Plotable, PassengerHandling, Identifiable, Locatable, Driveable, Speedable
from src.model.track import Track
from src.model.schedule import Schedule, ScheduleSection, SectionTypes


class Train(Identifiable, Locatable, Plotable, PassengerHandling, Speedable):
    """
    This class implements the train component and the basic train logic

    """
    def __init__(self, train_id: str, env: simpy.core.Environment, capacity: int, max_speed: int, accel: float = 1.3):

        Locatable.__init__(self, (0, 0))
        Identifiable.__init__(self, train_id)

        self.capacity = capacity
        self._max_speed = max_speed
        self._acceleration = accel
        self.train_line: Union[None, Schedule] = None

        self._env = env
        self._passengers = simpy.Container(self._env, capacity=capacity, init=0)
        self.driving_direction = 1

        self._ticks_on_obj = 0

        self._currently_on_object: Union[Driveable, type(None)] = None

        self._lock_pass_put = threading.Lock()
        self._lock_pass_pop = threading.Lock()
        self._lock_drain = threading.Lock()

        self.sim_force_stop_time = 0

    @property
    def train_id(self):
        return self.id

    @property
    def max_speed(self):
        return self._max_speed

    @property
    def acceleration(self):
        return self._acceleration

    def get_passenger_capacity_left(self) -> int:
        return self._passengers.capacity - self._passengers.level

    def get_passenger_level(self) -> int:
        return self._passengers.level

    def put_passengers(self, amount: int):

        if amount <= 0:
            raise ValueError("Amount cannot be negative or null")

        with self._lock_pass_put:
            if self.get_passenger_capacity_left() >= amount:
                return self._passengers.put(amount)

            else:
                raise ValueError("Amount is greater than passenger capacity left ")

    def pop_passengers(self, amount: int):

        if amount <= 0:
            raise ValueError("Amount cannot be negativ or null")

        with self._lock_pass_pop:

            if amount > self.get_passenger_level():
                return self._passengers.get(self.get_passenger_level())

            else:
                return self._passengers.get(amount)

    def set_position(self, obj: Identifiable):

        if isinstance(obj, Locatable):
            obj: Locatable
            self.position = obj.position

        self._currently_on_object = obj

    def plot(self):
        plt.scatter(self.position[0], self.position[1], marker="x", zorder=20)
        plt.text(self.position[0] + 20, self.position[1], self.train_id, fontsize=9, zorder=21)
        plt.text(self.position[0] + 20, self.position[1] - 120,
                 '{}/{}'.format(self._passengers.level, self._passengers.capacity), fontsize=9, zorder=21)

    def simulate(self):

        if not self.train_line:
            raise ValueError("Cannot start simulation. Train line is not set")

        previous_hob: Union[Driveable, type(None)] = None
        req = None
        last_section: Union[ScheduleSection, type(None)] = None
        current_section = self.train_line.next_section()

        while True:

            last_req = req
            next_section = self.train_line.next_section()

            if last_section is not None:
                if current_section.section_id != last_section.section_id:
                    req = self._currently_on_object.request(train=self, direction=next_section.section_id)
                    yield req

            if last_req is not None and previous_hob is not None:
                yield previous_hob.release(req=last_req, train=self, direction=self._currently_on_object.id)

            if self.sim_force_stop_time > 0:
                yield self._env.timeout(self.sim_force_stop_time)
                self.sim_force_stop_time = 0

            if current_section.section_type is SectionTypes.START:
                pass

            elif current_section.section_type is SectionTypes.PASSENGER_STOP:
                self.position = self._currently_on_object.position
                if last_section is None or last_section.section_type is SectionTypes.START or last_section.section_type is SectionTypes.TURNAROUND:
                    yield from sim_transfer_passengers(env=self._env, station=self._currently_on_object, train=self,
                                                       section=current_section, ignore_early=True)

                else:
                    yield from sim_transfer_passengers(env=self._env, station=self._currently_on_object, train=self,
                                                       section=current_section)

            elif current_section.section_type is SectionTypes.TRAVEL:
                if isinstance(self._currently_on_object, PassengerHandling):
                    self.position = self._currently_on_object.position
                else:
                    yield from sim_travel(env=self._env, train=self, track=self._currently_on_object,
                                          destination_id=next_section.section_id)

            elif current_section.section_type is SectionTypes.TURNAROUND:
                yield from sim_turnaround(self._env, current_section)

            elif current_section.section_type is SectionTypes.END:
                self.train_line.get_next_schedule_from_start_position(self._env.now)

            else:
                raise Exception("Reached invalid state in Train logic")

            previous_hob = self._currently_on_object
            if current_section.section_id != next_section.section_id:
                self._currently_on_object = self._currently_on_object.get_adjacent_node(next_section.section_id)

            last_section = current_section
            current_section = next_section

    def get_state(self) -> {}:
        """
        Generates a Pandas Series with the Object Id in the Id column

        Returns: pd.Series

        """
        data_series = {'Id': self.id,
                       'Capacity': int(self.capacity),
                       'MaxSpeed': int(self.max_speed),
                       'PassengerLevel': int(self.get_passenger_level()),
                       'Location': self.position,
                       'PositionOnInfra': self._currently_on_object.id}

        return data_series

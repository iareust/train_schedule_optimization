import copy
import math
from typing import List, Union
import enum
import warnings


class SectionTypes(enum.Enum):
    """
    Enumeration for the section types
    """

    START = 10
    TURNAROUND = 20
    PASSENGER_STOP = 30
    TRAVEL = 40
    END = 50


class ScheduleSection(object):
    """
    A schedule section is a single section of a schedule. They are defined by a object id and section type.
    For passenger stop sections the unloading_factor, minimum stopping time and the planned entry are also defined.

    """

    def __init__(self, object_id: str, section_type: SectionTypes, unloading_factor: float = None,
                 min_stopping_time=None, entry_planed=None):
        self.section_id: str = object_id
        self.section_type: SectionTypes = section_type

        if unloading_factor is not None:
            if 0 <= unloading_factor <= 1.0:
                self.unloading_factor = unloading_factor
            else:
                raise ValueError("Unload factor has to be between 0 and 1.0")

        self.delay_weight: int = 1

        self.min_stopping_time: Union[None, int] = min_stopping_time
        self.entry_planed: Union[None, int] = entry_planed


class Schedule(object):
    """
    A schedule defines the route which a train follows, as well as the arrival time at stations.

    """

    def __init__(self, id, connections_per_h: int = 1):
        self.id = id
        self._sections: List[ScheduleSection] = []
        self.connections_per_h = connections_per_h
        self._list_pointer = 0

    def next_section(self):
        self._list_pointer = (self._list_pointer + 1) % len(self._sections)
        return self._sections[self._list_pointer - 1]

    def current_section(self):
        return self._sections[self._list_pointer]

    def add_section(self, section: ScheduleSection):
        self._sections.append(section)

    def remove_section(self, section: ScheduleSection):
        self._sections.remove(section)

    def set_schedule(self, arrival_times_stations: List[int]):
        if len(arrival_times_stations) != sum(n.section_type == SectionTypes.PASSENGER_STOP for n in self._sections):
            raise ValueError("""
                Lists with arrival times must match the number of Passenger Stops in the Schedule.
                Expected number of items: {}
                Given number of items : {}
                """.format(sum(n.section_type == SectionTypes.PASSENGER_STOP for n in self._sections),
                           len(arrival_times_stations))
                             )

        schedule_items = arrival_times_stations.copy()
        for section in self._sections:
            if section.section_type is SectionTypes.PASSENGER_STOP:
                section.entry_planed = schedule_items.pop(0)
                if section.min_stopping_time is not None:
                    section.exit_latest = section.entry_planed + section.min_stopping_time
                else:
                    section.exit_latest = None

        return self

    def get_schedule(self) -> List[int]:
        schedule = []
        for section in self._sections:
            if section.section_type is SectionTypes.PASSENGER_STOP:
                schedule.append(section.entry_planed)

        return schedule

    def get_next_schedule_from_start_position(self, current_time: int):
        """
        Generates a new schedule from the start section by checkig which schedules can feasably be realised by the train
        the current time. If the train has to much delay it is possible that a schedule is jumped.

        :param current_time: The current simulation time
        :return: returns an updated reference to itself
        """
        schedule = self.get_schedule()
        while schedule[0] < current_time:
            if self.connections_per_h != 0:
                schedule = [x + (int(60 / self.connections_per_h)) for x in schedule]
            else:
                schedule = [x + (int(60 / 1)) for x in schedule]

        self.set_schedule(schedule)
        return self


def schedule_factory(base_schedule: Schedule, connections_per_h) -> List[Schedule]:
    """
    Helper function to create Schedules from a provided base schedule and a given number of connections per hour.
    :param base_schedule:
    :param connections_per_h:
    :return:
    """
    schedules = [base_schedule]
    schedule_duration = max(base_schedule.get_schedule()) - min(base_schedule.get_schedule())

    if connections_per_h is not None and connections_per_h > 0:
        if not (60.0 / connections_per_h).is_integer():
            warnings.warn("Selected Number of connections per h ({}) results in an uneven schedule period {}".format(
                connections_per_h, (60.0 / connections_per_h)))
        num_of_trains_on_line = int(math.ceil(schedule_duration / (60 / connections_per_h)))

    else:
        num_of_trains_on_line = 1

    for i in range(1, num_of_trains_on_line):
        schedule = copy.deepcopy(base_schedule)
        schedule.set_schedule([x - (i * int(60 / connections_per_h)) for x in schedule.get_schedule()])
        schedules.append(schedule)

    return schedules

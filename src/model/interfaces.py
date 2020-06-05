from __future__ import annotations
from typing import Dict, Tuple, Union

import abc
import scipy.spatial
import simpy


class PassengerHandling:
    """
    Interface which defines the functions used to transfer passengers between ressources. Possible components with
    the PassengerHandling interface are stations and trains.

    """
    @abc.abstractmethod
    def put_passengers(self, amount: int):
        """
        Adds a defined amount of passengers to the ressource
        :param amount: Amount of passengers to be added to the ressource. Amount has to be greater 0.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def pop_passengers(self, amount: int):
        """
        Remove a defined amount of passenger from the ressource
        :param amount: Amount of passengers to be removed from the ressource. Amount has to be greater 0 or an value exeption will be raised
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_passenger_capacity_left(self) -> int:
        """
        Returns the passenger capacity of the ressource.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_passenger_level(self) -> int:
        """
        Returns the current passenger level of the ressource.

        """
        raise NotImplementedError


class Speedable:
    """
    Interface for components which move in the simulation (e.g. Trains)

    """
    @property
    def max_speed(self):
        """
        Returns the maximum speed of the object in m/s

        """
        raise NotImplementedError

    @property
    def acceleration(self):
        """
        Returns the acceleration of the object im m/s^2
        """
        raise NotImplementedError


class Identifiable:
    """
    Interface for objects which have an id. Examples are trains, stations, tracks.

    """
    def __init__(self, id: str):
        self._id = id

    @property
    def id(self) -> str:
        """
        Get the id of the object in the simulator
        :return: Id of object as str
        """
        return self._id


class Driveable(Identifiable):
    """
    Interface for infrastructure which can be used by the trains to drive on. Examples are tracks.

    """
    def __init__(self, simulation_environment: simpy.core.Environment, capacity: int, id: str, length: int = 1) -> None:
        """
        Initialize the drivable object

        :param simulation_environment: The SimPy simulation environment in which the object is simulated
        :param capacity: The capacity of the Object (e.g. number of rails for tracks)
        :param id: The id of the object
        :param length: The length of the driveable segment
        """
        Identifiable.__init__(self, id)
        self._capacity = simpy.Resource(simulation_environment, capacity=capacity)
        self._adjacent_nodes: Dict[str, Driveable] = {}
        self.length = length

    def get_adjacent_node(self, adjacent_node: Union[str, Driveable]) -> Driveable:
        """
        Returns the Driveable object which is connected to this object and has the id adjacent_node.

        :param adjacent_node: The id of the connected object.
        :return: The object which was referenced in the functions.
        """
        if type(adjacent_node) == str:
            id = adjacent_node

        elif type(adjacent_node) == Driveable:
            id = adjacent_node.id

        else:
            raise ValueError("Invalid type for adjecent_node. Should be str or Driveable")

        try:
            return self._adjacent_nodes[id]

        except KeyError:
            raise KeyError("The Object {} is not reachable from {}".format(id, self.id))

    def add_adjacent_node(self, adjacent_node: Driveable) -> None:
        """
        Adds a Drivable object which is conneted to this object.
        :param adjacent_node:
        """
        self._adjacent_nodes[adjacent_node.id] = adjacent_node

    @property
    def capacity(self):
        """
        Return the free capacity of the object (e.g. number of free tracks or stations)
        :return:
        """
        return self._capacity.capacity

    def request(self, train=None, direction: Identifiable = None):
        """
        Request access to the ressource. If the ressource is currently fully occupied, the requesting component will
        wait until the ressource is freed up again.

        :param train: A reference (self) of the train which requests the ressource
        :param direction: Direction in which the train wants to travel (In case of track; the destination station)
        :return: SimPy Request Object which has to be yielded by the caller.
        """
        return self._capacity.request()

    def release(self, req, train=None, direction=None):
        """
        Release the access on a ressource. This function is used by trains after they left the ressource (e.g. left station or track)
        :param req: The request object that was return when requesting the ressource
        :param train: A reference (self) to the train which releases the ressource.
        :param direction: Direction in which the train traveled on the ressource
        :return: SimPy Release Object which has to be yielded by the caller
        """
        return self._capacity.release(req)


class Simulatable:
    """
    Interface for objects which have a simulated behaviour (e.g. stations, trains)

    """
    @abc.abstractmethod
    def simulate(self):
        """
        Methods which defines the simulated behaviour of the object. This function has to be added as a process to the
        SimPy Envrionment;

        _Example_
        env.process(station.simulate())
        """
        raise NotImplementedError


class Plotable(object):
    """
    Interface for objects which can be plotet in the simulation visualisation.

    """
    @abc.abstractmethod
    def plot(self):
        """
        Metode which is called by the plot handler to plot the object.s
        """
        raise NotImplementedError


class Locatable(object):
    """
    Interface for Objects which have a position

    """

    def __init__(self, position: Tuple[int, int]):
        self._position = position

    @property
    def position(self):
        """
        Returns the position of the object

        :return: Postition as (int, int) tuple representing (x/y)-coordinate
        """
        return self._position

    @position.setter
    def position(self, value: tuple):
        """
        Set position of the object.

        :param value:
        """
        self._position = value

    def _distance_from_obj(self, other: Locatable):
        p = self.position
        q = other.position

        return scipy.spatial.distance.euclidean(p, q)

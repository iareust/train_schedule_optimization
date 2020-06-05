from enum import Enum

from src.model.station import Station
from src.model.track import Track


class InfraType(Enum):
    TRANSIT = 1
    STATION = 2
    CHANGE_DRIVING_DIRECTION = 3
    REVERSE_LINE = 4


def connect_to_station(source_station: Station, dest_station: Station, env, track_id: str, length_of_track: int = 1,
                       capacity_of_track: int = 1, avg_speed=250) -> Track:

    stations = {source_station.id: source_station, dest_station.id: dest_station}
    track = Track(track_id, endpoints=stations, env=env, num_parallel_tracks=capacity_of_track, length=length_of_track, avg_speed=avg_speed)

    source_station.add_adjacent_node(track)
    dest_station.add_adjacent_node(track)

    return track

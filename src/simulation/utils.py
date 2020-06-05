import simpy
import warnings
import pandas as pd
import numpy as np

from src.model.station import Station
from src.simulation import settings
from src.model.utils import connect_to_station
from src.model.schedule import Schedule, ScheduleSection, SectionTypes, schedule_factory
from src.model.train import Train
from typing import Dict


def generate_dataframe_from_state(stations: {}) -> pd.DataFrame:
    df = []
    for key in stations:
        df.append(stations[key].get_state())

    return pd.DataFrame(df)


def sim_save_state(store: [], stations: {}, env: simpy.core.Environment):
    while True:
        df = generate_dataframe_from_state(stations)
        store.append(df)

        yield env.timeout(1)


class DebugNetwork(object):
    NETWORK_CAPACITY = [
        [10, 1],
        [1, 10],


    ]

    NETWORK_DISTANCE = [
        [0, 60000],
        [60000, 0],
    ]

    NETWORK_ID = [
        ['sA', 'tAB'],
        ['tAB', 'sB'],
    ]

    STATION_POSITION = [
        (100, 100),
        (6000, 100),
    ]

    STATION_DEST_FACTOR = [
        1.0,
        1.0,
    ]

    MAX_PASSENGERS_PER_H = 200

    TRAIN_CAPACITY = 600
    TRAIN_MAX_SPEED = 44  # m/s

    STATION_MAX_PAS_PER_H = []

    LINES = [
        ('tlAB', [
            ('sA', 1.0), ('tAB', None), ('sB', 1.0), ('_ta', 'sB'),
            ('sB', 1.0), ('tAB', None), ('sA', 1.0), ('_ta', 'sA')
        ]),
        ('tlBA', [
            ('sB', 1.0), ('tAB', None), ('sA', 1.0), ('_ta', 'sA'),
            ('sA', 1.0), ('tAB', None), ('sB', 1.0), ('_ta', 'sB')
        ])
    ]


class DemoNetwork1(object):
    NETWORK_CAPACITY = [
        [4, 1, 0, 0],
        [1, 6, 2, 1],
        [0, 2, 4, 1],
        [0, 1, 1, 4],
    ]

    NETWORK_DISTANCE = [
        [0, 2500, 0, 0],
        [2500, 0, 3000, 4000],
        [0, 3000, 0, 8000],
        [0, 4000, 8000, 0],
    ]

    NETWORK_ID = [
        ['sA', 'tAB', '', ''],
        ['tAB', 'sB', 'tBC', 'tBD'],
        ['', 'tBC', 'sC', 'tCD'],
        ['', 'tBD', 'tCD', 'sD'],
    ]

    STATION_POSITION = [
        (100, 100),
        (3500, 100),
        (6000, 3000),
        (9900, 100)
    ]

    STATION_DEST_FACTOR = [
        1.0,
        0.6,
        0.8,
        1.0
    ]

    MAX_PASSENGERS_PER_H = 200

    TRAIN_CAPACITY = 600
    TRAIN_MAX_SPEED = 44  # m/S

    STATION_MAX_PAS_PER_H = []

    LINES = [
        ('tlABC', [
            ('sA', 1.0), ('tAB', None), ('sB', 0.8), ('tBC', None), ('sC', 1.0), ('_ta', 'sC'),
            ('sC', 1.0), ('tBC', None), ('sB', 0.4), ('tAB', None), ('sA', 1.0), ('_ta', 'sA')
        ]),
        ('tlACD', [
            ('sA', 1.0), ('tAB', None), ('_tr', 'sB'), ('tBC', None), ('sC', 0.6), ('tCD', None), ('sD', 1.0),
            ('_ta', 'sD'),
            ('sD', 1.0), ('tCD', None), ('sC', 0.6), ('tBC', None), ('_tr', 'sB'), ('tAB', None), ('sA', 1.0),
            ('_ta', 'sA')
        ]),
        ('tlCDB', [
            ('sC', 1.0), ('tCD', None), ('sD', 0.3), ('tBD', None), ('sB', 1.0), ('_ta', 'sB'),
            ('sB', 1.0), ('tBD', None), ('sD', 0.6), ('tCD', None), ('sC', 1.0), ('_ta', 'sC')
        ])
    ]


class DemoNetwork2(object):
    NETWORK_CAPACITY = [
        #A  B  C  D  E  F  G  H  I  J  K  L  M
        [4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A
        [0, 6, 3, 0, 0, 2, 0, 0, 0, 2, 2, 0, 0],  # B
        [0, 0, 6, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # C
        [0, 0, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # D
        [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],  # E
        [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],  # F
        [0, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 0, 0],  # G
        [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],  # H
        [0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0],  # I
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],  # J
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 0],  # K
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],  # L
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],  # M
    ]

    NETWORK_DISTANCE = [
        # A  B  C  D  E  F  G  H  I  J  K  L  M
        [0, 30000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A
        [0, 0, 60000, 0, 0, 30000, 0, 0, 0, 30000, 30000, 0, 0],  # B
        [0, 0, 0, 30000, 0, 0, 30000, 0, 0, 0, 0, 0, 0],  # C
        [0, 0, 0, 0, 30000, 0, 0, 0, 0, 0, 0, 0, 0],  # D
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # E
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # F
        [0, 0, 0, 0, 0, 0, 0, 30000, 0, 0, 0, 0, 0],  # G
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # H
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 30000, 0, 0, 0],  # I
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # J
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30000, 0],  # K
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30000],  # L
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # M
    ]

    NETWORK_ID = [
        ['sA', 'tAB', 'tAC', 'tAD', 'tAE', 'tAF', 'tAG', 'tAH', 'tAI', 'tAJ', 'tAK', 'tAL', 'tAM'],
        ['tBA', 'sB', 'tBC', 'tBD', 'tBE', 'tBF', 'tBG', 'tBH', 'tBI', 'tBJ', 'tBK', 'tBL', 'tBM'],
        ['tCA', 'tCB', 'sC', 'tCD', 'tCE', 'tCF', 'tCG', 'tCH', 'tCI', 'tCJ', 'tCK', 'tCL', 'tCM'],
        ['tDA', 'tDB', 'tDC', 'sD', 'tDE', 'tDF', 'tDG', 'tDH', 'tDI', 'tDJ', 'tDK', 'tDL', 'tDM'],
        ['tEA', 'tEB', 'tEC', 'tED', 'sE', 'tEF', 'tEG', 'tEH', 'tEI', 'tEJ', 'tEK', 'tEL', 'tEM'],
        ['tFA', 'tFB', 'tFC', 'tFD', 'tFE', 'sF', 'tFG', 'tFH', 'tFI', 'tFJ', 'tFK', 'tFL', 'tFM'],
        ['tGA', 'tGB', 'tGC', 'tGD', 'tGE', 'tGF', 'sG', 'tGH', 'tGI', 'tGJ', 'tGK', 'tGL', 'tGM'],
        ['tHA', 'tHB', 'tHC', 'tHD', 'tHE', 'tHF', 'tHG', 'sH', 'tHI', 'tHJ', 'tHK', 'tHL', 'tHM'],
        ['tIA', 'tIB', 'tIC', 'tID', 'tIE', 'tIF', 'tIG', 'tIH', 'sI', 'tIJ', 'tIK', 'tIL', 'tIM'],
        ['tJA', 'tJB', 'tJC', 'tJD', 'tJE', 'tJF', 'tJG', 'tJH', 'tJI', 'sJ', 'tJK', 'tJL', 'tJM'],
        ['tKA', 'tKB', 'tKC', 'tKD', 'tKE', 'tKF', 'tKG', 'tKH', 'tKI', 'tKJ', 'sK', 'tKL', 'tKM'],
        ['tLA', 'tLB', 'tLC', 'tLD', 'tLE', 'tLF', 'tLG', 'tLH', 'tLI', 'tLJ', 'tLK', 'sL', 'tLM'],
        ['tMA', 'tMB', 'tMC', 'tMD', 'tME', 'tMF', 'tMG', 'tMH', 'tMI', 'tMJ', 'tMK', 'tML', 'sM']
    ]

    STATION_POSITION = [
        (5000, 100),  # A
        (5000, 2100),  # B
        (5000, 4100),  # C
        (5000, 6100),  # D
        (5000, 8100),  # E
        (3000, 100),  # F
        (3000, 6100),  # G
        (3000, 8100),  # H
        (7000, 100),  # I
        (7000, 1100),  # J
        (7000, 4100),  # K
        (7000, 6100),  # L
        (7000, 8100),  # M
    ]

    STATION_DEST_FACTOR = [
        1.0,  # A
        0.8,  # B
        0.6,  # C
        0.4,  # D
        1.0,  # E
        1.0,  # F
        0.2,  # G
        1.0,  # H
        1.0,  # I
        0.2,  # J
        0.7,  # K
        0.4,  # L
        1.0,  # M
    ]

    MAX_PASSENGERS_PER_H = [
        400,  # A
        400,  # B
        400,  # C
        400,  # D
        400,  # E
        400,  # F
        300,  # G
        400,  # H
        400,  # I
        400,  # J
        400,  # K
        400,  # L
        300,  # M
    ]

    TRAIN_CAPACITY = 600
    TRAIN_MAX_SPEED = 44  # m/S

    LINES = [
        ('tlABCDE', [
            ('sA', 1.0), ('tAB', None), ('sB', 0.8), ('tBC', None), ('sC', 0.7), ('tCD', None), ('sD', 0.4), ('tDE', None), ('sE', 1.0), ('_ta', 'sE'),
            ('sE', 1.0), ('tDE', None), ('sD', 0.2), ('tCD', None), ('sC', 0.4), ('tBC', None), ('sB', 0.9), ('tAB', None), ('sA', 1.0), ('_ta', 'sA')
        ]),
        ('tlFBCGH', [
            ('sF', 1.0), ('tBF', None), ('sB', 0.8), ('tBC', None), ('sC', 0.7), ('tCG', None), ('sG', 0.4), ('tGH', None), ('sH', 1.0), ('_ta', 'sH'),
            ('sH', 1.0), ('tGH', None), ('sG', 0.2), ('tCG', None), ('sC', 0.4), ('tBC', None), ('sB', 0.9), ('tBF', None), ('sF', 1.0), ('_ta', 'sF')
        ]),
        ('tlIJBKLM', [
            ('sI', 1.0), ('tIJ', None), ('sJ', 0.3), ('tBJ', None), ('sB', 0.8), ('tBK', None), ('sK', 0.4), ('tKL', None), ('sL', 0.4), ('tLM', None), ('sM', 1.0), ('_ta', 'sM'),
            ('sM', 1.0), ('tLM', None), ('sL', 0.2), ('tKL', None), ('sK', 0.4), ('tBK', None), ('sB', 0.9), ('tBJ', None), ('sJ', 0.6), ('tIJ', None), ('sI', 1.0), ('_ta', 'sI')
        ]),
    ]


def _generate_sceleton_schedule(id, node_list: []):
    warnings.warn("Function Deprecated", DeprecationWarning)

    LINE = Schedule(id=id)
    LINE.add_section(ScheduleSection(object_id=node_list[0][0], section_type=SectionTypes.START))

    for node in node_list:
        if node[0].startswith('s'):
            LINE.add_section(
                ScheduleSection(object_id=node[0], section_type=SectionTypes.PASSENGER_STOP, unloading_factor=node[1],
                                min_stopping_time=settings.MIN_WAIT_TIME))
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


class DemoScheduleSceleton(object):
    LINE_ABC = _generate_sceleton_schedule('tlABC', [
        ('sA', 1.0), ('tAB', None), ('sB', 0.8), ('tBC', None), ('sC', 1.0), ('_ta', 'sC'),
        ('sC', 1.0), ('tBC', None), ('sB', 0.4), ('tAB', None), ('sA', 1.0), ('_ta', 'sA')
    ])

    LINE_ACD = _generate_sceleton_schedule('tlACD', [
        ('sA', 1.0), ('tAB', None), ('_tr', 'sB'), ('tBC', None), ('sC', 0.6), ('tCD', None), ('sD', 1.0),
        ('_ta', 'sD'),
        ('sD', 1.0), ('tCD', None), ('sC', 0.6), ('tBC', None), ('_tr', 'sB'), ('tAB', None), ('sA', 1.0), ('_ta', 'sA')
    ])

    LINE_CDB = _generate_sceleton_schedule('tlCDB', [
        ('sC', 1.0), ('tCD', None), ('sD', 0.3), ('tBD', None), ('sB', 1.0), ('_ta', 'sB'),
        ('sB', 1.0), ('tBD', None), ('sD', 0.6), ('tCD', None), ('sC', 1.0), ('_ta', 'sC')
    ])


def generate_network(env, network_capacity_matrix, network_distance_matrix, network_id_matrix, station_dest_factor_list,
                     station_position_list=None, speed_matrix=None, max_passengers_per_h=None):
    stations = {}
    tracks = {}

    for i in range(len(network_capacity_matrix)):
        if station_position_list is not None:
            position = station_position_list[i]
        else:
            position = (int(np.random.rand(1) * 10000), int(np.random.rand(1) * 10000))

        if max_passengers_per_h is None:
            value = settings.MAX_PASSENGERS_PER_H
        elif isinstance(max_passengers_per_h, list):
            value = max_passengers_per_h[i]
        else:
            value = max_passengers_per_h

        station = Station(station_id=network_id_matrix[i][i],
                          num_platforms=network_capacity_matrix[i][i],
                          position=position,
                          env=env,
                          max_passengers_per_h=value,
                          factor_destination=station_dest_factor_list[i]
                          )

        stations[network_id_matrix[i][i]] = station

    for i in range(len(network_capacity_matrix)):
        for j in range(i, len(network_capacity_matrix)):
            if i != j and network_capacity_matrix[i][j] != 0:
                if speed_matrix is None:
                    track = connect_to_station(track_id=network_id_matrix[i][j],
                                               source_station=stations[network_id_matrix[i][i]],
                                               dest_station=stations[network_id_matrix[j][j]],
                                               env=env,
                                               capacity_of_track=network_capacity_matrix[i][j],
                                               length_of_track=network_distance_matrix[i][j])
                else:

                    track = connect_to_station(track_id=network_id_matrix[i][j],
                                               source_station=stations[network_id_matrix[i][i]],
                                               dest_station=stations[network_id_matrix[j][j]],
                                               env=env,
                                               capacity_of_track=network_capacity_matrix[i][j],
                                               length_of_track=network_distance_matrix[i][j],
                                               avg_speed=speed_matrix[i][j])

                tracks[network_id_matrix[i][j]] = track

    return stations, tracks


def populate_network_with_trains_from_schedule(train_prefix: str, base_schedule: Schedule, stations: Dict[str, Station],
                                               connections_per_h: int,
                                               env, max_speed: int, capacity_per_train: int):
    i = 0
    trains = {}
    gen_schedules = schedule_factory(base_schedule=base_schedule, connections_per_h=connections_per_h)

    for schedule in gen_schedules:

        section = schedule.current_section()
        while section.entry_planed is None or section.entry_planed < 0:
            section = schedule.next_section()

        schedule._list_pointer -= 1
        start_position = stations[section.section_id]
        train = Train('{}{:03d}'.format(train_prefix, i), env=env, max_speed=max_speed, capacity=capacity_per_train)
        train.train_line = schedule
        train.set_position(start_position)

        trains[train.id] = train
        i += 1

    return trains

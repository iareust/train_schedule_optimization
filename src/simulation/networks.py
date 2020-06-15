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


class STAR_6S_2L_01(object):
    NETWORK_CAPACITY = [
        # A  B  C  D  E  F
        [2, 1, 0, 0, 0, 0],
        [0, 4, 2, 0, 1, 0],
        [0, 0, 4, 1, 0, 1],
        [0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 0, 2],

    ]

    NETWORK_DISTANCE = [
        [0, 10000, 0, 0, 0, 0],
        [0, 0, 10000, 0, 10000, 0],
        [0, 0, 0, 10000, 0, 10000],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]

    NETWORK_ID = [
        ['sA', 'tAB', 'tAC', 'tAD', 'tAE', 'tAF'],
        ['tBA', 'sB', 'tBC', 'tBD', 'tBE', 'tBF'],
        ['tCA', 'tCB', 'sC', 'tCD', 'tCE', 'tCF'],
        ['tDA', 'tDB', 'tDC', 'sD', 'tDE', 'tDF'],
        ['tEA', 'tEB', 'tEC', 'tED', 'sE', 'tEF'],
        ['tFA', 'tFB', 'tFC', 'tFD', 'tFE', 'sF'],
    ]

    STATION_POSITION = [
        (2000, 7000),  # A
        (4000, 5000),  # B
        (6000, 5000),  # C
        (8000, 7000),  # D
        (2000, 3000),  # E
        (8000, 3000),  # F
    ]

    STATION_DEST_FACTOR = [
        1.0,  # A
        0.8,  # B
        0.8,  # C
        1.0,  # D
        1.0,  # E
        1.0,  # F
    ]

    MAX_PASSENGERS_PER_H = [
        200,  # A
        400,  # B
        400,  # C
        200,  # D
        200,  # E
        200,  # F
    ]

    TRAIN_CAPACITY = 600
    TRAIN_MAX_SPEED = 44  # m/S

    LINES = [
        ('tlABCDE', [
            ('sA', 1.0), ('tAB', None), ('sB', 0.6), ('tBC', None), ('sC', 0.6), ('tCD', None), ('sD', 1.0),
            ('_ta', 'sD'),
            ('sD', 1.0), ('tCD', None), ('sC', 0.6), ('tBC', None), ('sB', 0.6), ('tAB', None), ('sA', 1.0),
            ('_ta', 'sA')
        ]),
        ('tlEBCF', [
            ('sE', 1.0), ('tBE', None), ('sB', 0.6), ('tBC', None), ('sC', 0.6), ('tCF', None), ('sF', 1.0),
            ('_ta', 'sF'),
            ('sF', 1.0), ('tCF', None), ('sC', 0.6), ('tBC', None), ('sB', 0.6), ('tBE', None), ('sE', 1.0),
            ('_ta', 'sE')
        ]),
    ]


class STAR_9S_2L_01(object):
    NETWORK_CAPACITY = [
        #A  B  C  D  E  F  G  H  I
        [2, 1, 0, 0, 0, 0, 0, 0, 0],  # A
        [0, 2, 1, 0, 0, 0, 0, 0, 0],  # B
        [0, 0, 4, 1, 0, 0, 1, 1, 0],  # C
        [0, 0, 0, 2, 1, 0, 0, 0, 0],  # D
        [0, 0, 0, 0, 2, 0, 0, 0, 0],  # E
        [0, 0, 0, 0, 0, 2, 1, 0, 0],  # F
        [0, 0, 0, 0, 0, 0, 2, 0, 0],  # G
        [0, 0, 0, 0, 0, 0, 0, 2, 1],  # H
        [0, 0, 0, 0, 0, 0, 0, 0, 2],  # I
    ]

    NETWORK_DISTANCE = [
        #A  B  C  D  E  F  G  H  I
        [0, 10000, 0, 0, 0, 0, 0, 0, 0],  # A
        [0, 0, 10000, 0, 0, 0, 0, 0, 0],  # B
        [0, 0, 0, 10000, 0, 0, 10000, 10000, 0],  # C
        [0, 0, 0, 0, 10000, 0, 0, 0, 0],  # D
        [0, 0, 0, 0, 0, 0, 0, 0, 0],  # E
        [0, 0, 0, 0, 0, 0, 10000, 0, 0],  # F
        [0, 0, 0, 0, 0, 0, 0, 0, 0],  # G
        [0, 0, 0, 0, 0, 0, 0, 0, 10000],  # H
        [0, 0, 0, 0, 0, 0, 0, 0, 0],  # I
    ]

    NETWORK_ID = [
        ['sA', 'tAB', 'tAC', 'tAD', 'tAE', 'tAF', 'tAG', 'tAH', 'tAI'],
        ['tBA', 'sB', 'tBC', 'tBD', 'tBE', 'tBF', 'tBG', 'tBH', 'tBI'],
        ['tCA', 'tCB', 'sC', 'tCD', 'tCE', 'tCF', 'tCG', 'tCH', 'tCI'],
        ['tDA', 'tDB', 'tDC', 'sD', 'tDE', 'tDF', 'tDG', 'tDH', 'tDI'],
        ['tEA', 'tEB', 'tEC', 'tED', 'sE', 'tEF', 'tEG', 'tEH', 'tEI'],
        ['tFA', 'tFB', 'tFC', 'tFD', 'tFE', 'sF', 'tFG', 'tFH', 'tFI'],
        ['tGA', 'tGB', 'tGC', 'tGD', 'tGE', 'tGF', 'sG', 'tGH', 'tGI'],
        ['tHA', 'tHB', 'tHC', 'tHD', 'tHE', 'tHF', 'tHG', 'sH', 'tHI'],
        ['tIA', 'tIB', 'tIC', 'tID', 'tIE', 'tIF', 'tIG', 'tIH', 'sI'],
    ]

    STATION_POSITION = [
        (1000, 7000),  # A
        (3000, 7000),  # B
        (5000, 5000),  # C
        (7000, 7000),  # D
        (9000, 7000),  # E
        (1000, 3000),  # F
        (3000, 3000),  # G
        (7000, 3000),  # H
        (9000, 3000),  # I
    ]

    STATION_DEST_FACTOR = [
        1.0,  # A
        1.0,  # B
        0.8,  # C
        1.0,  # D
        1.0,  # E
        1.0,  # F
        1.0,  # G
        1.0,  # H
        1.0,  # I
    ]

    MAX_PASSENGERS_PER_H = [
        200,  # A
        200,  # B
        400,  # C
        200,  # D
        200,  # E
        200,  # F
        200,  # G
        200,  # H
        200,  # I
    ]

    TRAIN_CAPACITY = 600
    TRAIN_MAX_SPEED = 44  # m/S

    LINES = [
        ('tlABCDE', [
            ('sA', 1.0), ('tAB', None), ('sB', 0.2), ('tBC', None), ('sC', 0.6), ('tCD', None), ('sD', 0.2), ('tDE', None), ('sE', 1.0), ('_ta', 'sE'),
            ('sE', 1.0), ('tDE', None), ('sD', 0.2), ('tCD', None), ('sC', 0.6), ('tBC', None), ('sB', 0.2), ('tAB', None), ('sA', 1.0), ('_ta', 'sA')
        ]),
        ('tlFGCHI', [
            ('sF', 1.0), ('tFG', None), ('sG', 0.2), ('tCG', None), ('sC', 0.6), ('tCH', None), ('sH', 0.2), ('tHI', None), ('sI', 1.0), ('_ta', 'sI'),
            ('sI', 1.0), ('tHI', None), ('sH', 0.2), ('tCH', None), ('sC', 0.6), ('tCG', None), ('sG', 0.2), ('tFG', None), ('sF', 1.0), ('_ta', 'sF')
        ])
    ]


class STAR_10S_2L_01(object):

    NETWORK_CAPACITY = [
        #A  B  C  D  E  F  G  H  I  J
        [3, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # A
        [0, 2, 1, 0, 0, 0, 0, 0, 0, 0],  # B
        [0, 0, 4, 2, 0, 0, 0, 1, 0, 0],  # C
        [0, 0, 0, 4, 1, 0, 0, 0, 1, 0],  # D
        [0, 0, 0, 0, 2, 1, 0, 0, 0, 0],  # E
        [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],  # F
        [0, 0, 0, 0, 0, 0, 3, 1, 0, 0],  # G
        [0, 0, 0, 0, 0, 0, 0, 2, 0, 0],  # H
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 1],  # I
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3],  # J
    ]

    NETWORK_DISTANCE = [
        #A  B  C  D  E  F  G  H  I  J
        [0, 10000, 0, 0, 0, 0, 0, 0, 0, 0],  # A
        [0, 0, 10000, 0, 0, 0, 0, 0, 0, 0],  # B
        [0, 0, 0, 10000, 0, 0, 0, 10000, 0, 0],  # C
        [0, 0, 0, 0, 10000, 0, 0, 0, 10000, 0],  # D
        [0, 0, 0, 0, 0, 10000, 0, 0, 0, 0],  # E
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # F
        [0, 0, 0, 0, 0, 0, 0, 10000, 0, 0],  # G
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # H
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 10000],  # I
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # J
    ]

    NETWORK_ID = [
        ['sA', 'tAB', 'tAC', 'tAD', 'tAE', 'tAF', 'tAG', 'tAH', 'tAI', 'tAJ'],
        ['tBA', 'sB', 'tBC', 'tBD', 'tBE', 'tBF', 'tBG', 'tBH', 'tBI', 'tBJ'],
        ['tCA', 'tCB', 'sC', 'tCD', 'tCE', 'tCF', 'tCG', 'tCH', 'tCI', 'tCJ'],
        ['tDA', 'tDB', 'tDC', 'sD', 'tDE', 'tDF', 'tDG', 'tDH', 'tDI', 'tDJ'],
        ['tEA', 'tEB', 'tEC', 'tED', 'sE', 'tEF', 'tEG', 'tEH', 'tEI', 'tEJ'],
        ['tFA', 'tFB', 'tFC', 'tFD', 'tFE', 'sF', 'tFG', 'tFH', 'tFI', 'tFJ'],
        ['tGA', 'tGB', 'tGC', 'tGD', 'tGE', 'tGF', 'sG', 'tGH', 'tGI', 'tGJ'],
        ['tHA', 'tHB', 'tHC', 'tHD', 'tHE', 'tHF', 'tHG', 'sH', 'tHI', 'tHJ'],
        ['tIA', 'tIB', 'tIC', 'tID', 'tIE', 'tIF', 'tIG', 'tIH', 'sI', 'tIJ'],
        ['tJA', 'tJB', 'tJC', 'tJD', 'tJE', 'tJF', 'tJG', 'tJH', 'tJI', 'sJ'],
    ]

    STATION_POSITION = [
        (2500, 7000),  # A
        (3500, 7000),  # B
        (4500, 5000),  # C
        (5500, 5000),  # D
        (6500, 7000),  # E
        (7500, 7000),  # F
        (2500, 3000),  # G
        (3500, 3000),  # H
        (6500, 3000),  # I
        (7500, 3000),  # J
    ]

    STATION_DEST_FACTOR = [
        1.0,  # A
        1.0,  # B
        0.8,  # C
        0.8,  # D
        1.0,  # E
        1.0,  # F
        1.0,  # G
        1.0,  # H
        1.0,  # I
        1.0,  # J
    ]

    MAX_PASSENGERS_PER_H = [
        200,  # A
        200,  # B
        400,  # C
        400,  # D
        200,  # E
        200,  # F
        200,  # G
        200,  # H
        200,  # I
        200,  # J
    ]

    TRAIN_CAPACITY = 600
    TRAIN_MAX_SPEED = 44  # m/S

    LINES = [
        ('tlABCDEF', [
            ('sA', 1.0), ('tAB', None), ('sB', 0.2), ('tBC', None), ('sC', 0.6), ('tCD', None), ('sD', 0.6),
            ('tDE', None), ('sE', 0.2), ('tEF', None), ('sF', 1.0), ('_ta', 'sF'),
            ('sF', 1.0), ('tEF', None), ('sE', 0.2), ('tDE', None), ('sD', 0.6), ('tCD', None), ('sC', 0.6),
            ('tBC', None), ('sB', 0.2), ('tAB', None), ('sA', 1.0), ('_ta', 'sA')
        ]),
        ('tlGHCDIJ', [
            ('sG', 1.0), ('tGH', None), ('sH', 0.2), ('tCH', None), ('sC', 0.6), ('tCD', None), ('sD', 0.6),
            ('tDI', None), ('sI', 0.2), ('tIJ', None), ('sJ', 1.0), ('_ta', 'sJ'),
            ('sJ', 1.0), ('tIJ', None), ('sI', 0.2), ('tDI', None), ('sD', 0.6), ('tCD', None), ('sC', 0.6),
            ('tCH', None), ('sH', 0.2), ('tGH', None), ('sG', 1.0), ('_ta', 'sG')
        ])
    ]


class STAR_14S_3L_01(object):

    NETWORK_CAPACITY = [
        #A  B  C  D  E  F  G  H  I  J  K  L  M  N
        [3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A
        [0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # B
        [0, 0, 4, 2, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],  # C
        [0, 0, 0, 4, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],  # D
        [0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # E
        [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],  # F
        [0, 0, 0, 0, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0],  # G
        [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],  # H
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0],  # I
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0],  # J
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 0],  # K
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],  # L
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],  # M
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],  # N
    ]

    NETWORK_DISTANCE = [
        #A  B  C  D  E  F  G  H  I  J  K  L  M  N
        [0, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A
        [0, 0, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # B
        [0, 0, 0, 10000, 0, 0, 0, 10000, 0, 0, 0, 10000, 0, 0],  # C
        [0, 0, 0, 0, 10000, 0, 0, 0, 10000, 0, 0, 0, 10000, 0],  # D
        [0, 0, 0, 0, 0, 10000, 0, 0, 0, 0, 0, 0, 0, 0],  # E
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # F
        [0, 0, 0, 0, 0, 0, 0, 10000, 0, 0, 0, 0, 0, 0],  # G
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # H
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 10000, 0, 0, 0, 0],  # I
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # J
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10000, 0, 0],  # K
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # L
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10000],  # M
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # N
    ]

    NETWORK_ID = [
        ['sA', 'tAB', 'tAC', 'tAD', 'tAE', 'tAF', 'tAG', 'tAH', 'tAI', 'tAJ', 'tAK', 'tAL', 'tAM', 'tAN'],
        ['tBA', 'sB', 'tBC', 'tBD', 'tBE', 'tBF', 'tBG', 'tBH', 'tBI', 'tBJ', 'tBK', 'tBL', 'tBM', 'tBN'],
        ['tCA', 'tCB', 'sC', 'tCD', 'tCE', 'tCF', 'tCG', 'tCH', 'tCI', 'tCJ', 'tCK', 'tCL', 'tCM', 'tCN'],
        ['tDA', 'tDB', 'tDC', 'sD', 'tDE', 'tDF', 'tDG', 'tDH', 'tDI', 'tDJ', 'tDK', 'tDL', 'tDM', 'tDN'],
        ['tEA', 'tEB', 'tEC', 'tED', 'sE', 'tEF', 'tEG', 'tEH', 'tEI', 'tEJ', 'tEK', 'tEL', 'tEM', 'tEN'],
        ['tFA', 'tFB', 'tFC', 'tFD', 'tFE', 'sF', 'tFG', 'tFH', 'tFI', 'tFJ', 'tFK', 'tFL', 'tFM', 'tFN'],
        ['tGA', 'tGB', 'tGC', 'tGD', 'tGE', 'tGF', 'sG', 'tGH', 'tGI', 'tGJ', 'tGK', 'tGL', 'tGM', 'tGN'],
        ['tHA', 'tHB', 'tHC', 'tHD', 'tHE', 'tHF', 'tHG', 'sH', 'tHI', 'tHJ', 'tHK', 'tHL', 'tHM', 'tHN'],
        ['tIA', 'tIB', 'tIC', 'tID', 'tIE', 'tIF', 'tIG', 'tIH', 'sI', 'tIJ', 'tIK', 'tIL', 'tIM', 'tIN'],
        ['tJA', 'tJB', 'tJC', 'tJD', 'tJE', 'tJF', 'tJG', 'tJH', 'tJI', 'sJ', 'tJK', 'tJL', 'tJM', 'tJN'],
        ['tKA', 'tKB', 'tKC', 'tKD', 'tKE', 'tKF', 'tKG', 'tKH', 'tKI', 'tKJ', 'sK', 'tKL', 'tKM', 'tKN'],
        ['tLA', 'tLB', 'tLC', 'tLD', 'tLE', 'tLF', 'tLG', 'tLH', 'tLI', 'tLJ', 'tLK', 'sL', 'tLM', 'tLN'],
        ['tMA', 'tMB', 'tMC', 'tMD', 'tME', 'tMF', 'tMG', 'tMH', 'tMI', 'tMJ', 'tMK', 'tML', 'sM', 'tMN'],
        ['tNA', 'tNB', 'tNC', 'tND', 'tNE', 'tNF', 'tNG', 'tNH', 'tNI', 'tNJ', 'tNK', 'tNL', 'tNM', 'sN'],
    ]

    STATION_POSITION = [
        (2500, 7000),  # A
        (3500, 7000),  # B
        (4500, 5000),  # C
        (5500, 5000),  # D
        (6500, 7000),  # E
        (7500, 7000),  # F
        (2500, 5000),  # G
        (3500, 5000),  # H
        (6500, 5000),  # I
        (7500, 5000),  # J
        (2500, 3000),  # K
        (3500, 3000),  # L
        (6500, 3000),  # M
        (7500, 3000),  # M
    ]

    STATION_DEST_FACTOR = [
        1.0,  # A
        1.0,  # B
        0.8,  # C
        0.8,  # D
        1.0,  # E
        1.0,  # F
        1.0,  # G
        1.0,  # H
        1.0,  # I
        1.0,  # J
        1.0,  # K
        1.0,  # L
        1.0,  # M
        1.0,  # N
    ]

    MAX_PASSENGERS_PER_H = [
        200,  # A
        200,  # B
        400,  # C
        400,  # D
        200,  # E
        200,  # F
        200,  # G
        200,  # H
        200,  # I
        200,  # J
        200,  # K
        200,  # L
        200,  # M
        200,  # N
    ]

    TRAIN_CAPACITY = 600
    TRAIN_MAX_SPEED = 44  # m/S

    LINES = [
        ('tlABCDEF', [
            ('sA', 1.0), ('tAB', None), ('sB', 0.2), ('tBC', None), ('sC', 0.6), ('tCD', None), ('sD', 0.6),
            ('tDE', None), ('sE', 0.2), ('tEF', None), ('sF', 1.0), ('_ta', 'sF'),
            ('sF', 1.0), ('tEF', None), ('sE', 0.2), ('tDE', None), ('sD', 0.6), ('tCD', None), ('sC', 0.6),
            ('tBC', None), ('sB', 0.2), ('tAB', None), ('sA', 1.0), ('_ta', 'sA')
        ]),
        ('tlGHCDIJ', [
            ('sG', 1.0), ('tGH', None), ('sH', 0.2), ('tCH', None), ('sC', 0.6), ('tCD', None), ('sD', 0.6),
            ('tDI', None), ('sI', 0.2), ('tIJ', None), ('sJ', 1.0), ('_ta', 'sJ'),
            ('sJ', 1.0), ('tIJ', None), ('sI', 0.2), ('tDI', None), ('sD', 0.6), ('tCD', None), ('sC', 0.6),
            ('tCH', None), ('sH', 0.2), ('tGH', None), ('sG', 1.0), ('_ta', 'sG')
        ]),
        ('tlKLCDMN', [
            ('sK', 1.0), ('tKL', None), ('sL', 0.2), ('tCL', None), ('sC', 0.6), ('tCD', None), ('sD', 0.6),
            ('tDM', None), ('sM', 0.2), ('tMN', None), ('sN', 1.0), ('_ta', 'sN'),
            ('sN', 1.0), ('tMN', None), ('sM', 0.2), ('tDM', None), ('sD', 0.6), ('tCD', None), ('sC', 0.6),
            ('tCL', None), ('sL', 0.2), ('tKL', None), ('sK', 1.0), ('_ta', 'sK')
        ])
    ]

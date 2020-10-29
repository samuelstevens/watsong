import math

import scipy.integrate as integrate
from typing import List, Dict, Any
from .spotify import album_from_title_artist, get_album_features, get_spotify


def get_intervals(value: float, rng: float) -> List[float]:
    neg = False
    if rng < 0:
        neg = True
        rng *= -1.0
        value *= -1.0

    offset = rng / 20.0
    result = [0.0, 0.0]
    if value + offset > rng:
        result[1] = rng
        result[0] = value - offset - (value + offset - rng)
    elif value - offset < 0:
        result[0] = 0.0
        result[1] = value + offset + (0 - value + offset)
    else:
        result[0] = value - offset
        result[1] = value + offset

    if neg:
        result[0], result[1] = -result[1], -result[0]
    return result


def gen_proc(features: Dict[str, float], alb: List[str]) -> float:
    fields: Dict[str, List[Any]] = {
        "danceability": [
            lambda x: (1050 * (math.e ** (-abs(x - 0.6) ** 2 / 0.06))) / 451,
            1,
        ],
        "energy": [
            lambda x: (715 * (math.e ** (-abs(x - 0.76) ** 2 / 0.27))) / 476.7,
            1,
        ],
        "speechiness": [lambda x: (115 + 4685 / (1 + (x / 0.05) ** 3)) / 398, 1],
        "acousticness": [lambda x: (267.5 + 2732.5 / (1 + (x / 0.04) ** 2)) / 434.8, 1],
        "valence": [
            lambda x: (451.4 * x ** 3 - 1636.9 * x ** 2 + 1177.2 * x + 324.5) / 480.4,
            1,
        ],
        "loudness": [
            lambda x: (3163.25 * (math.e ** (-((x + 6.7) ** 2)) / 13.3)) / 20351.4,
            -60,
        ],
        "tempo": [
            lambda x: (1777.6 * (math.e ** (-((x - 117.7) ** 2)) / 1212.1)) / 109692,
            225,
        ],
    }

    album = album_from_title_artist(alb[0], alb[1:], get_spotify())
    if album is not None:
        album_id = album.spotify_id
    f1 = features
    f2 = get_album_features([album_id])

    dot = 0.0
    dr = 0.0
    for k, v in fields.items():
        rng = get_intervals(f1[k], v[1])
        prob = integrate.quad(v[0], rng[0], rng[1])
        weight = 1 - prob[0]
        if k == "tempo":
            f1[k], f2[k] = f1[k] / 225, f2[k] / 225
        elif k == "loudness":
            f1[k], f2[k] = f1[k] / 60, f2[k] / 60
        dot += f1[k] * f2[k] * weight ** 1
        dr += (f1[k] ** 2 + f2[k] ** 2 - f1[k] * f2[k]) * weight ** 1

    return dot / dr

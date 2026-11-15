import bisect
import math
import os
import random
import time
import warnings
from functools import lru_cache
from pathlib import Path

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")

import pygame

VIEW_W, VIEW_H = 1500, 920
CANVAS_W, CANVAS_H = 1500, 1285
FPS = 30
TOTAL_FRAMES = 1143
DURATION = 38.089
SCALE = 32

WORDS = [
    "i hmangaih kha",
    "I Hmangaih Kha",
    "bawihte",
    "nun hlui",
    "rauthla",
    "ka thlah nang che",
    "♪ Fmaj7",
    "♫ Bbmaj7",
    "♩ Dm7",
    "♪ C7",
    "♫ Am7",
    "♪ F3 • Bb3 • D4",
    "♫ A4 • C5 • F4",
]

COLORS = [
    (255, 250, 245),
    (235, 245, 255),
    (176, 216, 255),
    (137, 189, 255),
    (79, 174, 255),
    (65, 212, 255),
]

LYRIC_TIMELINE = [
    (
        0.5,
        4.7,
        "♪  C(add9)  •  Bb/F  •  Fmaj7  ♫",
        "Intro Notes:  G4 → C4   |   F3 • Bb3 • D4 • Bb4   |   F3 • A4 • C4 • F4",
    ),
    (
        4.8,
        11.6,
        "Min liam san mai rawh, ka thlah mai nang che,",
        "Fmaj7  →  C7/E  →  Dm7  →  Bb  →  F     (Notes: F4 • A4 • C5 • E4 • D4)",
    ),
    (
        11.8,
        19.6,
        "I hlimna tur chuan min kal san ta la;",
        "Bbmaj7  →  C  →  F  →  Dm7  →  Gm7  →  C7     (Notes: C4 • D5 • Bb4 • G4)",
    ),
    (
        19.8,
        27.6,
        "Kei chuan rauthlain ka fang leh nun hlui,",
        "Fmaj7  →  Am7  →  Dm7  →  Bbmaj7  →  Am7     (Notes: F4 • A4 • E5 • D5 • C5)",
    ),
    (
        27.8,
        38.089,
        "Mahse maw, bawihte, kei ka ni i hmangaih kha",
        "Gm7  →  C7  →  Fmaj7  →  Bbmaj7  →  C7  →  F     (Notes: E5 • D4 • C5 • A4 • F4)",
    ),
]

CHORD_SEGMENTS = [
    (0.0, 'C'),
    (0.741, 'Bb'),
    (2.87, 'F'),
    (6.296, 'Am'),
    (8.611, 'Bb'),
    (10.648, 'F'),
    (12.407, 'Bb'),
    (14.167, 'F'),
    (16.481, 'Gm'),
    (18.148, 'C'),
    (20.0, 'C7'),
    (20.463, 'F'),
    (21.389, 'Fmaj7'),
    (22.13, 'Am'),
    (23.426, 'Fmaj7'),
    (23.981, 'Gm7'),
    (25.37, 'Bb'),
    (26.111, 'F'),
    (26.944, 'Fmaj7'),
    (27.87, 'Am'),
    (28.056, 'C'),
    (28.148, 'C7'),
    (29.074, 'Bb'),
    (29.167, 'C7'),
    (30.0, 'F'),
    (31.852, 'Gm7'),
    (31.944, 'Gm'),
    (33.796, 'C'),
    (35.556, 'F'),
]

CHORD_STARTS = [t for t, _ in CHORD_SEGMENTS]
CHORD_SYMBOLS = [c for _, c in CHORD_SEGMENTS]

OUTLINE_MARKS = [(0.0, 0.0), (0.15, 0.396), (0.32, 0.857), (0.65, 2.883), (1.0, 4.5)]
FILL_BEATS = [4.838, 5.289, 6.299, 6.738, 7.349, 7.674, 8.131, 8.434, 9.140]

PEAK_ROWS = [
    (0.857, 26, True),
    (1.823, 55, True),
    (2.883, 86, True),
    (5.289, 159, False),
    (9.14, 274, False),
    (10.587, 318, True),
    (12.501, 375, True),
    (14.413, 432, True),
    (16.356, 491, True),
    (17.835, 535, False),
    (19.254, 578, False),
    (24.743, 742, False),
    (26.439, 793, False),
    (26.96, 809, False),
    (29.917, 898, True),
    (34.401, 1032, False),
    (35.927, 1078, False),
    (36.416, 1092, False),
]

PEAK_CUES = [
    (frame_idx, 1.38 if sec == 35.927 else (1.0 if strong else 0.64))
    for sec, frame_idx, strong in PEAK_ROWS
]
SHIMMER_FRAMES = [frame_idx for frame_idx, _ in PEAK_CUES]

ENERGY = [1559, 1302, 1340, 1525, 1314, 1275, 1381, 1160, 1283, 1195, 1122, 1103, 1056, 1052, 951, 937, 851, 881, 917, 854, 903, 857, 875, 822, 824, 2296, 2212, 2199, 1902, 1949, 1718, 1749, 1776, 1758, 1686, 1679, 1594, 1641, 1645, 2259, 2477, 2267, 2353, 2401, 2397, 2365, 2212, 2085, 1994, 1940, 2014, 1879, 1807, 1468, 2021, 1530, 1644, 1593, 1557, 1562, 1625, 1558, 1451, 1474, 1404, 1380, 1384, 1255, 1211, 1254, 1047, 1074, 1109, 998, 1047, 952, 947, 983, 1021, 995, 1039, 1091, 1079, 1142, 1851, 2167, 2371, 2091, 2081, 1943, 2076, 2063, 1990, 1973, 1973, 1837, 1831, 1711, 1697, 1586, 1578, 1550, 1452, 1433, 1353, 1317, 1280, 1358, 1368, 1277, 1166, 1142, 1023, 1194, 1237, 1044, 1010, 985, 764, 710, 735, 714, 781, 835, 870, 858, 862, 829, 808, 747, 684, 581, 572, 566, 544, 591, 618, 630, 681, 597, 559, 2093, 4340, 6753, 8433, 6647, 6820, 7337, 4759, 6171, 7484, 6294, 6758, 7498, 7463, 7268, 6822, 7278, 7790, 7568, 7788, 7373, 7431, 6645, 6601, 6410, 6330, 4544, 1664, 1868, 1607, 2347, 2470, 5525, 4029, 3932, 3264, 3236, 4475, 3756, 3634, 4096, 4729, 4437, 4256, 4005, 4684, 5556, 3801, 3692, 3745, 4121, 4163, 3347, 3038, 3788, 3757, 3884, 4112, 4005, 3345, 4781, 4197, 3461, 3934, 3866, 4281, 3271, 3869, 3637, 4158, 4110, 3882, 2995, 1711, 1624, 2467, 2862, 2744, 3418, 2772, 3233, 3441, 3828, 3317, 3081, 2122, 1500, 2036, 1974, 1838, 1836, 1785, 1563, 1470, 1361, 1229, 1345, 1047, 889, 1040, 1150, 942, 916, 993, 793, 852, 682, 567, 657, 550, 518, 2077, 1828, 764, 810, 705, 1350, 1515, 2008, 3563, 3064, 3282, 3171, 2880, 2604, 2231, 2074, 1265, 1136, 920, 2225, 2673, 3451, 2627, 2836, 3353, 3877, 3684, 3643, 3298, 2979, 2808, 2748, 2731, 3081, 3438, 3226, 2603, 2722, 2590, 2224, 1856, 2317, 3024, 3298, 3092, 3053, 1718, 965, 911, 1015, 1119, 2517, 2621, 3144, 3139, 2961, 2960, 3350, 2664, 2426, 2170, 2315, 2775, 2651, 2438, 2553, 2195, 1660, 2769, 1702, 1434, 1380, 1603, 1501, 1217, 966, 842, 732, 1061, 1047, 1244, 1291, 1334, 1392, 1229, 1576, 1226, 1462, 1426, 1260, 1435, 1209, 1320, 1262, 1295, 1214, 1264, 1208, 1220, 1207, 1150, 1203, 996, 1075, 934, 906, 1037, 844, 859, 798, 740, 740, 597, 599, 553, 1862, 4083, 5350, 2741, 1734, 3142, 5562, 6120, 4463, 5181, 6090, 5811, 5781, 5822, 5622, 4651, 5216, 5348, 5358, 5212, 5848, 4979, 4787, 4247, 4019, 4579, 4139, 4296, 4316, 3793, 3356, 1349, 1294, 976, 1280, 1144, 2463, 2767, 3051, 3559, 3422, 2938, 2901, 3105, 3931, 3944, 3224, 1322, 1301, 875, 821, 1917, 3669, 4000, 3867, 3644, 3894, 3558, 3245, 3348, 2739, 2914, 2668, 2311, 3414, 3282, 2991, 3090, 2538, 2796, 2292, 2286, 2369, 2027, 1367, 1156, 907, 766, 552, 1124, 1361, 1329, 1658, 1473, 1740, 1536, 1465, 1183, 1174, 1201, 1252, 1193, 1147, 3334, 4179, 4954, 5312, 5580, 4094, 4681, 4708, 4389, 4416, 4342, 4447, 3148, 857, 1071, 964, 3575, 3525, 3637, 3765, 3424, 4159, 4007, 4231, 3961, 4835, 4208, 3774, 4208, 3546, 4970, 4453, 3134, 3772, 3806, 4416, 3191, 2885, 2886, 1896, 908, 541, 899, 1403, 1743, 3009, 3696, 3481, 3773, 3867, 4136, 4447, 4120, 4181, 4089, 2156, 1106, 1177, 1631, 3551, 3263, 3294, 3308, 2887, 3145, 2457, 2276, 2047, 2326, 2252, 2481, 3289, 3617, 3245, 2966, 2868, 2926, 3145, 3120, 2868, 2563, 3230, 3080, 3080, 3215, 3449, 3585, 3399, 3429, 3255, 2855, 3023, 3055, 2973, 2479, 2283, 2455, 2626, 3015, 2481, 2121, 2562, 2347, 2795, 2273, 1884, 2054, 1830, 1794, 1735, 1645, 1572, 1215, 1252, 1233, 1218, 1384, 1352, 1754, 1797, 1759, 1673, 1556, 1627, 1492, 1383, 1456, 1391, 1479, 1468, 1414, 2305, 2498, 2587, 2516, 2317, 2060, 1764, 1657, 1769, 1540, 1405, 1443, 1316, 1189, 2191, 3506, 5227, 5514, 5382, 5609, 5335, 4287, 4885, 4939, 4470, 3139, 1475, 1338, 1298, 2420, 5801, 5812, 5356, 4615, 4498, 4689, 4677, 4616, 4444, 4568, 4567, 4676, 4610, 2247, 3639, 3697, 3197, 2964, 2905, 2694, 2321, 2452, 2787, 3440, 2738, 1320, 1517, 1381, 1193, 935, 948, 1527, 2308, 2431, 2879, 2345, 2365, 2753, 3065, 2864, 2239, 2346, 2229, 2631, 3206, 2974, 2524, 2773, 2852, 2447, 2353, 2215, 2813, 2200, 2082, 1990, 1831, 1302, 1816, 2142, 2805, 3867, 3531, 3861, 2478, 3582, 2259, 1806, 1526, 888, 719, 1928, 3358, 1765, 1980, 2232, 2295, 1623, 1276, 1523, 1497, 1435, 1546, 1111, 1057, 1148, 933, 1034, 993, 879, 878, 650, 819, 629, 1755, 3223, 1925, 786, 542, 465, 1428, 1832, 4066, 3340, 3053, 3491, 3445, 3184, 3217, 3418, 3744, 3943, 4380, 4114, 3730, 3377, 3401, 3862, 4114, 3423, 4428, 3205, 2891, 2555, 2145, 1854, 1316, 1328, 2323, 2445, 2885, 2839, 2953, 2855, 2848, 2941, 3252, 4026, 3977, 3971, 3738, 1575, 908, 1151, 981, 1436, 2865, 3180, 3620, 3587, 4342, 4690, 4451, 4599, 4753, 4452, 4141, 4160, 4043, 4339, 4621, 4274, 3938, 3900, 4392, 3062, 2975, 1964, 3797, 4622, 4443, 3783, 2999, 2045, 2012, 3007, 3788, 2732, 1502, 1567, 2269, 1973, 2332, 1536, 1655, 942, 1042, 1362, 1157, 1211, 1159, 1007, 855, 815, 829, 781, 744, 682, 606, 631, 675, 923, 1191, 1003, 963, 760, 756, 673, 659, 677, 584, 548, 527, 476, 1602, 2924, 3064, 3165, 2827, 2769, 2479, 2301, 2257, 2054, 1996, 1438, 1223, 1075, 1061, 1133, 1055, 1676, 3964, 3796, 3440, 3733, 4156, 3894, 3791, 4266, 4397, 4185, 3812, 3586, 4046, 4674, 3472, 2953, 2695, 2976, 3202, 2465, 1951, 2525, 2503, 2800, 2551, 2751, 1798, 1813, 1468, 2532, 3184, 3147, 3281, 2858, 2577, 3522, 3407, 3180, 3373, 3294, 3103, 3436, 3917, 3890, 3074, 2017, 1361, 1011, 718, 990, 754, 1748, 2915, 3118, 3085, 3021, 3695, 3355, 3220, 3196, 3289, 3398, 2799, 2669, 2323, 2044, 1572, 1551, 1622, 1517, 1544, 1286, 1435, 1442, 1355, 1345, 1342, 1276, 1276, 1270, 1180, 1122, 1096, 971, 890, 869, 790, 2066, 3938, 4263, 4555, 4791, 4442, 4669, 4540, 4587, 3091, 359, 371, 455, 625, 2098, 3657, 3278, 2993, 2984, 2729, 2501, 2897, 2861, 2833, 3106, 3088, 3180, 3205, 2850, 2631, 2891, 2838, 2819, 3059, 2500, 2579, 2923, 3248, 3612, 3069, 2953, 2738, 3784, 2986, 2553, 2966, 2472, 3020, 2492, 2824, 2442, 2085, 1535, 1655, 1891, 2469, 2148, 1134, 1067, 1016, 787, 741, 700, 619, 652, 571, 539, 1210, 3196, 2165, 930, 692, 1917, 2252, 3435, 3323, 3007, 2975, 3165, 3372, 3375, 3370, 3354, 3381, 3363, 3107, 3725, 3889, 3618, 3015, 2822, 2852, 2747, 2504, 2233, 2448, 2478, 2714, 2122, 2459, 2522, 2834, 3137, 2931, 3158, 3275, 3030, 2645, 2368, 2909, 2436, 1943, 1713, 1532, 1454, 1376, 1397, 1472, 2844, 2944, 2965, 2765, 3040, 2879, 3447, 2938, 3048, 3232, 2882, 3027, 2860, 3496, 3083, 3554, 3142, 3399, 3107, 3533, 3152, 3197, 3154, 4176, 4394, 4318, 3593, 3052, 1923, 1856, 2008, 2031, 2101, 2710, 3902, 3703, 2639, 2366, 3090, 2640, 1952, 2524, 2887, 2765, 1812, 2197, 2386, 1800, 1757, 1715, 1852, 1759, 1391, 1299, 1163, 1165, 1007, 1034, 957, 782, 850, 859, 782, 791, 712, 723, 760, 859, 787, 684, 1299, 1835, 2069, 2113, 2105, 2164, 1898, 1973, 1982, 1902, 1822, 1697, 1648, 1703, 1343]
BASELINE = sorted(ENERGY)[len(ENERGY) * 3 // 4]

PHRASES = []
for _s, _e, _line, _ in LYRIC_TIMELINE[1:]:
    _w = _line.split()
    PHRASES.append((_s, _e, [" ".join(_w[i : i + 2]) for i in range(0, len(_w), 2)]))


def heart_xy(t):
    x = 16 * (math.sin(t) ** 3)
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    return x, -y


def to_screen(x, y):
    return x * SCALE + CANVAS_W / 2, y * SCALE * 1.12 + 463


def outline_cue(progress):
    for (left, t0), (right, t1) in zip(OUTLINE_MARKS, OUTLINE_MARKS[1:]):
        if progress <= right:
            return round(60 * (t0 + (t1 - t0) * (progress - left) / (right - left)))
    return round(60 * OUTLINE_MARKS[-1][1])


def fill_cue(p):
    radius = min(1.0, math.hypot((p.x - 750) / 500, (p.y - 490) / 405))
    travel = min(0.999, max(0.0, (1.0 - radius) * 1.12))
    phase = int(travel * len(FILL_BEATS))
    return round(60 * (FILL_BEATS[phase] + (p.order % 7) * 0.012))


@lru_cache(maxsize=2400)
def peak_pulse(tick):
    value = 0.0
    for cue, weight in PEAK_CUES:
        delta = tick - cue * 2
        span = 8 if delta < 0 else 23
        if abs(delta) < span:
            value = max(value, weight * (0.5 + 0.5 * math.cos(math.pi * delta / span)))
    return value


def beat_brightness(tick, flicker):
    return min(1.0, 0.82 + 0.08 * math.sin(tick * 0.04 + flicker) + 0.10 * peak_pulse(tick - 1))


@lru_cache(maxsize=256)
def dot_text(word, size, color):
    font = pygame.font.SysFont("consolas", size, bold=True)
    glyph = font.render(word, True, (255, 255, 255)).convert_alpha()
    step = 4
    cols = max(1, round(glyph.get_width() / step))
    rows = max(1, round(glyph.get_height() / step))
    mask = pygame.transform.smoothscale(glyph, (cols, rows))
    dots = pygame.Surface((cols * step, rows * step), pygame.SRCALPHA)
    for y in range(rows):
        for x in range(cols):
            if mask.get_at((x, y)).a >= 60:
                pygame.draw.circle(
                    dots,
                    (*color, 255),
                    (x * step + step // 2, y * step + step // 2),
                    step // 2,
                )
    return dots


@lru_cache(maxsize=900)
def soft_halo(glyph, color, padding, blur):
    silhouette = pygame.mask.from_surface(glyph, 50).to_surface(
        setcolor=(*color, 255), unsetcolor=(0, 0, 0, 0)
    )
    padded = pygame.Surface(
        (glyph.get_width() + 2 * padding, glyph.get_height() + 2 * padding),
        pygame.SRCALPHA,
    )
    padded.blit(silhouette, (padding, padding))
    coarse = pygame.transform.smoothscale(
        padded, (max(2, padded.get_width() // blur), max(2, padded.get_height() // blur))
    )
    return pygame.transform.smoothscale(coarse, padded.get_size())


@lru_cache(maxsize=360)
def split_amount(tick):
    f = tick / 2.0
    if f <= 260 or f >= 318:
        return 0.0
    if f <= 274:
        progress = (f - 260) / (274 - 260)
        return 0.5 - 0.5 * math.cos(math.pi * progress)
    if f <= 290:
        return 1.0
    progress = (f - 290) / (318 - 290)
    return 0.5 + 0.5 * math.cos(math.pi * progress)


@lru_cache(maxsize=360)
def memory_spread(tick):
    frame_index = tick / 2.0
    keys = ((608, 0.0), (623, 0.34), (682, 1.0), (717, 0.83), (742, 0.0))
    for (start, low), (end, high) in zip(keys, keys[1:]):
        if start <= frame_index <= end:
            u = (frame_index - start) / (end - start)
            return low + (high - low) * (0.5 - 0.5 * math.cos(math.pi * u))
    return 0.0


class Particle:
    __slots__ = (
        "x",
        "y",
        "order",
        "kind",
        "word",
        "color",
        "alpha",
        "flicker",
        "delay",
        "size_mult",
        "txt_surf",
        "glow_small",
        "glow_big",
    )

    def __init__(self, x, y, order, kind, base_font_size):
        self.x = x
        self.y = y
        self.order = order
        self.kind = kind
        self.word = random.choice(WORDS)
        self.color = random.choice(COLORS)
        self.alpha = 0
        self.flicker = random.uniform(0, math.pi * 2)
        self.delay = 0
        self.size_mult = random.uniform(0.85, 1.15)

        scaled_size = max(11, int(base_font_size * self.size_mult))
        font = pygame.font.SysFont("arial", scaled_size, bold=True)
        txt = font.render(self.word, True, self.color).convert_alpha()

        max_word_width = max(1, int(2 * (min(x, CANVAS_W - x) - 24) / 1.72))
        if txt.get_width() > max_word_width:
            fitted_height = max(1, round(txt.get_height() * max_word_width / txt.get_width()))
            txt = pygame.transform.smoothscale(txt, (max_word_width, fitted_height))

        self.txt_surf = txt
        self.glow_small = pygame.transform.smoothscale(
            txt, (max(1, int(txt.get_width() * 1.6)), max(1, int(txt.get_height() * 1.6)))
        )
        self.glow_big = pygame.transform.smoothscale(
            txt, (max(1, int(txt.get_width() * 2.4)), max(1, int(txt.get_height() * 2.4)))
        )


def build_outline_particles(n_outline=160, min_gap=57):
    particles = []
    placed = []
    for i in range(n_outline):
        t = (i / n_outline) * 2 * math.pi
        bx, by = heart_xy(t)
        sx, sy = to_screen(bx, by)
        if any(math.hypot(sx - px, sy - py) < min_gap for (px, py) in placed):
            continue
        placed.append((sx, sy))
        particles.append(Particle(sx, sy, i, "outline", base_font_size=40))
    return particles


def build_fill_particles(n_fill=130, min_gap=84):
    particles = []
    placed = []
    attempts = 0
    max_attempts = n_fill * 80
    while len(particles) < n_fill and attempts < max_attempts:
        attempts += 1
        t = random.uniform(0, 2 * math.pi)
        r = random.uniform(0.0, 0.86)
        bx, by = heart_xy(t)
        sx, sy = to_screen(bx * r, by * r)
        if any(math.hypot(sx - qx, sy - qy) < min_gap for (qx, qy) in placed):
            continue
        placed.append((sx, sy))
        particles.append(Particle(sx, sy, random.randint(0, 320), "fill", base_font_size=34))
    return particles


def find_song():
    source_dir = Path(__file__).resolve().parent
    names = ("ihmangaihkha.mp3", "i hmangaih kha.mp3", "i_hmangaih_kha.mp3")
    for folder in (source_dir, Path.cwd(), Path.home() / "Downloads"):
        for name in names:
            candidate = folder / name
            if candidate.is_file():
                return candidate
    raise SystemExit("Put ihmangaihkha.mp3 next to this script or in Downloads.")


def main():
    song_path = find_song()
    random.seed(42)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(str(song_path))

    desktop = pygame.display.get_desktop_sizes()[0]
    win_scale = min(1.0, (desktop[0] - 40) / VIEW_W, (desktop[1] - 80) / VIEW_H)
    preview = pygame.display.set_mode((round(VIEW_W * win_scale), round(VIEW_H * win_scale)))
    pygame.display.set_caption("I Hmangaih Kha ♡")
    clock = pygame.time.Clock()

    font_center = pygame.font.SysFont("consolas", 54, bold=True)
    chord_font = pygame.font.SysFont("segoeui", 31, bold=True)
    active_chord_font = pygame.font.SysFont("segoeui", 41, bold=True)
    intro_font = pygame.font.SysFont("segoeui", 24, bold=True)

    @lru_cache(maxsize=24)
    def chord_glyph(chord):
        return active_chord_font.render(chord, True, (238, 255, 255))

    outline = build_outline_particles(n_outline=160)
    fill = build_fill_particles(n_fill=130)
    outline_span = max(p.order for p in outline) if outline else 1

    for p in outline:
        p.delay = outline_cue(p.order / outline_span)
    for p in fill:
        p.delay = fill_cue(p)

    particles = outline + fill
    particle_order = {}
    texture_cache = {}

    heart_surface = pygame.Surface((CANVAS_W, CANVAS_H)).convert()
    glow_layer = pygame.Surface((CANVAS_W, CANVAS_H), pygame.SRCALPHA)
    text_layer = pygame.Surface((CANVAS_W, CANVAS_H), pygame.SRCALPHA)
    canvas = pygame.Surface((VIEW_W, VIEW_H))

    trace_layer = pygame.Surface((CANVAS_W, CANVAS_H), pygame.SRCALPHA)
    trace_pts = [to_screen(*heart_xy(i * math.tau / 180)) for i in range(180)]
    pygame.draw.lines(trace_layer, (25, 119, 255, 66), True, trace_pts, 13)
    pygame.draw.lines(trace_layer, (75, 191, 255, 175), True, trace_pts, 3)

    def draw_particle(p, alpha, elapsed, sim_tick, pulse, phrase):
        x, y = p.x, p.y
        saved = p.txt_surf, p.glow_small, p.glow_big
        memory_light = 0.0
        try:
            p.x = x + (x - 750) * 0.048 * pulse
            p.y = y + (y - 463) * 0.028 * pulse
            if p.kind == "fill" and phrase >= 0:
                section_time = elapsed - PHRASES[phrase][0]
                if p.order % 4 == 0:
                    wave = (1.0 - math.exp(-2.8 * section_time)) * math.exp(-0.38 * section_time)
                    if phrase == 1:
                        p.x += (1 if x > 750 else -1) * 43 * wave
                        p.y += 12 * wave
                    elif phrase == 2:
                        p.y -= 9 * wave
                        p.x += 6 * math.sin(elapsed * 1.8 + p.flicker) * wave
                    elif phrase == 3:
                        p.x -= (x - 750) * 0.065 * wave
                        p.y -= (y - 463) * 0.05 * wave

                i = particle_order.setdefault(p, len(particle_order))
                if i % 3 != 2:
                    chunks = PHRASES[phrase][2]
                    memory_index = -1
                    if phrase == 2:
                        for moment, ox, oy, w_idx in (
                            (23.884, 570, 650, 0),
                            (24.743, 920, 480, 1),
                            (26.439, 690, 325, 0),
                        ):
                            dist = math.hypot(x - ox, y - oy)
                            age = elapsed - moment - dist * 0.0007
                            if 0.0 <= age <= 0.68 and dist < 330:
                                power = (math.sin(math.pi * age / 0.68) ** 0.55) * (1.0 - dist / 500.0)
                                if power > memory_light:
                                    memory_light, memory_index = power, w_idx
                        if memory_light > 0.13:
                            chunks = PHRASES[memory_index][2]
                            p.y -= 12 * memory_light
                            p.x += 8 * memory_light * math.sin(p.flicker)
                        else:
                            memory_index = -1

                    word = chunks[(i - i // 3) % len(chunks)]
                    key = (p, phrase, memory_index)
                    if key not in texture_cache:
                        font = pygame.font.SysFont("arial", max(21, round(33 * p.size_mult)), bold=True)
                        surf = font.render(word, True, p.color).convert_alpha()
                        limit = max(1, int(2 * (min(x, CANVAS_W - x) - 49) / 1.72))
                        if surf.get_width() > limit:
                            surf = pygame.transform.smoothscale(
                                surf,
                                (limit, max(1, round(surf.get_height() * limit / surf.get_width()))),
                            )
                        texture_cache[key] = (
                            surf,
                            *(
                                pygame.transform.smoothscale(
                                    surf,
                                    (round(surf.get_width() * k), round(surf.get_height() * k)),
                                )
                                for k in (1.6, 2.4)
                            ),
                        )
                    p.txt_surf, p.glow_small, p.glow_big = texture_cache[key]

            split = split_amount(sim_tick)
            if split:
                side = -1 if x < 750 else 1
                p.x += side * (107 - 0.145 * abs(x - 750)) * split
                p.y += side * 17 * split

            spread = memory_spread(sim_tick)
            if spread:
                if p.kind == "fill":
                    col = -1 if x < 750 else 1
                    tier = -1 if y < 515 else 1
                    lift = 58 if tier < 0 else 33
                    p.x += col * (45 + 41 * (1.0 - min(1.0, abs(x - 750) / 390.0))) * spread
                    p.y += tier * lift * spread
                    alpha = round(alpha * (1.0 - 0.22 * spread))
                else:
                    p.x += (x - 750) * 0.014 * spread

            margin = p.txt_surf.get_width() / 2 + 14
            p.x = max(margin, min(CANVAS_W - margin, p.x))

            if y > 805:
                release = 1092 / 30.0
            elif abs(x - 750) > 240 or y > 650:
                release = 1109 / 30.0
            else:
                release = 1130 / 30.0
            release += ((p.order * 17) % 9) / 130.0
            drain = max(0.0, elapsed - release)

            if elapsed >= DURATION:
                alpha = 0
            if drain > 0:
                u = min(1.0, drain / 0.83)
                pull = min(0.91, 0.35 * u + 0.56 * u * u)
                p.x += (750 - x) * pull + 17 * math.sin(p.flicker + 7 * drain) * u
                p.y += (1000 - y) * (0.62 * u * u) + 115 * u
                fade = max(0.0, min(1.0, (DURATION - elapsed) / max(0.1, DURATION - release), (1094 - p.y) / 110.0))
                alpha = round(alpha * fade)
                streak = 16 + round(102 * u)
                if alpha > 0 and p.order % 3 != 1:
                    tint = (max(65, p.color[0] // 2), max(128, p.color[1]), 255)
                    tail_x = round(p.x + (x - 750) * 0.08 * u)
                    pygame.draw.line(
                        glow_layer,
                        (*tint, round(alpha * 0.24)),
                        (tail_x, round(p.y - streak)),
                        (round(p.x), round(p.y + 3)),
                        max(1, round(5 - 2 * u)),
                    )
                    pygame.draw.circle(
                        glow_layer,
                        (*tint, round(alpha * 0.47)),
                        (round(p.x), round(p.y + 7)),
                        max(2, round(4 - 2 * u)),
                    )

            phase_y = min(1.0, max(0.0, (990 - y) / 900.0))
            frame_pos = sim_tick / 2.0
            latest = bisect.bisect_right(SHIMMER_FRAMES, frame_pos) - 1
            glint = 0.0
            if latest >= 0 and elapsed < 36.4:
                age = frame_pos - SHIMMER_FRAMES[latest]
                glint = math.exp(-(((age - (1.0 + phase_y * 12.0)) / 2.8) ** 2))

            phrase_ripple = 0.0
            if 19.75 <= elapsed <= 21.15:
                phrase_ripple = max(
                    math.exp(-(((elapsed - onset - phase_y * 0.42) / 0.075) ** 2))
                    for onset in (19.792, 20.281, 20.776)
                )

            light = max(0.62 * glint, phrase_ripple)
            if elapsed < 36.4:
                wave = math.sin(elapsed * 4.2 + y * 0.015 + x * 0.004)
                drift = math.cos(elapsed * 2.9 + x * 0.011 - y * 0.004)
                is_outline = p.kind == "outline"
                p.x += (7 if is_outline else 11) * drift + (x - 750) * 0.021 * light
                p.y += (5 if is_outline else 9) * wave - (11 if is_outline else 17) * light
                p.x = max(margin, min(CANVAS_W - margin, p.x))
                alpha = min(255, round(alpha * (1.0 + 0.22 * light)))

            if alpha <= 0:
                return

            halo = soft_halo(
                p.txt_surf,
                (121, 195, 255) if memory_light > 0.13 else (42, 167, 255),
                12,
                6,
            )
            halo.set_alpha(
                round(min(255, alpha * (0.10 + 0.76 * pulse + 0.59 * light + 0.65 * memory_light + 0.22 * spread)))
            )
            glow_layer.blit(halo, halo.get_rect(center=(p.x, p.y)))

            p.glow_big.set_alpha(alpha // 9)
            glow_layer.blit(p.glow_big, p.glow_big.get_rect(center=(p.x, p.y)))
            p.glow_small.set_alpha(alpha // 3)
            glow_layer.blit(p.glow_small, p.glow_small.get_rect(center=(p.x, p.y)))

            glyph = p.txt_surf
            if drain > 0:
                u = min(1.0, drain / 0.55)
                glyph = pygame.transform.smoothscale(
                    glyph,
                    (
                        max(1, round(glyph.get_width() * (1.0 - 0.84 * u))),
                        max(1, round(glyph.get_height() * (1.0 + 0.70 * u))),
                    ),
                )
            glyph.set_alpha(alpha)
            text_layer.blit(glyph, glyph.get_rect(center=(p.x, p.y)))
        finally:
            p.x, p.y = x, y
            p.txt_surf, p.glow_small, p.glow_big = saved

    def draw_chords(surface, elapsed, sim_tick):
        active_index = max(0, bisect.bisect_right(CHORD_STARTS, elapsed) - 1)
        first = max(0, min(active_index - 2, len(CHORD_SYMBOLS) - 5))
        chords = CHORD_SYMBOLS[first : first + 5]
        active = active_index - first
        widths = [
            (active_chord_font if i == active else chord_font).size(c)[0]
            for i, c in enumerate(chords)
        ]
        gap = 38
        x = (surface.get_width() - sum(widths) - gap * (len(chords) - 1)) // 2
        idx = min(len(ENERGY) - 1, int(elapsed * 30))
        local = max(ENERGY[max(0, idx - 2) : idx + 1])
        pulse = min(1.0, local / max(1, BASELINE))

        for i, chord in enumerate(chords):
            current = i == active
            word = (active_chord_font if current else chord_font).render(
                chord, True, (238, 255, 255) if current else (149, 183, 218)
            )
            y = 1143 - word.get_height() // 2
            if current:
                hit = peak_pulse(sim_tick)
                halo = soft_halo(chord_glyph(chord), (38, 186, 255), 17, 7)
                halo.set_alpha(round(min(255, 155 + 55 * pulse + 60 * hit)))
                surface.blit(
                    halo,
                    halo.get_rect(center=(x + word.get_width() / 2, y + word.get_height() / 2)),
                )
            surface.blit(word, (x, y))
            x += widths[i] + gap
            if i < len(chords) - 1:
                arrow = intro_font.render("→", True, (130, 177, 217))
                surface.blit(arrow, (x - gap + 9, 1143 - arrow.get_height() // 2))

    pygame.mixer.music.play()
    started_at = time.perf_counter()
    prev_sim_tick = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

        pos_ms = pygame.mixer.music.get_pos() if pygame.mixer.music.get_busy() else -1
        wall_elapsed = time.perf_counter() - started_at
        elapsed = (pos_ms / 1000.0) if pos_ms >= 0 else wall_elapsed

        sim_tick = max(prev_sim_tick + 1, round(elapsed * 60))
        tick_step = max(1, sim_tick - prev_sim_tick)
        prev_sim_tick = sim_tick

        heart_surface.fill((0, 0, 0))
        glow_layer.fill((0, 0, 0, 0))
        text_layer.fill((0, 0, 0, 0))

        pulse = peak_pulse(sim_tick)
        phrase = next(
            (i for i, (s, e, _) in enumerate(PHRASES) if s <= elapsed <= e),
            -1,
        )

        for p in particles:
            if sim_tick > p.delay and p.alpha < 255:
                p.alpha = min(255, p.alpha + (14 + random.randint(0, 4)) * tick_step)
            flick = beat_brightness(sim_tick, p.flicker) if p.alpha >= 255 else 1.0
            alpha = int(p.alpha * flick)
            if alpha > 0:
                draw_particle(p, alpha, elapsed, sim_tick, pulse, phrase)

        heart_surface.blit(glow_layer, (0, 0))
        heart_surface.blit(text_layer, (0, 0))

        if elapsed <= 0.72:
            intensity = max(0.0, 1.0 - abs(elapsed - 0.105) / (0.12 if elapsed < 0.105 else 0.615))
            trace_layer.set_alpha(round(145 * intensity))
            heart_surface.blit(trace_layer, (0, 0))

        active_lyric = None
        for s_t, e_t, mizo_line, chord_line in LYRIC_TIMELINE[1:]:
            if s_t <= elapsed <= e_t:
                active_lyric = (s_t, e_t, mizo_line, chord_line)
                break
        if active_lyric is None and elapsed > LYRIC_TIMELINE[-1][1]:
            active_lyric = LYRIC_TIMELINE[-1]

        if active_lyric is not None:
            s_t, e_t, mizo_line, _ = active_lyric
            typing_ratio = 0.74 if active_lyric == LYRIC_TIMELINE[-1] else 0.85
            typing_dur = (e_t - s_t) * typing_ratio
            typing_prog = min(1.0, max(0.0, (elapsed - s_t) / typing_dur))
            chars = 1 + int(typing_prog * (len(mizo_line) - 1))
            visible_line = mizo_line[:chars]

            center_surf = pygame.Surface(font_center.size(mizo_line), pygame.SRCALPHA)
            typed_surf = dot_text(visible_line, 54, (255, 250, 245))
            center_surf.blit(typed_surf, (0, 0))

            text_pulse = 1.0 + 0.025 * math.sin(sim_tick * 0.05)
            nw = max(1, int(center_surf.get_width() * text_pulse))
            nh = max(1, int(center_surf.get_height() * text_pulse))
            center_surf = pygame.transform.smoothscale(center_surf, (nw, nh))

            glow_center = pygame.transform.smoothscale(
                center_surf,
                (int(center_surf.get_width() * 1.035), int(center_surf.get_height() * 1.035)),
            )
            glow_center.set_alpha(255 // 15)
            heart_surface.blit(glow_center, glow_center.get_rect(center=(CANVAS_W / 2, 1240)))
            heart_surface.blit(center_surf, center_surf.get_rect(center=(CANVAS_W / 2, 1240)))

        draw_chords(heart_surface, elapsed, sim_tick)

        canvas.fill((0, 0, 0))
        margin = 26
        fit_scale = min(
            (VIEW_W - 2 * margin) / CANVAS_W,
            (VIEW_H - 2 * margin) / CANVAS_H,
        )
        scaled_size = (round(CANVAS_W * fit_scale), round(CANVAS_H * fit_scale))
        output = pygame.transform.smoothscale(heart_surface, scaled_size)
        canvas.blit(output, output.get_rect(center=(VIEW_W // 2, VIEW_H // 2)))

        picture = (
            canvas
            if preview.get_size() == canvas.get_size()
            else pygame.transform.smoothscale(canvas, preview.get_size())
        )
        preview.blit(picture, (0, 0))
        pygame.display.flip()

        if elapsed >= DURATION + 0.3:
            waiting = True
            while waiting:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT or (
                        ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE
                    ):
                        waiting = False
                        running = False
                pygame.time.wait(20)
        else:
            clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
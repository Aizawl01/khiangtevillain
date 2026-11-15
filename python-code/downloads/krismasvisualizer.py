#!/usr/bin/env python3
"""
render_lidar_mp4.py — Standalone Self-Contained 30 FPS MP4 Video Renderer
Aizawl 3D LiDAR Point-Cloud ASCII Christmas Tree (720x1280 Vertical 9:16)
Includes:
- 3-Mode Lyric Selector Table (Mode 1: Sky Starlight Stage + Vocal EQ default)
- Concentric Cyan LiDAR Topographic Ground Rings & Sweeping Laser Scan Beams
- Separated Left Foreground Gift Cluster (x = -0.95 .. -0.22) with 3D Bows
- Enlarged 1.8x Right Foreground 3D Nativity Pavilion (nat_x = +0.82, nat_z = +0.82)
- Self-contained 30 FPS RMS, Bass (35-180 Hz), and Vocal (280-3,400 Hz) envelopes
"""

import argparse
import os
import pygame
import shutil
from pathlib import Path
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 720, 1280
FPS = 30
DURATION = 15.074
TOTAL_FRAMES = int(round(FPS * DURATION))

TOP_H = 836
BAR_H = 34
BOT_Y = TOP_H + BAR_H
BOT_H = H - BOT_Y

CW, CH = 5, 8
COLS = 140  # 700px wide
ROWS = 94   # 752px tall

TAU = 2.0 * np.pi
Y0, Y1 = 0.42, 2.55
NEEDLE, TRUNK, BALL, LIGHT, GARLAND, GIFT, RIBBON, SNOWCAP, GROUND, STAR, NATIVITY = range(11)
RAMP_STR = " .:-=+*#%@"
CIPHER_CHARS = ".:-=+*#%@"

# Embedded 30 FPS audio envelopes extracted from nov christmas song mizo.mp3 (135.7 BPM)
RMS_ENV_30 = np.array([0.058, 0.6, 0.733, 0.518, 0.398, 0.313, 0.19, 0.106, 0.097, 0.127, 0.437, 0.532, 0.4, 0.332, 0.403, 0.569, 0.736, 0.694, 0.512, 0.477, 0.494, 0.427, 0.322, 0.388, 0.49, 0.527, 0.454, 0.538, 0.644, 0.576, 0.517, 0.486, 0.443, 0.428, 0.43, 0.368, 0.304, 0.323, 0.347, 0.307, 0.316, 0.529, 0.734, 0.702, 0.632, 0.597, 0.492, 0.42, 0.414, 0.514, 0.535, 0.481, 0.565, 0.746, 0.928, 0.851, 0.597, 0.535, 0.542, 0.514, 0.451, 0.492, 0.474, 0.389, 0.308, 0.323, 0.415, 0.559, 0.664, 0.653, 0.636, 0.539, 0.382, 0.311, 0.278, 0.287, 0.383, 0.422, 0.44, 0.54, 0.628, 0.669, 0.615, 0.537, 0.486, 0.513, 0.525, 0.469, 0.444, 0.402, 0.458, 0.566, 0.524, 0.42, 0.541, 0.576, 0.474, 0.422, 0.347, 0.307, 0.305, 0.279, 0.276, 0.265, 0.179, 0.082, 0.612, 0.77, 0.633, 0.549, 0.436, 0.39, 0.439, 0.479, 0.507, 0.516, 0.496, 0.48, 0.468, 0.498, 0.598, 0.564, 0.438, 0.406, 0.4, 0.341, 0.23, 0.358, 0.578, 0.677, 0.591, 0.433, 0.534, 0.62, 0.585, 0.632, 0.572, 0.441, 0.43, 0.396, 0.38, 0.37, 0.35, 0.384, 0.389, 0.39, 0.655, 0.915, 0.805, 0.566, 0.561, 0.516, 0.508, 0.614, 0.561, 0.416, 0.398, 0.353, 0.512, 0.838, 0.906, 0.691, 0.473, 0.415, 0.418, 0.309, 0.261, 0.313, 0.331, 0.39, 0.406, 0.437, 0.598, 0.785, 0.714, 0.541, 0.622, 0.587, 0.45, 0.377, 0.321, 0.3, 0.26, 0.164, 0.288, 0.919, 0.98, 0.604, 0.526, 0.446, 0.41, 0.374, 0.407, 0.436, 0.433, 0.456, 0.45, 0.42, 0.538, 0.638, 0.606, 0.634, 0.604, 0.459, 0.455, 0.471, 0.436, 0.537, 0.592, 0.541, 0.491, 0.539, 0.617, 0.561, 0.462, 0.451, 0.454, 0.474, 0.542, 0.586, 0.498, 0.391, 0.451, 0.453, 0.494, 0.565, 0.562, 0.508, 0.407, 0.315, 0.259, 0.258, 0.256, 0.228, 0.222, 0.18, 0.095, 0.662, 0.802, 0.565, 0.396, 0.252, 0.161, 0.121, 0.11, 0.127, 0.228, 0.244, 0.195, 0.184, 0.277, 0.612, 0.652, 0.466, 0.448, 0.51, 0.57, 0.537, 0.519, 0.565, 0.649, 0.633, 0.503, 0.475, 0.498, 0.439, 0.512, 0.751, 0.701, 0.654, 0.857, 1.0, 0.851, 0.585, 0.549, 0.766, 0.801, 0.609, 0.677, 0.686, 0.623, 0.518, 0.414, 0.361, 0.485, 0.539, 0.43, 0.38, 0.317, 0.478, 0.781, 0.734, 0.512, 0.583, 0.586, 0.468, 0.361, 0.339, 0.373, 0.419, 0.437, 0.44, 0.527, 0.665, 0.632, 0.587, 0.669, 0.622, 0.519, 0.435, 0.361, 0.391, 0.459, 0.461, 0.458, 0.48, 0.634, 0.675, 0.573, 0.625, 0.615, 0.551, 0.536, 0.481, 0.505, 0.513, 0.481, 0.44, 0.41, 0.566, 0.68, 0.61, 0.613, 0.553, 0.383, 0.361, 0.318, 0.302, 0.286, 0.227, 0.201, 0.226, 0.822, 0.875, 0.595, 0.691, 0.598, 0.441, 0.396, 0.469, 0.444, 0.33, 0.329, 0.358, 0.437, 0.614, 0.665, 0.602, 0.526, 0.452, 0.357, 0.196, 0.17, 0.198, 0.474, 0.688, 0.65, 0.568, 0.567, 0.479, 0.439, 0.453, 0.447, 0.437, 0.455, 0.541, 0.529, 0.422, 0.513, 0.482, 0.241, 0.309, 0.539, 0.651, 0.63, 0.561, 0.501, 0.467, 0.415, 0.422, 0.412, 0.364, 0.326, 0.357, 0.68, 0.824, 0.72, 0.651, 0.543, 0.399, 0.368, 0.303, 0.234, 0.365, 0.366, 0.239, 0.302, 0.484, 0.59, 0.57, 0.514, 0.455, 0.392, 0.434, 0.521, 0.439, 0.272, 0.307, 0.39, 0.441, 0.496, 0.51, 0.426, 0.36, 0.43, 0.465, 0.393, 0.289, 0.219, 0.256, 0.333, 0.291, 0.191, 0.186, 0.363, 0.508, 0.484, 0.413, 0.391, 0.335, 0.268, 0.258, 0.278, 0.281, 0.28, 0.221, 0.195, 0.741, 0.781, 0.487, 0.421, 0.256, 0.241], dtype=float)

BASS_ENV_30 = np.array([0.022, 0.209, 0.925, 0.304, 0.301, 0.166, 0.116, 0.073, 0.061, 0.104, 0.145, 0.145, 0.081, 0.041, 0.062, 0.265, 0.255, 0.213, 0.127, 0.053, 0.045, 0.037, 0.025, 0.093, 0.364, 0.249, 0.26, 0.374, 0.56, 0.319, 0.26, 0.268, 0.236, 0.219, 0.247, 0.259, 0.248, 0.209, 0.38, 0.256, 0.161, 0.148, 0.628, 0.288, 0.539, 0.413, 0.436, 0.372, 0.388, 0.301, 0.372, 0.338, 0.256, 0.39, 0.818, 0.472, 0.448, 0.335, 0.232, 0.26, 0.111, 0.139, 0.146, 0.219, 0.096, 0.075, 0.066, 0.184, 0.462, 0.285, 0.288, 0.247, 0.079, 0.057, 0.066, 0.049, 0.326, 0.306, 0.252, 0.267, 0.253, 0.48, 0.281, 0.253, 0.237, 0.251, 0.235, 0.235, 0.233, 0.222, 0.214, 0.255, 0.278, 0.218, 0.32, 0.41, 0.313, 0.348, 0.308, 0.311, 0.31, 0.299, 0.273, 0.283, 0.134, 0.035, 0.389, 0.687, 0.316, 0.3, 0.146, 0.092, 0.064, 0.067, 0.102, 0.097, 0.071, 0.033, 0.04, 0.045, 0.295, 0.225, 0.196, 0.066, 0.023, 0.018, 0.019, 0.015, 0.14, 0.251, 0.191, 0.186, 0.156, 0.294, 0.292, 0.251, 0.237, 0.25, 0.231, 0.221, 0.209, 0.224, 0.215, 0.199, 0.243, 0.188, 0.243, 0.365, 0.321, 0.319, 0.321, 0.313, 0.267, 0.306, 0.313, 0.268, 0.261, 0.27, 0.276, 0.929, 0.341, 0.422, 0.209, 0.135, 0.083, 0.052, 0.088, 0.112, 0.082, 0.053, 0.036, 0.034, 0.301, 0.364, 0.243, 0.286, 0.269, 0.232, 0.236, 0.276, 0.223, 0.24, 0.209, 0.074, 0.034, 0.896, 0.44, 0.409, 0.261, 0.135, 0.08, 0.06, 0.069, 0.105, 0.087, 0.056, 0.029, 0.037, 0.055, 0.404, 0.387, 0.379, 0.217, 0.099, 0.03, 0.014, 0.013, 0.172, 0.335, 0.248, 0.236, 0.256, 0.407, 0.254, 0.246, 0.21, 0.198, 0.208, 0.201, 0.195, 0.226, 0.173, 0.186, 0.177, 0.205, 0.424, 0.203, 0.245, 0.216, 0.218, 0.213, 0.231, 0.21, 0.191, 0.174, 0.173, 0.061, 0.468, 0.761, 0.361, 0.292, 0.132, 0.114, 0.095, 0.065, 0.084, 0.189, 0.239, 0.181, 0.185, 0.168, 0.388, 0.339, 0.207, 0.278, 0.215, 0.194, 0.232, 0.212, 0.145, 0.328, 0.341, 0.299, 0.3, 0.24, 0.218, 0.097, 0.017, 0.012, 0.016, 0.02, 0.017, 0.016, 0.013, 0.013, 0.02, 0.023, 0.427, 0.515, 0.512, 0.416, 0.415, 0.371, 0.335, 0.35, 0.324, 0.286, 0.066, 0.015, 0.057, 0.937, 0.348, 0.369, 0.218, 0.127, 0.07, 0.05, 0.1, 0.098, 0.097, 0.061, 0.03, 0.038, 0.172, 0.293, 0.197, 0.174, 0.097, 0.036, 0.013, 0.012, 0.022, 0.276, 0.236, 0.204, 0.204, 0.21, 0.389, 0.242, 0.266, 0.255, 0.264, 0.244, 0.225, 0.197, 0.208, 0.223, 0.241, 0.229, 0.231, 0.35, 0.428, 0.288, 0.38, 0.308, 0.346, 0.294, 0.285, 0.303, 0.16, 0.051, 0.116, 0.718, 0.63, 0.44, 0.31, 0.135, 0.109, 0.068, 0.086, 0.107, 0.113, 0.059, 0.03, 0.028, 0.21, 0.515, 0.45, 0.469, 0.37, 0.271, 0.092, 0.041, 0.035, 0.39, 0.525, 0.407, 0.428, 0.383, 0.36, 0.26, 0.255, 0.191, 0.218, 0.215, 0.197, 0.217, 0.178, 0.198, 0.245, 0.163, 0.186, 0.349, 0.291, 0.284, 0.2, 0.224, 0.187, 0.199, 0.163, 0.165, 0.178, 0.17, 0.2, 0.222, 1.0, 0.401, 0.41, 0.197, 0.123, 0.089, 0.063, 0.084, 0.121, 0.082, 0.051, 0.043, 0.029, 0.315, 0.276, 0.213, 0.233, 0.097, 0.049, 0.044, 0.042, 0.063, 0.257, 0.155, 0.136, 0.163, 0.328, 0.286, 0.207, 0.208, 0.199, 0.187, 0.177, 0.172, 0.164, 0.185, 0.165, 0.145, 0.152, 0.187, 0.349, 0.344, 0.333, 0.33, 0.304, 0.304, 0.238, 0.298, 0.25, 0.309, 0.219, 0.077, 0.865, 0.463, 0.42, 0.286, 0.121, 0.082], dtype=float)

VOX_ENV_30 = np.array([0.071, 0.176, 0.246, 0.113, 0.101, 0.098, 0.099, 0.084, 0.08, 0.065, 0.513, 0.701, 0.405, 0.27, 0.247, 0.756, 1.0, 0.833, 0.584, 0.408, 0.392, 0.307, 0.314, 0.282, 0.362, 0.358, 0.284, 0.2, 0.3, 0.478, 0.53, 0.536, 0.453, 0.451, 0.478, 0.377, 0.233, 0.213, 0.194, 0.162, 0.448, 0.853, 0.87, 0.698, 0.686, 0.497, 0.379, 0.33, 0.307, 0.355, 0.359, 0.252, 0.206, 0.296, 0.679, 0.702, 0.325, 0.464, 0.465, 0.462, 0.386, 0.363, 0.438, 0.333, 0.255, 0.277, 0.409, 0.543, 0.76, 0.702, 0.661, 0.506, 0.415, 0.286, 0.242, 0.208, 0.211, 0.298, 0.311, 0.333, 0.757, 0.549, 0.533, 0.465, 0.393, 0.449, 0.493, 0.526, 0.441, 0.413, 0.373, 0.402, 0.365, 0.324, 0.651, 0.526, 0.438, 0.32, 0.23, 0.156, 0.128, 0.119, 0.173, 0.181, 0.107, 0.063, 0.246, 0.464, 0.526, 0.463, 0.532, 0.547, 0.584, 0.505, 0.475, 0.46, 0.463, 0.443, 0.484, 0.487, 0.839, 0.632, 0.486, 0.501, 0.502, 0.398, 0.26, 0.313, 0.498, 0.552, 0.461, 0.297, 0.519, 0.678, 0.423, 0.462, 0.362, 0.279, 0.362, 0.356, 0.273, 0.301, 0.266, 0.372, 0.252, 0.173, 0.697, 0.893, 0.677, 0.597, 0.416, 0.408, 0.335, 0.398, 0.367, 0.341, 0.318, 0.186, 0.269, 0.807, 0.669, 0.497, 0.335, 0.362, 0.387, 0.307, 0.253, 0.283, 0.354, 0.397, 0.398, 0.413, 0.665, 0.821, 0.645, 0.557, 0.594, 0.549, 0.489, 0.35, 0.236, 0.229, 0.218, 0.154, 0.151, 0.782, 0.593, 0.475, 0.363, 0.346, 0.326, 0.336, 0.362, 0.322, 0.327, 0.369, 0.359, 0.301, 0.6, 0.67, 0.579, 0.525, 0.594, 0.426, 0.389, 0.339, 0.333, 0.457, 0.436, 0.349, 0.364, 0.681, 0.555, 0.404, 0.31, 0.296, 0.345, 0.341, 0.374, 0.4, 0.376, 0.346, 0.323, 0.306, 0.442, 0.7, 0.61, 0.533, 0.337, 0.222, 0.143, 0.139, 0.127, 0.136, 0.145, 0.121, 0.084, 0.28, 0.192, 0.074, 0.043, 0.041, 0.038, 0.034, 0.034, 0.031, 0.088, 0.1, 0.059, 0.045, 0.151, 0.82, 0.89, 0.504, 0.496, 0.5, 0.481, 0.388, 0.376, 0.45, 0.494, 0.479, 0.372, 0.467, 0.646, 0.398, 0.243, 0.42, 0.39, 0.429, 0.495, 0.505, 0.51, 0.419, 0.331, 0.435, 0.436, 0.626, 0.598, 0.615, 0.618, 0.429, 0.244, 0.226, 0.335, 0.522, 0.459, 0.359, 0.357, 0.297, 0.406, 0.258, 0.251, 0.426, 0.391, 0.339, 0.233, 0.254, 0.277, 0.294, 0.349, 0.283, 0.351, 0.67, 0.657, 0.584, 0.682, 0.589, 0.566, 0.471, 0.35, 0.382, 0.392, 0.457, 0.393, 0.34, 0.766, 0.516, 0.343, 0.469, 0.504, 0.469, 0.456, 0.429, 0.425, 0.344, 0.405, 0.307, 0.266, 0.605, 0.707, 0.566, 0.506, 0.389, 0.256, 0.228, 0.237, 0.208, 0.173, 0.162, 0.13, 0.098, 0.374, 0.294, 0.403, 0.531, 0.466, 0.406, 0.437, 0.425, 0.412, 0.349, 0.357, 0.361, 0.422, 0.62, 0.688, 0.454, 0.456, 0.349, 0.256, 0.229, 0.241, 0.223, 0.365, 0.542, 0.423, 0.398, 0.509, 0.439, 0.271, 0.354, 0.354, 0.283, 0.231, 0.235, 0.218, 0.219, 0.251, 0.165, 0.089, 0.171, 0.666, 0.793, 0.692, 0.522, 0.509, 0.427, 0.396, 0.416, 0.399, 0.37, 0.224, 0.22, 0.247, 0.354, 0.19, 0.163, 0.148, 0.158, 0.141, 0.126, 0.139, 0.153, 0.205, 0.147, 0.129, 0.143, 0.544, 0.484, 0.399, 0.32, 0.238, 0.182, 0.22, 0.2, 0.166, 0.198, 0.181, 0.166, 0.214, 0.591, 0.21, 0.124, 0.136, 0.147, 0.136, 0.108, 0.087, 0.108, 0.139, 0.11, 0.088, 0.06, 0.425, 0.49, 0.425, 0.352, 0.245, 0.162, 0.113, 0.097, 0.096, 0.114, 0.107, 0.063, 0.063, 0.323, 0.144, 0.082, 0.085, 0.061, 0.031], dtype=float)

LYRIC_WORDS = [
    (0, "Kan",       0.50, 1.05, False),
    (0, "nghah",     1.05, 1.65, False),
    (0, "Krismas",   1.65, 2.55, False),
    (0, "ni",        2.55, 3.55, False),
    (0, "eng",       3.65, 4.35, False),
    (0, "a",         4.35, 4.75, False),
    (0, "lo",        4.75, 5.20, False),
    (0, "zam",       5.20, 5.72, False),
    (0, "thar",      5.72, 6.25, False),
    (0, "leh",       6.25, 6.60, False),
    (0, "ta,",       6.60, 7.75, False),
    (1, "A",         8.38, 8.72, False),
    (1, "mawi",      8.72, 9.25, False),
    (1, "tizuala'n", 9.25, 11.05, False),
    (1, "Bethlehem", 11.10, 12.65, True),
    (1, "par",       12.65, 13.40, True),
    (1, "nen,",      13.40, 14.95, True),
]

CODE_LINES = [
    (67, "def fib(n):"),
    (68, "    i = np.arange(n) + 0.5"),
    (69, "    y = 1 - 2 * i / n"),
    (70, "    r = np.sqrt(1 - y * y)"),
    (71, "    th = np.pi * (3 - np.sqrt(5)) * i"),
    (72, "    return np.stack([r * np.cos(th), y, r * np.sin(th)], 1)"),
    (73, ""),
    (74, "# --- 3-mode aesthetic ascii lyric selector table ------------------"),
    (75, "LYRIC_STYLES = {"),
    (76, "    '1': ('sky_eq',      'Sky Starlight Stage + Vocal EQ'),  # default"),
    (77, "    '2': ('cipher_halo', 'Mid-Screen Cipher Halo'),"),
    (78, "    '3': ('cinema_sub',  'Snow Crest Cinema + Beat Wave'),"),
    (79, "}"),
    (80, "LIDAR_SCAN_HZ = 30.0                        # Aizawl 3D LiDAR Point Cloud"),
    (81, "Y0, Y1 = 0.42, 2.55                         # foliage elevation bounds"),
    (82, ""),
    (83, "def lidar_pulse(y, r, t, bass):"),
    (84, "    scan_y = Y0 + ((t * 1.45) % (Y1 - Y0 + 0.5))"),
    (85, "    beam = np.exp(-((y - scan_y) / 0.09) ** 2)"),
    (86, "    ring = np.exp(-((r - (t * 1.35) % 1.55) / 0.08) ** 2) * bass"),
    (87, "    return np.maximum(beam, ring)"),
    (88, ""),
    (89, "def build():"),
    (90, "    rng = np.random.default_rng(7); q = Parts()"),
    (91, "    tiers = np.linspace(Y0 + 0.02, Y1 - 0.04, 24)"),
    (92, "    for i, y in enumerate(tiers):"),
    (93, "        R = envelope(y); nb = int(7 + 11 * (1 - (y - Y0) / (Y1 - Y0)))"),
    (94, "        for b in range(nb):"),
    (95, "            a = TAU * b / nb + i * 0.618 * TAU + rng.normal(0, 0.08)"),
    (96, "            L = R * rng.uniform(0.82, 1.06); s = rng.random(900) ** 0.65"),
    (97, "            col = np.column_stack([0.02+0.12*s, 0.42+0.48*s, 0.28+0.48*f])"),
    (98, "            q.add(p[~snow], nrm[~snow], col[~snow], NEEDLE, t0[~snow])"),
    (99, ""),
    (100, "    # --- Left Foreground Terrace: 4 Wrapped Present Gift Boxes --------"),
    (101, "    gift_specs = [(-0.95, 0.65, 0.34, 0.30), (-0.58, 0.78, 0.32, 0.24),"),
    (102, "                  (-0.22, 0.86, 0.28, 0.21), (-0.78, 0.94, 0.22, 0.17)]"),
    (103, "    for gx, gz, gw, gh in gift_specs:"),
    (104, "        q.add(pts_world[~is_rib], nrm_world[~is_rib], bcol, GIFT, gt0)"),
    (105, "        q.add(bow_pts, [0, 1, 0], rcol, RIBBON, gt0 + 0.12, shine=0.85)"),
    (106, ""),
    (107, "    # --- Right Foreground Terrace: Enlarged 1.8x 3D Nativity (Ran In) -"),
    (108, "    nat_x, nat_z = 0.82, 0.82               # separated right terrace"),
    (109, "    q.add(to_nat(roof_pts), nrm_nat(roof_nrm), (0.98, 0.76, 0.30), NATIVITY, 8.5)"),
    (110, "    q.add(to_nat(baby_sph + [0.0, 0.19, 0.04]), baby_sph, (1.0, 0.98, 0.75), STAR, 8.8)"),
    (111, "    q.add(to_nat(mary_pts), nrm_nat(mary_nrm), (0.18, 0.85, 1.00), NATIVITY, 8.9)"),
    (112, "    q.add(to_nat(jos_pts),  nrm_nat(jos_nrm),  (0.98, 0.72, 0.32), NATIVITY, 8.9)"),
]


def unit(v):
    v = np.asarray(v, float)
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    return np.where(n > 1e-9, v / np.maximum(n, 1e-9), 0.0)


def fib(n):
    i = np.arange(n) + 0.5
    y = 1 - 2 * i / n
    r = np.sqrt(np.maximum(0.0, 1 - y * y))
    th = np.pi * (3 - np.sqrt(5)) * i
    return np.stack([r * np.cos(th), y, r * np.sin(th)], 1)


def envelope(y):
    f = np.clip((y - Y0) / (Y1 - Y0), 0, 1)
    return 0.03 + 0.84 * (1 - f) ** 1.08


class Parts:
    def __init__(s):
        s.P, s.N, s.C, s.K, s.T, s.PH, s.SH = [], [], [], [], [], [], []

    def add(s, p, n, col, kind, t0, ph=0.0, shine=0.0):
        p = np.asarray(p, float)
        m = len(p)
        s.P.append(p)
        s.N.append(unit(np.broadcast_to(n, (m, 3))))
        s.C.append(np.broadcast_to(np.asarray(col, float), (m, 3)))
        s.K.append(np.full(m, kind, dtype=np.int32))
        for lst, v in ((s.T, t0), (s.PH, ph), (s.SH, shine)):
            lst.append(np.broadcast_to(np.asarray(v, float), (m,)).copy())

    def done(s):
        return [np.concatenate(v) for v in (s.P, s.N, s.C, s.K, s.T, s.PH, s.SH)]


def build_scene():
    rng = np.random.default_rng(7)
    q = Parts()
    tips = []

    # 1. 24 tiers of drooping branch whorls (exact LiDAR cyber-emerald to cyan-teal palette)
    tiers = np.linspace(Y0 + 0.02, Y1 - 0.04, 24)
    for i, y in enumerate(tiers):
        R = envelope(y)
        nb = int(7 + 11 * (1 - (y - Y0) / (Y1 - Y0)))
        for b in range(nb):
            a = TAU * b / nb + i * 0.618 * TAU + rng.normal(0, 0.08)
            L = R * rng.uniform(0.82, 1.06)
            n = int((250 + 1400 * L) * 0.65)
            s = rng.random(n) ** 0.65
            d = np.array([np.cos(a), 0, np.sin(a)])
            side = np.array([-np.sin(a), 0, np.cos(a)])
            spread = (0.035 + 0.11 * s) * rng.normal(0, 1, n)
            yy = y + 0.07 * s * L - 0.22 * (s * L) ** 2 + 0.03 * rng.normal(0, 1, n)
            p = d[None] * (s * L)[:, None] + side[None] * spread[:, None] + np.array([0, 1, 0]) * yy[:, None]
            nrm = d[None] * 0.75 + np.array([0, 0.55, 0]) + rng.normal(0, 0.25, (n, 3))
            ao = 0.35 + 0.65 * s ** 1.3
            tone = ao * rng.uniform(0.75, 1.1, n)
            elev_f = np.clip((yy - Y0) / (Y1 - Y0), 0.0, 1.0)
            col = np.column_stack([
                0.02 + 0.12 * (s ** 1.2),
                0.42 + 0.48 * (s ** 1.2),
                0.28 + 0.48 * elev_f,
            ])
            t0 = 0.52 + 2.75 * (y - Y0) / (Y1 - Y0) + 0.30 * s
            snow = (s > 0.45) & (rng.random(n) < 0.06 * s) & (nrm[:, 1] > 0.28)
            q.add(p[~snow], nrm[~snow], col[~snow] * tone[~snow, None], NEEDLE, t0[~snow], shine=0.25)
            q.add(p[snow], np.array([0, 1.0, 0]), (0.55, 0.98, 1.0), SNOWCAP, t0[snow] + 0.18, shine=0.5)
            tips.append((d * L * 0.93 + np.array([0, y + 0.07 * L - 0.22 * L ** 2, 0]), R, y, a))

    # 2. Trunk
    h, a = np.meshgrid(np.linspace(-0.05, 0.6, 50), np.linspace(0, TAU, 40, endpoint=False))
    p = np.stack([0.085 * np.cos(a), h, 0.085 * np.sin(a)], -1).reshape(-1, 3)
    nn = np.stack([np.cos(a), 0 * a, np.sin(a)], -1).reshape(-1, 3)
    bark = 0.75 + 0.25 * np.sin(h * 90 + a * 3).ravel()
    q.add(p, nn, np.array([0.18, 0.52, 0.68])[None] * bark[:, None], TRUNK, 0.25 + 0.55 * (h.ravel() + 0.05) / 0.65)

    # 3. 5-strand drooping gold spiral tinsel garland in swags
    u = np.linspace(0, 1, 2000)
    turns = 3.6
    yg = Y0 + 0.15 + (Y1 - Y0 - 0.45) * u
    ag = TAU * turns * u + 0.9
    swag = -0.06 * np.abs(np.sin(ag * 2.5))
    rg = envelope(yg) * 1.02 + 0.02
    base = np.stack([rg * np.cos(ag), yg + swag, rg * np.sin(ag)], 1)
    for k in range(5):
        off = rng.normal(0, 0.014, base.shape)
        gcol = np.array([1.0, 0.84, 0.25]) * rng.uniform(0.82, 1.15, (len(u), 1))
        q.add(base + off, off, gcol, GARLAND, 3.57 + 1.55 * u, ph=u * 25.0 + k, shine=0.90)

    # 4. Crisp Ornament Balls & 170 String Lights
    ball_cols = np.array([
        [1.00, 0.16, 0.36],
        [1.00, 0.86, 0.18],
        [0.98, 0.20, 0.42],
        [0.08, 0.88, 1.00],
        [0.75, 0.96, 1.00],
    ])
    light_cols = np.array([
        [0.20, 0.98, 1.00],
        [1.00, 0.24, 0.45],
        [1.00, 0.92, 0.35],
        [0.25, 1.00, 0.65],
    ])
    sph_ball = fib(64)
    sph_light = fib(12)
    rng.shuffle(tips)

    for idx, (tip_p, _, ty, _) in enumerate(tips[:56]):
        rad = rng.uniform(0.056, 0.072)
        center = tip_p + np.array([0.0, -rad * 0.75, 0.0])
        bcol = ball_cols[idx % len(ball_cols)]
        t_ball = 4.45 + 1.15 * (ty - Y0) / (Y1 - Y0) + rng.uniform(0, 0.15)
        q.add(center[None] + sph_ball * rad, sph_ball, bcol, BALL, t_ball, ph=rng.uniform(0, TAU), shine=0.92)

    light_tips = tips[56 : 56 + 170]
    for idx, (tip_p, _, ty, _) in enumerate(light_tips):
        lcol = light_cols[idx % len(light_cols)]
        t_light = 5.32 + 1.30 * (idx / 170.0)
        q.add(tip_p[None] + sph_light * 0.020, sph_light, lcol, LIGHT, t_light, ph=rng.uniform(0, TAU), shine=1.0)

    # 5. LEFT-SIDE CLUSTER OF 4 WRAPPED PRESENT BOXES (x = -0.95 .. -0.22, z = +0.65 .. +0.94)
    gift_specs = [
        (-0.95, 0.65, 0.34, 0.30, 0.30,  0.28, (0.96, 0.14, 0.30), (1.00, 0.86, 0.22), 7.20),
        (-0.58, 0.78, 0.32, 0.24, 0.28,  0.15, (0.12, 0.62, 1.00), (0.40, 0.98, 1.00), 7.55),
        (-0.22, 0.86, 0.28, 0.21, 0.26, -0.12, (1.00, 0.78, 0.16), (0.98, 0.16, 0.36), 7.90),
        (-0.78, 0.94, 0.22, 0.17, 0.22,  0.38, (0.85, 0.96, 1.00), (0.98, 0.18, 0.38), 8.20),
    ]
    for gx, gz, gw, gh, gd, gang, bcol, rcol, gt0 in gift_specs:
        u_g = np.linspace(-0.5, 0.5, 16)
        v_g = np.linspace(0.0, 1.0, 16)
        uu, vv = np.meshgrid(u_g, v_g)
        uu, vv = uu.ravel(), vv.ravel()
        faces_p, faces_n, faces_rib = [], [], []
        for z_sgn in (-0.5, 0.5):
            fx, fy, fz = uu * gw, vv * gh, np.full_like(uu, z_sgn * gd)
            fn = np.broadcast_to([0, 0, np.sign(z_sgn)], (len(uu), 3))
            rib = (np.abs(fx) < gw * 0.15) | (np.abs(fy - gh * 0.5) < gh * 0.14)
            faces_p.append(np.stack([fx, fy, fz], 1)); faces_n.append(fn); faces_rib.append(rib)
        for x_sgn in (-0.5, 0.5):
            fx, fy, fz = np.full_like(uu, x_sgn * gw), vv * gh, uu * gd
            fn = np.broadcast_to([np.sign(x_sgn), 0, 0], (len(uu), 3))
            rib = (np.abs(fz) < gd * 0.15) | (np.abs(fy - gh * 0.5) < gh * 0.14)
            faces_p.append(np.stack([fx, fy, fz], 1)); faces_n.append(fn); faces_rib.append(rib)
        tx, ty, tz = uu * gw, np.full_like(uu, gh), (vv - 0.5) * gd
        tn = np.broadcast_to([0, 1, 0], (len(uu), 3))
        trib = (np.abs(tx) < gw * 0.16) | (np.abs(tz) < gd * 0.16)
        faces_p.append(np.stack([tx, ty, tz], 1)); faces_n.append(tn); faces_rib.append(trib)

        pts_b = np.concatenate(faces_p, 0)
        nrm_b = np.concatenate(faces_n, 0)
        is_rib = np.concatenate(faces_rib, 0)

        ca, sa = np.cos(gang), np.sin(gang)
        rot_g = np.array([[ca, 0, sa], [0, 1, 0], [-sa, 0, ca]])
        ground_y = 0.30 * np.exp(-1.05 * (gx * gx + gz * gz)) - 0.04
        pts_world = pts_b @ rot_g.T + np.array([gx, ground_y, gz])
        nrm_world = nrm_b @ rot_g.T

        q.add(pts_world[~is_rib], nrm_world[~is_rib], bcol, GIFT, gt0, shine=0.35)
        q.add(pts_world[is_rib], nrm_world[is_rib], rcol, RIBBON, gt0 + 0.06, shine=0.75)

        bow_t = np.linspace(0, TAU, 90)
        bow_r = min(gw, gd) * 0.28 * np.sin(2 * bow_t)
        bow_pts = np.stack([
            bow_r * np.cos(bow_t),
            gh + 0.02 + np.abs(bow_r) * 0.50,
            bow_r * np.sin(bow_t),
        ], 1) @ rot_g.T + np.array([gx, ground_y, gz])
        q.add(bow_pts, np.array([0, 1, 0]), rcol, RIBBON, gt0 + 0.12, shine=0.85)

    # 6. ENLARGED 1.8x GRAND 3D NATIVITY SCENE (Bethlehem Manger / Ran In) on Right Terrace
    nat_x, nat_z = 0.82, 0.82
    nat_y0 = 0.30 * np.exp(-1.05 * (nat_x ** 2 + nat_z ** 2)) - 0.04
    nat_ang = -0.22
    ca_n, sa_n = np.cos(nat_ang), np.sin(nat_ang)
    rot_nat = np.array([[ca_n, 0, sa_n], [0, 1, 0], [-sa_n, 0, ca_n]])
    def to_nat(pts):
        return np.asarray(pts, float) @ rot_nat.T + np.array([nat_x, nat_y0, nat_z])
    def nrm_nat(nrms):
        return unit(np.asarray(nrms, float) @ rot_nat.T)

    nx_fl, nz_fl = np.meshgrid(np.linspace(-0.42, 0.42, 30), np.linspace(-0.20, 0.20, 14))
    fl_pts = np.column_stack([nx_fl.ravel(), np.full(nx_fl.size, 0.01), nz_fl.ravel()])
    q.add(to_nat(fl_pts), nrm_nat([0, 1, 0]), (0.20, 0.82, 0.95), NATIVITY, 8.2, shine=0.35)

    for px_post in (-0.38, 0.38):
        for pz_post in (-0.14, 0.14):
            py_p = np.linspace(0.0, 0.54, 48)
            for dx_p in (-0.012, 0.0, 0.012):
                post_pts = np.column_stack([np.full_like(py_p, px_post + dx_p), py_p, np.full_like(py_p, pz_post)])
                q.add(to_nat(post_pts), nrm_nat([np.sign(dx_p) if dx_p != 0 else 0, 0, 1]), (0.88, 0.64, 0.28), NATIVITY, 8.35, shine=0.4)

    lx_b = np.linspace(-0.40, 0.40, 50)
    lintel_pts = np.column_stack([lx_b, np.full_like(lx_b, 0.54), np.full_like(lx_b, 0.14)])
    q.add(to_nat(lintel_pts), nrm_nat([0, 0.5, 1]), (0.95, 0.72, 0.32), NATIVITY, 8.4, shine=0.5)

    rx_grid, rz_grid = np.meshgrid(np.linspace(-0.46, 0.46, 56), np.linspace(-0.18, 0.18, 18))
    rx_f, rz_f = rx_grid.ravel(), rz_grid.ravel()
    ry_f = 0.88 - 0.74 * np.abs(rx_f)
    roof_pts = np.column_stack([rx_f, ry_f, rz_f])
    roof_nrm = np.column_stack([np.sign(rx_f) * 0.6, np.full_like(rx_f, 0.8), np.full_like(rx_f, 0.25)])
    q.add(to_nat(roof_pts), nrm_nat(roof_nrm), (0.98, 0.76, 0.30), NATIVITY, 8.5, shine=0.55)

    for leg_s in (-1, 1):
        ly_l = np.linspace(0.0, 0.15, 20)
        lx_l = leg_s * (ly_l - 0.075) * 1.1
        leg_pts = np.column_stack([lx_l, ly_l, np.full_like(ly_l, 0.04)])
        q.add(to_nat(leg_pts), nrm_nat([0, 0, 1]), (0.85, 0.58, 0.24), NATIVITY, 8.65, shine=0.4)

    cr_x, cr_z = np.meshgrid(np.linspace(-0.11, 0.11, 22), np.linspace(-0.06, 0.06, 10))
    cr_xf, cr_zf = cr_x.ravel(), cr_z.ravel()
    cr_yf = 0.13 + 0.35 * np.abs(cr_xf)
    q.add(to_nat(np.column_stack([cr_xf, cr_yf, cr_zf])), nrm_nat([0, 0.8, 0.6]), (0.98, 0.82, 0.38), NATIVITY, 8.7, shine=0.7)

    baby_sph = fib(80) * np.array([0.075, 0.048, 0.048])
    q.add(to_nat(baby_sph + np.array([0.0, 0.19, 0.04])), baby_sph, (1.0, 0.98, 0.75), STAR, 8.8, shine=1.0)

    my_g, ma_g = np.meshgrid(np.linspace(0.0, 0.31, 34), np.linspace(0, TAU, 26, endpoint=False))
    my_f, ma_f = my_g.ravel(), ma_g.ravel()
    mr_f = 0.078 * (1.0 - 0.52 * (my_f / 0.31))
    mx_f = -0.22 + 0.06 * (my_f / 0.31) + mr_f * np.cos(ma_f)
    mz_f = mr_f * np.sin(ma_f)
    mary_nrm = np.column_stack([np.cos(ma_f), np.full_like(ma_f, 0.35), np.sin(ma_f)])
    q.add(to_nat(np.column_stack([mx_f, my_f, mz_f])), nrm_nat(mary_nrm), (0.18, 0.85, 1.00), NATIVITY, 8.9, shine=0.55)
    mary_head = fib(55) * 0.048
    q.add(to_nat(mary_head + np.array([-0.16, 0.36, 0.0])), nrm_nat(mary_head), (0.95, 0.96, 1.00), NATIVITY, 8.95, shine=0.65)

    jy_g, ja_g = np.meshgrid(np.linspace(0.0, 0.38, 38), np.linspace(0, TAU, 26, endpoint=False))
    jy_f, ja_f = jy_g.ravel(), ja_g.ravel()
    jr_f = 0.082 * (1.0 - 0.48 * (jy_f / 0.38))
    jx_f = 0.22 - 0.05 * (jy_f / 0.38) + jr_f * np.cos(ja_f)
    jz_f = jr_f * np.sin(ja_f)
    jos_nrm = np.column_stack([np.cos(ja_f), np.full_like(ja_f, 0.35), np.sin(ja_f)])
    q.add(to_nat(np.column_stack([jx_f, jy_f, jz_f])), nrm_nat(jos_nrm), (0.98, 0.72, 0.32), NATIVITY, 8.9, shine=0.55)
    jos_head = fib(55) * 0.050
    q.add(to_nat(jos_head + np.array([0.17, 0.44, 0.0])), nrm_nat(jos_head), (0.95, 0.96, 1.00), NATIVITY, 8.95, shine=0.65)

    staff_y = np.linspace(0.0, 0.48, 44)
    staff_pts = np.column_stack([np.full_like(staff_y, 0.31), staff_y, np.full_like(staff_y, 0.06)])
    q.add(to_nat(staff_pts), nrm_nat([0, 0, 1]), (0.55, 0.98, 1.00), NATIVITY, 9.0, shine=0.8)
    crook_a = np.linspace(0, np.pi * 1.15, 20)
    crook_pts = np.column_stack([0.28 + 0.03 * np.cos(crook_a), 0.48 + 0.03 * np.sin(crook_a), np.full_like(crook_a, 0.06)])
    q.add(to_nat(crook_pts), nrm_nat([0, 0, 1]), (0.55, 0.98, 1.00), NATIVITY, 9.0, shine=0.8)

    # 7. Concentric Cyan LiDAR Topographic Contour Ground Mound
    rg_grid, ag_grid = np.meshgrid(np.linspace(0.01, 1.55, 85), np.linspace(0, TAU, 180, endpoint=False))
    rg_flat = rg_grid.ravel()
    ag_flat = ag_grid.ravel()
    yg_flat = 0.30 * np.exp(-1.05 * rg_flat ** 2) - 0.05 + 0.01 * np.sin(rg_flat * 20)
    pg = np.stack([rg_flat * np.cos(ag_flat), yg_flat, rg_flat * np.sin(ag_flat)], 1)
    ng = unit(np.stack([0.55 * rg_flat * np.cos(ag_flat), np.ones_like(rg_flat), 0.55 * rg_flat * np.sin(ag_flat)], 1))
    is_ring = (np.round(rg_flat * 40).astype(int) % 5) == 0
    g_shade = np.where(is_ring, 0.95, 0.32 + 0.52 * np.exp(-0.85 * rg_flat ** 2))[:, None] * np.array([0.22, 0.88, 1.0])
    q.add(pg, ng, g_shade, GROUND, 0.07 + 0.45 * (rg_flat / 1.55), shine=0.4)

    # 8. Apex Star Core
    star_center = np.array([0.0, Y1 + 0.09, 0.0])
    core_sph = fib(140) * 0.075
    q.add(star_center[None] + core_sph, core_sph, (0.65, 1.0, 1.0), STAR, 7.93, shine=1.0)

    return q.done()


def build_aizawl_lidar_ridges(width: int, height: int):
    rng = np.random.default_rng(796001)
    horizon_base = int(height * 0.64)
    x_norm = np.linspace(-1.0, 1.0, width)
    r1 = 0.26 + 0.26 * np.exp(-((x_norm + 0.64) / 0.40) ** 2) + 0.025 * np.sin(x_norm * 12.0)
    r2 = 0.25 + 0.28 * np.exp(-((x_norm - 0.65) / 0.42) ** 2) + 0.025 * np.cos(x_norm * 14.0)
    r3 = 0.18 + 0.08 * np.cos(x_norm * 4.5) + 0.015 * np.sin(x_norm * 21.0)
    skyline_h = np.maximum.reduce([r1, r2, r3])

    win_palette = [
        (0.0, 0.96, 1.0),
        (0.31, 1.0, 0.76),
        (1.0, 0.84, 0.43),
        (1.0, 0.37, 0.57),
        (0.72, 0.94, 1.0),
    ]
    ridge_cells = []
    for c in range(width):
        top_row = int(horizon_base - skyline_h[c] * height)
        for r in range(max(4, top_row), horizon_base + 2):
            d_frac = (r - top_row) / max(1, (horizon_base + 2 - top_row))
            is_iso = (r % 4) == 0
            if d_frac > 0.85:
                if rng.random() < 0.48:
                    ridge_cells.append((r, c, ord("~") if rng.random() < 0.5 else ord("."), (0.29, 0.65, 0.76), 0.07, 0.0))
                continue
            ridge_cells.append((r, c, ord("-") if is_iso else ord("."), (0.11, 0.36, 0.50) if is_iso else (0.07, 0.19, 0.28), 0.05, 0.0))

            density = 0.44 * (1.0 - 0.35 * abs(x_norm[c])) * (0.65 + 0.35 * np.sin(c * 0.7 + r * 0.45))
            if rng.random() < density:
                ch = int(rng.choice([ord("="), ord(":"), ord("+"), ord("*"), ord("#")], p=[0.32, 0.28, 0.20, 0.14, 0.06]))
                col = win_palette[rng.integers(0, len(win_palette))]
                fade = 0.55 + 0.45 * (1.0 - d_frac * 0.55)
                fg = (col[0] * fade, col[1] * fade, col[2] * fade)
                t0_r = 0.07 + 0.75 * (1.0 - d_frac) + rng.uniform(0, 0.20)
                ridge_cells.append((r, c, ch, fg, t0_r, float(rng.uniform(0, TAU))))

    return ridge_cells


def load_font(size: int):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf",
        "C:/Windows/Fonts/consola.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def build_glyph_atlas(font):
    atlas = np.zeros((128, CH, CW), dtype=np.float32)
    for code in range(32, 127):
        img = Image.new("L", (CW, CH), 0)
        draw = ImageDraw.Draw(img)
        draw.text((0, -1), chr(code), fill=255, font=font)
        atlas[code] = np.asarray(img, dtype=np.float32) / 255.0
    return atlas


def main():
    parser = argparse.ArgumentParser(description="Live Mizo Christmas LiDAR visualizer")
    parser.add_argument(
        "--audio",
        default=str(Path(__file__).resolve().parent / "nov christmas song mizo.mp3"),
        help="Path to nov christmas song mizo.mp3 (optional if running locally without audio file)",
    )
    args = parser.parse_args()

    t_start = time.perf_counter()
    rms_env = RMS_ENV_30
    bass_env = BASS_ENV_30
    vox_env = VOX_ENV_30

    audio_mp3 = args.audio
    if not os.path.isfile(audio_mp3):
        raise FileNotFoundError(f"Song not found: {audio_mp3}. Put it beside this script or pass --audio.")

    font_grid = load_font(9)
    font_hud = load_font(13)
    font_code = load_font(13)
    font_lyric = load_font(21)
    yy_grade, xx_grade = np.mgrid[:TOP_H, :W]
    tree_grade = np.clip(1 - ((xx_grade - 360) / 210)**4, 0, 1)
    tree_grade *= np.clip((yy_grade - 180) / 90, 0, 1) * np.clip((810 - yy_grade) / 65, 0, 1)
    grade_gain = .87 + .25 * tree_grade
    grade_gain[:155] = 1
    grade_gain[755:] = 1.07
    atlas = build_glyph_atlas(font_grid)
    ramp_codes = np.array([ord(c) for c in RAMP_STR], dtype=np.int32)

    scene = build_scene()
    P, N, C, K, T, PH, SH = scene
    P_rad = np.sqrt(P[:, 0] ** 2 + P[:, 2] ** 2)

    ridge_cells = build_aizawl_lidar_ridges(COLS, ROWS)
    r_rows = np.array([x[0] for x in ridge_cells], dtype=np.int32)
    r_cols = np.array([x[1] for x in ridge_cells], dtype=np.int32)
    r_chs = np.array([x[2] for x in ridge_cells], dtype=np.int32)
    r_fgs = np.array([x[3] for x in ridge_cells], dtype=np.float32)
    r_t0s = np.array([x[4] for x in ridge_cells], dtype=np.float32)
    r_phs = np.array([x[5] for x in ridge_cells], dtype=np.float32)

    rng_bg = np.random.default_rng(42)
    n_bg = 90
    bg_x = rng_bg.integers(0, COLS, n_bg)
    bg_y = rng_bg.integers(0, int(ROWS * 0.42), n_bg)
    bg_ch = rng_bg.choice([ord("."), ord("*"), ord("+")], n_bg)
    bg_ph = rng_bg.uniform(0, TAU, n_bg)

    yy_k, xx_k = np.mgrid[-80:81, -80:81]
    rr_k = np.sqrt(xx_k ** 2 + yy_k ** 2)
    glow_kernel = np.exp(-rr_k / 24.0) * (rr_k <= 80)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_mp3)
    song_length = pygame.mixer.Sound(audio_mp3).get_length()
    info = pygame.display.Info()
    wh = max(480, min(960, info.current_h - 100))
    ww = max(640, min(1000, info.current_w - 100))
    window = pygame.display.set_mode((ww, wh), pygame.RESIZABLE)
    pygame.display.set_caption("Krismas Visualizer | Drag: rotate | Wheel: zoom | Space: pause | R: replay")
    button_font = pygame.font.SysFont("segoeui", 14)
    mode_labels = ["Sky Starlight + Vocal EQ", "Mid-Screen Cipher Halo", "Snow Crest + Beat Wave"]
    mode = 0
    buttons = []
    clock = pygame.time.Clock()
    paused = dragging = False
    yaw = tilt = 0.0
    zoom = 1.0
    t = 0.0
    pygame.mixer.music.play(loops=-1)
    running = True

    cam_y = 1.34
    pitch = np.deg2rad(5.5)
    cp, sp = np.cos(pitch), np.sin(pitch)
    pitch_m = np.array([[1.0, 0.0, 0.0], [0.0, cp, -sp], [0.0, sp, cp]])
    fov = min(COLS * 0.45, ROWS * 0.88)
    light_dir = unit(np.array([0.42, 0.68, 0.60]))
    half_dir = unit(light_dir + np.array([0.0, 0.0, 1.0]))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    mode = event.key - pygame.K_1
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    (pygame.mixer.music.pause if paused else pygame.mixer.music.unpause)()
                elif event.key == pygame.K_r:
                    pygame.mixer.music.play(loops=-1)
                    paused, t = False, 0.0
                elif event.key == pygame.K_HOME:
                    yaw, tilt, zoom = 0.0, 0.0, 1.0
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                hit = next((i for i, rect in enumerate(buttons) if rect.collidepoint(event.pos)), None)
                if hit is not None:
                    mode = hit
                else:
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                yaw += event.rel[0] * .4
                tilt = float(np.clip(tilt + event.rel[1] * .25, -35, 35))
            elif event.type == pygame.MOUSEWHEEL:
                zoom = float(np.clip(zoom * 1.08 ** event.y, .6, 1.35))
        if not running:
            break
        position = pygame.mixer.music.get_pos()
        if not paused and position >= 0:
            t = (position / 1000.0) % song_length
        frame_idx = min(TOTAL_FRAMES - 1, int(t * FPS))
        pitch = np.deg2rad(5.5 + tilt)
        cp, sp = np.cos(pitch), np.sin(pitch)
        pitch_m = np.array([[1., 0., 0.], [0., cp, -sp], [0., sp, cp]])
        fov = min(COLS * .45, ROWS * .88) * zoom
        e_idx = min(len(rms_env) - 1, frame_idx)
        rms_val = float(rms_env[e_idx])
        bass_val = float(bass_env[e_idx])
        vox_val = float(vox_env[e_idx])
        is_beth_phase = 11.10 <= t <= 14.95

        rot_deg = (yaw + t * 22.0 + 4.5 * np.sin(TAU * (135.7 / 60.0) * t)) % 360.0
        theta = np.deg2rad(rot_deg)
        ca, sa = np.cos(theta), np.sin(theta)
        rot_m = np.array([[ca, 0.0, sa], [0.0, 1.0, 0.0], [-sa, 0.0, ca]])

        active = t >= T
        P_orig = P[active]
        N_orig = N[active]
        P_act = P_orig @ rot_m.T
        N_act = N_orig @ rot_m.T
        C_act = C[active].copy()
        K_act = K[active]
        T_act = T[active]
        PH_act = PH[active]
        SH_act = SH[active]
        R_act = P_rad[active]
        Y_orig = P_orig[:, 1]
        sway_rad = np.deg2rad(yaw + 7.5 * np.sin(TAU * (135.7 / 120.0) * t))
        cs, ss = np.cos(sway_rad), np.sin(sway_rad)
        sway_m = np.array([[cs, 0.0, ss], [0.0, 1.0, 0.0], [-ss, 0.0, cs]])
        is_fg_prop = (K_act == GIFT) | (K_act == RIBBON) | (K_act == NATIVITY) | ((K_act == STAR) & (Y_orig < 1.0))
        P_act[is_fg_prop] = P_orig[is_fg_prop] @ sway_m.T
        N_act[is_fg_prop] = N_orig[is_fg_prop] @ sway_m.T

        # LiDAR vertical laser scan plane & ground radial range pulse
        lidar_scan_y = Y0 - 0.1 + ((t * 1.45) % (Y1 - Y0 + 0.45))
        lidar_ring_r = (t * 1.35) % 1.55
        beam_hit = np.exp(-((Y_orig - lidar_scan_y) / 0.085) ** 2)
        ring_hit = np.where(K_act == GROUND, np.exp(-((R_act - lidar_ring_r) / 0.08) ** 2), 0.0)
        scan_hit = np.maximum(beam_hit, ring_hit)

        m_scan = scan_hit > 0.25
        if np.any(m_scan):
            sh_w = (scan_hit[m_scan] * 0.72)[:, None]
            C_act[m_scan] = C_act[m_scan] * (1.0 - sh_w) + np.array([0.35, 1.0, 1.0]) * sh_w

        age = t - T_act
        frontier = ((K_act == NEEDLE) | (K_act == SNOWCAP)) & (age < 0.38)
        if np.any(frontier):
            blend = np.clip(1.0 - age[frontier] / 0.38, 0.0, 1.0)[:, None]
            C_act[frontier] = C_act[frontier] * (1.0 - blend) + np.array([0.15, 0.98, 1.0]) * blend

        cam_dist = 3.55 - 0.08 * bass_val
        P_rel = P_act - np.array([0.0, cam_y, 0.0])
        P_cam = P_rel @ pitch_m.T
        N_cam = N_act @ pitch_m.T

        z_depth = cam_dist - P_cam[:, 2]
        valid = z_depth > 0.35
        px = (COLS * 0.5 + (P_cam[:, 0] / z_depth) * fov * 1.68).astype(np.int32)
        py = (ROWS * 0.55 - (P_cam[:, 1] / z_depth) * fov).astype(np.int32)
        in_b = valid & (px >= 0) & (px < COLS) & (py >= 0) & (py < ROWS)

        ndotl = np.clip(N_cam @ light_dir, 0.0, 1.0)
        spec = np.clip(N_cam @ half_dir, 0.0, 1.0) ** 12
        lum = np.clip(0.30 + 0.70 * ndotl + SH_act * (0.50 * spec) + 0.14 * bass_val + 0.45 * scan_hit, 0.0, 1.0)

        is_light = K_act == LIGHT
        is_star = K_act == STAR
        is_garland = K_act == GARLAND
        is_snowcap = K_act == SNOWCAP

        twinkle = (0.75 + 0.25 * np.sin(TAU * (135.7 / 60.0) * t + PH_act)) * (1.0 + 0.45 * bass_val)
        C_act[is_light] *= (1.45 * twinkle[is_light])[:, None]
        lum[is_light] = 0.99

        shimmer = (0.82 + 0.18 * np.sin(4.5 * t + PH_act)) * (1.0 + 0.25 * rms_val)
        C_act[is_garland] *= shimmer[is_garland, None]

        C_act[is_star] = np.array([0.65, 1.0, 1.0])
        lum[is_star] = 0.99

        rgb_pts = np.clip(C_act * (0.55 + 0.65 * lum[:, None]), 0.0, 1.0)
        max_idx = np.where((K_act == RIBBON) | (K_act == GARLAND) | (scan_hit > 0.65), 8, 7)
        r_idx = np.minimum(max_idx, np.maximum(1, (lum * (max_idx + 0.6)).astype(np.int32)))
        ch_codes = ramp_codes[r_idx]
        ch_codes[is_snowcap] = np.where(lum[is_snowcap] > 0.7, ord("%"), ord("*"))
        ch_codes[is_light] = ord("@") if bass_val > 0.55 else ord("o")
        ch_codes[is_star] = ord("#")

        char_grid = np.full((ROWS, COLS), 32, dtype=np.int32)
        rgb_grid = np.zeros((ROWS, COLS, 3), dtype=np.float32)

        tw_bg = np.minimum(1.0, (0.45 + 0.38 * np.sin(2.5 * t + bg_ph)) * (1.0 + 0.35 * bass_val)).astype(np.float32)
        char_grid[bg_y, bg_x] = bg_ch
        rgb_grid[bg_y, bg_x, 0] = tw_bg * 0.65
        rgb_grid[bg_y, bg_x, 1] = tw_bg
        rgb_grid[bg_y, bg_x, 2] = np.minimum(1.0, tw_bg + 0.15)

        # Aizawl LiDAR cliffside ridges
        r_act = t >= r_t0s
        if np.any(r_act):
            rr_a = r_rows[r_act]
            rc_a = r_cols[r_act]
            rch_a = r_chs[r_act]
            rfg_a = r_fgs[r_act].copy()
            rph_a = r_phs[r_act]
            ridge_scan_r = int(ROWS * (0.64 - ((t * 0.28) % 0.42)))
            r_scan_hit = np.exp(-((rr_a - ridge_scan_r) / 3.2) ** 2)
            tw_r = np.where(rph_a > 0, (0.78 + 0.22 * np.sin(3.8 * t + rph_a)) * (1.0 + 0.35 * bass_val), 1.0)
            rfg_a = np.clip(rfg_a * tw_r[:, None] + np.array([0.3, 0.85, 1.0])[None, :] * (r_scan_hit[:, None] * 0.65), 0.0, 1.0)
            char_grid[rr_a, rc_a] = np.where((r_scan_hit > 0.55) & (rph_a > 0), ord("#"), rch_a)
            rgb_grid[rr_a, rc_a] = rfg_a

        z_sort = z_depth.copy()
        z_sort[(K_act == BALL) | (K_act == LIGHT) | (K_act == GARLAND)] -= 0.06
        z_sort[(K_act == GIFT) | (K_act == RIBBON) | (K_act == NATIVITY) | ((K_act == STAR) & (Y_orig < 1.0))] -= 0.45
        idx = np.flatnonzero(in_b)
        order = idx[np.argsort(z_sort[idx])[::-1]]
        py_o = py[order]
        px_o = px[order]
        char_grid[py_o, px_o] = ch_codes[order]
        rgb_grid[py_o, px_o] = rgb_pts[order]

        # Vectorized glyph blit with 22% background cell glow
        glyph_masks = atlas[char_grid]
        occupied_mask = (char_grid != 32)[..., None, None].astype(np.float32)
        cell_alpha = np.maximum(glyph_masks, occupied_mask * 0.22)
        colored_cells = cell_alpha[..., None] * rgb_grid[:, :, None, None, :]
        term_img = (
            colored_cells.transpose(0, 2, 1, 3, 4).reshape(ROWS * CH, COLS * CW, 3) * 255.0
        ).astype(np.uint8)

        frame = np.zeros((H, W, 3), dtype=np.uint8)
        frame[:TOP_H] = (6, 10, 16)
        frame[TOP_H:BOT_Y] = (20, 24, 31)
        frame[BOT_Y:] = (13, 16, 23)

        y_off = 12
        x_off = (W - COLS * CW) // 2
        frame[y_off : y_off + ROWS * CH, x_off : x_off + COLS * CW] = np.maximum(
            frame[y_off : y_off + ROWS * CH, x_off : x_off + COLS * CW], term_img
        )

        pil_img = Image.fromarray(frame)
        draw = ImageDraw.Draw(pil_img)

        # LiDAR Celestial Nova Laser Turret Topper (t >= 7.93s)
        if t >= 7.93:
            fade = min(1.0, (t - 7.93) / 0.55)
            sry = (Y1 + 0.09) - cam_y
            scy = sry * cp
            scz = sry * sp
            sz = cam_dist - scz
            sx = int(x_off + (COLS * 0.5) * CW)
            sy = int(y_off + (ROWS * 0.55 - (scy / sz) * fov) * CH)

            y0_g, y1_g = max(0, sy - 80), min(TOP_H, sy + 81)
            x0_g, x1_g = max(0, sx - 80), min(W, sx + 81)
            ky0, ky1 = y0_g - (sy - 80), y1_g - (sy - 80)
            kx0, kx1 = x0_g - (sx - 80), x1_g - (sx - 80)
            sub = np.asarray(pil_img)[y0_g:y1_g, x0_g:x1_g].astype(np.float32)
            gk = glow_kernel[ky0:ky1, kx0:kx1, None] * fade * (1.0 + 0.42 * bass_val)
            cyan_bloom = np.array([65.0, 245.0, 255.0])[None, None, :] * gk * 0.62
            sub = np.clip(sub + cyan_bloom, 0, 255).astype(np.uint8)
            frame_arr = np.asarray(pil_img).copy()
            frame_arr[y0_g:y1_g, x0_g:x1_g] = sub
            pil_img = Image.fromarray(frame_arr)
            draw = ImageDraw.Draw(pil_img)

            ring_glyphs = ["#", "%", "*", "+", ":"]
            for ring in range(2):
                rad_x = (36 if ring == 0 else 54) * fade * (1.0 + 0.22 * bass_val)
                rad_y = (13 if ring == 0 else 20) * fade * (1.0 + 0.22 * bass_val)
                tilt = (0.32 if ring == 0 else -0.28) + 0.15 * np.sin(t * 2.2)
                spd = (2.6 if ring == 0 else -1.9) * t
                n_pts = 18 if ring == 0 else 24
                for k in range(n_pts):
                    ang = (TAU * k) / n_pts + spd
                    lx0 = rad_x * np.cos(ang)
                    ly0 = rad_y * np.sin(ang)
                    px_r = sx + lx0 * np.cos(tilt) - ly0 * np.sin(tilt)
                    py_r = sy + lx0 * np.sin(tilt) + ly0 * np.cos(tilt)
                    d_sh = 0.55 + 0.45 * np.sin(ang)
                    col_r = (0, int(245 * d_sh * fade), int(255 * d_sh * fade)) if ring == 0 else (int(255 * d_sh * fade), int(225 * d_sh * fade), int(115 * d_sh * fade))
                    draw.text((px_r - 3, py_r - 5), ring_glyphs[(k + ring) % 5], fill=col_r, font=font_grid)

            ray_angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi, 5 * np.pi / 4, 3 * np.pi / 2, 7 * np.pi / 4]
            ray_chars = ["-", "/", "|", "\\", "-", "/", "|", "\\"]
            for r_i, r_ang in enumerate(ray_angles):
                max_s = 9 if (r_i % 2 == 0) else 6
                pulse = (1.0 + 0.38 * bass_val) * fade
                for step in range(2, max_s + 1):
                    dist = step * 7.5 * pulse
                    rx = sx + np.cos(r_ang) * dist * 1.15
                    ry = sy - np.sin(r_ang) * dist * 0.85
                    alpha = (1.0 - step / (max_s + 1.5)) * fade
                    col_s = (int(140 * alpha), int(250 * alpha), int(255 * alpha))
                    draw.text((rx - 3, ry - 5), ray_chars[r_i], fill=col_s, font=font_grid)

        # Guiding Star of Bethlehem above the Right Nativity Pavilion (t >= 8.5s)
        if t >= 8.5:
            n_fade = min(1.0, (t - 8.5) / 0.5)
            nat_peak = (np.array([0.82, 0.90, 0.82]) @ sway_m.T - np.array([0.0, cam_y, 0.0])) @ pitch_m.T
            nsz = cam_dist - nat_peak[2]
            nsx = int(x_off + (COLS * 0.5 + (nat_peak[0] / nsz) * fov * 1.68) * CW)
            nsy = int(y_off + (ROWS * 0.55 - (nat_peak[1] / nsz) * fov) * CH)
            draw.text((nsx - 3, nsy - 6), "@", fill=(220, 255, 255), font=font_hud)
            for ds in range(1, 5):
                c_ray = (int(120 * n_fade), int(245 * n_fade), int(255 * n_fade))
                draw.text((nsx - 3 - ds * 6, nsy - 5), "-", fill=c_ray, font=font_grid)
                draw.text((nsx - 3 + ds * 6, nsy - 5), "-", fill=c_ray, font=font_grid)
                if ds <= 3:
                    draw.text((nsx - 3, nsy - 5 - ds * 7), "|", fill=c_ray, font=font_grid)
                    draw.text((nsx - 3, nsy - 5 + ds * 7), ":", fill=(int(255 * n_fade), int(235 * n_fade), int(140 * n_fade)), font=font_grid)

        # Mode 1: Sky Starlight Stage + Vocal EQ Kinetic Lyrics
        active_line = 1 if t >= 7.93 else 0
        line_words = [w for w in LYRIC_WORDS if w[0] == active_line]
        full_str = " ".join(w[1] for w in line_words)
        char_w_px = font_lyric.getlength("M")
        total_w_px = len(full_str) * char_w_px
        start_x = (W - total_w_px) // 2
        base_y = (98, 210, TOP_H - 140)[mode]
        assert total_w_px <= W - 64, "Lyric line exceeds its side margins"


        eq_cols = min(48, (total_w_px + 12) // 8)
        mid_eq = max(1.0, eq_cols / 2.0)
        eq_chars = []
        for c_i in range(eq_cols):
            dist = abs(c_i - mid_eq) / mid_eq
            wave = max(0.0, (1.0 - dist * 0.85) * (0.35 * bass_val + 0.65 * vox_val) * (0.75 + 0.25 * np.sin(c_i * 0.9 - t * 14.0)))
            r_idx = min(len(CIPHER_CHARS) - 1, int(wave * len(CIPHER_CHARS)))
            eq_chars.append(CIPHER_CHARS[r_idx])
        eq_str = "".join(eq_chars)
        eq_col = (255, 92, 138) if is_beth_phase else (0, 245, 255)
        draw.text(((W - len(eq_str) * char_w_px) // 2, base_y + 26), eq_str, fill=eq_col, font=font_lyric)

        cur_x = start_x
        for w_i, (_, w_str, wt0, wt1, is_cr) in enumerate(line_words):
            w_px = len(w_str) * char_w_px
            if wt0 <= t <= wt1:
                bg_c = (175, 20, 62) if is_cr else (0, 125, 165)
                draw.rectangle([cur_x - 3, base_y - 2, cur_x + w_px + 3, base_y + 25], fill=bg_c)
                fg_c = (255, 214, 229) if is_cr else (224, 255, 255)
                draw.text((cur_x, base_y), w_str, fill=fg_c, font=font_lyric)
                sp_c = (255, 117, 159) if is_cr else (0, 245, 255)
                for s_k in range(max(2, int(2 + 3 * vox_val))):
                    sx_p = cur_x + int(((s_k + 0.5) / 4.0) * w_px)
                    sy_p = base_y - 12 - int((t * 18 + s_k * 3) % 7)
                    draw.text((sx_p, sy_p), "*" if s_k % 2 == 0 else "+", fill=sp_c, font=font_hud)
            elif t > wt1:
                fg_c = (255, 117, 159) if is_cr else (126, 249, 255)
                draw.text((cur_x, base_y), w_str, fill=fg_c, font=font_lyric)
            elif t >= wt0 - 0.45:
                prog = (t - (wt0 - 0.45)) / 0.45
                c_word = "".join(
                    ch_o if (c_k / max(1, len(w_str))) < prog * 0.7 else CIPHER_CHARS[int(t * 24 + c_k * 3 + w_i) % len(CIPHER_CHARS)]
                    for c_k, ch_o in enumerate(w_str)
                )
                draw.text((cur_x, base_y), c_word, fill=(88, 166, 255), font=font_lyric)
            else:
                draw.text((cur_x, base_y), "." * len(w_str), fill=(48, 72, 96), font=font_lyric)
            cur_x += (len(w_str) + 1) * char_w_px

        active_lights = int(np.count_nonzero(is_light) // 18)
        occupied_n = int(np.count_nonzero(char_grid != 32))
        letters_count = int(occupied_n * (14784.0 / (COLS * ROWS)))
        beat_bars = min(10, max(1, int(round(bass_val * 10))))
        vox_bars = min(10, max(1, int(round(vox_val * 10))))
        beat_meter = "|" * beat_bars + "." * (10 - beat_bars)
        vox_meter = ":" * vox_bars + "." * (10 - vox_bars)

        draw.text((W - 135, 10), f"LIDAR t {t:05.2f}s", fill=(0, 245, 255), font=font_hud)
        draw.text((W - 155, TOP_H - 40), f"BEAT [{beat_meter}]", fill=(255, 229, 143), font=font_hud)
        draw.text((W - 155, TOP_H - 22), f"VOX  [{vox_meter}]", fill=(0, 245, 255), font=font_hud)

        draw.text((14, TOP_H - 76), "KRISMAS RIM A NAM TAN · AIZAWL LIDAR", fill=(0, 245, 255), font=font_hud)
        draw.text((14, TOP_H - 58), "AIZAWL · 23.733°N 92.718°E · 1,132m", fill=(141, 150, 160), font=font_hud)
        draw.text((14, TOP_H - 40), f"azimuth {rot_deg:06.2f}°   lights {active_lights}", fill=(201, 209, 217), font=font_hud)
        draw.text((14, TOP_H - 22), f"returns {letters_count:,}", fill=(126, 249, 255), font=font_hud)

        graded = np.asarray(pil_img, dtype=np.float32).copy()
        graded[:TOP_H] *= grade_gain[..., None]
        graded[BOT_Y:] *= 1.13
        graded = np.minimum(graded, 255)
        high = graded > 210
        graded[high] = 210 + (graded[high] - 210) * .88
        picture = np.clip(graded[:TOP_H], 0, 255).astype(np.uint8)
        surface = pygame.image.frombuffer(picture.tobytes(), (W, TOP_H), "RGB")
        window.fill((4, 9, 15))
        scale = min(window.get_width() / W, (window.get_height() - 52) / TOP_H)
        size = (max(1, int(W * scale)), max(1, int(TOP_H * scale)))
        window.blit(pygame.transform.smoothscale(surface, size), ((window.get_width() - size[0]) // 2, 52 + (window.get_height() - 52 - size[1]) // 2))
        buttons = []
        for i, label in enumerate(mode_labels):
            rect = pygame.Rect(i * window.get_width() // 3 + 4, 5, window.get_width() // 3 - 8, 40)
            pygame.draw.rect(window, (27, 34, 43) if i == mode else (15, 18, 23), rect, border_radius=10)
            pygame.draw.rect(window, (155, 215, 245) if i == mode else (45, 55, 66), rect, 1, border_radius=10)
            label_image = button_font.render(f"{i+1}. {label}", True, (230, 242, 255))
            if label_image.get_width() > rect.width - 10:
                label_image = pygame.transform.smoothscale(label_image, (max(1, rect.width - 10), label_image.get_height()))
            window.blit(label_image, label_image.get_rect(center=rect.center))
            buttons.append(rect)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()

"""
=========================================
UE5GestureBridge
utils.py

Math and Utility Functions
=========================================
"""

import math



# -------------------------------------
# Calculate distance between two points
# -------------------------------------

def distance(point_a, point_b):

    return math.sqrt(
        (point_a[0] - point_b[0]) ** 2 +
        (point_a[1] - point_b[1]) ** 2
    )



# -------------------------------------
# Calculate 2D angle
# -------------------------------------

def angle(point_a, point_b, point_c):

    """
    Calculates angle ABC

    Example:
    Thumb joint angle
    Finger bend detection
    """

    ba = (
        point_a[0] - point_b[0],
        point_a[1] - point_b[1]
    )

    bc = (
        point_c[0] - point_b[0],
        point_c[1] - point_b[1]
    )


    dot = (
        ba[0] * bc[0] +
        ba[1] * bc[1]
    )


    magnitude = (

        math.sqrt(
            ba[0] ** 2 +
            ba[1] ** 2
        )

        *

        math.sqrt(
            bc[0] ** 2 +
            bc[1] ** 2
        )

    )


    if magnitude == 0:
        return 0


    value = dot / magnitude


    value = max(
        -1,
        min(1,value)
    )


    return math.degrees(
        math.acos(value)
    )



# -------------------------------------
# Normalize value
# -------------------------------------

def normalize(value, minimum, maximum):

    if maximum - minimum == 0:

        return 0


    return (
        value - minimum
    ) / (
        maximum - minimum
    )



# -------------------------------------
# Clamp value
# -------------------------------------

def clamp(value, minimum, maximum):

    return max(
        minimum,
        min(
            maximum,
            value
        )
    )



# -------------------------------------
# Convert pixel coordinates
# to normalized coordinates
# -------------------------------------

def normalize_point(x, y, width, height):

    return (

        round(
            x / width,
            4
        ),

        round(
            y / height,
            4
        )

    )



# -------------------------------------
# FPS Counter helper
# -------------------------------------

class FPSCounter:


    def __init__(self):

        self.start = None

        self.frames = 0

        self.fps = 0



    def update(self):

        import time


        if self.start is None:

            self.start = time.time()


        self.frames += 1


        elapsed = (
            time.time()
            -
            self.start
        )


        if elapsed >= 1:

            self.fps = (
                self.frames /
                elapsed
            )


            self.frames = 0

            self.start = time.time()


        return round(
            self.fps,
            2
        )
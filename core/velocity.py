"""
=========================================
UE5GestureBridge
velocity.py

Hand Movement Velocity Tracking
=========================================
"""

import time
import math



class VelocityTracker:


    """
    Calculates hand movement velocity.

    Useful for:
    - punches
    - throws
    - swings
    - swipes
    - fast gestures
    """



    def __init__(self):

        self.previous_position = None

        self.previous_time = None



    # -------------------------------------
    # Update Position
    # -------------------------------------

    def update(self, position):


        current_time = time.time()


        # First frame

        if self.previous_position is None:

            self.previous_position = position

            self.previous_time = current_time


            return {

                "x": 0,
                "y": 0,

                "speed": 0

            }



        delta_time = (
            current_time -
            self.previous_time
        )


        if delta_time == 0:

            delta_time = 0.001



        velocity_x = (
            position[0]
            -
            self.previous_position[0]
        ) / delta_time



        velocity_y = (
            position[1]
            -
            self.previous_position[1]
        ) / delta_time



        speed = math.sqrt(

            velocity_x ** 2 +
            velocity_y ** 2

        )



        self.previous_position = position

        self.previous_time = current_time



        return {


            "x": round(
                velocity_x,
                4
            ),


            "y": round(
                velocity_y,
                4
            ),


            "speed": round(
                speed,
                4
            )

        }



    # -------------------------------------
    # Direction
    # -------------------------------------

    def direction(self, velocity):


        x = velocity["x"]

        y = velocity["y"]


        threshold = 0.15



        if abs(x) < threshold and abs(y) < threshold:

            return "idle"



        if abs(x) > abs(y):


            if x > 0:

                return "right"

            else:

                return "left"



        else:


            if y > 0:

                return "down"

            else:

                return "up"
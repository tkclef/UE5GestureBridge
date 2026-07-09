"""
=========================================
UE5GestureBridge
gestures.py

Gesture Recognition Engine
=========================================
"""


class GestureRecognizer:

    def __init__(self):

        self.gesture_map = {

            "open_hand": "open_hand",
            "fist": "fist",
            "thumb_up": "thumb_up",
            "point": "point",
            "peace": "peace",
            "rock": "rock",
            "three": "three",
            "four": "four"

        }


    # -------------------------------------
    # Main Gesture Detection
    # -------------------------------------

    def detect(self, fingers, pinch):

        thumb = fingers[0]
        index = fingers[1]
        middle = fingers[2]
        ring = fingers[3]
        pinky = fingers[4]


        total = sum(fingers)


        # Pinch gesture
        if pinch > 0.75:

            return "pinch"


        # Closed fist
        if total == 0:

            return "fist"


        # Open hand

        if total == 5:

            return "open_hand"


        # Thumb up

        if (
            thumb == 1 and
            index == 0 and
            middle == 0 and
            ring == 0 and
            pinky == 0
        ):

            return "thumb_up"


        # Pointing

        if (
            index == 1 and
            middle == 0 and
            ring == 0 and
            pinky == 0
        ):

            return "point"


        # Peace sign

        if (
            index == 1 and
            middle == 1 and
            ring == 0 and
            pinky == 0
        ):

            return "peace"


        # Rock sign

        if (
            index == 1 and
            pinky == 1 and
            middle == 0 and
            ring == 0
        ):

            return "rock"


        # Three fingers

        if total == 3:

            return "three"


        # Four fingers

        if total == 4:

            return "four"


        return "none"
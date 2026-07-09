"""
=========================================
UE5GestureBridge
tracker.py

Integrated Hand Tracking Engine
=========================================
"""

from cvzone.HandTrackingModule import HandDetector

from core.gestures import GestureRecognizer
from core.smoothing import LandmarkSmoother
from core.velocity import VelocityTracker
from core.utils import normalize_point


class HandTracker:


    def __init__(self, detection_confidence=0.8, max_hands=2):

        self.detector = HandDetector(
            detectionCon=detection_confidence,
            maxHands=max_hands
        )


        self.gesture_engine = GestureRecognizer()


        self.smoothers = {

            "left": LandmarkSmoother(0.35),

            "right": LandmarkSmoother(0.35)

        }


        self.velocity = {

            "left": VelocityTracker(),

            "right": VelocityTracker()

        }



    # -------------------------------------
    # Pinch strength
    # -------------------------------------

    def calculate_pinch(self, landmarks):

        thumb = landmarks[4]

        index = landmarks[8]


        distance = (

            (
                (thumb[0] - index[0]) ** 2
            )

            +

            (
                (thumb[1] - index[1]) ** 2
            )

        ) ** 0.5


        strength = 1 - min(
            distance / 120,
            1
        )


        return round(
            strength,
            3
        )



    # -------------------------------------
    # Process one hand
    # -------------------------------------

    def process_hand(self, hand, width, height):


        hand_type = hand["type"].lower()


        lm_list = hand["lmList"]


        # Smooth landmarks

        landmarks = []


        raw_landmarks = []


        for point in lm_list:


            raw_landmarks.append({

                "x": point[0],

                "y": point[1],

                "z": point[2]

            })



        landmarks = self.smoothers[hand_type].update(
            raw_landmarks
        )



        # Convert to normalized coordinates

        normalized = []


        for point in landmarks:

            x, y = normalize_point(

                point["x"],

                point["y"],

                width,

                height

            )


            normalized.append({

                "x": x,

                "y": y,

                "z": point["z"]

            })



        fingers = self.detector.fingersUp(
            hand
        )


        pinch = self.calculate_pinch(
            lm_list
        )


        gesture = self.gesture_engine.detect(

            fingers,

            pinch

        )


        center = hand["center"]


        center_normalized = normalize_point(

            center[0],

            center[1],

            width,

            height

        )


        wrist = normalize_point(

            lm_list[0][0],

            lm_list[0][1],

            width,

            height

        )


        velocity = self.velocity[hand_type].update(

            center_normalized

        )



        return {


            "tracked": True,


            "hand": hand_type,


            "gesture": gesture,


            "fingers": fingers,


            "pinch": pinch,


            "center": center_normalized,


            "wrist": wrist,


            "velocity": velocity,


            "landmarks": normalized


        }



    # -------------------------------------
    # Update tracker
    # -------------------------------------

    def update(self, frame):


        hands, frame = self.detector.findHands(
            frame
        )


        height, width = frame.shape[:2]


        result = []



        if hands:


            for hand in hands:


                result.append(

                    self.process_hand(

                        hand,

                        width,

                        height

                    )

                )



        return frame, result
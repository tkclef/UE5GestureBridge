"""
=========================================
UE5GestureBridge
tracker.py
=========================================
"""

import math

from cvzone.HandTrackingModule import HandDetector
from core.gestures import GestureRecognizer


class HandTracker:

    def __init__(self):

        self.detector = HandDetector(
            detectionCon=0.8,
            maxHands=2
        )

        self.gesture = GestureRecognizer()

    # -------------------------------------
    # Normalize coordinates
    # -------------------------------------

    def normalize(self, x, y, width, height):

        return (
            round(x / width, 4),
            round(y / height, 4)
        )

    # -------------------------------------
    # Distance
    # -------------------------------------

    def distance(self, p1, p2):

        return math.sqrt(
            (p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2
        )

    # -------------------------------------
    # Pinch Strength
    # -------------------------------------

    def pinch_strength(self, lmList, bbox):

        thumb = lmList[4]
        index = lmList[8]

        dist = self.distance(thumb, index)

        hand_size = max(bbox[2], bbox[3])

        strength = 1.0 - min(dist / hand_size, 1.0)

        return round(strength, 3)

    # -------------------------------------
    # Build Hand Packet
    # -------------------------------------

    def build_hand_data(self, hand, width, height):

        lmList = hand["lmList"]

        bbox = hand["bbox"]

        center = hand["center"]

        hand_type = hand["type"].lower()

        fingers = self.detector.fingersUp(hand)

        gesture = self.gesture.detect(
            fingers,
            self.pinch_strength(lmList, bbox)
        )

        landmarks = []

        for point in lmList:

            nx, ny = self.normalize(
                point[0],
                point[1],
                width,
                height
            )

            landmarks.append({
                "x": nx,
                "y": ny,
                "z": point[2]
            })

        cx, cy = self.normalize(
            center[0],
            center[1],
            width,
            height
        )

        wx, wy = self.normalize(
            lmList[0][0],
            lmList[0][1],
            width,
            height
        )

        return {

            "tracked": True,

            "hand": hand_type,

            "gesture": gesture,

            "fingers": fingers,

            "pinch": self.pinch_strength(
                lmList,
                bbox
            ),

            "center": (cx, cy),

            "wrist": (wx, wy),

            "bbox": bbox,

            "landmarks": landmarks

        }

    # -------------------------------------
    # Update
    # -------------------------------------

    def update(self, frame):

        hands, frame = self.detector.findHands(frame)

        h, w = frame.shape[:2]

        packet = []

        if hands:

            for hand in hands:

                packet.append(

                    self.build_hand_data(
                        hand,
                        w,
                        h
                    )

                )

        return frame, packet
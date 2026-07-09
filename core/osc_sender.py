"""
=========================================
UE5GestureBridge
osc_sender.py

Unreal Engine 5 OSC Communication Layer
=========================================
"""

from pythonosc.udp_client import SimpleUDPClient
import time


class OSCSender:

    def __init__(self, ip="127.0.0.1", port=8000):

        self.client = SimpleUDPClient(
            ip,
            port
        )

        print(
            f"OSC Connected -> {ip}:{port}"
        )


    # -------------------------------------
    # Send Hand Data
    # -------------------------------------

    def send(self, hands):

        current_hands = {
            "left": False,
            "right": False
        }


        for hand in hands:

            hand_name = hand["hand"]

            current_hands[hand_name] = True


            prefix = (
                f"/UE5GestureBridge/{hand_name}"
            )


            # Tracking state

            self.client.send_message(
                f"{prefix}/tracked",
                1
            )


            # Gesture

            self.client.send_message(
                f"{prefix}/gesture",
                hand["gesture"]
            )


            # Finger states

            self.client.send_message(
                f"{prefix}/fingers",
                hand["fingers"]
            )


            # Pinch strength

            self.client.send_message(
                f"{prefix}/pinch",
                hand["pinch"]
            )


            # Wrist position

            self.client.send_message(
                f"{prefix}/wrist",
                [
                    hand["wrist"][0],
                    hand["wrist"][1]
                ]
            )


            # Palm center

            self.client.send_message(
                f"{prefix}/center",
                [
                    hand["center"][0],
                    hand["center"][1]
                ]
            )


            # Send landmarks

            self.send_landmarks(
                prefix,
                hand["landmarks"]
            )


        self.send_timestamp()



    # -------------------------------------
    # Send 21 MediaPipe Landmarks
    # -------------------------------------

    def send_landmarks(self, prefix, landmarks):

        for index, point in enumerate(landmarks):

            self.client.send_message(

                f"{prefix}/landmark/{index}",

                [
                    point["x"],
                    point["y"],
                    point["z"]
                ]

            )



    # -------------------------------------
    # Sync timestamp
    # -------------------------------------

    def send_timestamp(self):

        self.client.send_message(

            "/UE5GestureBridge/time",

            time.time()

        )
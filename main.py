"""
====================================================
UE5GestureBridge
Author: Tkclef Theonel
Version: 0.1
====================================================
"""

import cv2

from core.tracker import HandTracker
from core.osc_sender import OSCSender


class UE5GestureBridge:

    def __init__(self):

        self.camera = cv2.VideoCapture(0)

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        if not self.camera.isOpened():
            raise RuntimeError("Unable to open camera.")

        self.tracker = HandTracker()

        self.osc = OSCSender(
            ip="127.0.0.1",
            port=8000
        )

        print("=" * 45)
        print("UE5GestureBridge Started")
        print("Camera Ready")
        print("OSC Ready")
        print("Press Q to Exit")
        print("=" * 45)

    def run(self):

        while True:

            success, frame = self.camera.read()

            if not success:
                continue

            frame, hands = self.tracker.update(frame)

            self.osc.send(hands)

            cv2.imshow("UE5GestureBridge", frame)

            key = cv2.waitKey(1)

            if key & 0xFF == ord("q"):
                break

        self.camera.release()

        cv2.destroyAllWindows()


if __name__ == "__main__":

    bridge = UE5GestureBridge()

    bridge.run()
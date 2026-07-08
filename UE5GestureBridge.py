import cv2
import time
import json

from cvzone.HandTrackingModule import HandDetector
from pythonosc.udp_client import SimpleUDPClient


class UE5GestureBridge:

    def __init__(self, camera_id=0, osc_ip="127.0.0.1", osc_port=8000):

        self.cap = cv2.VideoCapture(camera_id)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.detector = HandDetector(
            detectionCon=0.8,
            maxHands=2
        )

        self.osc = SimpleUDPClient(
            osc_ip,
            osc_port
        )

        self.previous_hands = {
            "left": False,
            "right": False
        }

        print("================================")
        print(" UE5GestureBridge Started")
        print(" Press Q to exit")
        print("================================")


    def normalize(self, value, max_value):
        return round(value / max_value, 4)


    def detect_gestures(self, hand):

        fingers = self.detector.fingersUp(hand)

        gesture = "none"

        if fingers[0] == 1 and sum(fingers[1:]) == 0:
            gesture = "thumb_up"

        elif sum(fingers) == 5:
            gesture = "open_hand"

        elif sum(fingers) == 0:
            gesture = "fist"

        elif fingers[1] == 1 and sum(fingers[2:]) == 0:
            gesture = "point"

        return gesture, fingers


    def process_hand(self, hand, frame):

        height, width = frame.shape[:2]

        hand_type = hand["type"].lower()

        landmarks = []

        for point in hand["lmList"]:

            x, y, z = point

            landmarks.append([
                self.normalize(x, width),
                self.normalize(y, height),
                z
            ])


        center = hand["center"]

        center_data = [
            self.normalize(center[0], width),
            self.normalize(center[1], height)
        ]


        gesture, fingers = self.detect_gestures(hand)


        data = {

            "hand": hand_type,

            "tracked": True,

            "gesture": gesture,

            "fingers": fingers,

            "center": center_data,

            "landmarks": landmarks,

            "timestamp": time.time()

        }


        return data


    def send(self, data):

        message = json.dumps(data)

        self.osc.send_message(
            "/UE5GestureBridge/hand",
            message
        )


    def run(self):

        while True:

            success, frame = self.cap.read()

            if not success:
                break


            hands, frame = self.detector.findHands(frame)


            current_hands = {
                "left": False,
                "right": False
            }


            if hands:

                for hand in hands:

                    data = self.process_hand(
                        hand,
                        frame
                    )

                    current_hands[data["hand"]] = True

                    self.send(data)



            for hand in current_hands:

                if (
                    self.previous_hands[hand]
                    and not current_hands[hand]
                ):

                    self.send({

                        "hand": hand,

                        "tracked": False,

                        "timestamp": time.time()

                    })


            self.previous_hands = current_hands


            cv2.imshow(
                "UE5GestureBridge",
                frame
            )


            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


        self.cap.release()

        cv2.destroyAllWindows()



if __name__ == "__main__":

    bridge = UE5GestureBridge()

    bridge.run()
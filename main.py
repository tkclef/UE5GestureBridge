"""
=========================================
UE5GestureBridge

main.py

Main Application Entry
=========================================
"""

import cv2
import time

from core.config import Config
from core.tracker import HandTracker
from core.osc_sender import OSCSender
from core.utils import FPSCounter



class UE5GestureBridge:


    def __init__(self):


        # -----------------------------
        # Camera
        # -----------------------------

        self.camera = cv2.VideoCapture(
            Config.CAMERA_ID
        )


        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            Config.CAMERA_WIDTH
        )


        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            Config.CAMERA_HEIGHT
        )


        if not self.camera.isOpened():

            raise RuntimeError(
                "Camera could not be opened"
            )



        # -----------------------------
        # Modules
        # -----------------------------

        self.tracker = HandTracker(

            detection_confidence=
            Config.DETECTION_CONFIDENCE,

            max_hands=
            Config.MAX_HANDS

        )


        self.osc = OSCSender(

            ip=Config.OSC_IP,

            port=Config.OSC_PORT

        )


        self.fps = FPSCounter()



        print("=" * 50)

        print("UE5GestureBridge Started")

        print(
            f"Camera: {Config.CAMERA_WIDTH}x{Config.CAMERA_HEIGHT}"
        )

        print(
            f"OSC: {Config.OSC_IP}:{Config.OSC_PORT}"
        )

        print("Press Q to exit")

        print("=" * 50)



    # ---------------------------------
    # Main Loop
    # ---------------------------------

    def run(self):


        try:


            while True:


                success, frame = self.camera.read()


                if not success:

                    continue



                frame, hands = self.tracker.update(

                    frame

                )



                # Send data to Unreal

                self.osc.send(

                    hands

                )



                fps = self.fps.update()



                cv2.putText(

                    frame,

                    f"FPS: {fps}",

                    (20,40),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    1,

                    (0,255,0),

                    2

                )



                cv2.imshow(

                    "UE5GestureBridge",

                    frame

                )



                if cv2.waitKey(1) & 0xFF == ord("q"):

                    break



                # Maintain target frame rate

                time.sleep(
                    1 / Config.TARGET_FPS
                )



        except KeyboardInterrupt:

            print(
                "Stopping..."
            )


        finally:

            self.shutdown()



    # ---------------------------------
    # Cleanup
    # ---------------------------------

    def shutdown(self):


        self.camera.release()

        cv2.destroyAllWindows()


        print(
            "UE5GestureBridge Closed"
        )




if __name__ == "__main__":


    bridge = UE5GestureBridge()


    bridge.run()
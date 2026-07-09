"""
=========================================
UE5GestureBridge
config.py

Central Configuration
=========================================
"""


class Config:


    # -------------------------------
    # Camera Settings
    # -------------------------------

    CAMERA_ID = 0

    CAMERA_WIDTH = 1280

    CAMERA_HEIGHT = 720



    # -------------------------------
    # MediaPipe Settings
    # -------------------------------

    DETECTION_CONFIDENCE = 0.8

    MAX_HANDS = 2



    # -------------------------------
    # Unreal OSC Settings
    # -------------------------------

    OSC_IP = "127.0.0.1"

    OSC_PORT = 8000



    # -------------------------------
    # Filtering
    # -------------------------------

    SMOOTHING_ALPHA = 0.35



    # -------------------------------
    # Performance
    # -------------------------------

    TARGET_FPS = 60
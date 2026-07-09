"""
=========================================
UE5GestureBridge
smoothing.py

Hand Tracking Data Smoothing
=========================================
"""



class ExponentialSmoother:

    """
    Simple EMA (Exponential Moving Average)
    filter.

    Reduces MediaPipe landmark jitter while
    keeping low latency.
    """


    def __init__(self, alpha=0.35):

        self.alpha = alpha

        self.previous = None



    def update(self, value):

        # First frame

        if self.previous is None:

            self.previous = value

            return value



        # Smooth numeric values

        if isinstance(value, (int, float)):

            result = (
                self.alpha * value +
                (1 - self.alpha) * self.previous
            )


        # Smooth arrays

        elif isinstance(value, list):

            result = []

            for current, old in zip(
                value,
                self.previous
            ):

                result.append(
                    self.alpha * current +
                    (1 - self.alpha) * old
                )


        # Smooth tuples

        elif isinstance(value, tuple):

            result = tuple(

                self.alpha * current +
                (1 - self.alpha) * old

                for current, old in zip(
                    value,
                    self.previous
                )

            )


        else:

            result = value



        self.previous = result

        return result




class LandmarkSmoother:


    """
    Smooths MediaPipe's 21 hand landmarks.
    """


    def __init__(self, alpha=0.35):

        self.alpha = alpha

        self.landmarks = []



    def update(self, landmarks):


        # First frame

        if not self.landmarks:

            self.landmarks = landmarks

            return landmarks



        smoothed = []


        for current, previous in zip(
            landmarks,
            self.landmarks
        ):


            smoothed.append({

                "x":
                    self.alpha * current["x"]
                    +
                    (1-self.alpha) * previous["x"],


                "y":
                    self.alpha * current["y"]
                    +
                    (1-self.alpha) * previous["y"],


                "z":
                    self.alpha * current["z"]
                    +
                    (1-self.alpha) * previous["z"]

            })



        self.landmarks = smoothed


        return smoothed
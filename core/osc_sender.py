def send(self, hands):

    # Default state
    left_found = False
    right_found = False

    for hand in hands:

        hand_name = hand["hand"]

        if hand_name == "left":
            left_found = True
        elif hand_name == "right":
            right_found = True

        prefix = f"/UE5GestureBridge/{hand_name}"

        self.client.send_message(f"{prefix}/tracked", 1)
        self.client.send_message(f"{prefix}/gesture", hand["gesture"])
        self.client.send_message(f"{prefix}/fingers", hand["fingers"])
        self.client.send_message(f"{prefix}/pinch", hand["pinch"])
        self.client.send_message(f"{prefix}/wrist", list(hand["wrist"]))
        self.client.send_message(f"{prefix}/center", list(hand["center"]))

        self.send_landmarks(prefix, hand["landmarks"])

    # Tell UE5 when a hand is NOT visible
    if not left_found:
        self.client.send_message("/UE5GestureBridge/left/tracked", 0)

    if not right_found:
        self.client.send_message("/UE5GestureBridge/right/tracked", 0)

    self.send_timestamp()
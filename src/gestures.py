class GestureRecognizer:
    def __init__(self):
        pass

    def is_index_finger_up(self, hand_landmarks):
        index_tip = hand_landmarks.landmark[8]
        index_pip = hand_landmarks.landmark[6]

        return index_tip.y < index_pip.y
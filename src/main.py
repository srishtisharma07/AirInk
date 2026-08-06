import cv2

from hand_tracker import HandTracker
from gestures import GestureRecognizer


cap = cv2.VideoCapture(0)

tracker = HandTracker()
gesture = GestureRecognizer()

canvas = None

prev_x = None
prev_y = None

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = frame.copy()
        canvas[:] = 255

    frame, results = tracker.find_hands(frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            index_tip = hand_landmarks.landmark[8]

            h, w, _ = frame.shape
            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

            index_up = gesture.is_index_finger_up(hand_landmarks)
            middle_up = gesture.is_middle_finger_up(hand_landmarks)

            if index_up and not middle_up:

                cv2.putText(
                    frame,
                    "DRAW MODE",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

                if prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), (255, 0, 255), 5)

                prev_x = x
                prev_y = y

            elif index_up and middle_up:
                cv2.putText(
                    frame,
                    "SELECTION MODE",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2,
                )

                prev_x = None
                prev_y = None

            else:
                prev_x = None
                prev_y = None

    else:
        prev_x = None
        prev_y = None

    cv2.imshow("AirInk", frame)
    cv2.imshow("Canvas", canvas)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
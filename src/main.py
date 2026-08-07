import cv2
import os
from datetime import datetime

from constants import *
from hand_tracker import HandTracker
from gestures import GestureRecognizer
from drawing import DrawingCanvas


def main():

    tracker = HandTracker()
    gesture = GestureRecognizer()
    drawing = DrawingCanvas()

    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    os.makedirs("drawings", exist_ok=True)

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        drawing.initialize(frame)

        frame, results = tracker.find_hands(frame)

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                index_tip = hand_landmarks.landmark[8]

                h, w, _ = frame.shape

                x = int(index_tip.x * w)
                y = int(index_tip.y * h)

                cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

                index_up = gesture.is_index_finger_up(hand_landmarks)
                middle_up = gesture.is_middle_finger_up(hand_landmarks)

                if index_up and not middle_up:

                    cv2.putText(
                        frame,
                        "DRAW MODE",
                        (20, 110),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2,
                    )

                    drawing.draw(x, y)

                elif index_up and middle_up:

                    cv2.putText(
                        frame,
                        "SELECTION MODE",
                        (20, 110),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 0, 0),
                        2,
                    )

                    drawing.reset()
                    drawing.select_color(x, y)

                else:
                    drawing.reset()

        else:
            drawing.reset()

        overlay = cv2.addWeighted(
            frame,
            0.7,
            drawing.canvas,
            0.3,
            0,
        )

        drawing.draw_toolbar(overlay)

        cv2.imshow("AirInk", overlay)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):

            filename = datetime.now().strftime(
                "drawings/drawing_%Y%m%d_%H%M%S.png"
            )

            cv2.imwrite(filename, drawing.canvas)

            print(f"Drawing saved to {filename}")

        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
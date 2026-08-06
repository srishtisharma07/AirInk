import cv2

from hand_tracker import HandTracker
from gestures import GestureRecognizer
from drawing import DrawingCanvas


def main():
    tracker = HandTracker()
    gesture = GestureRecognizer()
    drawing = DrawingCanvas()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

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

                    drawing.draw(x, y)

                elif index_up and middle_up:

                    cv2.putText(
                        frame,
                        "SELECTION MODE",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                        2,
                    )

                    drawing.reset()
                    drawing.select_color(x, y)

                else:
                    drawing.reset()

        else:
            drawing.reset()

        drawing.draw_toolbar(frame)
        cv2.imshow("AirInk", frame)
        cv2.imshow("Canvas", drawing.canvas)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
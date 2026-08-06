import cv2

from hand_tracker import HandTracker
from gestures import GestureRecognizer
from drawing import DrawingCanvas


def main():
    # Initialize components
    tracker = HandTracker()
    gesture = GestureRecognizer()
    drawing = DrawingCanvas()

    # Open webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        success, frame = cap.read()

        if not success:
            break

        # Mirror effect
        frame = cv2.flip(frame, 1)

        # Initialize white canvas only once
        drawing.initialize(frame)

        # Detect hands
        frame, results = tracker.find_hands(frame)

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                # Get index fingertip
                index_tip = hand_landmarks.landmark[8]

                h, w, _ = frame.shape
                x = int(index_tip.x * w)
                y = int(index_tip.y * h)

                # Green circle on fingertip
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

                # Detect gestures
                index_up = gesture.is_index_finger_up(hand_landmarks)
                middle_up = gesture.is_middle_finger_up(hand_landmarks)

                # ---------------- DRAW MODE ----------------
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

                # ---------------- SELECTION MODE ----------------
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

                # ---------------- OTHER GESTURES ----------------
                else:
                    drawing.reset()

        else:
            drawing.reset()

        # Display windows
        drawing.draw_toolbar(frame)
        cv2.imshow("AirInk", frame)
        cv2.imshow("Canvas", drawing.canvas)

        # Quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
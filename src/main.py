import cv2
from datetime import datetime

from hand_tracker import HandTracker
from gestures import GestureRecognizer
from drawing import DrawingCanvas
from constants import GREEN, BLUE

def save_drawing(canvas):
    if canvas is None:
        return

    filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
    path = f"drawings/{filename}"

    cv2.imwrite(path, canvas)

    print(f"Drawing saved: {path}")


def main():

    tracker = HandTracker()
    gesture = GestureRecognizer()
    drawing = DrawingCanvas()

    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

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

                cv2.circle(
                    frame,
                    (x, y),
                    8,
                    (0, 255, 0),
                    -1
                )

                index_up = gesture.is_index_finger_up(
                    hand_landmarks
                )

                middle_up = gesture.is_middle_finger_up(
                    hand_landmarks
                )

                # ==========================================
                # DRAW MODE
                # ==========================================

                if index_up and not middle_up:

                    cv2.putText(
                        frame,
                        "DRAW MODE",
                        (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        GREEN,
                        2,
                    )

                    drawing.draw(x, y)

                # ==========================================
                # SELECTION MODE
                # ==========================================

                elif index_up and middle_up:

                    cv2.putText(
                        frame,
                        "SELECTION MODE",
                        (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        BLUE,
                        2,
                    )

                    drawing.reset()

                    action = drawing.select_color(x, y)

                    if action == "save":
                        save_drawing(drawing.canvas)

                # ==========================================
                # IDLE
                # ==========================================

                else:

                    drawing.reset()

        else:

            drawing.reset()

        # Draw toolbar AFTER hand detection
        drawing.draw_toolbar(frame)

        cv2.imshow("AirInk", frame)

        cv2.imshow(
            "Canvas",
            drawing.canvas
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
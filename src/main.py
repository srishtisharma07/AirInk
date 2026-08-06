import cv2

from hand_tracker import HandTracker
from gestures import GestureRecognizer


# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize classes
tracker = HandTracker()
gesture = GestureRecognizer()

# Canvas for drawing
canvas = None

# Previous finger position
prev_x = None
prev_y = None

while True:
    success, frame = cap.read()

    if not success:
        break

    # Flip the frame for mirror effect
    frame = cv2.flip(frame, 1)

    # Create canvas only once
    if canvas is None:
        canvas = frame.copy()
        canvas[:] = 255

    # Detect hands
    frame, results = tracker.find_hands(frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Get index finger tip
            index_tip = hand_landmarks.landmark[8]

            h, w, _ = frame.shape
            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            # Draw green circle on fingertip
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

            # Check if index finger is raised
            if gesture.is_index_finger_up(hand_landmarks):

                cv2.putText(
                    frame,
                    "DRAW MODE",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

                # Draw on canvas
                if prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), (255, 0, 255), 5)

                prev_x = x
                prev_y = y

            else:
                # Reset previous point so new strokes don't connect
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
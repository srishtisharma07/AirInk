import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Drawing utilities
mp_draw = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        break

    # Flip for a mirror view
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    results = hands.process(rgb_frame)

    # If hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
            
            # Get index finger tip
            index_tip = hand_landmarks.landmark[8]

            # Convert normalized coordinates to pixel coordinates
            h, w, _ = frame.shape
            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            # Draw a green circle on the index finger tip
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

            # Print coordinates in terminal
            print(f"Index Finger: ({x}, {y})")

    cv2.imshow("AirInk", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
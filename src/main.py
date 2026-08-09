import cv2
import os
import time

from hand_tracker import HandTracker
from gestures import GestureRecognizer
from drawing import DrawingCanvas
from constants import GREEN, BLUE


def save_drawing(canvas):

    if canvas is None:
        return False

    os.makedirs("drawings", exist_ok=True)

    filename = time.strftime(
        "drawing_%Y%m%d_%H%M%S.png"
    )

    path = os.path.join(
        "drawings",
        filename
    )

    success = cv2.imwrite(
        path,
        canvas
    )

    if success:
        print(f"Drawing saved: {path}")

    return success


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

    # =========================================================
    # SAVE NOTIFICATION
    # =========================================================

    notification = ""
    notification_start = 0
    notification_duration = 2

    # =========================================================
    # COLOR SELECTION STATE
    # =========================================================

    # Currently hovered color
    hovered_color = None

    # When the finger first entered that color
    color_hover_start = 0

    # Time required to hold over a color
    color_selection_delay = 0.55

    # Prevent immediate repeated toolbar actions
    last_action_time = 0
    action_cooldown = 0.35

    # =========================================================
    # MAIN LOOP
    # =========================================================

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        drawing.initialize(frame)

        frame, results = tracker.find_hands(frame)

        # =====================================================
        # HAND DETECTED
        # =====================================================

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                index_tip = hand_landmarks.landmark[8]

                h, w, _ = frame.shape

                x = int(index_tip.x * w)
                y = int(index_tip.y * h)

                # -------------------------------------------------
                # Fingertip
                # -------------------------------------------------

                cv2.circle(
                    frame,
                    (x, y),
                    8,
                    (0, 255, 0),
                    -1
                )

                # -------------------------------------------------
                # Gestures
                # -------------------------------------------------

                index_up = gesture.is_index_finger_up(
                    hand_landmarks
                )

                middle_up = gesture.is_middle_finger_up(
                    hand_landmarks
                )

                # =================================================
                # DRAW MODE
                # =================================================

                if index_up and not middle_up:

                    cv2.putText(
                        frame,
                        "DRAW MODE",
                        (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        GREEN,
                        2
                    )

                    # Reset color-hover state
                    hovered_color = None
                    color_hover_start = 0

                    drawing.draw(x, y)

                # =================================================
                # SELECTION MODE
                # =================================================

                elif index_up and middle_up:

                    cv2.putText(
                        frame,
                        "SELECTION MODE",
                        (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        BLUE,
                        2
                    )

                    drawing.reset()

                    current_time = time.time()

                    # =================================================
                    # PALETTE IS OPEN
                    # =================================================

                    if drawing.show_color_palette:

                        # -------------------------------------------------
                        # IMPORTANT:
                        #
                        # Do NOT call drawing.select_color() immediately.
                        #
                        # First determine whether the finger is actually
                        # sitting over a color.
                        # -------------------------------------------------

                        current_color = None

                        # Red
                        if 120 <= x <= 162 and 68 <= y <= 108:
                            current_color = "red"

                        # Green
                        elif 177 <= x <= 219 and 68 <= y <= 108:
                            current_color = "green"

                        # Blue
                        elif 234 <= x <= 276 and 68 <= y <= 108:
                            current_color = "blue"

                        # Black
                        elif 291 <= x <= 333 and 68 <= y <= 108:
                            current_color = "black"

                        # Yellow
                        elif 348 <= x <= 390 and 68 <= y <= 108:
                            current_color = "yellow"

                        # Purple
                        elif 405 <= x <= 447 and 68 <= y <= 108:
                            current_color = "purple"

                        # -------------------------------------------------
                        # Finger is NOT over a color
                        # -------------------------------------------------

                        if current_color is None:

                            hovered_color = None
                            color_hover_start = 0

                        # -------------------------------------------------
                        # Finger is over a color
                        # -------------------------------------------------

                        else:

                            # Finger moved onto a new color
                            if current_color != hovered_color:

                                hovered_color = current_color
                                color_hover_start = current_time

                            # -------------------------------------------------
                            # Show selection progress
                            # -------------------------------------------------

                            elapsed = (
                                current_time
                                - color_hover_start
                            )

                            progress = min(
                                elapsed / color_selection_delay,
                                1.0
                            )

                            # Progress bar
                            cv2.rectangle(
                                frame,
                                (120, 125),
                                (447, 140),
                                (80, 80, 80),
                                -1
                            )

                            progress_width = int(
                                327 * progress
                            )

                            cv2.rectangle(
                                frame,
                                (120, 125),
                                (
                                    120 + progress_width,
                                    140
                                ),
                                BLUE,
                                -1
                            )

                            # -------------------------------------------------
                            # Color selected
                            # -------------------------------------------------

                            if elapsed >= color_selection_delay:

                                # Map our temporary color name to
                                # the actual palette coordinate.
                                color_positions = {
                                    "red": (140, 85),
                                    "green": (197, 85),
                                    "blue": (254, 85),
                                    "black": (311, 85),
                                    "yellow": (368, 85),
                                    "purple": (425, 85)
                                }

                                select_x, select_y = (
                                    color_positions[current_color]
                                )

                                drawing.select_color(
                                    select_x,
                                    select_y
                                )

                                hovered_color = None
                                color_hover_start = 0

                                last_action_time = (
                                    current_time
                                )

                    # =================================================
                    # PALETTE CLOSED
                    # =================================================

                    else:

                        # -------------------------------------------------
                        # Only process toolbar actions after cooldown
                        # -------------------------------------------------

                        if (
                            current_time - last_action_time
                            >= action_cooldown
                        ):

                            # ---------------------------------------------
                            # Color button
                            # ---------------------------------------------

                            if (
                                110 <= x <= 235
                                and 5 <= y <= 65
                            ):

                                drawing.select_color(
                                    x,
                                    y
                                )

                                last_action_time = (
                                    current_time
                                )

                            # ---------------------------------------------
                            # Eraser / Clear / Save / Brush
                            # ---------------------------------------------

                            elif (
                                225 <= x <= 800
                                and 5 <= y <= 65
                            ):

                                action = drawing.select_color(
                                    x,
                                    y
                                )

                                last_action_time = (
                                    current_time
                                )

                                # -----------------------------------------
                                # SAVE
                                # -----------------------------------------

                                if action == "save":

                                    saved = save_drawing(
                                        drawing.canvas
                                    )

                                    if saved:

                                        notification = (
                                            "Drawing Saved!"
                                        )

                                        notification_start = (
                                            time.time()
                                        )

                # =================================================
                # IDLE
                # =================================================

                else:

                    drawing.reset()

                    hovered_color = None
                    color_hover_start = 0

        # =====================================================
        # NO HAND
        # =====================================================

        else:

            drawing.reset()

            # Keep the palette open if it was already open.
            # Only reset the temporary color hover.
            hovered_color = None
            color_hover_start = 0

        # =====================================================
        # TOOLBAR
        # =====================================================

        drawing.draw_toolbar(frame)

        # =====================================================
        # SAVE NOTIFICATION
        # =====================================================

        if notification:

            elapsed = (
                time.time()
                - notification_start
            )

            if elapsed < notification_duration:

                cv2.rectangle(
                    frame,
                    (300, 150),
                    (660, 210),
                    (50, 50, 50),
                    -1
                )

                cv2.putText(
                    frame,
                    "Drawing Saved!",
                    (335, 190),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    GREEN,
                    2
                )

            else:

                notification = ""

        # =====================================================
        # WINDOWS
        # =====================================================

        cv2.imshow(
            "AirInk",
            frame
        )

        cv2.imshow(
            "Canvas",
            drawing.canvas
        )

        # =====================================================
        # KEYBOARD
        # =====================================================

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    # =========================================================
    # CLEANUP
    # =========================================================

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
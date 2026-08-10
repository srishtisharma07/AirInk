import cv2
from constants import *


class DrawingCanvas:

    def __init__(self):

        # =====================================================
        # CANVAS
        # =====================================================

        self.canvas = None

        # =====================================================
        # DRAWING POSITION
        # =====================================================

        self.prev_x = None
        self.prev_y = None

        self.smooth_x = None
        self.smooth_y = None

        # =====================================================
        # DRAWING SETTINGS
        # =====================================================

        self.min_movement = 1

        self.color = PURPLE
        self.selected_color = PURPLE

        # Brush sizes
        self.thickness = 6

        self.eraser_thickness = 45

        # =====================================================
        # COLOR PALETTE
        # =====================================================

        self.show_color_palette = False

    # =========================================================
    # INITIALIZE CANVAS
    # =========================================================

    def initialize(self, frame):

        if self.canvas is None:

            self.canvas = frame.copy()

            self.canvas[:] = WHITE

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self, x, y):

        # -----------------------------------------------------
        # First point
        # -----------------------------------------------------

        if self.smooth_x is None:

            self.smooth_x = float(x)
            self.smooth_y = float(y)

            self.prev_x = int(x)
            self.prev_y = int(y)

            return

        # -----------------------------------------------------
        # Calculate movement
        # -----------------------------------------------------

        dx = x - self.smooth_x
        dy = y - self.smooth_y

        distance = (dx * dx + dy * dy) ** 0.5

        # -----------------------------------------------------
        # Adaptive smoothing
        # -----------------------------------------------------

        if distance < 5:

            alpha = 0.12

        elif distance < 12:

            alpha = 0.22

        elif distance < 25:

            alpha = 0.38

        else:

            alpha = 0.60

        self.smooth_x += alpha * dx
        self.smooth_y += alpha * dy

        current_x = int(round(self.smooth_x))
        current_y = int(round(self.smooth_y))

        # -----------------------------------------------------
        # Brush / eraser thickness
        # -----------------------------------------------------

        if self.color == WHITE:

            thickness = self.eraser_thickness

        else:

            thickness = self.thickness

        # -----------------------------------------------------
        # Draw line
        # -----------------------------------------------------

        if self.prev_x is not None:

            dx = current_x - self.prev_x
            dy = current_y - self.prev_y

            movement = (dx * dx + dy * dy) ** 0.5

            if movement >= self.min_movement:

                cv2.line(
                    self.canvas,
                    (self.prev_x, self.prev_y),
                    (current_x, current_y),
                    self.color,
                    thickness,
                    cv2.LINE_AA
                )

        # -----------------------------------------------------
        # Update position
        # -----------------------------------------------------

        self.prev_x = current_x
        self.prev_y = current_y

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.prev_x = None
        self.prev_y = None

        self.smooth_x = None
        self.smooth_y = None

    # =========================================================
    # CLEAR CANVAS
    # =========================================================

    def clear_canvas(self):

        if self.canvas is not None:

            self.canvas[:] = WHITE

        self.reset()

    # =========================================================
    # DRAW TOOLBAR
    # =========================================================

    def draw_toolbar(self, frame):

        # -----------------------------------------------------
        # Toolbar background
        # -----------------------------------------------------

        cv2.rectangle(
            frame,
            (0, 0),
            (WINDOW_WIDTH, TOOLBAR_HEIGHT),
            GRAY,
            -1
        )

        # -----------------------------------------------------
        # AIRINK
        # -----------------------------------------------------

        cv2.putText(
            frame,
            "AIRINK",
            (18, 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            BLACK,
            2
        )

        # -----------------------------------------------------
        # COLOR BUTTON
        # -----------------------------------------------------

        color_border = (
            BLUE
            if self.show_color_palette
            else BLACK
        )

        cv2.rectangle(
            frame,
            (120, 12),
            (225, 55),
            WHITE,
            -1
        )

        cv2.rectangle(
            frame,
            (120, 12),
            (225, 55),
            color_border,
            3
        )

        cv2.putText(
            frame,
            "Color",
            (143, 42),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            BLACK,
            2
        )

        # -----------------------------------------------------
        # ERASER
        # -----------------------------------------------------

        eraser_border = (
            BLUE
            if self.selected_color == WHITE
            else BLACK
        )

        cv2.rectangle(
            frame,
            (235, 12),
            (345, 55),
            WHITE,
            -1
        )

        cv2.rectangle(
            frame,
            (235, 12),
            (345, 55),
            eraser_border,
            3
        )

        cv2.putText(
            frame,
            "Eraser",
            (255, 42),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            BLACK,
            2
        )

        # -----------------------------------------------------
        # CLEAR
        # -----------------------------------------------------

        cv2.rectangle(
            frame,
            (355, 12),
            (455, 55),
            (205, 205, 205),
            -1
        )

        cv2.rectangle(
            frame,
            (355, 12),
            (455, 55),
            BLACK,
            3
        )

        cv2.putText(
            frame,
            "Clear",
            (378, 42),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            BLACK,
            2
        )

        # -----------------------------------------------------
        # SAVE
        # -----------------------------------------------------

        cv2.rectangle(
            frame,
            (465, 12),
            (565, 55),
            (205, 205, 205),
            -1
        )

        cv2.rectangle(
            frame,
            (465, 12),
            (565, 55),
            BLACK,
            3
        )

        cv2.putText(
            frame,
            "Save",
            (490, 42),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            BLACK,
            2
        )

        # -----------------------------------------------------
        # BRUSH LABEL
        # -----------------------------------------------------

        cv2.putText(
            frame,
            "Brush:",
            (585, 42),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            BLACK,
            2
        )

        # =====================================================
        # SMALL BRUSH - 3
        # =====================================================

        border = (
            BLUE
            if self.thickness == 3
            else BLACK
        )

        cv2.rectangle(
            frame,
            (650, 12),
            (690, 55),
            WHITE,
            -1
        )

        cv2.rectangle(
            frame,
            (650, 12),
            (690, 55),
            border,
            3
        )

        cv2.circle(
            frame,
            (670, 34),
            3,
            BLACK,
            -1
        )

        # =====================================================
        # MEDIUM BRUSH - 6
        # =====================================================

        border = (
            BLUE
            if self.thickness == 6
            else BLACK
        )

        cv2.rectangle(
            frame,
            (700, 12),
            (740, 55),
            WHITE,
            -1
        )

        cv2.rectangle(
            frame,
            (700, 12),
            (740, 55),
            border,
            3
        )

        cv2.circle(
            frame,
            (720, 34),
            6,
            BLACK,
            -1
        )

        # =====================================================
        # LARGE BRUSH - 12
        # =====================================================

        border = (
            BLUE
            if self.thickness == 12
            else BLACK
        )

        cv2.rectangle(
            frame,
            (750, 12),
            (790, 55),
            WHITE,
            -1
        )

        cv2.rectangle(
            frame,
            (750, 12),
            (790, 55),
            border,
            3
        )

        cv2.circle(
            frame,
            (770, 34),
            12,
            BLACK,
            -1
        )

        # =====================================================
        # COLOR PALETTE
        # =====================================================

        if self.show_color_palette:

            cv2.rectangle(
                frame,
                (110, 60),
                (470, 120),
                WHITE,
                -1
            )

            cv2.rectangle(
                frame,
                (110, 60),
                (470, 120),
                BLACK,
                2
            )

            colors = [
                RED,
                GREEN,
                BLUE,
                BLACK,
                YELLOW,
                PURPLE
            ]

            x_positions = [
                120,
                177,
                234,
                291,
                348,
                405
            ]

            for color, x in zip(
                colors,
                x_positions
            ):

                border = (
                    BLUE
                    if self.selected_color == color
                    else BLACK
                )

                cv2.rectangle(
                    frame,
                    (x, 68),
                    (x + 42, 108),
                    color,
                    -1
                )

                cv2.rectangle(
                    frame,
                    (x, 68),
                    (x + 42, 108),
                    border,
                    2
                )

    # =========================================================
    # SELECT COLOR / TOOL
    # =========================================================

    def select_color(self, x, y):

        # =====================================================
        # PALETTE
        # =====================================================

        if self.show_color_palette:

            if 112 <= x <= 172 and 55 <= y <= 120:

                self.color = RED
                self.selected_color = RED
                self.show_color_palette = False

                return None

            elif 172 < x <= 229 and 55 <= y <= 120:

                self.color = GREEN
                self.selected_color = GREEN
                self.show_color_palette = False

                return None

            elif 229 < x <= 286 and 55 <= y <= 120:

                self.color = BLUE
                self.selected_color = BLUE
                self.show_color_palette = False

                return None

            elif 286 < x <= 343 and 55 <= y <= 120:

                self.color = BLACK
                self.selected_color = BLACK
                self.show_color_palette = False

                return None

            elif 343 < x <= 400 and 55 <= y <= 120:

                self.color = YELLOW
                self.selected_color = YELLOW
                self.show_color_palette = False

                return None

            elif 400 < x <= 455 and 55 <= y <= 120:

                self.color = PURPLE
                self.selected_color = PURPLE
                self.show_color_palette = False

                return None

            return None

        # =====================================================
        # COLOR BUTTON
        # =====================================================

        if 110 <= x <= 235 and 5 <= y <= 65:

            self.show_color_palette = True

            return None

        # =====================================================
        # ERASER
        # =====================================================

        elif 225 <= x <= 350 and 5 <= y <= 65:

            self.color = WHITE
            self.selected_color = WHITE
            self.show_color_palette = False

            return None

        # =====================================================
        # CLEAR
        # =====================================================

        elif 350 <= x <= 460 and 5 <= y <= 65:

            self.clear_canvas()
            self.show_color_palette = False

            return None

        # =====================================================
        # SAVE
        # =====================================================

        elif 460 <= x <= 570 and 5 <= y <= 65:

            self.show_color_palette = False

            return "save"

        # =====================================================
        # SMALL BRUSH
        # =====================================================

        elif 640 <= x <= 695 and 5 <= y <= 65:

            self.thickness = 3

            return None

        # =====================================================
        # MEDIUM BRUSH
        # =====================================================

        elif 695 <= x <= 745 and 5 <= y <= 65:

            self.thickness = 6

            return None

        # =====================================================
        # LARGE BRUSH
        # =====================================================

        elif 745 <= x <= 800 and 5 <= y <= 65:

            self.thickness = 12

            return None

        return None
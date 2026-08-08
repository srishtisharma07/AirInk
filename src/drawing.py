import cv2
from constants import *


class DrawingCanvas:

    def __init__(self):

        self.canvas = None

        self.prev_x = None
        self.prev_y = None

        self.smooth_x = None
        self.smooth_y = None

        self.min_movement = 2

        self.color = PURPLE
        self.selected_color = PURPLE

        self.thickness = 6
        self.eraser_thickness = 35

    def initialize(self, frame):

        if self.canvas is None:
            self.canvas = frame.copy()
            self.canvas[:] = WHITE

    def draw(self, x, y):

        if self.smooth_x is None:
            self.smooth_x = x
            self.smooth_y = y

        alpha = 0.35

        self.smooth_x = int(
            alpha * x +
            (1 - alpha) * self.smooth_x
        )

        self.smooth_y = int(
            alpha * y +
            (1 - alpha) * self.smooth_y
        )

        thickness = self.thickness

        if self.color == WHITE:
            thickness = self.eraser_thickness

        if self.prev_x is not None and self.prev_y is not None:

            dx = self.smooth_x - self.prev_x
            dy = self.smooth_y - self.prev_y

            distance = (dx * dx + dy * dy) ** 0.5

            if distance >= self.min_movement:

                cv2.line(
                    self.canvas,
                    (self.prev_x, self.prev_y),
                    (self.smooth_x, self.smooth_y),
                    self.color,
                    thickness,
                    cv2.LINE_AA,
                )

        self.prev_x = self.smooth_x
        self.prev_y = self.smooth_y

    def reset(self):

        self.prev_x = None
        self.prev_y = None

        self.smooth_x = None
        self.smooth_y = None

    def clear_canvas(self):

        if self.canvas is not None:
            self.canvas[:] = WHITE

    def draw_toolbar(self, frame):

        height, width = frame.shape[:2]

        # =====================================================
        # TOOLBAR BACKGROUND
        # =====================================================

        cv2.rectangle(
            frame,
            (0, 0),
            (width, TOOLBAR_HEIGHT),
            GRAY,
            -1,
        )

        # =====================================================
        # TITLE
        # =====================================================

        cv2.putText(
            frame,
            "AIRINK",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            BLACK,
            2,
        )

        # =====================================================
        # COLOR BUTTONS
        # =====================================================

        colors = [
            RED,
            GREEN,
            BLUE,
            BLACK,
            YELLOW,
            PURPLE,
        ]

        x = 140

        for color in colors:

            border = (
                BLUE
                if self.selected_color == color
                else BLACK
            )

            cv2.rectangle(
                frame,
                (x, 10),
                (x + 40, 45),
                color,
                -1,
            )

            cv2.rectangle(
                frame,
                (x, 10),
                (x + 40, 45),
                border,
                2,
            )

            x += 55

        # =====================================================
        # SECOND ROW
        # =====================================================

        # Eraser
        eraser_border = (
            BLUE
            if self.selected_color == WHITE
            else BLACK
        )

        cv2.rectangle(
            frame,
            (20, 60),
            (130, 100),
            WHITE,
            -1,
        )

        cv2.rectangle(
            frame,
            (20, 60),
            (130, 100),
            eraser_border,
            2,
        )

        cv2.putText(
            frame,
            "Eraser",
            (38, 87),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            BLACK,
            2,
        )

        # =====================================================
        # CLEAR BUTTON
        # =====================================================

        cv2.rectangle(
            frame,
            (145, 60),
            (245, 100),
            (200, 200, 200),
            -1,
        )

        cv2.rectangle(
            frame,
            (145, 60),
            (245, 100),
            BLACK,
            2,
        )

        cv2.putText(
            frame,
            "Clear",
            (169, 87),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            BLACK,
            2,
        )

        # =====================================================
        # SAVE BUTTON
        # =====================================================

        cv2.rectangle(
            frame,
            (260, 60),
            (360, 100),
            (200, 200, 200),
            -1,
        )

        cv2.rectangle(
            frame,
            (260, 60),
            (360, 100),
            BLACK,
            2,
        )

        cv2.putText(
            frame,
            "Save",
            (284, 87),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            BLACK,
            2,
        )

        # =====================================================
        # BRUSH SIZE LABEL
        # =====================================================

        cv2.putText(
            frame,
            "Brush:",
            (385, 87),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            BLACK,
            2,
        )

        # =====================================================
        # SMALL BRUSH
        # =====================================================

        small_border = (
            BLUE if self.thickness == 3 else BLACK
        )

        cv2.rectangle(
            frame,
            (445, 60),
            (485, 100),
            WHITE,
            -1,
        )

        cv2.rectangle(
            frame,
            (445, 60),
            (485, 100),
            small_border,
            2,
        )

        cv2.circle(
            frame,
            (465, 80),
            3,
            BLACK,
            -1,
        )

        # =====================================================
        # MEDIUM BRUSH
        # =====================================================

        medium_border = (
            BLUE if self.thickness == 6 else BLACK
        )

        cv2.rectangle(
            frame,
            (495, 60),
            (535, 100),
            WHITE,
            -1,
        )

        cv2.rectangle(
            frame,
            (495, 60),
            (535, 100),
            medium_border,
            2,
        )

        cv2.circle(
            frame,
            (515, 80),
            6,
            BLACK,
            -1,
        )

        # =====================================================
        # LARGE BRUSH
        # =====================================================

        large_border = (
            BLUE if self.thickness == 10 else BLACK
        )

        cv2.rectangle(
            frame,
            (545, 60),
            (585, 100),
            WHITE,
            -1,
        )

        cv2.rectangle(
            frame,
            (545, 60),
            (585, 100),
            large_border,
            2,
        )

        cv2.circle(
            frame,
            (565, 80),
            10,
            BLACK,
            -1,
        )

    def select_color(self, x, y):

        # =====================================================
        # FIRST ROW - COLORS
        # =====================================================

        if 10 <= y <= 45:

            if 140 <= x <= 180:
                self.color = RED
                self.selected_color = RED

            elif 195 <= x <= 235:
                self.color = GREEN
                self.selected_color = GREEN

            elif 250 <= x <= 290:
                self.color = BLUE
                self.selected_color = BLUE

            elif 305 <= x <= 345:
                self.color = BLACK
                self.selected_color = BLACK

            elif 360 <= x <= 400:
                self.color = YELLOW
                self.selected_color = YELLOW

            elif 415 <= x <= 455:
                self.color = PURPLE
                self.selected_color = PURPLE

        # =====================================================
        # SECOND ROW - TOOLS
        # =====================================================

        elif 60 <= y <= 100:

            # Eraser
            if 20 <= x <= 130:

                self.color = WHITE
                self.selected_color = WHITE

            # Clear
            elif 145 <= x <= 245:

                self.clear_canvas()

            # Save
            elif 260 <= x <= 360:

                return "save"

            # Small brush
            elif 445 <= x <= 485:

                self.thickness = 3

            # Medium brush
            elif 495 <= x <= 535:

                self.thickness = 6

            # Large brush
            elif 545 <= x <= 585:

                self.thickness = 10

        return None
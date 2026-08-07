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

        cv2.rectangle(
            frame,
            (0, 0),
            (width, TOOLBAR_HEIGHT),
            GRAY,
            -1,
        )

        colors = [
            RED,
            GREEN,
            BLUE,
            BLACK,
            YELLOW,
            PURPLE,
        ]

        x = 40

        for color in colors:
            border = BLUE if self.selected_color == color else BLACK

            cv2.rectangle(
                frame,
                (x, 15),
                (x + 50, 65),
                color,
                -1,
            )

            cv2.rectangle(
                frame,
                (x, 15),
                (x + 50, 65),
                border,
                3,
            )

            x += 80

        # -------------------------
        # Eraser
        # -------------------------

        border = BLUE if self.selected_color == WHITE else BLACK

        cv2.rectangle(
            frame,
            (560, 15),
            (700, 65),
            WHITE,
            -1,
        )

        cv2.rectangle(
            frame,
            (560, 15),
            (700, 65),
            border,
            3,
        )

        cv2.putText(
            frame,
            "Eraser",
            (578, 48),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            BLACK,
            2,
        )

        # -------------------------
        # Clear
        # -------------------------

        cv2.rectangle(
            frame,
            (720, 15),
            (810, 65),
            (200, 200, 200),
            -1,
        )

        cv2.rectangle(
            frame,
            (720, 15),
            (810, 65),
            BLACK,
            2,
        )

        cv2.putText(
            frame,
            "Clear",
            (733, 48),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            BLACK,
            2,
        )

        # -------------------------
        # Brush Size Buttons
        # -------------------------

        brush_buttons = [
            ("S", 825),
            ("M", 870),
            ("L", 915),
        ]

        for text, bx in brush_buttons:
            cv2.rectangle(
                frame,
                (bx, 15),
                (bx + 35, 65),
                WHITE,
                -1,
            )

            cv2.rectangle(
                frame,
                (bx, 15),
                (bx + 35, 65),
                BLACK,
                2,
            )

            cv2.putText(
                frame,
                text,
                (bx + 9, 48),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                BLACK,
                2,
            )

    def select_color(self, x, y):
        if y > TOOLBAR_HEIGHT:
            return

        # -------------------------
        # Color Selection
        # -------------------------

        if 40 <= x <= 90:
            self.color = RED
            self.selected_color = RED

        elif 120 <= x <= 170:
            self.color = GREEN
            self.selected_color = GREEN

        elif 200 <= x <= 250:
            self.color = BLUE
            self.selected_color = BLUE

        elif 280 <= x <= 330:
            self.color = BLACK
            self.selected_color = BLACK

        elif 360 <= x <= 410:
            self.color = YELLOW
            self.selected_color = YELLOW

        elif 440 <= x <= 490:
            self.color = PURPLE
            self.selected_color = PURPLE

        # -------------------------
        # Eraser
        # -------------------------

        elif 560 <= x <= 700:
            self.color = WHITE
            self.selected_color = WHITE

        # -------------------------
        # Clear Canvas
        # -------------------------

        elif 720 <= x <= 810:
            self.clear_canvas()

        # -------------------------
        # Brush Size
        # -------------------------

        elif 825 <= x <= 860:
            self.thickness = 3

        elif 870 <= x <= 905:
            self.thickness = 6

        elif 915 <= x <= 950:
            self.thickness = 10
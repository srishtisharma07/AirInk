import cv2
from constants import *


class DrawingCanvas:

    def __init__(self):

        self.canvas = None

        self.prev_x = None
        self.prev_y = None

        # Smoothed Position
        self.smooth_x = None
        self.smooth_y = None

        # Smoothing factor
        self.alpha = 0.25

        # Ignore tiny movements
        self.min_movement = 4

        self.color = PURPLE
        self.selected_color = PURPLE

        self.thickness = 5
        self.eraser_thickness = 35

    def initialize(self, frame):

        if self.canvas is None:

            self.canvas = frame.copy()
            self.canvas[:] = WHITE

    def draw(self, x, y):

        # Initialize smoothing
        if self.smooth_x is None:

            self.smooth_x = x
            self.smooth_y = y

        # Exponential Moving Average
        self.smooth_x = int(
            self.alpha * x +
            (1 - self.alpha) * self.smooth_x
        )

        self.smooth_y = int(
            self.alpha * y +
            (1 - self.alpha) * self.smooth_y
        )

        thickness = self.thickness

        if self.color == WHITE:
            thickness = self.eraser_thickness

        if self.prev_x is not None and self.prev_y is not None:

            dx = self.smooth_x - self.prev_x
            dy = self.smooth_y - self.prev_y

            distance = (dx * dx + dy * dy) ** 0.5

            if distance < self.min_movement:
                return

            cv2.line(
                self.canvas,
                (self.prev_x, self.prev_y),
                (self.smooth_x, self.smooth_y),
                self.color,
                thickness,
            )

        self.prev_x = self.smooth_x
        self.prev_y = self.smooth_y

    def reset(self):

        self.prev_x = None
        self.prev_y = None

        self.smooth_x = None
        self.smooth_y = None

    def draw_toolbar(self, frame):

        cv2.rectangle(
            frame,
            (0, 0),
            (WINDOW_WIDTH, TOOLBAR_HEIGHT),
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

            cv2.rectangle(
                frame,
                (x, 15),
                (x + 50, 65),
                color,
                -1,
            )

            border = BLACK

            if self.selected_color == color:
                border = BLUE

            cv2.rectangle(
                frame,
                (x, 15),
                (x + 50, 65),
                border,
                3,
            )

            x += 80

        # Eraser Button

        cv2.rectangle(
            frame,
            (560, 15),
            (700, 65),
            WHITE,
            -1,
        )

        eraser_border = BLACK

        if self.selected_color == WHITE:
            eraser_border = BLUE

        cv2.rectangle(
            frame,
            (560, 15),
            (700, 65),
            eraser_border,
            3,
        )

        cv2.putText(
            frame,
            "Eraser",
            (580, 48),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            BLACK,
            2,
        )

    def select_color(self, x, y):

        if y > TOOLBAR_HEIGHT:
            return

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

        elif 560 <= x <= 700:
            self.color = WHITE
            self.selected_color = WHITE
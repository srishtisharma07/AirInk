import cv2


class DrawingCanvas:
    def __init__(self):
        self.canvas = None
        self.prev_x = None
        self.prev_y = None

        self.color = (255, 0, 255)   # Purple
        self.thickness = 5

    def initialize(self, frame):
        if self.canvas is None:
            self.canvas = frame.copy()
            self.canvas[:] = 255

    def draw(self, x, y):
        if self.prev_x is not None and self.prev_y is not None:
            cv2.line(
                self.canvas,
                (self.prev_x, self.prev_y),
                (x, y),
                self.color,
                self.thickness,
            )

        self.prev_x = x
        self.prev_y = y

    def reset(self):
        self.prev_x = None
        self.prev_y = None
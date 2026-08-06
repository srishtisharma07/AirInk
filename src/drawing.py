from constants import *
import cv2


class DrawingCanvas:

  def __init__(self):
    self.canvas = None
    self.prev_x = None
    self.prev_y = None

    self.color = (255, 0, 255)
    self.selected_color = PURPLE
    self.thickness = 5

  def initialize(self, frame):
    if self.canvas is None:
      self.canvas = frame.copy()
      self.canvas[:] = 255

  def draw(self, x, y):
    if self.prev_x is not None and self.prev_y is not None:
      thickness = self.thickness
      if self.color == WHITE:
        thickness = 25

      cv2.line(
          self.canvas,
          (self.prev_x, self.prev_y),
          (x, y),
          self.color,
          thickness,
      )

    self.prev_x = x
    self.prev_y = y

  def reset(self):
    self.prev_x = None
    self.prev_y = None

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

      cv2.rectangle(
          frame,
          (x, 15),
          (x + 50, 65),
          BLACK,
          2,
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
    cv2.rectangle(
        frame,
        (560, 15),
        (700, 65),
        BLACK,
        2,
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

    elif 120 <= x <= 170:
      self.color = GREEN

    elif 200 <= x <= 250:
      self.color = BLUE

    elif 280 <= x <= 330:
      self.color = BLACK

    elif 360 <= x <= 410:
      self.color = YELLOW

    elif 440 <= x <= 490:
      self.color = PURPLE

    elif 560 <= x <= 700:
      self.color = WHITE
      self.selected_color = WHITE
import json
from datetime import datetime, timedelta
from tkinter import *
from math import *

ROUND: str = "round"


class Clock:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def run_clock(self):
        root = Tk()
        root.title("PROJETO - RELÓGIO GMT")
        root.geometry(f"{self.width}x{self.height}")
        canvas = Canvas(root, width=self.width, height=self.height, bg="white")
        canvas.pack(padx=20, pady=20, anchor="center")

        # Propriedades da circunferencia (generalizando e padronizando)
        center_x, center_y = [self.width / 2, self.height / 2]
        clock_radius = min(self.width, self.height) / 3.1

        # Desenhando o fundo do relógio
        canvas.create_oval(center_x - clock_radius,
                           center_y + clock_radius,
                           center_x + clock_radius,
                           center_y - clock_radius,
                           fill="black")

        # Desenhando os ponteiros marcando as horas para o Rio de Janeiro:
        self.paint_hms(canvas, clock_radius)

        root.mainloop()

    def paint_hms(self, canvas: Canvas, radius, local_offset=None):
        canvas.delete("handles")
        h_angle, m_angle, s_angle = self.time_angle(-3)
        self.draw_handle(canvas, h_angle, 0.5 * radius, "red", 10)  # no exemplo radius = 0.5 (nao sei porque)
        self.draw_handle(canvas, m_angle, 0.9 * radius, "green", 10)
        self.draw_handle(canvas, s_angle, 0.95 * radius, "blue", 3.6)

    def draw_handle(self, canvas, angle, handle_length, color, wid=None):
        x, y = self.polar_2_cartesian(angle, handle_length)
        x, y = x + self.width/2, y + self.height/2
        print(f"x: {x}, y: {y}")
        canvas.create_line(self.width / 2, self.height / 2,
                           x, y,
                           fill=color,
                           tag="handles",
                           width=wid,
                           capstyle=ROUND)

    def time_angle(self, local: int):
        h, m, s = datetime.timetuple(datetime.utcnow() + timedelta(hours=local))[3:6]
        one_min = pi / 30
        five_min = pi / 6

        hour_angle = five_min * (h + (m / 60.0))
        min_angle = one_min * (m + (s / 60.0))
        sec_angle = one_min * s
        return hour_angle, min_angle, sec_angle

    def polar_2_cartesian(self, angle: float, radius: float):
        angle -= pi / 2
        return radius * cos(angle), radius * sin(angle)


relogio = Clock(500, 500)
relogio.run_clock()

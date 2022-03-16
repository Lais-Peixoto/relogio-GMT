import json
from datetime import datetime, timedelta
from tkinter import *
from math import *

ROUND: str = "round"


class Clock:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height, bg="white")

    def run_clock(self):
        self.root.title("PROJETO - RELÓGIO GMT")
        self.root.geometry(f"{self.width}x{self.height}")
        self.canvas.pack(padx=20, pady=20, anchor="center")

        # Propriedades da circunferencia (generalizando e padronizando)
        center_x, center_y = [self.width / 2, self.height / 2]
        clock_radius = min(self.width, self.height) / 3.1

        # Desenhando o fundo do relógio
        self.canvas.create_oval(center_x - clock_radius,
                           center_y + clock_radius,
                           center_x + clock_radius,
                           center_y - clock_radius,
                           fill="black")

        # Desenhando os ponteiros marcando as horas para o Rio de Janeiro:
        self.animate(clock_radius)
        self.root.mainloop()

    def animate(self, radius):
        self.paint_hms(radius)

    def paint_hms(self, radius: float, local_offset=-3):
        self.canvas.delete("handles")
        h_angle, m_angle, s_angle = self.time_angle(local_offset)
        self.draw_handle(h_angle, 0.5 * radius, "red", 10)
        self.draw_handle(m_angle, 0.9 * radius, "green", 10)
        self.draw_handle(s_angle, 0.95 * radius, "blue", 3.6)
        self.root.after(200, self.paint_hms, radius)

    def draw_handle(self, angle, handle_length, color, wid=None):
        x, y = self.polar_2_cartesian(angle, handle_length)
        x, y = x + self.width/2, y + self.height/2
        print(datetime.utcnow())
        self.canvas.create_line(self.width / 2, self.height / 2,
                                x, y,
                                fill=color,
                                tags="handles",
                                width=wid,
                                capstyle=ROUND)

    @staticmethod
    def time_angle(local: int):
        h, m, s = datetime.timetuple(datetime.utcnow() + timedelta(hours=local))[3:6]
        one_min = pi / 30
        five_min = pi / 6

        hour_angle = five_min * (h + (m / 60.0))
        min_angle = one_min * (m + (s / 60.0))
        sec_angle = one_min * s
        return hour_angle, min_angle, sec_angle

    @staticmethod
    def polar_2_cartesian(angle: float, radius: float):
        angle -= pi / 2
        return radius * cos(angle), radius * sin(angle)


relogio = Clock(500, 500)
relogio.run_clock()

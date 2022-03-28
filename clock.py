import json
import math
from datetime import datetime, timedelta
from tkinter import *
from math import *

class Clock:
    ROUND: str = "round"
    ONE_MIN: float = pi / 30
    FIVE_MIN: float = pi / 6

    def __init__(self, width, height):
        """!@brief Classe que representa um relógio GMT para a realização da AD1 de PIG
        @author Laís Pereira Peixoto de Moraes (Matricula: 20213050054)
        @param width tamanho da largura
        @param height tamanho da altura
        """
        self.canvas = None
        self.clock_radius = None
        self.cities = None
        self.offsets = None
        self.dropVar = None
        self.callId = None
        self.width = width
        self.height = height
        self.root = Tk()

    def run_clock(self, five_min=FIVE_MIN):
        """!@brief Executa a aplicação
        @param five_min constante referente ao ângulo para 5 minutos
        """
        self.root.title("PROJETO - RELÓGIO GMT")
        self.root.geometry(f"{self.width}x{self.height}")
        self.canvas = Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack(padx=20, pady=20, anchor="center", fill=BOTH, expand=YES)
        self.clock_bg(five_min)
        self.app_menu()
        self.paint_hms(-2)
        self.root.mainloop()

    def app_menu(self):
        """!@brief Desenha o menu da aplicação
        """
        option_list = self.read_zones()
        self.cities = []
        self.offsets = []

        for city in option_list["cities"]:
            self.cities.append(city["city"])
            self.offsets.append(city["offset"])

        self.dropVar = StringVar(self.root)
        self.dropVar.set(self.cities[0])
        drop_menu = OptionMenu(self.root, self.dropVar, *self.cities, command=self.on_select)
        drop_menu.place(x=20, y=20)

    def on_select(self, selection):
        """!@brief Atualiza a animação para cada localidade selecionada a partir do menu
        @param selection valor selecionado do menu da aplicação
        """
        city_offset = self.offsets[self.cities.index(selection)]
        if self.callId is not None:
            self.root.after_cancel(self.callId)
        self.paint_hms(city_offset)

    def paint_hms(self, local_offset):
        """!@brief Movimento os ponteiros do relógio dado a hora atual de uma localidade
        @param local_offset valor UTC de uma localidade
        """
        self.canvas.delete("handles")
        h_angle, m_angle, s_angle = self.time_angle(local_offset)
        self.draw_handle(h_angle, 0.4 * self.clock_radius, "red", 10)
        self.draw_handle(m_angle, 0.8 * self.clock_radius, "green", 10)
        self.draw_handle(s_angle, 0.85 * self.clock_radius, "blue", 3.6)
        self.callId = self.root.after(200, self.paint_hms, local_offset)

    def draw_handle(self, angle, handle_length, color, wid=None):
        """!@brief Desenho os ponteiros do relógio
               @param angle ângulo do ponteiro
               @param handle_length comprimento do ponteiro
               @param color cor do ponteiro
               @param wid largura do ponteiro
               """
        x, y = self.polar_2_cartesian(angle, handle_length)
        x, y = x + self.width / 2, y + self.height / 2
        self.canvas.create_line(self.width / 2, self.height / 2,
                                x, y,
                                fill=color,
                                tags="handles",
                                width=wid,
                                capstyle=ROUND)

    def clock_bg(self, five_min):
        """!@brief Desenha o fundo do relógio
       @param five_min constante referente ao ângulo para 5 minutos
       """
        center_x, center_y = [self.width / 2, self.height / 2]
        self.clock_radius = min(self.width, self.height) / 3.1
        self.canvas.create_oval(center_x - self.clock_radius,
                                center_y + self.clock_radius,
                                center_x + self.clock_radius,
                                center_y - self.clock_radius,
                                fill="black")

        hour_num = [3, 2, 1, 12, 11, 10, 9, 8, 7, 6, 5, 4]

        theta = 0
        for i in hour_num:
            text_x = center_x + self.clock_radius * 0.85 * math.cos(theta)
            text_y = center_y - self.clock_radius * 0.85 * math.sin(theta)
            theta += five_min
            self.canvas.create_text(text_x, text_y, text=i, font="Arial 25", fill="white")

    @staticmethod
    def read_zones():
        """!@brief Ler os dados de um arquivo com formato JSON
               """
        file = open('localtime.json')
        json_file = json.loads(file.read())
        file.close()
        return json_file

    @staticmethod
    def time_angle(local: int, five_min=FIVE_MIN, one_min=ONE_MIN):
        """!@brief Busca as horas em um local e converte em angulos
                       @param local valor UTC de uma localidade
                       @param five_min constante referente ao ângulo para 5 minutos
                       @param one_min constante referente ao ângulo para 1 minuto
                       """
        h, m, s = datetime.timetuple(datetime.utcnow() + timedelta(hours=local))[3:6]
        hour_angle = five_min * (h + (m / 60.0))
        min_angle = one_min * (m + (s / 60.0))
        sec_angle = one_min * s
        return hour_angle, min_angle, sec_angle

    @staticmethod
    def polar_2_cartesian(angle: float, radius: float):
        """!@brief Converte um vetor de coordenadas polares para cartesianas.
                       @param angle ângulo do vetor.
                       @param radius comprimento do vetor.
                       @return um ponto 2D (plano cartesiano).
                       """
        angle -= pi / 2
        return radius * cos(angle), radius * sin(angle)


relogio = Clock(500, 500)
relogio.run_clock()

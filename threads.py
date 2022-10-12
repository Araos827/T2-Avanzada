import sys
import time
import PyQt5.QtCore as core
import random
from parametros import LLEGADA_CLIENTES, PROB_APURADO, PROB_APURADO, TIEMPO_ESPERA_APURADO,\
     TIEMPO_ESPERA_RELAJADO, REPUTACION_INICIAL, DINERO_CLIENTE, PROPINA_CLIENTE, PLATOS_EXPERTO,\
          PLATOS_INTERMEDIO, DINERO_INICIAL, CHEFS_INICIALES, MESAS_INICIALES
import math
import random
import time


class PrepararPlato(core.QThread):


    def __init__(self, senal_actualizar_frames, senal_finish, tiempo_preparacion, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senal_actualizar_frames = senal_actualizar_frames
        self.tiempo_preparacion = tiempo_preparacion
        self.senal_termino = senal_finish

    def run(self):
        for i in range(8 * self.tiempo_preparacion):
            time.sleep(0.125)
            #print("hola")
            self.senal_actualizar_frames.emit()
        self.senal_termino.emit()

class Cliente(core.QThread):

    p = random.random()
    def __init__(self, senal_actualizar_frames, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.p < PROB_APURADO:
            self.tipo = "apurado"
        else:
            self.tipo = "relajado"

        if self.tipo == "apurado":
            self.tiempo_espera = TIEMPO_ESPERA_APURADO
        else:
            self.tiempo_espera = TIEMPO_ESPERA_RELAJADO

        self.senal_actualizar_frames = senal_actualizar_frames
        self.atendido = False
        self.__frame = 10
        self.estado = "tranquilo"
        self.mesa_y_pos = None
        self.dinero  = DINERO_CLIENTE
        self.propina = 0
        self.tiempo_total = self.tiempo_espera


    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, value):
        if self.estado == "tranquilo" and 12 < value:
            self.__frame = 10

        elif self.estado == "mad" and 41 < value:
            self.__frame = 13
        else:
            self.__frame = value

    def run(self):
        while (4 * self.tiempo_espera) > 0 and not self.atendido:
            self.frame += 1
            time.sleep(0.25)
            self.senal_actualizar_frames.emit(
                {'obj': "cliente",   
                    'x': self.mesa_y_pos[1].x,
                    'y': self.mesa_y_pos[1].y,
                    "frame": str(self.frame),
                    "sprite": "perro"
                }
            )
            self.tiempo_espera -= 0.25
            if self.tiempo_espera < self.tiempo_total/2:
                self.estado = "mad"

        self.senal_actualizar_frames.emit(
            {'obj': "cliente",
                    'x': self.mesa_y_pos[1].x,
                    'y': self.mesa_y_pos[1].y,
                    "delete": True
                }
            )
        self.mesa_y_pos[1].desocupada = True
        self.mesa_y_pos[1].cliente = None

class MiuEnzo(core.QObject):
    update_position_signal = core.pyqtSignal(dict)
    senal_chequear_colision = core.pyqtSignal(dict)

    def __init__(self, x, y):
        super().__init__()
        self.display_x = x
        self.display_y = y
        self.__x = 471 #Determinamos la posicion x incial
        self.__y = 801 #Determinamos la posicion y incial
        self.bocadillos = dict() 
        self.__frame = 1 #Determinamos el frame inicial
        self.colision_obj = list()
        self.colision_dir = set()
        self.plato = None

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, value):
        if 3 < value:
            self.__frame = 1
        else:
            self.__frame = value

    @property 
    def x(self):
        return self.__x

    @x.setter 
    def x(self, value):
        if 111 < value < 100 + self.display_x:
            self.__x = value

    @property 
    def y(self):
        return self.__y

    @y.setter 
    def y(self, value):
        if 376 < value < 370 + self.display_y:
            self.__y = value

    def move(self, event):
        self.frame += 1
        snack = ""
        if self.plato != None:
            snack = "_snack"
        if event == 'R':
            if not event in self.colision_dir:
                self.x += 10
            self.update_position_signal.emit( 
                {'obj': 'Enzo',
                 'x': self.x,
                 'y': self.y,
                 "frame": self.frame,
                 "sprite": "mesero",
                 "dir": "right" + snack
                 })

        if event == 'L':
            if not event in self.colision_dir:
                self.x -= 10
            self.update_position_signal.emit(
                {'obj': 'Enzo',
                    'x': self.x,
                    'y': self.y,
                    "frame": self.frame,
                    "sprite": "mesero",
                    "dir": "left" + snack
                    })

        if event == 'U':
            if not "D" in self.colision_dir:
                self.y -= 10
            self.update_position_signal.emit(
                {'obj': 'Enzo',
                    'x': self.x,
                    'y': self.y,
                    "frame": self.frame,
                    "sprite": "mesero",
                    "dir": "up" + snack
                    })


        if event == 'D':
            if not "U" in self.colision_dir:
                self.y += 10
            self.update_position_signal.emit(
                {'obj': 'Enzo',
                    'x': self.x,
                    'y': self.y,
                    "frame": self.frame,
                    "sprite": "mesero",
                    "dir": "down" + snack
                    })
        self.senal_chequear_colision.emit({"x" : self.x, "y" : self.y})

    def recibir_colision(self, event):
        self.colision_dir = event["set"]
        self.colision_obj = event["list"]

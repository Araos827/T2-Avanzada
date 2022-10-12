import os
import sys
import random
import time
import PyQt5.QtCore as core
from threads import PrepararPlato, Cliente, MiuEnzo
import math
from parametros import LLEGADA_CLIENTES, RONDAS, PROB_APURADO, PROB_APURADO, TIEMPO_ESPERA_APURADO,\
     TIEMPO_ESPERA_RELAJADO, REPUTACION_INICIAL, DINERO_CLIENTE, PROPINA_CLIENTE, PLATOS_EXPERTO,\
          PLATOS_INTERMEDIO, DINERO_INICIAL, CHEFS_INICIALES, MESAS_INICIALES


class DCCafe(core.QThread):

    senal_create_object = core.pyqtSignal(dict)
    senal_return_intersection = core.pyqtSignal(bool)
    senal_return_colision = core.pyqtSignal(dict)
    senal_recibir_plato = core.pyqtSignal()
    senal_update_position = core.pyqtSignal(dict)
    senal_generar_clientes = core.pyqtSignal()
    send_reputacion_signal = core.pyqtSignal(int)
    send_ronda_signal = core.pyqtSignal(int)
    send_dinero_signal = core.pyqtSignal(int)
    send_clientes_antedidos_signal = core.pyqtSignal(int)
    send_clientes_perdidos_signal = core.pyqtSignal(int)
    send_clientes_proximos_signal = core.pyqtSignal(int)
    send_resumen_ronda_signal = core.pyqtSignal(dict)

    def __init__(self, mesero):
        super().__init__()
        self.object_labels = dict()
        self.puntos_de_reputacion = REPUTACION_INICIAL
        self.clientes = list()
        self.ganancias_ronda = 0
        self.pedidos_exitosos = 0
        self.pedidos_totales = 0
        self.pedidos = 0
        self.dinero = DINERO_INICIAL
        self.dinero_ronda = 0
        self.mesero = mesero
        self.objetos_colisionados = list()
        self.clientes = list()
        self.disponibilidad = False
        self.ronda_actual = 1


    def run(self):
        win = True
        for r in range(RONDAS - self.ronda_actual): #se establece el numero de rondas
            self.ronda_actual = r + 1
            self.send_ronda_signal.emit(self.ronda_actual)
            self.send_dinero_signal.emit(self.dinero)
            self.disponibilidad = False
            print("Ahora puedes comprar de la tienda")
            print("Presiona comenzar para empezar la ronda")
            while not self.disponibilidad: #esto es la pausa del juego
                pass
            print("pausa desactivada")
            self.pedidos_exitosos = 0
            self.dinero_ronda = 0
            self.pedidos_totales = 0
            print("="*50)
            print(f"RONDA: {self.ronda_actual}")
            time.sleep(2)
            print("\nComienza en:")
            for t in range(3):
                print(3-t)
                time.sleep(1) 
            print("¡Comenzó!\n")
            mesas_ronda = {key:self.object_labels[key] for key in self.object_labels.keys()\
                 if self.object_labels[key].type == "mesa"}
            for i in range(self.clientes_ronda(self.ronda_actual)):
                self.crear_cliente()
            clientes_ronda = len(self.clientes)
            self.send_clientes_antedidos_signal.emit(0)
            self.send_clientes_perdidos_signal.emit(0)
            self.send_clientes_proximos_signal.emit(len(self.clientes))
            while any(not cliente.isFinished() for cliente in self.clientes)\
                 or len(self.clientes) > 0:
                while not self.disponibilidad:
                    pass #aqui ocurre la logica de la ronda
                if any(mesas_ronda[key].desocupada for key in mesas_ronda.keys()):
                    time.sleep(LLEGADA_CLIENTES)
                    self.lanzar_cliente()
                for c in self.clientes: #chequeamos a cada cliente
                    if c.isRunning():
                        continue
                    if self.puntos_de_reputacion == 0: 
                        break 
                    if c.isFinished(): #chequeamos si el Thread ha terminado
                        
                        if c.atendido: #chequeamos si no ha sido atendido
                            self.pedidos_exitosos += 1 
                            print("¡Un Cliente ha sido atenido existosamente!")
                            self.dinero_ronda += c.dinero + c.propina
                        else:
                            print("Un Cliente se ha ido sin comer")
                        
                        self.clientes.remove(c)
                        self.pedidos_totales += 1
                        self.send_clientes_proximos_signal.emit(len(self.clientes))
                        self.send_clientes_antedidos_signal.emit(self.pedidos_exitosos)
                        self.send_clientes_perdidos_signal.emit(self.pedidos_totales\
                             - self.pedidos_exitosos)
                if self.puntos_de_reputacion == 0: 
                    break
            self.pedidos += self.pedidos_totales
            self.calcular_reputacion()
            self.dinero += self.dinero_ronda
            self.send_resumen_ronda_signal.emit(
                {
                "ronda" : self.ronda_actual,
                "clientes_perdidos" : self.pedidos_totales - self.pedidos_exitosos,
                "clientes_atendidos" : self.pedidos_exitosos,
                "dinero_acumulado" : self.dinero_ronda,
                "reputacion" : self.puntos_de_reputacion
            })
            self.disponibilidad = False
            while not self.disponibilidad:
                pass
        
            if self.puntos_de_reputacion == 0: 
                win = False 
                break 
            print("\n¡RONDA SUPERADA!\n") 
        if win: 
            print("Felcidades, has ganado!!") 
        else:
            print("Oh no!, has perdido :(") 
        
    def recieve_pause(self):
        self.disponibilidad = not self.disponibilidad
    
    def comenzar_ronda(self, event):
        if event:
            self.disponibilidad = event

    def create_object(self, data):
        if data["obj"] == "desk":
            self.dinero -= 100
            self.senal_create_object.emit( 
                    {
                    'x': data["x"],
                    'y': data["y"],
                    "obj": data["obj"],
                    "sprite": "silla_mesa_roja"
                    })
        elif data["obj"] == "chef":
            self.dinero -= 300
            self.senal_create_object.emit( 
                    {
                    'x': data["x"],
                    'y': data["y"],
                    "obj": data["obj"],
                    "sprite": "meson"
                    })

    def chequear_superposicion(self, data):
        interseccion = False
        if len(self.object_labels) == 0:
            self.senal_return_intersection.emit(False)
        else:            
            for obj in self.object_labels.keys():
                if not data["obj"].geometry().intersects(obj.geometry()):
                    continue
                if data["obj"].geometry().intersects(obj.geometry()):
                    interseccion = True
        self.senal_return_intersection.emit(interseccion)

    def chequear_colision(self, data):
        obj_list = list()
        col_set = set()
        x = data["x"] - 121 #alamcenamos la posicion x
        y = data["y"] - 391 #almacenamos la posicion y
        for obj in self.object_labels.keys():
            v_x = obj.geometry().x() 
            v_y = obj.geometry().y() 
            d_x = x - v_x 
            d_y = y - v_y
            if -30 < d_x < -10 and -10 < d_y < obj.geometry().height() - 20:
                obj_list.append(obj)
                col_set.add("R")
            elif -10 < d_x < obj.geometry().width() - 10 and -35 < d_y < -15:
                obj_list.append(obj)
                col_set.add("U")
            elif  -10 < d_x < obj.geometry().width() -10 and obj.geometry().height()\
                 - 20 < d_y < obj.geometry().height() + 9:
                obj_list.append(obj)
                col_set.add("D")
            elif obj.geometry().width() - 10 < d_x < obj.geometry().width()\
                 + 10 and -10 < d_y < obj.geometry().height() - 20:
                obj_list.append(obj)
                col_set.add("L")

        self.objetos_colisionados = obj_list
        self.senal_return_colision.emit({"list" : obj_list, "set" : col_set})
        for obj in self.objetos_colisionados:
            instancia = self.object_labels[obj]
            if type(instancia) == Chef: #and instancia.mesero_in == True
                if instancia.estado == "desocupado":
                    instancia.preparar_bocadillo(self.puntos_de_reputacion)
                    instancia.estado = "cocinando"
                elif instancia.estado == "cocinando":
                    continue
                elif instancia.estado == "finished" and self.mesero.plato == None:
                    self.mesero.plato = instancia.plato
                    instancia.plato = None
                    instancia.estado = "desocupado"

            elif type(instancia) == Mesa:    
                if instancia.desocupada == True:
                    continue
                elif instancia.desocupada == False and self.mesero.plato\
                     != None and not instancia.cliente.atendido:
                    instancia.cliente.atendido = True
                    calidad_pedido = max(0, (self.mesero.plato.nivel_chef * \
                        (1 - instancia.cliente.tiempo_espera * 0.05)/3))
                    self.mesero.plato = None
                    p = random.random()
                    if p < calidad_pedido:
                        instancia.cliente.propina = PROPINA_CLIENTE
                    self.senal_update_position.emit(
                        {'obj': "cliente",
                        'x': instancia.x,
                        'y': instancia.y,
                        "delete": True
                        })

    def recieve_object(self, data):
        if data["type"] == "chef":
            self.object_labels[data["obj"]] = Chef(self.senal_update_position, data["x"],\
                 data["y"])
        elif data["type"] == "mesa":
            self.object_labels[data["obj"]] = Mesa(data["x"], data["y"])

    def calcular_reputacion(self):
        reputacion_actual = self.puntos_de_reputacion
        self.puntos_de_reputacion = max(0, min(5, (reputacion_actual + \
            math.floor((4 * self.pedidos_exitosos/self.pedidos) - 2))))
        self.send_reputacion_signal.emit(self.puntos_de_reputacion)
        print(f"nueva reputacion: {self.puntos_de_reputacion}")

    def clientes_ronda(self, ronda_acutal):
        return (5*(1 + ronda_acutal))

    def crear_cliente(self):
        c = Cliente(self.senal_update_position)
        self.clientes.append(c)


    def lanzar_cliente(self):
        if len(self.clientes) > 0:
            mesa_random_y_pos = random.choice([(key, self.object_labels[key]) for key in\
                 self.object_labels.keys() if self.object_labels[key].type\
                 == "mesa" and self.object_labels[key].desocupada == True])        
            clientes_libres = []
            for cliente in self.clientes:
                if not cliente.isRunning() or not cliente.isFinished():
                    clientes_libres.append(cliente)
            cliente_random = random.choice(clientes_libres)    
            cliente_random.mesa_y_pos = mesa_random_y_pos #le damos al cliente su mesa
            mesa_random_y_pos[1].cliente = cliente_random #le damos a la mesa su cliente xd
            mesa_random_y_pos[1].desocupada = False
            cliente_random.start()
                 
    def reiniciar_partida(self):
        with open("mapa.csv", "w", encoding = "utf-8") as file:
            file.write("")
        with open("mapa.csv", "a", encoding = "utf-8") as file:
            file.write(f"mesero,471,801\n")
        objects = []
        while len(objects) < CHEFS_INICIALES:
            x = random.randint(0, 650)
            y = random.randint(0, 350)
            choca = False
            for c in objects:
                if -60 < c[1] - x < 60:
                    choca = True
            if not choca:
                objects.append(("chef", x, y))
        while len(objects) < CHEFS_INICIALES + MESAS_INICIALES:
            x = random.randint(0, 650)
            y = random.randint(0, 350)
            choca = False
            for c in objects:
                if -60 < c[1] - x < 60:
                    choca = True
            if not choca:
                objects.append(("mesa", x, y))

        for o in objects:
            with open("mapa.csv", "a", encoding = "utf-8") as file:
                file.write(f"{o[0]},{o[1]},{o[2]}\n")
        
        with open("datos.csv", "w", encoding = "utf-8") as file:
            file.write(f"{DINERO_INICIAL},{REPUTACION_INICIAL},{0}\n")

        ceros = ["0" for i in range(CHEFS_INICIALES)]
        with open("datos.csv", "a", encoding = "utf-8") as file:
            file.write(",".join(ceros))

    def guardar_partida(self, ronda):
        objetos = []
        objetos.append(("mesero", self.mesero.x, self.mesero.y))
        platos_chefs = []
        for obj in self.object_labels.values():
            if obj.type == "chef":
                objetos.append((obj.type, obj.x, obj.y))
                platos_chefs.append(str(obj.platos_preparados))
            else:
                objetos.append((obj.type, obj.x, obj.y))
        with open("mapa.csv", "w", encoding = "utf-8") as file:
            for obj in objetos:
                file.write(f"{obj[0]},{obj[1]},{obj[2]}\n") 

        with open("datos.csv", "w", encoding = "utf-8") as file:
            file.write(f"{self.dinero},{self.puntos_de_reputacion},{ronda}\n")

        with open("datos.csv", "a", encoding = "utf-8") as file:
            file.write(",".join(platos_chefs))

    def cargar_partida(self, seguir):
        if not seguir:
            self.reiniciar_partida()
        datos = []
        objetos = []
        with open("datos.csv", "r", encoding = "utf-8") as file:
            for line in file:
                datos.append(line.split(","))
        with open("mapa.csv", "r", encoding = "utf-8") as file:
            for line in file:
                objetos.append(line.split(","))

        self.dinero = int(datos[0][0])
        self.puntos_de_reputacion = int(datos[0][1])
        self.ronda_actual = int(datos[0][2])
        
        for obj in objetos:
            if obj[0] == "chef":
                self.senal_create_object.emit(
                    {'x': int(obj[1]),
                    'y': int(obj[2]),
                    "obj": obj[0],
                    "sprite": "meson"
                    })

            elif obj[0] == "mesa":
                self.senal_create_object.emit(
                    {'x': int(obj[1]),
                    'y': int(obj[2]),
                    "obj": "desk",
                    "sprite": "silla_mesa_roja"
                    })
        contador = 0
        for obj in self.object_labels.values():
            if obj.type == "chef":
                obj.platos_preparados = int(datos[1][contador])
                contador += 1
        self.start()

class Chef(core.QObject):

    senal_thread = core.pyqtSignal()
    senal_finish = core.pyqtSignal()
    senal_update_frames = core.pyqtSignal()
    estados = ["desocupado", "cocinando", "finished", "entregado"]
    def __init__(self, senal_update_position, x, y):
        super().__init__()
        self.type =  "chef"
        self.x = x
        self.y = y
        self.nivel = 1
        self.platos_preparados = 0
        self.estado = "desocupado"
        self.__frame = 0
        self.thread_preparar_plato = None
        self.senal_thread.connect(self.actualizar_frames)
        self.plato = None
        self.senal_finish.connect(self.terminar_plato)
        self.prob_fail = 0.3/(self.nivel + 1)
        self.senal_update_position = senal_update_position

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, value):
        if 17 < value:
            self.__frame = 1
        else:
            self.__frame = value

    def preparar_bocadillo(self, reputacion):
        tiempo_de_espera = max(0, 15 - int(reputacion) - 2*self.nivel)
        if self.thread_preparar_plato is None or not self.thread_preparar_plato.isRunning():
            self.thread_preparar_plato = PrepararPlato(self.senal_thread,\
                 self.senal_finish, tiempo_de_espera)
            self.thread_preparar_plato.start()
    
    def actualizar_frames(self):
        self.frame += 1
        self.senal_update_position.emit(
                {'obj': "chef",   
                    'x': self.x,
                    'y': self.y,
                    "frame": self.frame,
                    "sprite": "meson",
                    })

    def terminar_plato(self):
        p = random.random()
       
        if p > self.prob_fail:
            self.plato = Bocadillo(self.nivel)
            self.estado = "finished"
            self.platos_preparados += 1
            self.calcular_nivel()
        else:
            self.estado = "desocupado"
            self.plato = None
            return
        if self.plato != None:
            self.senal_update_position.emit(
                {'obj': "chef",   
                    'x': self.x,
                    'y': self.y,
                    "frame": 16,
                    "sprite": "meson",
                })
        else:
            self.senal_update_position.emit(
                {'obj': "chef",   
                    'x': self.x,
                    'y': self.y,
                    "frame": 1,
                    "sprite": "meson",
                })
    def calcular_nivel(self):
        if self.platos_preparados > PLATOS_EXPERTO:
            self.nivel = 3
        elif self.platos_preparados > PLATOS_INTERMEDIO:
            self.nivel = 2


class Mesa(core.QObject):

    def __init__(self, x, y):
        super().__init__()
        self.type = "mesa"
        self.x = x
        self.y = y
        self.desocupada = True
        self.cliente = None


class Bocadillo(core.QObject):
    def __init__(self, nivel_chef):
        self.nivel_chef = nivel_chef

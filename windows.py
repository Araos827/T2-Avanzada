import os
import sys
import PyQt5.QtCore as core
from PyQt5 import uic
import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as gui
from CustomLabels import DraggableLabel, DropLabel

window_name, base_class = uic.loadUiType("MainWindow.ui")

#El grid layout mide 740 x 430 y esta en las cooredenas (121, 391)
#El MiuEnzo mide 20 x 32
#Los clientes miden ??
#Los chefs miden 55 x 64 
#Las mesas miden  20 x 32 
#el origen del mapa esta el (121, 391)

class VentanaJuego(window_name, base_class):

    senal_comenzar_ronda = core.pyqtSignal(bool) 
    senal_mover_character = core.pyqtSignal(str)
    senal_send_object = core.pyqtSignal(dict)
    senal_check_superposicion = core.pyqtSignal(dict)
    send_pause_signal = core.pyqtSignal()
    senal_reiniciar_partida = core.pyqtSignal()
    senal_guardar = core.pyqtSignal(int)
    senal_cargar_partida = core.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.move(300, 20)
        self._frame = 1
        self.display_y = 430
        self.display_x = 740
        self.setWindowTitle("Juego")
        self.setupUi(self)
        self.characters = dict()
        self.chefs_labels = dict()
        self.desks_labels = dict()
        self.label_MiuEnzo.raise_()
        self.characters["Enzo"] = self.label_MiuEnzo
        self.init_gui()
        self.superposicion = bool
        self.ventana_resumen = None
        self.ronda = 1
  
    def init_gui(self):
        self.display_label = DropLabel("",self)
        self.display_label.setGeometry(121, 391, self.display_x, self.display_y)
        self.tienda_layout.addWidget(DraggableLabel(os.path.join(\
            "sprites","chef","meson_02.png"), "chef"))
        precio_chef = widgets.QLabel("$300", self)
        precio_chef.setAlignment(core.Qt.AlignCenter)
        self.tienda_layout.addWidget(precio_chef)
        self.tienda_layout.addWidget(DraggableLabel(\
            os.path.join("sprites","mapa","accesorios","silla_mesa_roja.png"), "desk"))
        precio_mesa = widgets.QLabel("$100", self)
        precio_mesa.setAlignment(core.Qt.AlignCenter)
        self.tienda_layout.addWidget(precio_mesa)

    def comenzar_ronda(self):
        self.senal_comenzar_ronda.emit(True)

    def salir(self):
        self.senal_guardar.emit(self.ronda)
        sys.exit()

    def pausa(self):
        self.send_pause_signal.emit()

    def keyPressEvent(self, event):
        if event.key() in [core.Qt.Key_A]:
            self.senal_mover_character.emit('L')
        elif event.key() in [core.Qt.Key_D]:
            self.senal_mover_character.emit('R')
        elif event.key() in [core.Qt.Key_W]:
            self.senal_mover_character.emit("U")
        elif event.key() in [core.Qt.Key_S]:
            self.senal_mover_character.emit("D")
    
    def update_position(self, event):
        if event["obj"] == "Enzo":
            char = self.characters[event["obj"]]
            if event.get("sprite"):
                pixmap = gui.QPixmap(os.path.join("sprites", event['sprite'], event["dir"] + "_0"\
                     + str(event['frame']) + ".png"))
                char.setPixmap(pixmap)
                char.resize(20,32)
            elif event.get("delete"):
                char.setPixmap(gui.QPixmap(None))
                return
            char.move(event["x"], event["y"])

        if event["obj"] == "chef":
            char = self.chefs_labels[(event["x"], event["y"])]
            if event.get("sprite"):
                if event["frame"] > 9:
                    frame = str(event["frame"])
                else:
                    frame = "0" + str(event["frame"])
                pixmap = gui.QPixmap(os.path.join("sprites", "chef", event["sprite"]\
                     + f"_{frame}" + ".png"))
                char.setPixmap(pixmap)
                char.resize(55, 64)
                char.show()
            elif event.get("detele"):
                char.setPixmap(gui.QPixmap(None))
                return

        if event["obj"] == "cliente":
            char = self.desks_labels[(event["x"], event["y"])]
            if event.get("frame"):
                char = self.desks_labels[(event["x"], event["y"])]
                pixmap = gui.QPixmap(os.path.join("sprites", "clientes", event["sprite"],\
                     event["sprite"] + "_" + str(event["frame"]) + ".png"))
                char.setPixmap(pixmap)
                char.resize(32, 32)
                char.show()
            elif event.get("delete"):
                char.setPixmap(gui.QPixmap(os.path.join("sprites", "mapa",\
                    "accesorios","silla_mesa_roja.png")))
                char.resize(20, 32)
                char.show()

    def create_object(self, event):

        if event["obj"] == "desk":
            label = widgets.QLabel(self.display_label)
            label.setPixmap(gui.QPixmap(os.path.join("sprites", "mapa","accesorios",\
                "silla_mesa_roja.png")))
            label.resize(20, 32)
            label.setScaledContents(True)
            label.move(event["x"], event["y"])
            self.senal_check_superposicion.emit({"obj": label})
            if self.superposicion:
                label.setPixmap(gui.QPixmap(None).scaled(20, 32))
                return
            label.show()
            self.desks_labels[(event["x"], event["y"])] = label
            self.senal_send_object.emit({"obj" : label, "type" : "mesa",\
                 "x" : event["x"], "y" : event["y"]})

        elif event["obj"] == "chef":
            label = widgets.QLabel(self.display_label)
            label.setPixmap(gui.QPixmap(os.path.join("sprites", "chef", "meson_01.png")))
            label.resize(55, 64)
            label.setScaledContents(True)
            label.move(event["x"], event["y"])
            self.senal_check_superposicion.emit({"obj": label})
            if self.superposicion:
                label.setPixmap(gui.QPixmap(None).scaled(20, 32))
                return
            self.chefs_labels[(event["x"], event["y"])] = label
            label.show()
            self.senal_send_object.emit({"obj" : label, "type" : "chef",\
                 "x" : event["x"], "y" : event["y"]})

    def recive_superposicion(self, data):
        self.superposicion = data

    def create_client(self, data):
        char = widgets.QLabel(self)

        char.setPixmap(gui.QPixmap("path a clientes").scaled(32, 32))
        char.move(data["x"], data["y"]) 
        char.show()
        self.characters[data["char"]] = char

    def recibir_reputacion(self, reputacion):
        self.label_reputacion.setText(f"Reputacion: {reputacion}")

    def recibir_ronda(self, ronda):
        self.label_ronda.setText(f"Ronda: {ronda}")

    def recibir_dinero(self, dinero):
        self.label_dinero.setText(f"Dinero: {dinero}")

    def recibir_clientes_atendidos(self, clientes_atendidos):
        self.label_clientes_atendidos.setText(f"Atendidos: {clientes_atendidos}")

    def recibir_clientes_perdidos(self, clientes_perdidos):
        self.label_clientes_perdidos.setText(f"Perdidos: {clientes_perdidos}")

    def recibir_clientes_proximos(self, clientes_proximos):
        self.label_clientes_proximos.setText(f"Proximos: {clientes_proximos}")

    def recibir_resumen(self, data):
        self.ventana_resumen = VentanaResumenRonda(self.senal_guardar,\
             self.senal_reiniciar_partida, self.send_pause_signal, data["ronda"])
        self.ventana_resumen.label_encabezado.setText("RESUMEN RONDA Nº" + str(data["ronda"]))
        self.ventana_resumen.lcdNumber_cp.display(data["clientes_perdidos"])
        self.ventana_resumen.lcdNumber_ca.display(data["clientes_atendidos"])
        self.ventana_resumen.lcdNumber_da.display(data["dinero_acumulado"])
        self.ventana_resumen.label_reputacion.setText("Reputacion: " +\
             str(data["reputacion"]) + "/5")
        self.ventana_resumen.show()
        self.ronda = data["ronda"]

    def cargar_objetos(self, event):
        self.show()
        self.senal_cargar_partida.emit(event)


class VentanaInicio(widgets.QWidget):

    senal_abrir_ventana = core.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.iniciar_gui()
    
    def iniciar_gui(self):
        self.setWindowTitle("Inicio")
        self.setGeometry(500, 100, 400, 300)
        self.logo = widgets.QLabel(self)
        self.logo.setPixmap(gui.QPixmap(os.path.join("sprites", "otros", "logo_blanco.png")).\
            scaled(800,300))
        self.logo.setScaledContents(True)
        self.mensaje_bienvenida = widgets.QLabel("Bienvenidos al mejor café virtual del DCC", self)
        self.boton_seguir = widgets.QPushButton("Seguir Jugando", self)
        self.boton_reset = widgets.QPushButton("Comenzar Denuevo", self)
        self.boton_seguir.clicked.connect(self.seguir_partida)
        self.boton_reset.clicked.connect(self.abrir_ventana_juego)

        hbox = widgets.QHBoxLayout()
        hbox.addWidget(self.boton_seguir)
        hbox.addWidget(self.boton_reset)

        vbox_logo = widgets.QVBoxLayout()
        vbox_logo.addWidget(self.logo)
        vbox_logo.addWidget(self.mensaje_bienvenida)

        vbox_main = widgets.QVBoxLayout()
        vbox_main.addLayout(vbox_logo)
        vbox_main.addLayout(hbox)
        self.setLayout(vbox_main)

        self.show()

    def abrir_ventana_juego(self):
        self.hide()
        self.senal_abrir_ventana.emit(False)

    def seguir_partida(self):
        self.hide()
        self.senal_abrir_ventana.emit(True)
    
ventana_resumen, widget_class = uic.loadUiType("ResumenWindow.ui")

class VentanaResumenRonda(ventana_resumen, widget_class):
    
    def __init__(self, senal_guardar, senal_reiniciar_partida, senal_pausa, ronda):
        super().__init__()
        self.ronda = ronda
        self.setWindowTitle("Resumen Ronda")
        self.setupUi(self)
        self.senal_guardar = senal_guardar
        self.senal_reiniciar_partida = senal_reiniciar_partida
        self.senal_pausa = senal_pausa

    def salir(self):
        self.senal_reiniciar_partida.emit()
        self.hide()
        sys.exit()

    def continuar(self):
        self.senal_pausa.emit()
        self.hide()

    def guardar(self):
        self.senal_guardar.emit(self.ronda)
        self.hide()


if __name__ == '__main__':
    app = widgets.QApplication([])

    ventana_1 = VentanaInicio()
    ventana_2 = VentanaJuego()

    ventana_2.label_MiuEnzo.move(100, 100)
    ventana_2.update()

    ventana_2.update()
    ventana_1.senal_abrir_ventana = ventana_2.senal_abrir_ventana
    
   
    
    sys.exit(app.exec_())
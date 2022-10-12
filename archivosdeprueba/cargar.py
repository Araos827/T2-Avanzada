import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap

class VentanaInicio(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 800, 800)
        self.setWindowTitle("Inicio")
        self.senal_abrir_ventana = None
        self.iniciar_gui()

    def iniciar_gui(self):
        self.label_logo = QLabel(self)
        self.label_logo.setPixmap(QPixmap(os.path.join("sprites\chef\meson_01.png")).scaled(32,32))
        self.label_logo.setScaledContents(True)
        self.mensaje_bienvenida = QLabel("Bienvenidos al mejor café virtual del DCC", self)
        self.boton_seguir = QPushButton("Seguir Jugando", self)
        self.boton_seguir.resize(self.boton_seguir.sizeHint())
        self.boton_reset = QPushButton("Comenzar Denuevo", self)
        self.boton_reset.resize(self.boton_reset.sizeHint())
        #self.boton_seguir.clicked.connect(self.abrir_ventana_juego)
        #self.boton_reset.clicked.connect(self.abrir_ventana_juego)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.boton_seguir)
        hbox.addWidget(self.boton_reset)

        vbox_logo = QVBoxLayout()
        vbox_logo.addWidget(self.label_logo)
        vbox_logo.addWidget(self.mensaje_bienvenida)
 

        vbox_main = QVBoxLayout()
        vbox_main.addLayout(vbox_logo)
        vbox_main.addLayout(hbox)
        self.setLayout(vbox_main)

        self.show()



if __name__ == '__main__':
    app = QApplication([])
    
    # Instanciamos dos ventanas distintas
    # Cada una comienza con una señal propia que
    # le permite ser abierta por otra.
    ventana_1 = VentanaInicio()

    # Conectamos las señales correspondientes:
    # ventana 1 tiene acceso a la señal de ventana 2
    # Ahora ventana 2 puede ser abierta desde ventana 1

    # Con esta también vinculamos a ventana 1 desde ventana 2
    
    sys.exit(app.exec_())

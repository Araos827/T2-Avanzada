import sys
from time import sleep

from PyQt5.QtCore import pyqtSignal, QTimer, QObject
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QHBoxLayout,
                             QVBoxLayout, QPushButton)


class MiTimers(QObject):
    
    senal_actualizar = pyqtSignal(int, str)

    def __init__(self, i, tiempo):
        super().__init__()
        self.indice = i
        self.tiempo = tiempo
        self.indice_actual = 0
        self.timer = QTimer()
        self.timer.setInterval(tiempo * 1000)
        self.timer.timeout.connect(self.enviar_dato)

    def enviar_dato(self):
        if self.indice_actual < 9:
            self.senal_actualizar.emit(self.indice, str(self.indice_actual))
            self.indice_actual += 1
        else:
            self.senal_actualizar.emit(self.indice, 'Status: timer terminado')
            self.timer.stop()

    def comenzar(self):
        self.timer.start()

    def sigue_andando(self):
        return self.timer.isActive()


class MiVentana(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timers = []
        self.init_gui()

    def init_gui(self):
        # Configuramos los widgets de la interfaz
        # Definimos un montón de labels que corresponderán a un timer cada uno
        self.labels = {i : QLabel('Status: esperando timer', self) for i in range(1, 6)}
        self.boton = QPushButton('Ejecutar Timers', self)
        self.boton.clicked.connect(self.ejecutar_timers)

        hboxs = []
        for i in range(1, 6):
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            hbox.addWidget(self.labels[i])
            hbox.addStretch(1)
            hboxs.append(hbox)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.boton)
        hbox.addStretch(1)
        hboxs.append(hbox)

        vbox = QVBoxLayout()
        for hbox in hboxs:
            vbox.addStretch(1)
            vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # Configuramos las propiedades de la ventana.
        self.setWindowTitle('Ejemplo timers')
        self.setGeometry(50, 50, 250, 200)
        self.show()

    def ejecutar_timers(self):
        """
        Este método crea cinco threads cada vez que se presiona el botón en la
        interfaz. Los threads recibirás como argumento el índice del label 
        que les corresponde y el tiempo que toman entre cada iteración.
        """
        if len(self.timers) == 0 or not any([timer.sigue_andando() for timer in self.timers]):
            self.timers = []
            for i in range(1, 6):
                timer = MiTimers(i, i / 10)
                # Se conecta la señal emitida por el timer
                # a un método de la ventana
                timer.senal_actualizar.connect(self.actualizar_labels)
                self.timers.append(timer)
                timer.comenzar()

    def actualizar_labels(self, indice, texto):
        """
        Este método actualiza el label correspondiente según los datos 
        enviados desde un thread através del índice y aplica el texto.
        """
        self.labels[indice].setText(texto)


if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    sys.exit(app.exec_())
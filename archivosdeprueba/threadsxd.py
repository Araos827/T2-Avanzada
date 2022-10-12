import sys
from time import sleep
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QHBoxLayout,
                             QVBoxLayout, QPushButton)


class MiThread(QThread):
    """
    Esta clase representa un thread personalizado que será utilizado durante
    la ejecución de la GUI.
    """

    def __init__(self, senal_actualizar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senal_actualizar = senal_actualizar

    def run(self):
        for i in range(10):
            sleep(0.5)
            self.senal_actualizar.emit(str(i))
        self.senal_actualizar.emit('Status: thread terminado')


class MiVentana(QWidget):

    # Creamos una señal para manejar la respuesta del thread
    senal_thread = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread = None
        # Conectamos la señal del thread al método que maneja
        self.senal_thread.connect(self.actualizar_labels)

        self.init_gui()

    def init_gui(self):
        # Configuramos los widgets de la interfaz
        self.label = QLabel('Status: esperando thread', self)
        self.boton = QPushButton('Ejecutar Thread', self)
        self.boton.clicked.connect(self.ejecutar_threads)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.label)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.boton)
        hbox2.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addStretch(1)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # Configuramos las propiedades de la ventana.
        self.setWindowTitle('Ejemplo threads')
        self.setGeometry(50, 50, 250, 200)
        self.show()

    def ejecutar_threads(self):
        """
        Este método crea un thread cada vez que se presiona el botón en la
        interfaz. El thread recibirá como argumento la señal sobre la cual
        debe operar.
        """
        if self.thread is None or not self.thread.isRunning():
            self.thread = MiThread(self.senal_thread)
            self.thread.start()

    def actualizar_labels(self, evento):
        """
        Este método actualiza el label según los datos enviados desde el
        thread através del objeto evento. Para este ejemplo, el método
        recibe el evento, pero podría también no recibir nada.
        """
        self.label.setText(evento)


if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    sys.exit(app.exec_())
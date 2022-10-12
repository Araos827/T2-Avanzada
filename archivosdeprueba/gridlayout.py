import os
import sys
import PyQt5.QtCore as core
from PyQt5 import uic
import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as gui


window_name, base_class = uic.loadUiType("gridlayout.ui")

class CustomLabel(widgets.QLabel):
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()
    
    def dropEvent(self, e):
        self.setPixmap(gui.QPixmap(os.path.join("sprites","mapa","accesorios","silla_mesa_roja.png")).scaled(32, 32)) 

class GridLayout(window_name, base_class):

    def __init__(self):
        super().__init__()
        self.move(300, 20)
        self.display_y = 380
        self.display_x = 650
        self.setWindowTitle("Juego")
        self.setupUi(self)
        self.characters = dict()
        self.fill_grid()
        self.listWidget_chef.setViewMode(widgets.QListWidget.IconMode)
        self.listWidget_desk.setViewMode(widgets.QListWidget.IconMode)
        self.listWidget_chef.setAcceptDrops(False)
        self.listWidget_desk.setAcceptDrops(False)
        chef = widgets.QListWidgetItem(gui.QIcon(os.path.join("sprites","chef","meson_01.png")), "$300")
        desk = widgets.QListWidgetItem(gui.QIcon(os.path.join("sprites","mapa","accesorios","silla_mesa_roja.png")), "$100")

        self.listWidget_chef.insertItem(1, chef)
        self.listWidget_desk.insertItem(1, desk)

    def fill_grid(self):
        posiciones = [(i, j) for i in range(self.display_x//64) for j in range(self.display_y//32)]
        
        for posicion in posiciones:
            char = CustomLabel()
            char.setPixmap(gui.QPixmap(None).scaled(32, 32)) 
            self.grid_layout.addWidget(char, *posicion)

        self.show()


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    
    sys.__excepthook__ = hook
    app = widgets.QApplication([])
    form = GridLayout()
    print(type(form.grid_layout))
    sys.exit(app.exec_())
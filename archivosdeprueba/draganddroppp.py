import sys

from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor
from PyQt5.QtCore import QMimeData, Qt


class DraggableLabel(QLabel):
    
    def __init__(self, image_path, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pixmap = QPixmap(image_path)
        self.setPixmap(pixmap)
        self.text = text
        self.path = image_path

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(self.text)
        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.path)
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)

class DropLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        pos = event.pos()
        print((event.pos().x()), event.pos().y())
        text = event.mimeData().text()
        print((event.pos().x()), event.pos().y(), text)

        if text == "chef":
            pixmap = QPixmap("sprites\chef\meson_01.png")
            self.setPixmap(pixmap)
            event.acceptProposedAction()


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label = DropLabel("drop there", self)
        label.setGeometry(190, 65, 100,100)

        label_to_drag = DraggableLabel("sprites\chef\meson_02.png","chef", self)  
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
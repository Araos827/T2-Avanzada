
import PyQt5.QtCore as core
import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as gui

class DraggableLabel(widgets.QLabel):
    
    def __init__(self, image_path, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pixmap = gui.QPixmap(image_path)
        self.setPixmap(pixmap)
        self.setAlignment(core.Qt.AlignCenter)
        self.text = text
        self.path = image_path

    def mousePressEvent(self, event):
        if event.button() == core.Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & core.Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength()\
             < widgets.QApplication.startDragDistance():
            return
        drag = gui.QDrag(self)
        mimedata = core.QMimeData()
        mimedata.setText(self.text)
        drag.setMimeData(mimedata)
        drag.setHotSpot(event.pos())
        drag.exec_(core.Qt.CopyAction | core.Qt.MoveAction)

class DropLabel(widgets.QLabel):
    senal_drop = core.pyqtSignal(dict)
    def __init__(self, *args, **kwargs):
        widgets.QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        pos = event.pos()
        text = event.mimeData().text()
        self.senal_drop.emit({"x": event.pos().x(), "y": event.pos().y(), "obj": text})

import sys
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsPixmapItem
from PyQt5.QtGui import QColor, QPainter, QPixmap, QDragEnterEvent, QDropEvent, QPen
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QObject, QRectF, QPointF, QEvent
from selectable_item import SelectableImageItem
from PyQt5.QtWidgets import QAction
import json
from PyQt5.QtWidgets import QFileDialog
from video_player import VideoGraphicsItem
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem
from PyQt5.QtWidgets import QGraphicsProxyWidget, QLineEdit, QGraphicsSceneMouseEvent, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QCursor
from editableText import EditableTextItem



class InfiniteCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.text_edit = None
        self.text_input_placeholder = None

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.setSceneRect(-100000000, -100000000, 200000000, 200000000)

        self.setBackgroundBrush(QColor("#202020"))

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setRenderHint(QPainter.Antialiasing, False)
        self.setWindowTitle("BetterRef")
        self.selectedItem = None

        self.is_middle_button_dragging = False
        self.last_drag_position = None
        self.setShortcut()


    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.drag_position = event.globalPos()
        if event.button() == Qt.MiddleButton or (event.button() == Qt.LeftButton and event.modifiers() == Qt.AltModifier):
            self.is_middle_button_dragging = True
            self.last_drag_position = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
        else:
            item = self.itemAt(event.pos())
            if item:
                if self.selectedItem and self.selectedItem != item:
                    self.selectedItem.setSelected(False)
                item.setSelected(True)
                self.selectedItem = item
                self.scene.update()  # Force the scene to update and redraw items
            else:
                if self.selectedItem:
                    self.selectedItem.setSelected(False)
                    self.selectedItem = None
                self.scene.update()  # Update the scene if no item is clicked
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            delta = event.globalPos() - self.drag_position
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_position = event.globalPos()
        if self.is_middle_button_dragging:
            delta = event.pos() - self.last_drag_position
            self.last_drag_position = event.pos()

            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton or (event.button() == Qt.LeftButton and event.modifiers() == Qt.AltModifier):
            self.is_middle_button_dragging = False
            self.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_T and not any(isinstance(item, EditableTextItem) and item.textInteractionFlags() & Qt.TextEditorInteraction for item in self.scene.items()):
            self.addTextItem()   
        if event.key() == Qt.Key_Q and event.modifiers() == Qt.ControlModifier:
            self.close()
        else:
            super().keyPressEvent(event)
    
    def addTextItem(self):
        mouse_pos = self.mapToScene(self.mapFromGlobal(QCursor.pos()))  # Convert global mouse position to scene coordinates
        text_item = EditableTextItem("Text")
        text_item.setDefaultTextColor(Qt.white)  # Set text color
        text_item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)  # Make text item movable and selectable
        text_item.setPos(mouse_pos)  # Set position at the mouse position in the scene
        self.scene.addItem(text_item)
        text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        text_item.setFocus()
        text_item.setTextInteractionFlags(Qt.NoTextInteraction)
        


    def closeEvent(self, event):
        event.accept()
        sys.exit(0)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()

            if file_path.lower().endswith(('.mp4', '.avi', '.mov')):  # Check for common video file extensions
                self.addVideoToScene(file_path, event.pos())
            else:
                self.addImageToScene(file_path, event.pos())  # Existing method for images
                
    def addVideoToScene(self, file_path, position):
        print("adding video")
        videoItem = VideoGraphicsItem(file_path)
        videoItem.setData(0, file_path)  

        videoItem.setPos(position)
        videoItem.setScale(6.0)  # Adjust this value based on your needs

        self.scene.addItem(videoItem)
        videoItem.itemData.dataChanged.connect(lambda item=videoItem: self.updateItemData(item))
        print("video added")

    def addImageToScene(self, image_path, position):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            item = SelectableImageItem(pixmap)
            item.setData(0, image_path)  
            item.setPos(position)
            item.setScale(1) 
            item.setRotation(0)  
            item.setTransformOriginPoint(pixmap.width() / 2, pixmap.height() / 2) 
            self.scene.addItem(item)
            item.itemData.dataChanged.connect(lambda item=item: self.updateItemData(item))

    def updateItemData(self, item):
        data = {
            "image_path": item.data(0),
            "position": {"x": item.x(), "y": item.y()},
            "rotation": item.rotation(),
            "scale": item.scale() 
        }
        print("Updated item data:", data)

    def wheelEvent(self, event):
        zoomInFactor = 1.25 
        zoomOutFactor = 1 / zoomInFactor

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        if event.angleDelta().y() > 0:
            self.scale(zoomInFactor, zoomInFactor)
        else:
            self.scale(zoomOutFactor, zoomOutFactor)

    ##SAVE AND LOAD##
    def setShortcut(self):
        self.saveAction = QAction("Save", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.saveToFile)
        self.addAction(self.saveAction)

        self.openAction = QAction("Open", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.loadFromFile)
        self.addAction(self.openAction)




    def collectItemData(self):
        items_data = []
        for item in self.scene.items():
            if isinstance(item, SelectableImageItem):
                data = {
                    "image_path": item.data(0),  
                    "position": {"x": item.x(), "y": item.y()},
                    "rotation": item.rotation(),
                    "scale": item.scale() 
                }
                items_data.append(data)
        return items_data

    def saveToFile(self):
        items_data = self.collectItemData()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "BetterRef Files (*.brf)")
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(items_data, file, indent=4)
            print(f"File saved: {file_path}") 

    def loadFromFile(self, file_path):
        with open(file_path, 'r') as file:
            items_data = json.load(file)
        for data in items_data:
            self.addImageFromData(data)

    def addImageFromData(self, data):
        image_path = data["image_path"]
        position = QPointF(data["position"]["x"], data["position"]["y"])
        scale_x = data["scale"]["x"]
        scale_y = data["scale"]["y"]
        rotation = data["rotation"]
        pixmap = QPixmap(image_path)
        item = SelectableImageItem(pixmap)
        item.setData(0, image_path)
        item.setPos(position)
        item.setScale(scale_x) 
        item.setRotation(rotation)
        self.scene.addItem(item)

        ##LOAD SHIT


    def loadFromFile(self, file_path):            
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "BetterRef Files (*.brf)")
        if file_path:
            with open(file_path, 'r') as file:
                items_data = json.load(file)
            self.restoreScene(items_data)

    def restoreScene(self, items_data):
        self.scene.clear()  
        for data in items_data:
            self.addImageFromData(data)

    def addImageFromData(self, data):
        image_path = data["image_path"]
        position = QPointF(data["position"]["x"], data["position"]["y"])
        scale = data.get("scale", 1) 
        rotation = data.get("rotation", 0) 
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            item = SelectableImageItem(pixmap)
            item.setData(0, image_path) 
            item.setPos(position)
            item.setScale(scale)  
            item.setRotation(rotation)
            item.setTransformOriginPoint(pixmap.width() / 2, pixmap.height() / 2)
            self.scene.addItem(item)
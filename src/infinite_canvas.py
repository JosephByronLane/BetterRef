import sys
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsPixmapItem
from PyQt5.QtGui import QColor, QPainter, QPixmap, QDragEnterEvent, QDropEvent, QPen, QFont, QContextMenuEvent
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QObject, QRectF, QPointF, QEvent, QTimer, QPoint  
from selectable_item import SelectableImageItem
from PyQt5.QtWidgets import QAction
import json
from PyQt5.QtWidgets import QFileDialog
from video_player import VideoGraphicsItem
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem
from PyQt5.QtWidgets import QAction, QLineEdit, QGraphicsSceneMouseEvent, QGraphicsRectItem, QGraphicsItemGroup, QMessageBox
from PyQt5.QtGui import QCursor
from editableText import EditableTextItem
from handle_item import HandleItem
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QMenu, QAction
from settings_window import SettingsWindow


class InfiniteCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.text_edit = None
        self.text_input_placeholder = None
        self.settingsWindow = None

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
        self.group = None 
        self.groupBoundingBox = None
        self.is_middle_button_dragging = False
        self.last_drag_position = None
        self.setShortcut()


        #context menu right click
        self.drag_position = None
        self.context_menu_timer = QTimer(self)
        self.context_menu_timer.setSingleShot(True)
        self.context_menu_timer.timeout.connect(self.show_context_menu)
        self.context_menu_event = None
        self.right_button_pressed = False
        self.context_menu_position = None





    def selectAllItems(self):
        for item in self.scene.items():
            item.setSelected(True)
        self.groupSelectedItems()

    def groupSelectedItems(self):
        if self.group:
            self.scene.removeItem(self.group) 
            self.scene.removeItem(self.groupBoundingBox)  

        self.group = QGraphicsItemGroup()
        for item in self.scene.selectedItems():
            item.setSelected(False)  
            self.group.addToGroup(item)

        self.scene.addItem(self.group)
        self.group.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        self.group.setFiltersChildEvents(False)  

        self.groupBoundingBox = QGraphicsRectItem(self.group.boundingRect())
        self.groupBoundingBox.setPen(QPen(QColor('blue'), 3))
        self.groupBoundingBox.setBrush(QColor(0, 0, 0, 0))  
        self.groupBoundingBox.setParentItem(self.group)
        self.groupBoundingBox.setZValue(self.group.zValue() - 1)  
        
        self.groupBoundingBox.handles = [HandleItem(self.groupBoundingBox) for _ in range(4)]
        self.updateGroupHandles()
        

    def hideGroupHandles(self):
        if self.groupBoundingBox:
            for handle in self.groupBoundingBox.handles:
                handle.hide()
            self.groupBoundingBox.hide()

    def updateGroupHandles(self):
        if not self.groupBoundingBox:
            return

        rect = self.groupBoundingBox.rect()
        corners = [rect.topLeft(), rect.topRight(), rect.bottomRight(), rect.bottomLeft()]
        for handle, pos in zip(self.groupBoundingBox.handles, corners):
            handle.setPos(pos)
            handle.show()

    def deselectGroup(self):
        if self.groupBoundingBox:
            for handle in self.groupBoundingBox.handles:
                handle.hide()
            self.groupBoundingBox.hide()
        if self.group:
            items = self.group.childItems()
            for item in items:
                self.group.removeFromGroup(item)
                self.scene.addItem(item)
            self.scene.removeItem(self.group)
            self.group = None


    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.drag_position = event.globalPos()

            self.right_button_pressed = True
            self.context_menu_position = event.globalPos()  # Store the global position of the right-click

            self.context_menu_event = event
            self.context_menu_timer.start(1100)  # Start the timer for 200 ms

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
                self.scene.update()
            else:
                if self.selectedItem:
                    self.selectedItem.setSelected(False)
                    self.selectedItem = None
                if self.group:
                    self.deselectGroup()
                self.scene.update()
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:

            # Cancel the context menu timer if dragging
            if self.context_menu_timer.isActive():
                self.context_menu_timer.stop()

            delta = event.globalPos() - self.drag_position
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_position = event.globalPos()
            self.right_button_pressed = False  # Set to False, indicating this is a drag, not a click


        if self.is_middle_button_dragging:
            delta = event.pos() - self.last_drag_position
            self.last_drag_position = event.pos()

            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())

        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            # On releasing the right button, if no drag happened and the timer is not active, show the context menu
            if self.right_button_pressed and not self.context_menu_timer.isActive():
                self.show_context_menu()

            self.right_button_pressed = False  # Reset the flag

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
        mouse_pos = self.mapToScene(self.mapFromGlobal(QCursor.pos()))  
        text_item = EditableTextItem("Text")
        text_item.setDefaultTextColor(Qt.white) 

        font = text_item.font()
        font.setPointSize(24)  
        text_item.setFont(font)

        text_item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable) 
        text_item.setPos(mouse_pos)
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

            if file_path.lower().endswith(('.mp4', '.avi', '.mov')):  
                self.addVideoToScene(file_path, event.pos())
            elif file_path.lower().endswith(('.png', '.jpg', '.webp')):  
                self.addImageToScene(file_path, event.pos()) 
            else:
                QMessageBox.critical(self, "Error", "Unsupported file format. Please drop a supported file (mp4, avi, mov, png, jpg, webp).")
                
    def addVideoToScene(self, file_path, position):
        print("adding video")
        videoItem = VideoGraphicsItem(file_path)
        videoItem.setData(0, file_path)  

        videoItem.setPos(position)
        videoItem.setScale(6.0)  

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

        selectAllAction = QAction("Select All", self)
        selectAllAction.setShortcut("Ctrl+A")
        selectAllAction.triggered.connect(self.selectAllItems)
        self.addAction(selectAllAction)

    def collectItemData(self):
        items_data = []
        for item in self.scene.items():
            if isinstance(item, SelectableImageItem):
                data = {
                    "type": "image",
                    "image_path": item.data(0),
                    "position": {"x": item.x(), "y": item.y()},
                    "rotation": item.rotation(),
                    "scale": item.scale()
                }
                items_data.append(data)
            elif isinstance(item, VideoGraphicsItem):
                data = {
                    "type": "video",
                    "file_path": item.url,
                    "position": {"x": item.x(), "y": item.y()},
                    "rotation": item.rotation(),
                    "scale": item.scale(),
                    "media_position": item.mediaPlayer.position() 
                }
                items_data.append(data)
            elif isinstance(item, EditableTextItem):
                data = {
                    "type": "text",
                    "text": item.toPlainText(),
                    "position": {"x": item.x(), "y": item.y()},
                    "scale": item.scale(),
                    "font": item.font().toString(),
                    "color": item.defaultTextColor().name() 

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

    def loadFromFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "BetterRef Files (*.brf)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    items_data = json.load(file)
                self.restoreScene(items_data)
                print(f"Scene loaded successfully from {file_path}")
            except Exception as e:
                print(f"Error loading file: {e}")

    def restoreScene(self, items_data):
        self.scene.clear()
        for data in items_data:
            if data["type"] == "image":
                self.addImageFromData(data)
            elif data["type"] == "video":
                self.addVideoFromData(data)
            elif data["type"] == "text":
                self.addTextFromData(data)
        self.scene.update()
        print(f"Scene restored with {len(items_data)} items")

    def addVideoFromData(self, data):
        file_path = data["file_path"]
        position = QPointF(data["position"]["x"], data["position"]["y"])
        scale = data.get("scale", 1)
        rotation = data.get("rotation", 0)
        media_position = data.get("media_position", 0)

        videoItem = VideoGraphicsItem(file_path)
        videoItem.setPos(position)
        videoItem.setScale(scale)
        videoItem.setRotation(rotation)
        videoItem.mediaPlayer.setPosition(media_position) 
        self.scene.addItem(videoItem)

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

    def addTextFromData(self, data):
        text = data["text"]
        position = QPointF(data["position"]["x"], data["position"]["y"])
        scale = data.get("scale", 1)
        font_str = data.get("font", "")
        color_str = data.get("color", "#FFFFFF") 

        text_item = EditableTextItem(text)
        text_item.setPos(position)
        text_item.setScale(scale)
        if font_str:
            font = QFont()
            font.fromString(font_str)
            text_item.setFont(font)
        text_item.setDefaultTextColor(QColor(color_str)) 

        self.scene.addItem(text_item)

    ##CONTXT MNU

    def show_context_menu(self):
        if self.context_menu_position:
            menu = QMenu(self)
            print("open settings menu")
            settingsAction = QAction("Settings", self)
            settingsAction.triggered.connect(self.openSettings)

            menu.addAction(settingsAction)

            # Show the context menu at the stored position of the right-click event
            menu.exec_(self.context_menu_position)


    def contextMenuEvent(self, event):
        # Do nothing here, as we're now handling the context menu manually
        pass

    def openSettings(self):
        print("Opening settings...")
        if self.settingsWindow is None:
            self.settingsWindow = SettingsWindow(self)
        self.settingsWindow.show()
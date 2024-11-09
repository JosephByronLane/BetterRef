from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QPushButton, QSlider, QGraphicsProxyWidget, QHBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from handle_item import HandleItem
from PyQt5.QtGui import QMouseEvent

class ItemData(QObject):
    dataChanged = pyqtSignal()

class VideoGraphicsItem(QGraphicsVideoItem):
    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.url = url

        self.handles = [HandleItem(self) for _ in range(4)]  
        self.hideHandles() 

        self.initUI(url)

        self.itemData = ItemData()

    def initUI(self, url):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(url)))

        controlWidget = QWidget()
        layout = QHBoxLayout()
        self.playPauseButton = QPushButton("Pause") 
        self.playPauseButton.clicked.connect(self.togglePlayPause)
        layout.addWidget(self.playPauseButton)

        self.progressBar = QSlider(Qt.Horizontal)
        self.progressBar.setRange(0, 100)
        layout.addWidget(self.progressBar)
        controlWidget.setLayout(layout)

        self.controlsProxy = QGraphicsProxyWidget(self)
        self.controlsProxy.setWidget(controlWidget)
        self.controlsProxy.setPos(0, self.boundingRect().height())  

        self.mediaPlayer.positionChanged.connect(self.updateProgressBar)
        self.mediaPlayer.durationChanged.connect(self.updateProgressBar)
        
        self.mediaPlayer.play() 

        self.updateControlWidgetSize()

    def togglePlayPause(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playPauseButton.setText('Play')
        else:
            self.mediaPlayer.play()
            self.playPauseButton.setText('Pause')

    def updateProgressBar(self):
        duration = self.mediaPlayer.duration()
        position = self.mediaPlayer.position()
        if duration > 0:
            progress = int((position / duration) * 100)
            self.progressBar.setValue(progress)

        # Update control positioning and size
        self.updateControlWidgetSize()

    def updateControlWidgetSize(self):
        videoWidth = int(self.boundingRect().width())  # Cast to int
        self.controlsProxy.setPos(0, self.boundingRect().height())
        self.controlsProxy.widget().setFixedWidth(videoWidth)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Reposition controls when the video item is resized
        self.updateControlWidgetSize()

    def togglePlay(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        self.itemData.dataChanged.emit()

    def setVolume(self, volume):
        self.mediaPlayer.setVolume(volume)
        self.itemData.dataChanged.emit()

    def position(self):
        return self.mediaPlayer.position()

    def duration(self):
        return self.mediaPlayer.duration()

    def collectItemData(self):
        items_data = []
        for item in self.scene().items():
            if isinstance(item, VideoGraphicsItem):
                data = {
                    "file_path": item.url,
                    "position": {"x": item.x(), "y": item.y()},
                    "rotation": item.rotation(),
                    "scale": item.scale(),
                    "media_position": item.position(),  # Save current playback position
                    "type": "video"
                }
                items_data.append(data)
            # Include similar handling for images if mixed content
        return items_data    

    def boundingRect(self):
        originalRect = super().boundingRect()
        outlineWidth = 3  # Same as the outline pen width
        return originalRect.adjusted(-outlineWidth, -outlineWidth, outlineWidth, outlineWidth)

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self.isSelected():
            painter.setPen(QPen(QColor('blue'), 3))
            painter.drawRect(self.boundingRect().adjusted(3, 3, -3, -3))
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            if value:
                self.showHandles()
            else:
                self.hideHandles()
        return super().itemChange(change, value)
    def updateHandles(self):
        if not self.isSelected():
            for handle in self.handles:
                handle.hide()
            return

        # Ensure handles are shown and correctly positioned around the image
        rect = self.boundingRect()
        corners = [rect.topLeft(), rect.topRight(), rect.bottomRight(), rect.bottomLeft()]
        for handle, pos in zip(self.handles, corners):
            handle.setPos(self.mapToScene(pos))
            handle.show()
    def hideHandles(self):
        for handle in self.handles:
            handle.hide()

    def showHandles(self):
        self.positionHandles()
        for handle in self.handles:
            handle.show()

    def positionHandles(self):
        rect = self.boundingRect()
        # Adjust handle positions to be at the corners of the video item
        self.handles[0].setPos(rect.topLeft())
        self.handles[1].setPos(rect.topRight())
        self.handles[2].setPos(rect.bottomRight())
        self.handles[3].setPos(rect.bottomLeft())

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        if self.isSelected():
            painter.setPen(QPen(QColor('blue'), 3))
            painter.drawRect(self.boundingRect())
            self.showHandles()
        else:
            self.hideHandles()


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.isSelected():
            self.scene().update()
        if self.dragging:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            self.setCursor(Qt.ArrowCursor)
            self.itemData.dataChanged.emit()

        super().mouseReleaseEvent(event)

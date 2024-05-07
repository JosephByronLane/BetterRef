from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsPixmapItem, QGraphicsItem, QMenu
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import pyqtSignal, QObject


class ItemData(QObject):
    dataChanged = pyqtSignal()

class VideoGraphicsItem(QGraphicsVideoItem):
    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(url)))
        self.mediaPlayer.play()  

        self.itemData = ItemData()
        self.url = url  

    def contextMenuEvent(self, event):
        menu = QMenu()
        playAction = menu.addAction("Play")
        pauseAction = menu.addAction("Pause")
        stopAction = menu.addAction("Stop")

        action = menu.exec_(event.screenPos())
        if action == playAction:
            self.player.play()
        elif action == pauseAction:
            self.player.pause()
        elif action == stopAction:
            self.player.stop()

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
        for item in self.scene.items():
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
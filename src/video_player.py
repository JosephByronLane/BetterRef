from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QObject
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsPixmapItem, QGraphicsItem, QMenu
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QPushButton, QSlider, QVBoxLayout, QWidget


class ItemData(QObject):
    dataChanged = pyqtSignal()

class VideoGraphicsItem(QGraphicsVideoItem):
    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)

        # Initialize media player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVideoOutput(self)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(url)))
        self.mediaPlayer.play()  # Start playing immediately; adjust as needed

        # Metadata and signaling for changes
        self.itemData = ItemData()
        self.url = url  # Store video URL for saving/loading state

        # Layout for controls
        self.layout = QVBoxLayout()
        self.playPauseButton = QPushButton("Pause")
        self.playPauseButton.clicked.connect(self.togglePlay)
        self.timeline = QSlider(Qt.Horizontal)
        self.timeline.setMaximum(1000)  # Assuming 1000 steps
        self.timeline.sliderMoved.connect(self.setVideoPosition)
        self.layout.addWidget(self.playPauseButton)
        self.layout.addWidget(self.timeline)
        self.setLayout(self.layout)

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
            self.playPauseButton.setText("Play")
        else:
            self.mediaPlayer.play()
            self.playPauseButton.setText("Pause")

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
    

    def setVideoPosition(self, position):
        # Calculate the position in the video to seek to
        videoLength = self.mediaPlayer.duration()
        seekPosition = videoLength * (position / 1000)
        self.mediaPlayer.setPosition(seekPosition)

    def updateSlider(self):
        currentPosition = self.mediaPlayer.position()
        totalDuration = self.mediaPlayer.duration()
        if totalDuration > 0:
            sliderValue = 1000 * currentPosition / totalDuration
            self.timeline.setValue(int(sliderValue))

    def updateHandles(self):
        if not self.isSelected():
            for handle in self.handles:
                handle.hide()
        else:
            # Ensure handles are shown and correctly positioned around the video
            rect = self.boundingRect()
            corners = [rect.topLeft(), rect.topRight(), rect.bottomRight(), rect.bottomLeft()]
            for handle, pos in zip(self.handles, corners):
                handle.setPos(self.mapToScene(pos))
                handle.show()
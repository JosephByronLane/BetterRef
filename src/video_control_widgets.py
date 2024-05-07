from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QObject
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsPixmapItem, QGraphicsItem, QMenu
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QPushButton, QSlider, QVBoxLayout, QWidget

class VideoControlWidget(QWidget):
    def __init__(self, videoItem, parent=None):
        super().__init__(parent)
        self.videoItem = videoItem

        layout = QVBoxLayout()
        self.playPauseButton = QPushButton("Pause")
        self.playPauseButton.clicked.connect(self.togglePlayPause)
        layout.addWidget(self.playPauseButton)

        self.timeline = QSlider(Qt.Horizontal)
        self.timeline.setMaximum(1000)
        self.timeline.sliderMoved.connect(self.seekVideo)
        layout.addWidget(self.timeline)

        self.setLayout(layout)
        self.updateTimer = QTimer()
        self.updateTimer.timeout.connect(self.updateSlider)
        self.updateTimer.start(100)  # Update slider every 100 ms

    def togglePlayPause(self):
        self.videoItem.togglePlay()
        self.playPauseButton.setText("Play" if self.videoItem.mediaPlayer.state() == QMediaPlayer.PlayingState else "Pause")

    def seekVideo(self, value):
        totalDuration = self.videoItem.mediaPlayer.duration()
        newPosition = totalDuration * value / 1000
        self.videoItem.setPosition(newPosition)

    def updateSlider(self):
        currentPosition = self.videoItem.position()
        totalDuration = self.videoItem.duration()
        if totalDuration > 0:
            sliderValue = currentPosition * 1000 / totalDuration
            self.timeline.setValue(sliderValue)
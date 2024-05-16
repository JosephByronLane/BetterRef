import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog
import subprocess
import json
from infinite_canvas import InfiniteCanvas

class newwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('C:/Users/HP/Desktop/BetterRef/src/PureReffUIStart5.ui', self)
        
        self.pushButton.clicked.connect(self.onPushButtonClicked)
        self.pushButton_2.clicked.connect(self.onPushButton2Clicked)
        
    def onPushButtonClicked(self):
        subprocess.Popen(['python', 'C:/Users/HP/Desktop/BetterRef/src/main.py'])
        print("Botón 1 clicado")

    def onPushButton2Clicked(self):
        InfiniteCanvas.loadFromFile(self)
        print("Botón 2 clicado")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = newwindow()
    mainWindow.show()
    sys.exit(app.exec())

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QFileDialog
import subprocess
import json
from infinite_canvas import InfiniteCanvas

class newwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('C:/Users/HP/Desktop/BetterRef/src/PureReffUIStart.ui', self)
        
        self.pushButton.clicked.connect(self.onPushButtonClicked)
        self.pushButton_2.clicked.connect(self.onPushButton2Clicked)
        
    def onPushButtonClicked(self):
        subprocess.Popen(['python', 'C:/Users/HP/Desktop/BetterRef/src/main.py'])
        print("Botón 1 clicado")

    def onPushButton2Clicked(self):
        self.loadFromFile()
        print("Botón 2 clicado")
    
    def loadFromFile(self):            
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "BetterRef Files (*.brf)")
        if file_path:
            with open(file_path, 'r') as file:
                items_data = json.load(file)
            InfiniteCanvas.restoreScene(items_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = newwindow()
    mainWindow.show()
    sys.exit(app.exec())

import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog
import subprocess
from infinite_canvas import InfiniteCanvas

class newwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        dir_path = os.path.dirname(os.path.realpath(__file__))

        ui_path = os.path.join(dir_path, 'PureReffUIStart5.ui')
        loadUi(ui_path, self)
        
        self.pushButton.clicked.connect(self.onPushButtonClicked)
        self.pushButton_2.clicked.connect(self.onPushButton2Clicked)

        self.canvas = InfiniteCanvas()
        
        
    def onPushButtonClicked(self):
        script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'main.py')
        subprocess.Popen(['python', script_path])
        print("Botón 1 clicado")

    def onPushButton2Clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "BetterRef Files (*.brf)")
        if file_path:
            self.canvas.loadFromFile(file_path)
        print("Botón 2 clicado")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = newwindow()
    mainWindow.show()
    sys.exit(app.exec())

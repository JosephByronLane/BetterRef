import sys
from PyQt5.QtWidgets import QApplication
from infinite_canvas import InfiniteCanvas

if __name__ == '__main__':
    app = QApplication(sys.argv)
    canvas = InfiniteCanvas()
    if canvas.loadFromFile():
        canvas.show()
    sys.exit(app.exec_())
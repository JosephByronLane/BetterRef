from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
from PyQt5.QtGui import QImage, QColor

class ImageDisplayWidget(QWidget):
    def __init__(self, canvas_instance, parent=None):
        super().__init__(parent)

        # Set the widget's background to be transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        # Store reference to the InfiniteCanvas instance
        self.canvas_instance = canvas_instance

        # Set up the layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Top Element: Image Label
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.load_transparent_image()

        # Middle Element: Instruction Text Label
        self.instruction_label = QLabel("Try dragging in an image to get started!", self)
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("color: #5F5F5F; font-size: 16px;")

        self.instruction_label_or = QLabel("or", self)
        self.instruction_label_or.setAlignment(Qt.AlignCenter)
        self.instruction_label_or.setStyleSheet("color: #5F5F5F; font-size: 18px;")

        # Bottom Element: "Open File" Button with rounded corners, blue background, and white text
        self.open_file_button = QPushButton("Open a file", self)
        self.open_file_button.setStyleSheet("""
            QPushButton {
                background-color: #32a9ff;  /* Blue background */
                color: white;  /* White text */
                border-radius: 10px;  /* Rounded corners */
                padding: 10px 20px;  /* Add padding */
                font-size: 28px;
            }
            QPushButton:hover {
                background-color: #0056b3;  /* Darker blue when hovered */
            }
            QPushButton:pressed {
                background-color: #004085;  /* Even darker blue when pressed */
            }
        """)

        self.open_file_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        
        # Add all elements to the layout
        self.layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.instruction_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.instruction_label_or, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.open_file_button, alignment=Qt.AlignCenter)


    def load_transparent_image(self):
        # Load a transparent PNG image
        transparent_image_path = os.path.join(os.path.dirname(__file__), 'assets/image-gallery.png')
        if os.path.exists(transparent_image_path):
            image = QImage(transparent_image_path)

            # New color to override with (e.g., pure blue)
            new_color = QColor(95, 95, 95)  # RGB value

            # Iterate over each pixel to modify the color while preserving alpha
            for y in range(image.height()):
                for x in range(image.width()):
                    pixel_color = image.pixelColor(x, y)
                    alpha = pixel_color.alpha()  # Preserve the alpha channel

                    if alpha > 0:  # Only modify non-transparent pixels
                        # Set new color with the original alpha
                        modified_color = QColor(new_color.red(), new_color.green(), new_color.blue(), alpha)
                        image.setPixelColor(x, y, modified_color)

            # Convert modified QImage to QPixmap and set it to the label
            pixmap = QPixmap.fromImage(image)
            self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # If image is not found, just leave it as a placeholder label
            self.image_label.setText("Image not found")


    def open_file(self):
        # Call the loadFromFile() method from the InfiniteCanvas instance
        if hasattr(self.canvas_instance, 'loadFromFile'):
            self.canvas_instance.loadFromFile()
        else:
            print("Error: loadFromFile method not found in InfiniteCanvas instance")

import sys

from PIL import Image
from PyQt5.QtWidgets import (QApplication, QGroupBox, QDialog, QVBoxLayout,
                             QGridLayout, QAbstractButton)
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtCore import QSize

CARD_WIDTH = 40
CARD_HEIGHT = 75
N_ROWS = 6
N_COLS = 14


def create_card_images():
    # Crop images for each card
    all_images_path = Image.open('images/jeu_de_tarot_complet.png')
    offset = 1  # Border to remove at each card side
    paths = []
    for row in range(N_ROWS):
        paths.append([None] * N_COLS)
        for col in range(N_COLS):
            top_left_x = offset + col * (CARD_WIDTH + 2 * offset)
            top_left_y = offset + row * (CARD_HEIGHT + 2 * offset)
            image = all_images_path.crop((
                top_left_x,
                top_left_y,
                top_left_x + CARD_WIDTH,
                top_left_y + CARD_HEIGHT
            ))
            hover_image = image.point(lambda p: p * 0.8)
            greyed_image = image.point(lambda p: p * 0.5)

            path = f'images/{row}_{col:02d}.png'
            image.save(path)
            hover_image.save(path.replace('.png', '_hover.png'))
            greyed_image.save(path.replace('.png', '_greyed.png'))
            paths[row][col] = path
    return paths


class PicButton(QAbstractButton):
    def __init__(self, path, parent=None):
        super(PicButton, self).__init__(parent)
        image = QImage(path)
        greyed_image = QImage(path.replace('.png', '_greyed.png'))
        hover_image = QImage(path.replace('.png', '_hover.png'))
        self.pixmap = QPixmap.fromImage(image)
        self.pixmap_pressed = QPixmap.fromImage(greyed_image)
        self.pixmap_hover = QPixmap.fromImage(hover_image)
        self.pressed = False

    @property
    def current_pixmap(self):
        if self.pressed:
            return self.pixmap_pressed
        elif self.underMouse():
            return self.pixmap_hover
        else:
            return self.pixmap

    def paintEvent(self, event):
        if self.isDown():
            # When image is pressed, change the status
            self.pressed = not self.pressed
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.current_pixmap)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(CARD_WIDTH, CARD_HEIGHT)


class App(QDialog):
    def __init__(self, images_paths):
        super().__init__()
        self.images_paths = images_paths
        self.title = 'Tarot counter'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()

        for row in range(N_ROWS):
            for col in range(N_COLS):
                image_path = self.images_paths[row][col]
                layout.addWidget(PicButton(image_path), row, col)

        self.horizontalGroupBox.setLayout(layout)


if __name__ == '__main__':
    images_paths = create_card_images()
    app = QApplication(sys.argv)
    ex = App(images_paths)
    sys.exit(app.exec_())

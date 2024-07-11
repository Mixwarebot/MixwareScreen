from qtCore import *


class ImageItem(QFrame):
    def __init__(self, image=None, parent=None):
        super().__init__(parent)
        self._image_src = None
        if type(image) == str:
            self._image_src = QPixmap(image)
        elif type(image) == QPixmap:
            self._image_src = image

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._image = QLabel()
        self._image.setObjectName("frameOutLine")
        self._image.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self._image)

        self._title = QLabel()
        self._title.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self._title)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self._image.setPixmap(self._image_src.scaledToHeight(self.height()))

    def set_title(self, name: str):
        self._title.setText(name)

    def set_image(self, image):
        if type(image) == str:
            self._image_src = QPixmap(image)
        elif type(image) == QPixmap:
            self._image_src = image
        self._image.setPixmap(self._image_src.scaledToHeight(self.height()))

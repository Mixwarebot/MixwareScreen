from qtCore import *


class MovieLabel(QFrame):

    def __init__(self, movie: str, w=48, h=48, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignCenter)

        self._is_move = None

        self.logo = QLabel()
        self.logo.setFixedSize(QSize(w, h))
        self.logo.setScaledContents(True)

        self._movie = QMovie(movie)
        self._movie.setScaledSize(self.logo.size())
        self.logo.setMovie(self._movie)

        self.layout.addWidget(self.logo)

    def showEvent(self, *args, **kwargs):
        self._movie.start()

    def hideEvent(self, *args, **kwargs):
        self._movie.stop()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self._is_move = False

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if not self._is_move and 0 < a0.x() < self.width() and 0 < a0.y() < self.height():
            if self._movie.state() == QMovie.Running:
                self._movie.stop()
            else:
                self._movie.start()

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        self._is_move = True

    def set_movie(self, movie: QMovie):
        if self.isVisible():
            self._movie.stop()

        self._movie = movie
        self._movie.setScaledSize(self.size())
        self.logo.setMovie(self._movie)

        if self.isVisible():
            self._movie.start()

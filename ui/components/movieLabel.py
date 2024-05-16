from qtCore import *


class MovieLabel(QLabel):

    def __init__(self, movie: str, text=None, parent=None):
        super().__init__(text, parent)

        self.setScaledContents(True)

        self._is_move = None
        self._movie = QMovie(movie)
        self._movie.setScaledSize(self.size())
        self.setMovie(self._movie)

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

        if self.isVisible():
            self._movie.start()

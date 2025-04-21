from PyQt6.QtWidgets import QGraphicsEffect
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtCore import Qt, QPoint

class ShadowEffect(QGraphicsEffect):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._radius = 12
        self._color = QColor(0, 0, 0, 40)
        self._offset = QPoint(0, 4)
        self._blend_mode = QPainter.CompositionMode.CompositionMode_Multiply

    def set_radius(self, radius: int):
        self._radius = radius
        self.update()

    def set_color(self, color: QColor):
        self._color = color
        self.update()

    def set_offset(self, x: int, y: int):
        self._offset = QPoint(x, y)
        self.update()

    def draw(self, painter: QPainter):
        source = self.sourcePixmap(Qt.CoordinateSystem.DeviceCoordinates)
        if source.isNull():
            return

        # Configurar modo de mezcla
        painter.setCompositionMode(self._blend_mode)

        # Aplicar efecto de sombra
        for i in range(1, 5):
            offset = QPoint(
                self._offset.x() * i/4,
                self._offset.y() * i/4
            )
            alpha = self._color.alpha() / i
            painter.drawPixmap(
                offset, 
                source, 
                source.rect().translated(-offset)
            )
            painter.setOpacity(alpha / 255.0)

        # Dibujar el elemento original
        painter.setCompositionMode(Qt.BlendMode.SourceOver)
        painter.drawPixmap(QPoint(0, 0), source)

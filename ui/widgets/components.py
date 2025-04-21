from PyQt6.QtWidgets import QPushButton, QFrame, QLabel, QVBoxLayout
from PyQt6.QtGui import QIcon, QPainter, QColor
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt, QSize

class IconButton(QPushButton):
    """Botón con icono SVG y efecto hover profesional"""
    
    def __init__(self, icon_path: str, text: str = "", parent=None):
        super().__init__(parent)
        self._icon_path = icon_path
        self._setup_ui(text)
        
    def _setup_ui(self, text: str):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Layout personalizado
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(8, 8, 8, 8)
        self.layout().setSpacing(4)
        
        # Icono SVG
        self.icon_widget = QSvgWidget(self._icon_path)
        self.icon_widget.setFixedSize(24, 24)
        self.layout().addWidget(self.icon_widget, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Texto
        if text:
            self.label = QLabel(text)
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.label.setStyleSheet("font-size: 12px; color: inherit;")
            self.layout().addWidget(self.label)
            
    def setActive(self, state: bool):
        """Cambia el estilo cuando está activo"""
        color = "#407BFF" if state else "gray"
        self.icon_widget.load(self._icon_path.replace("#000000", color))

class CardWidget(QFrame):
    """Contenedor tipo tarjeta con sombra y bordes redondeados"""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self._setup_ui(title)
        
    def _setup_ui(self, title: str):
        self.setStyleSheet("""
            CardWidget {
                background: var(--color-card-bg);
                border: 1px solid var(--color-border);
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                font-size: 16px;
                font-weight: 600;
                color: var(--color-primary);
                margin-bottom: 8px;
            """)
            layout.addWidget(title_label)
            
        self.content_layout = QVBoxLayout()
        layout.addLayout(self.content_layout)
        
        self.setLayout(layout)

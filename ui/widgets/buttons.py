from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QPainter
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt, QSize

class IconButton(QPushButton):
    def __init__(self, icon_path: str, text: str = "", parent=None):
        super().__init__(parent)
        self.icon_path = icon_path
        self._setup_ui(text)
        
    def _setup_ui(self, text: str):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            IconButton {
                background: transparent;
                border: none;
                padding: 8px;
            }
            IconButton:hover {
                background: #00000010;
                border-radius: 4px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # Icono SVG
        self.icon = QSvgWidget(self.icon_path)
        self.icon.setFixedSize(24, 24)
        layout.addWidget(self.icon, 0, Qt.AlignmentFlag.AlignHCenter)
        
        # Texto
        if text:
            self.label = QLabel(text)
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.label.setStyleSheet("font-size: 12px; color: #2d3436;")
            layout.addWidget(self.label)
            
        self.setLayout(layout)
        
    def set_icon(self, new_path: str):
        self.icon.load(new_path)


class FloatingButton(QPushButton):
     def __init__(self, icon_path: str, parent=None):
        super().__init__(parent)
        self._setup_ui(icon_path)
 
     def _setup_ui(self, icon_path: str):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(48, 48)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(24, 24))
        self.setStyleSheet("""
            FloatingButton {
                background: #407BFF;
                border-radius: 24px;
                border: none;
            }
            FloatingButton:hover {
                background: #3060D0;
            }
            FloatingButton:pressed {
                background: #2040A0;
            }
        """)

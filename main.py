# main.py
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import sys
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)    
    app.setWindowIcon(QIcon("resources/icons/logo.ico"))

    # === Cargar estilos ===
    with open("resources/estilos.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())




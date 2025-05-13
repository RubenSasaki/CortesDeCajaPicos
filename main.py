# main.py
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from PyQt6.QtGui import QIcon
import sys,os


if __name__ == "__main__":
    app = QApplication(sys.argv)    
    app.setWindowIcon(QIcon("resources/icons/logo.ico"))

    # === Cargar estilos ===

    if getattr(sys, 'frozen', False):
        # Ejecutable compilado
        base_path = sys._MEIPASS
    else:
        # En modo desarrollo
        base_path = os.path.abspath(".")

    ruta_estilos = os.path.join(base_path, "resources", "estilos.qss")
    with open(ruta_estilos, "r") as f:
        app.setStyleSheet(f.read())


    window = MainWindow()
    window.show()
    sys.exit(app.exec())




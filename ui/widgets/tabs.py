from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHeaderView,QLabel

class RevisionGeneralTab(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        # Tabla de ejemplo
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Forma Pago", "Corte", "Revisión", "Diferencia"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.table)
        self.setLayout(layout)

class DepositsTab(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Fecha", "Movimiento", "Importe", "Cuenta", "Estatus"])
        layout.addWidget(self.table)
        self.setLayout(layout)

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Generador de Reportes (En desarrollo)"))
        self.setLayout(layout)

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QSplitter
from PyQt6.QtCore import Qt
from ui.components import crear_tabla, crear_panel_con_titulo

class RevisionGeneralTab(QWidget):
    def __init__(self):
        super().__init__()

        # === Tablas Superiores ===
        self.facturas = crear_tabla(["Forma de Pago", "Total"])
        self.notas = crear_tabla(["Forma de Pago", "Total"])
        self.cobranza = crear_tabla(["Forma de Pago", "Total"])
        self.devoluciones = crear_tabla(["Forma de Pago", "Total"])

        top_layout = QHBoxLayout()
        top_layout.addWidget(crear_panel_con_titulo("Facturas", self.facturas))
        top_layout.addWidget(crear_panel_con_titulo("Notas", self.notas))
        top_layout.addWidget(crear_panel_con_titulo("Cobranza", self.cobranza))
        top_layout.addWidget(crear_panel_con_titulo("Devoluciones", self.devoluciones))

        top_widget = QWidget()
        top_widget.setLayout(top_layout)

        # === Tablas Inferiores ===
        self.resumen = crear_tabla(["Forma de Pago", "Total Corte", "Total Revisión", "Diferencia"])
        self.corte = crear_tabla(["Forma de Pago", "Importe"])

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(crear_panel_con_titulo("Comprobación de Diferencias", self.resumen,mostrar_boton=False), 2)
        bottom_layout.addWidget(crear_panel_con_titulo("Corte de Caja", self.corte), 1)

        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_layout)
        bottom_widget.setMinimumHeight(500)
        bottom_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # === Split vertical 50/50 ===
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(top_widget)
        splitter.addWidget(bottom_widget)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)

        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

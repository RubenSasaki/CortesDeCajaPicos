from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QSplitter,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt
from ui.components import crear_tabla, crear_panel_con_titulo

class RevisionGeneralTab(QWidget):
    def __init__(self):
        super().__init__()

        self.facturas = crear_tabla(["Forma de Pago", "Total"])
        self.notas = crear_tabla(["Forma de Pago", "Total"])
        self.cobranza = crear_tabla(["Forma de Pago", "Total"])
        self.devoluciones = crear_tabla(["Forma de Pago", "Total"])
        self.resumen = crear_tabla(["Forma de Pago", "Total Corte", "Total Revisión", "Diferencia"])
        self.corte = crear_tabla(["Forma de Pago", "Importe"])

        top_layout = QHBoxLayout()
        top_layout.addWidget(crear_panel_con_titulo("Facturas", self.facturas))
        top_layout.addWidget(crear_panel_con_titulo("Notas", self.notas))
        top_layout.addWidget(crear_panel_con_titulo("Cobranza", self.cobranza))
        top_layout.addWidget(crear_panel_con_titulo("Devoluciones", self.devoluciones))

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(crear_panel_con_titulo("Comprobación de Diferencias", self.resumen), 2)
        bottom_layout.addWidget(crear_panel_con_titulo("Corte de Caja", self.corte), 1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        content_widget = QWidget()
        content_widget.setLayout(main_layout)

        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        final_layout = QVBoxLayout()
        final_layout.addWidget(scroll)
        self.setLayout(final_layout)

# ui/corte_z_tab.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame, QTableWidgetItem
from ui.components import crear_tabla, crear_panel_con_titulo


class CorteZTab(QWidget):
    def __init__(self):
        super().__init__()

        # Diccionario de tablas por sección
        self.tablas = {
            "apertura": crear_tabla(["Movimiento", "FormaCobro", "Apertura"]),
            "movimientos": crear_tabla(["Movimiento", "Concepto", "Cobro", "Agente"]),
            "corte": crear_tabla(["FormaCobro", "Corte"]),
            "diferencia": crear_tabla(["Concepto", "Valor"]),
            "ventas_credito": crear_tabla(["Agente", "AgenteNombre", "Credito"])
        }

        # Layout interno sin scroll individual
        content_layout = QVBoxLayout()
        for nombre, tabla in self.tablas.items():
            titulo = nombre.replace("_", " ").title()
            panel = crear_panel_con_titulo(titulo, tabla, mostrar_boton=False)
            content_layout.addWidget(panel)

        content_widget = QWidget()
        content_widget.setLayout(content_layout)

        # Scroll general para toda la pestaña
        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def actualizar_tablas(self, columnas, datos):
        campos = {
            "apertura": ["Movimiento", "FormaCobro", "Apertura"],
            "movimientos": ["Movimiento", "Concepto", "Cobro", "Agente"],
            "corte": ["FormaCobro", "Corte"],
            "diferencia": ["Concepto", "DiFSobrantes"],
            "ventas_credito": ["Agente", "AgenteNombre", "Credito"]
        }

        for seccion, tabla in self.tablas.items():
            tabla.setRowCount(0)
            indices = [columnas.index(campo) for campo in campos[seccion] if campo in columnas]
            for fila in datos.get(seccion, []):
                row_idx = tabla.rowCount()
                tabla.insertRow(row_idx)
                for col_idx, pos in enumerate(indices):
                    valor = fila[pos] if fila[pos] is not None else ""
                    tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(valor)))

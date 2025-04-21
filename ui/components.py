# ui/components.py
from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, QGroupBox,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication
)
from PyQt6.QtCore import Qt

def crear_tabla(encabezados):
    tabla = QTableWidget()
    tabla.setColumnCount(len(encabezados))
    tabla.setHorizontalHeaderLabels(encabezados)
    tabla.verticalHeader().setVisible(False)
    tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
    tabla.setAlternatingRowColors(True)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # Hacer que seleccione todo al hacer clic una vez
    original_event = tabla.mousePressEvent

    def mouse_press_override(event):
        if event.button() == Qt.MouseButton.LeftButton:
            tabla.selectAll()
        original_event(event)

    tabla.mousePressEvent = mouse_press_override

    return tabla

def crear_panel_con_titulo(titulo, tabla):
    box = QGroupBox()
    layout = QVBoxLayout()

    # Título + botón copiar
    top = QHBoxLayout()
    lbl = QLabel(f"<b>{titulo}</b>")
    btn = QPushButton("Copiar")
    btn.setFixedSize(70, 25)
    btn.clicked.connect(lambda: copiar_tabla_al_portapapeles(tabla))

    top.addWidget(lbl)
    top.addStretch()
    top.addWidget(btn)

    layout.addLayout(top)
    layout.addWidget(tabla)
    box.setLayout(layout)
    return box

def copiar_tabla_al_portapapeles(tabla: QTableWidget):
    texto = ""
    for fila in range(tabla.rowCount()):
        valores = []
        for col in range(tabla.columnCount()):
            item = tabla.item(fila, col)
            valores.append(item.text() if item else "")
        texto += "\t".join(valores) + "\n"
    QApplication.clipboard().setText(texto.strip())



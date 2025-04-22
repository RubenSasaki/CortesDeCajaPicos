# ui/components.py
from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, QGroupBox,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication
)
from PyQt6.QtCore import Qt

from PyQt6.QtGui import QIcon

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

def crear_panel_con_titulo(titulo, contenido_widget, mostrar_boton=True):
    from PyQt6.QtWidgets import QPushButton, QLabel

    box = QGroupBox()
    layout = QVBoxLayout()

    top = QHBoxLayout()
    lbl = QLabel(f"<b>{titulo}</b>")
    top.addWidget(lbl)
    top.addStretch()

    if mostrar_boton:
        btn = QPushButton("")        
        btn.setIcon(QIcon("resources/icons/copy.svg"))
        btn.setFixedSize(70, 25)
        btn.setObjectName("secundario")
        btn.clicked.connect(lambda: copiar_tabla_al_portapapeles(contenido_widget))
        top.addWidget(btn)

    layout.addLayout(top)
    layout.addWidget(contenido_widget)
    box.setLayout(layout)
    return box


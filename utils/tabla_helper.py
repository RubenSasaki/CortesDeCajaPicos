# utils/tabla_helper.py
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QApplication


def cargar_tabla(tabla: QTableWidget, datos: list[tuple]):
    tabla.setRowCount(0)
    for row_idx, fila in enumerate(datos):
        tabla.insertRow(row_idx)
        for col_idx, valor in enumerate(fila):
            tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(valor)))


def copiar_tabla_al_portapapeles(tabla: QTableWidget):
    texto = ""
    for fila in range(tabla.rowCount()):
        valores = []
        for col in range(tabla.columnCount()):
            item = tabla.item(fila, col)
            valores.append(item.text() if item else "")
        texto += "\t".join(valores) + "\n"
    QApplication.clipboard().setText(texto.strip())



# ui/main_window.py
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox, QDateEdit,
    QVBoxLayout, QHBoxLayout, QTabWidget, QTableWidgetItem, QMainWindow, QHeaderView,QSizePolicy,QGroupBox
)
from PyQt6.QtCore import QDate,Qt
from PyQt6.QtGui import QColor

from ui.revision_general_tab import RevisionGeneralTab
from ui.corte_z_tab import CorteZTab

from services.consulta_service import (
    obtener_facturas, obtener_notas, obtener_cobranza, obtener_devoluciones, obtener_corte, obtener_depositos
)
from services.resumen_service import calcular_resumen
from utils.tabla_helper import cargar_tabla
from config.fondos import get_fondo_fijo
from reports.exportador_excel import exportar_reporte
from ui.components import crear_tabla, crear_panel_con_titulo
from services.fondos import fondos
from services.validaciones import validar_deposito_fondo

from services.consulta_service import obtener_corte_z

SUCURSALES = {
    "01MATRIZ": "1",
    "02IXCOTEL": "2",
    "03SERRANO": "3",
    "04MONTOYA": "4",
    "05RIVERAS": "5",
    "06FERRO": "6",
    "07RIOS": "7",
    "08VOLCANES": "8",
    "09XOXO": "9"
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Revisión de Cortes y Depósitos")
        self.setGeometry(100, 100, 1200, 800)

        # === Widgets principales ===
        self.sucursal_combo = QComboBox()
        self.sucursal_combo.addItems([
            "-- Seleccione --", "01MATRIZ", "02IXCOTEL", "03SERRANO", "04MONTOYA",
            "05RIVERAS", "06FERRO", "07RIOS", "08VOLCANES", "09XOXO"
        ])
        self.sucursal_combo.currentIndexChanged.connect(self.consultar)


        self.fecha_edit = QDateEdit()
        self.fecha_edit.setDate(QDate.currentDate())
        self.fecha_edit.setCalendarPopup(True)
        
        self.btn_hoy = QPushButton("Hoy")
        self.btn_hoy.setObjectName("secundario")
        self.btn_hoy.clicked.connect(lambda: self.fecha_edit.setDate(QDate.currentDate()))

        self.consultar_btn = QPushButton("Consultar")
        self.consultar_btn.clicked.connect(self.consultar)

        # === Layout de controles superiores ===
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Fecha:"))
        top_layout.addWidget(self.fecha_edit)
        top_layout.addWidget(self.btn_hoy)
        top_layout.addSpacing(20)
        top_layout.addWidget(QLabel("Sucursal:"))
        top_layout.addWidget(self.sucursal_combo)        
        top_layout.addStretch()
        top_layout.addWidget(self.consultar_btn)

        top_container = QGroupBox("Filtros") # título encima de la card
        top_container.setLayout(top_layout)
        top_container.setObjectName("Filtros") # para el estilo QSS

        # === Tabs principales ===

        self.tabs = QTabWidget()

        self.revision_tab = RevisionGeneralTab()
        self.tabs.addTab(self.revision_tab, "Revisión General")

        self.corte_z_tab = CorteZTab()
        self.tabs.addTab(self.corte_z_tab, "Corte Z")

        self.deposito_tab = self.crear_tab_depositos()
        self.tabs.addTab(self.deposito_tab, "Depósito Caja")


        # === Pestaña de Reportes ===
        reporte_widget = QWidget()
        reporte_layout = QVBoxLayout()
        reporte_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Estilo visual de contenedor
        contenedor = QWidget()
        contenedor.setFixedWidth(300)
        contenedor_layout = QVBoxLayout()
        contenedor_layout.setSpacing(20)

        # Reporte único por ahora
        btn_general = QPushButton("Reporte General del Día")
        btn_general.setMinimumHeight(40)
        btn_general.clicked.connect(self.generar_reporte)

        contenedor_layout.addWidget(btn_general)        
        contenedor_layout.addWidget(QPushButton("Reporte de XYZ"))

        contenedor.setLayout(contenedor_layout)

        reporte_layout.addWidget(contenedor)
        reporte_widget.setLayout(reporte_layout)
        self.tabs.addTab(reporte_widget, "Reportes")


        # === Layout principal ===
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_container)
        main_layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.showMaximized()

    def consultar(self):
        sucursal_nombre = self.sucursal_combo.currentText()
        if sucursal_nombre == "-- Seleccione --":
            return

        #sucursal_id = str(self.sucursal_combo.currentIndex())
        
        sucursal_id = SUCURSALES.get(sucursal_nombre, "0")

        cuenta = sucursal_nombre
        fecha_qdate = self.fecha_edit.date()
        fecha_str = fecha_qdate.toString("yyyy/MM/dd")

        funciones_consulta = {
            'facturas': obtener_facturas,
            'notas': obtener_notas,
            'cobranza': obtener_cobranza,
            'devoluciones': obtener_devoluciones,
            'corte': obtener_corte
        }

        # === Cargar tablas ===
        cargar_tabla(self.revision_tab.facturas, funciones_consulta['facturas'](fecha_str, sucursal_id, cuenta))
        cargar_tabla(self.revision_tab.notas, funciones_consulta['notas'](fecha_str, sucursal_id, cuenta))
        cargar_tabla(self.revision_tab.cobranza, funciones_consulta['cobranza'](fecha_str, sucursal_id, cuenta))
        cargar_tabla(self.revision_tab.devoluciones, funciones_consulta['devoluciones'](fecha_str, sucursal_id, cuenta))
        cargar_tabla(self.revision_tab.corte, funciones_consulta['corte'](fecha_str, sucursal_id))

        # === Depósitos ===
        depositos = obtener_depositos(fecha_str, sucursal_id)

        self.tabla_generales.setRowCount(0)
        self.tabla_origen.setRowCount(0)
        self.tabla_operacion.setRowCount(0)

        config_fondo = fondos.get(sucursal_nombre, {})

        for i, fila in enumerate(depositos):
            self.tabla_generales.insertRow(i)
            self.tabla_origen.insertRow(i)
            self.tabla_operacion.insertRow(i)

            # Validar contra fondo fijo esperado
            validaciones = validar_deposito_fondo(fila, config_fondo)

            # === TABLA 1: Generales
            for j in range(4):
                self.tabla_generales.setItem(i, j, QTableWidgetItem(str(fila[j])))

            # === TABLA 2: Origen
            for j in range(4, 8):
                item = QTableWidgetItem(str(fila[j]))
                if j == 4 and config_fondo:  # Cuenta Origen
                    item.setBackground(QColor("#CCFFCC") if validaciones[0] else QColor("#FFCCCC"))
                if j == 5 and config_fondo:  # Cuenta Desc
                    item.setBackground(QColor("#CCFFCC") if validaciones[1] else QColor("#FFCCCC"))
                self.tabla_origen.setItem(i, j - 4, item)

            # === TABLA 3: Operación
            for j in range(8, 13):
                item = QTableWidgetItem(str(fila[j]))
                if j == 8 and config_fondo:  # Importe
                    item.setBackground(QColor("#CCFFCC") if validaciones[2] else QColor("#FFCCCC"))
                if j == 9 and config_fondo:  # Forma Pago
                    item.setBackground(QColor("#CCFFCC") if validaciones[3] else QColor("#FFCCCC"))
                if j == 12 and config_fondo:  # Estatus
                    item.setBackground(QColor("#CCFFCC") if validaciones[4] else QColor("#FFCCCC"))
                self.tabla_operacion.setItem(i, j - 8, item)
        


        # === Resumen ===
        fondo_fijo = get_fondo_fijo(sucursal_nombre)
        formas = [
            "Cheque", "Efectivo", "Fondo Fijo", "No Aplica",
            "Tarjeta Banamex Crédito", "Tarjeta Banamex Débito",
            "Tarjeta Bancomer Crédito", "Tarjeta Bancomer Débito",
            "Transferencia Banamex", "Transferencia Bancomer", "Transferencia HSBC"
        ]

        resumen = calcular_resumen(fecha_str, sucursal_id, cuenta, fondo_fijo, formas, funciones_consulta)
        tabla = self.revision_tab.resumen
        tabla.setRowCount(0)

        for i, (forma, corte, revision, diferencia) in enumerate(resumen):
            tabla.insertRow(i)
            tabla.setItem(i, 0, QTableWidgetItem(forma))
            tabla.setItem(i, 1, QTableWidgetItem(f"{corte:,.2f}"))
            tabla.setItem(i, 2, QTableWidgetItem(f"{revision:,.2f}"))

            item_dif = QTableWidgetItem(f"{diferencia:,.2f}")
            if abs(diferencia) > 0.005:
                item_dif.setBackground(QColor("#FFCCCC"))
                item_dif.setForeground(QColor("red"))
            tabla.setItem(i, 3, item_dif)

        # === Depósitos ===
        depositos = obtener_depositos(fecha_str, sucursal_id)
        tabla = self.tabs.widget(1).findChild(type(self.revision_tab.facturas))
        cargar_tabla(tabla, depositos)

        
        # === Corte Z ===
        try:
            print("==== TEST: CORTE Z ====")
            resultado = obtener_corte_z(fecha_str, sucursal_id)

            if not resultado:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(self, "Sin datos", "No se encontraron datos del Corte Z para la fecha y sucursal seleccionadas.")
                return

            columnas = resultado.get("columnas", [])
            datos = resultado.get("datos", {})
            self.corte_z_tab.actualizar_tablas(columnas, datos)

        except Exception as e:
            print(f"[ERROR Corte Z] {e}")




        # === Ajustar tamaño de tablas ===

    def crear_tab_depositos(self):
        from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

        # TABLA 1 - Datos Generales
        tabla_generales = QTableWidget()
        tabla_generales.setColumnCount(4)
        tabla_generales.setHorizontalHeaderLabels(["Movimiento", "Folio", "Fecha", "Tipo de Cambio"])        
        tabla_generales.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tabla_generales.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


        # TABLA 2 - Cuenta / Origen
        tabla_origen = QTableWidget()
        tabla_origen.setColumnCount(4)
        tabla_origen.setHorizontalHeaderLabels(["Cuenta Origen", "Cuenta Desc", "Origen", "Origen ID"])
        tabla_origen.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tabla_origen.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


        # TABLA 3 - Operación
        tabla_operacion = QTableWidget()
        tabla_operacion.setColumnCount(5)
        tabla_operacion.setHorizontalHeaderLabels(["Importe", "Forma Pago", "Referencia", "Moneda", "Estatus"])
        tabla_operacion.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tabla_operacion.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Guardamos las referencias para llenar desde consultar()
        self.tabla_generales = tabla_generales
        self.tabla_origen = tabla_origen
        self.tabla_operacion = tabla_operacion

        # Layout vertical para las 3 tablas
        layout = QVBoxLayout()
        layout.addWidget(crear_panel_con_titulo("Datos Generales", tabla_generales, mostrar_boton=False))
        layout.addWidget(crear_panel_con_titulo("Cuenta / Origen", tabla_origen, mostrar_boton=False))
        layout.addWidget(crear_panel_con_titulo("Datos de Operación", tabla_operacion, mostrar_boton=False))


        widget = QWidget()
        widget.setLayout(layout)        
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return widget





    def generar_reporte(self):
        fecha = self.fecha_edit.date().toString("yyyy/MM/dd")
        sucursales = [
            "01MATRIZ", "02IXCOTEL", "03SERRANO", "04MONTOYA",
            "05RIVERAS", "06FERRO", "07RIOS", "08VOLCANES", "09XOXO"
        ]

        def obtener_datos(sucursal):
            idx = sucursales.index(sucursal) + 1
            cuenta = sucursal
            funciones_consulta = {
                'facturas': obtener_facturas,
                'notas': obtener_notas,
                'cobranza': obtener_cobranza,
                'devoluciones': obtener_devoluciones,
                'corte': obtener_corte
            }
            return {
                "facturas": funciones_consulta['facturas'](fecha, str(idx), cuenta),
                "notas": funciones_consulta['notas'](fecha, str(idx), cuenta),
                "cobranza": funciones_consulta['cobranza'](fecha, str(idx), cuenta),
                "devoluciones": funciones_consulta['devoluciones'](fecha, str(idx), cuenta),
                "corte": funciones_consulta['corte'](fecha, str(idx)),
                "resumen": calcular_resumen(fecha, str(idx), cuenta, get_fondo_fijo(sucursal), [
                    "Cheque", "Efectivo", "Fondo Fijo", "No Aplica",
                    "Tarjeta Banamex Crédito", "Tarjeta Banamex Débito",
                    "Tarjeta Bancomer Crédito", "Tarjeta Bancomer Débito",
                    "Transferencia Banamex", "Transferencia Bancomer", "Transferencia HSBC"
                ], funciones_consulta)
            }

        ruta = exportar_reporte(fecha, sucursales, obtener_datos)
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Reporte Generado", f"Archivo guardado en:\n{ruta}")



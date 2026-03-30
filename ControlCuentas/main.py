import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QPushButton, 
    QLabel, QLineEdit, QFrame, QHeaderView, QAbstractItemView,
    QInputDialog, QMessageBox, QDialog, QFormLayout, QDialogButtonBox,
    QDoubleSpinBox, QDateEdit, QScrollArea, QComboBox, QCompleter, QMenu
)
from PySide6.QtCore import Qt, QDate, QRect, QBuffer, QIODevice
from PySide6.QtGui import QIcon, QAction, QPixmap, QPainter, QFont, QColor, QBrush
import pandas as pd
from datetime import datetime
from database import DatabaseManager
from styles import get_main_style

class AddClientDialog(QDialog):
    def __init__(self, parent=None, communities=[]):
        super().__init__(parent)
        self.setWindowTitle("Mi Libro Digital - Nuevo Cliente")
        self.setFixedWidth(400)
        self.setStyleSheet(get_main_style())
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        title = QLabel("📝 Registrar Cliente")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #38bdf8; margin-bottom: 10px;")
        main_layout.addWidget(title)
        
        form_container = QFrame()
        form_layout = QFormLayout(form_container)
        form_layout.setSpacing(15)
        
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre completo")
        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Ej. 809-000-0000")
        
        self.comunidad_input = QComboBox()
        self.comunidad_input.setEditable(True)
        self.comunidad_input.addItem("Sin Comunidad")
        self.comunidad_input.addItems(communities)
        
        form_layout.addRow("Nombre:", self.nombre_input)
        form_layout.addRow("Teléfono:", self.telefono_input)
        form_layout.addRow("Comunidad:", self.comunidad_input)
        
        main_layout.addWidget(form_container)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.setStyleSheet("QPushButton { padding: 10px; }")
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        main_layout.addWidget(self.buttons)
        
    def get_data(self):
        return (self.nombre_input.text(), self.telefono_input.text(), 
                self.comunidad_input.currentText())

class TransactionDialog(QDialog):
    def __init__(self, parent=None, title="Registrar", is_credit=True, data=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedWidth(350)
        self.setStyleSheet(get_main_style())
        
        layout = QFormLayout(self)
        
        self.monto_input = QDoubleSpinBox()
        self.monto_input.setRange(0, 1000000)
        self.monto_input.setPrefix("$ ")
        from PySide6.QtWidgets import QAbstractSpinBox
        self.monto_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Descripción...")
        
        if data:
            self.date_input.setDate(QDate.fromString(data[2][:10], "yyyy-MM-dd"))
            self.monto_input.setValue(data[3] if is_credit else data[4])
            self.desc_input.setText(data[5])
        
        layout.addRow("Fecha:", self.date_input)
        layout.addRow("Monto:", self.monto_input)
        layout.addRow("Descripción:", self.desc_input)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addRow(self.buttons)
        
    def get_data(self):
        return self.monto_input.value(), self.desc_input.text(), self.date_input.date().toString("yyyy-MM-dd")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Libro Digital - Control de Cuentas")
        self.resize(1100, 750)
        
        # Base Path
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Conexión DB
        self.db = DatabaseManager()
        
        # Icono
        icon_path = os.path.join(self.base_dir, "icono.ico")
        self.setWindowIcon(QIcon(icon_path))
        
        # UI Principal
        self.init_ui()
        self.load_clients()
        
        # Aplicar Estilos
        self.setStyleSheet(get_main_style())

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Barra Lateral (Sidebar) ---
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        
        title_label = QLabel("Mi Libro Digital")
        title_label.setObjectName("Title")
        sidebar_layout.addWidget(title_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar cliente...")
        self.search_input.textChanged.connect(self.load_clients)
        sidebar_layout.addWidget(self.search_input)
        
        self.combo_comunidad = QComboBox()
        self.combo_comunidad.addItem("Todas")
        self.combo_comunidad.currentIndexChanged.connect(self.load_clients)
        sidebar_layout.addWidget(self.combo_comunidad)
        
        self.clients_list = QListWidget()
        self.clients_list.itemClicked.connect(self.on_client_selected)
        sidebar_layout.addWidget(self.clients_list)
        
        btn_add_client = QPushButton("+ Agregar Cliente")
        btn_add_client.setObjectName("BtnSuccess")
        btn_add_client.clicked.connect(self.add_client)
        sidebar_layout.addWidget(btn_add_client)
        
        btn_export_all = QPushButton("📊 Exportar Excel")
        btn_export_all.setStyleSheet("background-color: #334155; color: white;")
        btn_export_all.clicked.connect(self.export_client_excel)
        sidebar_layout.addWidget(btn_export_all)
        
        main_layout.addWidget(sidebar)
        
        # --- Contenedor de Scroll para el Contenido Principal ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(30)
        
        scroll_area.setWidget(content_frame)
        main_layout.addWidget(scroll_area)
        
        # Encabezado (Header)
        header_layout = QHBoxLayout()
        header_text_layout = QVBoxLayout()
        
        self.lbl_client_name = QLabel("Seleccione un cliente")
        self.lbl_client_name.setStyleSheet("font-size: 32px; font-weight: 800; color: #f8fafc;")
        
        self.lbl_client_phone = QLabel("")
        self.lbl_client_phone.setObjectName("UserPhone")
        
        header_text_layout.addWidget(self.lbl_client_name)
        header_text_layout.addWidget(self.lbl_client_phone)
        header_layout.addLayout(header_text_layout)
        header_layout.addStretch()
        content_layout.addLayout(header_layout)
        
        # Tarjetas de Resumen (Cards)
        cards_layout = QHBoxLayout()
        
        self.card_balance = self.create_card("SALDO PENDIENTE", "$ 0.00", "#f87171")
        self.card_deuda = self.create_card("Créditos Totales", "$ 0.00", "#94a3b8")
        self.card_pagado = self.create_card("Pagos Registrados", "$ 0.00", "#34d399")
        
        cards_layout.addWidget(self.card_balance)
        cards_layout.addWidget(self.card_deuda)
        cards_layout.addWidget(self.card_pagado)
        content_layout.addLayout(cards_layout)
        
        # Acciones de Transacción
        actions_layout = QHBoxLayout()
        btn_credit = QPushButton("💳 Registrar Crédito")
        btn_credit.clicked.connect(lambda: self.add_transaction(is_credit=True))
        
        btn_payment = QPushButton("💰 Registrar Pago")
        btn_payment.setObjectName("BtnSuccess")
        btn_payment.clicked.connect(lambda: self.add_transaction(is_credit=False))
        
        btn_delete_client = QPushButton("Eliminar Cliente")
        btn_delete_client.setObjectName("BtnDelete")
        btn_delete_client.clicked.connect(self.delete_client)
        
        actions_layout.addWidget(btn_credit)
        actions_layout.addWidget(btn_payment)
        actions_layout.addStretch()
        actions_layout.addWidget(btn_delete_client)
        content_layout.addLayout(actions_layout)
        
        # Filtros de Fecha
        filter_panel = QFrame()
        filter_panel.setObjectName("FilterPanel")
        filter_layout = QHBoxLayout(filter_panel)
        filter_layout.setContentsMargins(15, 10, 15, 10)
        
        lbl_f = QLabel("Filtrar Historia — Desde:")
        lbl_f.setStyleSheet("font-weight: bold; color: #94a3b8;")
        filter_layout.addWidget(lbl_f)
        
        self.date_start = QDateEdit()
        self.date_start.setCalendarPopup(True)
        self.date_start.setDate(QDate.currentDate().addYears(-1)) # Un año atrás para que vean datos
        self.date_start.dateChanged.connect(self.refresh_data)
        filter_layout.addWidget(self.date_start)
        
        filter_layout.addWidget(QLabel("Hasta:"))
        self.date_end = QDateEdit()
        self.date_end.setCalendarPopup(True)
        self.date_end.setDate(QDate.currentDate())
        self.date_end.dateChanged.connect(self.refresh_data)
        filter_layout.addWidget(self.date_end)
        
        btn_reset_dates = QPushButton("Ver Todo")
        btn_reset_dates.setFixedWidth(100)
        btn_reset_dates.setStyleSheet("background-color: #334155; color: white; font-size: 11px;")
        btn_reset_dates.clicked.connect(self.reset_filters)
        filter_layout.addWidget(btn_reset_dates)
        filter_layout.addStretch()
        
        content_layout.addWidget(filter_panel)
        
        # Tabla de Historial
        table_container = QFrame()
        table_container.setObjectName("TableContainer")
        table_container.setMinimumHeight(400) # Garantiza visibilidad en cualquier resolución
        table_vbox = QVBoxLayout(table_container)
        table_vbox.setContentsMargins(10, 10, 10, 10) # Espacio interno para que respire
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Fecha", "Crédito", "Pago", "Descripción"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setShowGrid(True)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.history_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_table.customContextMenuRequested.connect(self.show_context_menu)
        
        table_vbox.addWidget(self.history_table)
        
        # --- Barra de Acciones de Fila (NUEVO) ---
        row_actions_layout = QHBoxLayout()
        self.btn_edit_row = QPushButton("✏️ Editar Registro")
        self.btn_edit_row.setObjectName("BtnRowAction")
        self.btn_edit_row.setStyleSheet("background-color: #334155; color: white;")
        self.btn_edit_row.clicked.connect(self.edit_selected_row)
        
        self.btn_del_row = QPushButton("🗑️ Eliminar")
        self.btn_del_row.setObjectName("BtnRowAction")
        self.btn_del_row.setStyleSheet("background-color: #334155; color: white;")
        self.btn_del_row.clicked.connect(self.delete_selected_row)
        
        self.btn_receipt_row = QPushButton("🖼️ Generar Recibo (Imagen)")
        self.btn_receipt_row.setObjectName("BtnSuccess")
        self.btn_receipt_row.clicked.connect(self.share_receipt)
        
        row_actions_layout.addWidget(self.btn_edit_row)
        row_actions_layout.addWidget(self.btn_del_row)
        row_actions_layout.addStretch()
        row_actions_layout.addWidget(self.btn_receipt_row)
        
        table_vbox.addLayout(row_actions_layout)
        content_layout.addWidget(table_container)
        
        # Eliminar el addStretch anterior que causaba problemas de altura infinita

    def create_card(self, label, value, color):
        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        
        lbl_text = QLabel(label)
        lbl_text.setObjectName("CardLabel")
        
        lbl_val = QLabel(value)
        lbl_val.setObjectName("CardValue")
        lbl_val.setStyleSheet(f"color: {color};")
        
        layout.addWidget(lbl_text)
        layout.addWidget(lbl_val)
        
        # Guardar referencia al label del valor para actualizarlo luego
        if "PENDIENTE" in label: self.lbl_val_balance = lbl_val
        elif "Créditos" in label: self.lbl_val_deuda = lbl_val
        elif "Pagos" in label: self.lbl_val_pagado = lbl_val
        
        return card

    # --- Lógica de Clientes ---
    def load_clients(self):
        self.clients_list.clear()
        busqueda = self.search_input.text()
        comunidad = self.combo_comunidad.currentText()
        
        clientes = self.db.obtener_clientes(busqueda, comunidad)
        for c in clientes:
            item = QListWidgetItem(c[1])  # Nombre
            item.setData(Qt.UserRole, c[0]) # ID
            item.setData(Qt.UserRole + 1, c[2]) # Teléfono
            item.setData(Qt.UserRole + 2, c[3]) # Comunidad
            self.clients_list.addItem(item)
        
        # Actualizar lista de comunidades en el combo
        self.combo_comunidad.blockSignals(True)
        current = self.combo_comunidad.currentText()
        self.combo_comunidad.clear()
        self.combo_comunidad.addItem("Todas")
        self.combo_comunidad.addItems(self.db.obtener_comunidades())
        self.combo_comunidad.setCurrentText(current)
        self.combo_comunidad.blockSignals(False)

    def add_client(self):
        comunidades = self.db.obtener_comunidades()
        dialog = AddClientDialog(self, comunidades)
        if dialog.exec():
            nombre, telefono, comunidad = dialog.get_data()
            if nombre:
                self.db.agregar_cliente(nombre, telefono, comunidad)
                self.load_clients()

    def delete_client(self):
        current_item = self.clients_list.currentItem()
        if not current_item: return
        res = QMessageBox.question(self, "Confirmar", "¿Eliminar cliente y todo su historial?", 
                                 QMessageBox.Yes | QMessageBox.No)
        if res == QMessageBox.Yes:
            self.db.eliminar_cliente(current_item.data(Qt.UserRole))
            self.load_clients()
            self.lbl_client_name.setText("Seleccione un cliente")
            self.lbl_client_phone.setText("")
            self.clear_data()

    def on_client_selected(self, item):
        self.current_client_id = item.data(Qt.UserRole)
        phone = item.data(Qt.UserRole + 1)
        comun = item.data(Qt.UserRole + 2)
        
        # Mostrar nombre limpio y comunidad abajo
        self.lbl_client_name.setText(item.text())
        self.lbl_client_phone.setText(f"📍 {comun or 'Sin Comunidad'}   |   📞 {phone or 'Sin teléfono'}")
        self.refresh_data()

    # --- Lógica de Transacciones ---
    def refresh_data(self):
        if not hasattr(self, 'current_client_id'): return
        d_start = self.date_start.date().toString("yyyy-MM-dd")
        d_end = self.date_end.date().toString("yyyy-MM-dd")
        
        cred, pago, bal = self.db.obtener_saldos_cliente(self.current_client_id)
        self.lbl_val_balance.setText(f"$ {bal:,.2f}")
        self.lbl_val_deuda.setText(f"$ {cred:,.2f}")
        self.lbl_val_pagado.setText(f"$ {pago:,.2f}")
        
        historial = self.db.obtener_historial_cliente(self.current_client_id, d_start, d_end)
        self.history_table.setRowCount(0)
        from PySide6.QtWidgets import QTableWidgetItem
        for row, move in enumerate(historial):
            self.history_table.insertRow(row)
            self.history_table.setItem(row, 0, QTableWidgetItem(str(move[0])[:10]))
            
            c_item = QTableWidgetItem(f"$ {move[1]:,.2f}")
            c_item.setForeground(Qt.red if move[1] > 0 else Qt.gray)
            self.history_table.setItem(row, 1, c_item)
            
            p_item = QTableWidgetItem(f"$ {move[2]:,.2f}")
            p_item.setForeground(Qt.green if move[2] > 0 else Qt.gray)
            self.history_table.setItem(row, 2, p_item)
            
            desc_item = QTableWidgetItem(move[3])
            desc_item.setData(Qt.UserRole, move[4]) # ID del movimiento
            self.history_table.setItem(row, 3, desc_item)

    def add_transaction(self, is_credit=True):
        if not hasattr(self, 'current_client_id'): return
        dialog = TransactionDialog(self, "Registrar Crédito" if is_credit else "Registrar Pago")
        if dialog.exec():
            monto, desc, fecha = dialog.get_data()
            if monto > 0:
                if is_credit: self.db.registrar_movimiento(self.current_client_id, monto_credito=monto, descripcion=desc, fecha=fecha)
                else: self.db.registrar_movimiento(self.current_client_id, monto_pago=monto, descripcion=desc, fecha=fecha)
                self.refresh_data()

    def show_context_menu(self, pos):
        # Seleccionar la fila bajo el cursor
        row = self.history_table.rowAt(pos.y())
        if row < 0: return
        
        self.history_table.selectRow(row)
        mid_item = self.history_table.item(row, 3)
        if not mid_item: return
        mid = mid_item.data(Qt.UserRole)
        
        menu = QMenu(self)
        edit_act = QAction("✏️ Editar Registro", self)
        del_act = QAction("🗑️ Eliminar Fila", self)
        share_act = QAction("🖼️ Generar Recibo (Imagen)", self)
        
        menu.addAction(edit_act)
        menu.addAction(del_act)
        menu.addSeparator()
        menu.addAction(share_act)
        
        # Usar viewport() para que la posición sea relativa al área visible de la tabla
        action = menu.exec(self.history_table.viewport().mapToGlobal(pos))
        if action == edit_act: self.edit_transaction(mid)
        elif action == del_act: self.delete_transaction(mid)
        elif action == share_act: self.share_receipt()

    def edit_selected_row(self):
        row = self.history_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona una fila de la tabla primero.")
            return
        mid = self.history_table.item(row, 3).data(Qt.UserRole)
        self.edit_transaction(mid)

    def delete_selected_row(self):
        row = self.history_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona una fila de la tabla primero.")
            return
        mid = self.history_table.item(row, 3).data(Qt.UserRole)
        self.delete_transaction(mid)

    def edit_transaction(self, mid):
        move = self.db.obtener_movimiento(mid)
        is_credit = move[3] > 0
        dialog = TransactionDialog(self, "Editar Registro", is_credit, move)
        if dialog.exec():
            monto, desc, fecha = dialog.get_data()
            if is_credit: self.db.actualizar_movimiento(mid, monto, 0, desc, fecha)
            else: self.db.actualizar_movimiento(mid, 0, monto, desc, fecha)
            self.refresh_data()

    def delete_transaction(self, mid):
        if QMessageBox.question(self, "Confirmar", "¿Eliminar este registro?") == QMessageBox.Yes:
            self.db.eliminar_movimiento(mid)
            self.refresh_data()

    def share_receipt(self):
        if not hasattr(self, 'current_client_id'): return
        cred, pago, bal = self.db.obtener_saldos_cliente(self.current_client_id)
        name = self.lbl_client_name.text() # Nombre limpio sin comunidad
        
        img = self.generate_receipt_image(name, cred, pago, bal)
        path = os.path.join(self.base_dir, f"recibo_{name[:10].strip()}.png")
        img.save(path)
        QMessageBox.information(self, "Recibo Generado", f"Se ha guardado el recibo como imagen:\n{path}\nYa puedes enviarlo por WhatsApp.")

    def generate_receipt_image(self, name, total_cred, total_pago, balance):
        pix = QPixmap(400, 480)
        pix.fill(QColor("#0f172a"))
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        
        # Fondo sutil
        p.setBrush(QBrush(QColor("#1e293b")))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(10, 10, 380, 460, 25, 25)
        
        # Título
        p.setPen(QColor("#38bdf8"))
        p.setFont(QFont("Segoe UI", 18, QFont.Bold))
        p.drawText(QRect(0, 50, 400, 40), Qt.AlignCenter, "ESTADO DE CUENTA")
        
        # Nombre del Cliente
        p.setPen(Qt.white)
        p.setFont(QFont("Segoe UI", 16, QFont.Medium))
        p.drawText(QRect(20, 120, 360, 40), Qt.AlignCenter, name)
        
        # Caja de Saldo Pendiente (Enfocada)
        p.setBrush(QBrush(QColor("#0f172a")))
        p.drawRoundedRect(50, 180, 300, 140, 15, 15)
        
        p.setPen(QColor("#f87171"))
        p.setFont(QFont("Segoe UI", 42, QFont.Bold))
        p.drawText(QRect(50, 205, 300, 70), Qt.AlignCenter, f"$ {balance:,.2f}")
        
        p.setPen(QColor("#94a3b8"))
        p.setFont(QFont("Segoe UI", 11))
        p.drawText(QRect(50, 275, 300, 30), Qt.AlignCenter, "SALDO ACTUAL PENDIENTE")
        
        # Footer
        p.setPen(QColor("#38bdf8"))
        p.setFont(QFont("Segoe UI", 12, QFont.Bold))
        p.drawText(QRect(0, 380, 400, 30), Qt.AlignCenter, "Mi Libro Digital")
        
        p.setPen(QColor("#64748b"))
        p.setFont(QFont("Segoe UI", 9))
        p.drawText(QRect(0, 420, 400, 30), Qt.AlignCenter, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        p.end()
        return pix

    def export_client_excel(self):
        if not hasattr(self, 'current_client_id'):
            QMessageBox.warning(self, "Aviso", "Selecciona un cliente para exportar.")
            return
        
        name = self.lbl_client_name.text()
        historial = self.db.obtener_historial_cliente(self.current_client_id)
        df = pd.DataFrame(historial, columns=["Fecha", "Crédito", "Pago", "Descripción", "ID"])
        df = df.drop(columns=["ID"])
        
        path = os.path.join(self.base_dir, f"Reporte_{name[:15].replace(' ','_')}.xlsx")
        df.to_excel(path, index=False)
        QMessageBox.information(self, "Exportación Exitosa", f"Datos exportados a:\n{path}")

    def reset_filters(self):
        f_min = self.db.obtener_fecha_minima()
        self.date_start.setDate(QDate.fromString(f_min, "yyyy-MM-dd"))
        self.date_end.setDate(QDate.currentDate())
        self.refresh_data()

    def clear_data(self):
        self.lbl_val_deuda.setText("$ 0.00")
        self.lbl_val_pagado.setText("$ 0.00")
        self.lbl_val_balance.setText("$ 0.00")
        self.history_table.setRowCount(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

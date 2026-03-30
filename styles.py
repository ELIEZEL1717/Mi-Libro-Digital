def get_main_style():
    return """
    QMainWindow {
        background-color: #0f172a;
    }
    
    QFrame#Sidebar {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    
    QLabel {
        color: #f1f5f9;
        font-family: 'Segoe UI Variable', 'Segoe UI', sans-serif;
    }
    
    QLabel#Title {
        font-size: 28px;
        font-weight: 800;
        color: #38bdf8;
        padding: 10px 0px 30px 0px;
    }
    
    QLineEdit {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 12px 15px;
        color: #f1f5f9;
        font-size: 14px;
    }
    
    QLineEdit:focus {
        border: 2px solid #38bdf8;
    }
    
    QListWidget {
        background-color: transparent;
        border: none;
        outline: none;
        color: #94a3b8;
        font-size: 15px;
    }
    
    QListWidget::item {
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 8px;
    }
    
    QListWidget::item:selected {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38bdf8, stop:1 #0ea5e9);
        color: #0f172a;
        font-weight: bold;
    }
    
    QListWidget::item:hover:!selected {
        background-color: #334155;
        color: #f1f5f9;
    }
    
    /* --- TABLA RE-DISEÑADA --- */
    QTableWidget {
        background-color: #1e293b;
        alternate-background-color: #1a2333;
        gridline-color: #334155;
        border: 1px solid #334155;
        border-radius: 15px;
        color: #f8fafc;
        font-size: 14px;
        outline: none; /* Eliminar borde de enfoque de Windows */
    }
    
    QTableWidget::item {
        padding: 12px;
        border: none;
    }
    
    QTableWidget::item:selected {
        background-color: rgba(56, 189, 248, 40); /* Azul suave translúcido */
        color: #f8fafc;
    }
    
    QHeaderView::section {
        background-color: #334155;
        color: #94a3b8;
        padding: 12px;
        border-right: 1px solid #1e293b;
        border-bottom: 2px solid #38bdf8;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 11px;
    }
    
    QFrame#TableContainer {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 1px; /* Para mostrar el borde de la tabla contenido */
    }
    
    QPushButton {
        background-color: #38bdf8;
        color: #0f172a;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 14px;
    }
    
    QPushButton:hover {
        background-color: #7dd3fc;
    }
    
    QPushButton#BtnDelete {
        background-color: transparent;
        border: 1px solid #ef4444;
        color: #ef4444;
        font-size: 11px;
    }
    
    QPushButton#BtnDelete:hover {
        background-color: #ef4444;
        color: white;
    }

    QPushButton#BtnSuccess {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);
        color: white;
    }

    QFrame#Card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 24px;
        padding: 25px;
    }
    
    QLabel#CardValue {
        font-size: 34px;
        font-weight: 800;
        margin-top: 5px;
    }
    
    QLabel#CardLabel {
        color: #64748b;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    QLabel#UserPhone {
        color: #38bdf8;
        font-size: 16px;
        font-weight: 600;
    }
    
    QDateEdit {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 10px 15px;
        color: #f1f5f9;
        font-size: 14px;
        font-weight: 500;
    }
    
    QDateEdit::drop-down {
        width: 0px;
        image: none;
    }
    
    QComboBox {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 10px 15px;
        color: #f1f5f9;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 30px;
    }
    
    QComboBox QAbstractItemView {
        background-color: #1e293b;
        color: #f1f5f9;
        selection-background-color: #38bdf8;
        border: 1px solid #334155;
        padding: 5px;
    }
    
    QMenu {
        background-color: #1a2333;
        color: #f1f5f9;
        border: 1px solid #38bdf8;
        border-radius: 12px;
        padding: 8px;
    }
    
    QMenu::item {
        padding: 10px 30px;
        border-radius: 8px;
        font-size: 13px;
        margin: 2px;
    }
    
    QMenu::item:selected {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38bdf8, stop:1 #0ea5e9);
        color: #0f172a;
        font-weight: bold;
    }
    
    QDialog {
        background-color: #0f172a;
        border: 1px solid #334155;
    }
    
    QFormLayout { padding: 20px; }
    
    QFrame#FilterPanel {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 15px;
    }
    
    QScrollArea {
        background-color: transparent;
        border: none;
    }
    
    QScrollBar:vertical {
        background: transparent;
        width: 10px;
        margin: 0px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #1e293b;
        min-height: 20px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #334155;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
        height: 0px;
    }
    """

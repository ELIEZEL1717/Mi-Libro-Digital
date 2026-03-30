import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path=None):
        if not db_path:
            # Forzar ruta siempre dentro de la carpeta del script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, "data", "cuentas.db")
            
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()
        self._migrar_db()

    def create_tables(self):
        # Tabla de Clientes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                comunidad TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Tabla de Movimientos (Créditos y Pagos)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                monto_credito REAL DEFAULT 0,
                monto_pago REAL DEFAULT 0,
                descripcion TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE
            )
        ''')
        self.connection.commit()

    def _migrar_db(self):
        try:
            self.cursor.execute("ALTER TABLE clientes ADD COLUMN comunidad TEXT")
            self.connection.commit()
        except:
            pass

    # --- Métodos de Clientes ---
    def agregar_cliente(self, nombre, telefono="", comunidad=""):
        self.cursor.execute("INSERT INTO clientes (nombre, telefono, comunidad) VALUES (?, ?, ?)", 
                           (nombre, telefono, comunidad))
        self.connection.commit()
        return self.cursor.lastrowid

    def obtener_clientes(self, busqueda="", comunidad=""):
        sql = "SELECT id, nombre, telefono, comunidad FROM clientes WHERE nombre LIKE ?"
        params = [f"%{busqueda}%"]
        if comunidad and comunidad != "Todas":
            sql += " AND comunidad = ?"
            params.append(comunidad)
        
        sql += " ORDER BY nombre"
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def obtener_comunidades(self):
        self.cursor.execute("SELECT DISTINCT comunidad FROM clientes WHERE comunidad IS NOT NULL AND comunidad != ''")
        return [c[0] for c in self.cursor.fetchall()]

    def eliminar_cliente(self, cliente_id):
        self.cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        self.connection.commit()

    # --- Métodos de Movimientos ---
    def registrar_movimiento(self, cliente_id, monto_credito=0, monto_pago=0, descripcion="", fecha=None):
        if not fecha:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.cursor.execute('''
            INSERT INTO movimientos (cliente_id, monto_credito, monto_pago, descripcion, fecha)
            VALUES (?, ?, ?, ?, ?)
        ''', (cliente_id, monto_credito, monto_pago, descripcion, fecha))
        self.connection.commit()

    def obtener_movimiento(self, mid):
        self.cursor.execute("SELECT * FROM movimientos WHERE id = ?", (mid,))
        return self.cursor.fetchone()

    def actualizar_movimiento(self, mid, monto_credito, monto_pago, descripcion, fecha):
        self.cursor.execute('''
            UPDATE movimientos SET monto_credito=?, monto_pago=?, descripcion=?, fecha=?
            WHERE id=?
        ''', (monto_credito, monto_pago, descripcion, fecha, mid))
        self.connection.commit()

    def eliminar_movimiento(self, mid):
        self.cursor.execute("DELETE FROM movimientos WHERE id = ?", (mid,))
        self.connection.commit()

    def obtener_historial_cliente(self, cliente_id, fecha_inicio=None, fecha_fin=None):
        sql = '''
            SELECT fecha, monto_credito, monto_pago, descripcion, id 
            FROM movimientos 
            WHERE cliente_id = ? 
        '''
        params = [cliente_id]
        
        if fecha_inicio:
            sql += " AND date(fecha) >= date(?)"
            params.append(fecha_inicio)
        if fecha_fin:
            sql += " AND date(fecha) <= date(?)"
            params.append(fecha_fin)
            
        sql += " ORDER BY fecha DESC"
        
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def obtener_saldos_cliente(self, cliente_id):
        self.cursor.execute('''
            SELECT SUM(monto_credito), SUM(monto_pago) 
            FROM movimientos 
            WHERE cliente_id = ?
        ''', (cliente_id,))
        res = self.cursor.fetchone()
        creditos = res[0] if res[0] else 0
        pagos = res[1] if res[1] else 0
        return creditos, pagos, (creditos - pagos)

    def obtener_fecha_minima(self):
        self.cursor.execute("SELECT MIN(fecha) FROM movimientos")
        res = self.cursor.fetchone()
        if res and res[0]:
            return res[0][:10] # Retorna solo YYYY-MM-DD
        return "2000-01-01" 

    def cerrar(self):
        self.connection.close()

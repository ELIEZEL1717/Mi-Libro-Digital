# Mi Libro Digital - Control de Cuentas y Deudas 📚

**Mi Libro Digital** es una aplicación de escritorio diseñada para reemplazar el cuaderno físico de cobros por una herramienta digital moderna y profesional. Está enfocada en dueños de negocios o prestamistas que necesitan llevar control de créditos y pagos de clientes.e

## 🚀 Características Principales

* **Gestión de Clientes**
  Permite registrar clientes con nombre, teléfono y comunidad.

* **Control de Deudas Automático**
  Calcula automáticamente el saldo pendiente restando los pagos de los créditos otorgados.

* **Organización por Comunidad**
  Permite agrupar y filtrar clientes por comunidad para organizar mejor los cobros.

* **Registro de Movimientos**
  Historial detallado de créditos y pagos con fechas y descripciones personalizadas.

* **Generación de Recibos**
  Crea recibos digitales profesionales para compartir con los clientes.

* **Exportación a Excel**
  Permite exportar reportes detallados de clientes en formato `.xlsx`.

* **Modo Oscuro**
  Interfaz moderna y cómoda para uso prolongado.

## 🛠️ Tecnologías Usadas

* Python 3.10+
* PySide6 (Qt for Python)
* SQLite
* Pandas
* OpenPyXL

## 📦 Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/mi-libro-digital.git
cd mi-libro-digital
```

### 2. Instalar dependencias

```bash
pip install pyside6 pandas openpyxl
```

### 3. Ejecutar la aplicación

```bash
python main.py
```

## 🔒 Privacidad y Datos

Todos los datos se guardan localmente en la carpeta `data/` dentro del archivo `cuentas.db`.
La aplicación no envía información a internet, garantizando la privacidad de los datos.

---

Desarrollado para digitalizar y modernizar el control de cuentas y deudas.

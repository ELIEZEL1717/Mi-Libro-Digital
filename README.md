# Mi Libro Digital - Control de Cuentas y Deudas 📚

**Mi Libro Digital** es una aplicación de escritorio diseñada para transformar el cuaderno físico de cobros en una herramienta digital robusta y profesional. Está enfocada en dueños de negocios o prestamistas que necesitan un control estricto de créditos y pagos de clientes.

![Vista Previa](.assets/vista_previa.png)

## 🚀 Características Principales

- **Gestión de Clientes**: Registra clientes con nombre, teléfono y comunidad.
- **Control de Deudas Inteligente**: Calcula automáticamente el **Saldo Pendiente** restando los pagos de los créditos otorgados.
- **Organización Geográfica**: Agrupa y filtra a tus clientes por **Comunidad** para organizar mejor tus rutas de cobro.
- **Registro de Movimientos**: Historial detallado de créditos y pagos con descripciones personalizadas.
- **Recibos Digitales en Imagen**: Genera recibos elegantes (estilo App Treinta) para enviar por WhatsApp en un solo clic.
- **Exportación a Excel**: Saca reportes detallados de cada cliente en archivos `.xlsx`.
- **Modo Oscuro Premium**: Interfaz moderna, rápida y descansada para la vista.

## 📸 Recibos Profesionales
La app genera automáticamente una imagen limpia que puedes compartir con tus clientes para recordarles su deuda de forma profesional:

![Ejemplo Recibo](.assets/recibo.png)

## 🛠️ Tecnologías Usadas
- **Python 3.10+**
- **PySide6** (Qt for Python) para la interfaz gráfica.
- **SQLite** para una base de datos local ligera y segura.
- **Pandas** para la exportación de reportes.

## 📦 Instalación y Uso

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/mi-libro-digital.git
   cd mi-libro-digital
   ```

2. **Instalar dependencias**:
   ```bash
   pip install pyside6 pandas openpyxl
   ```

3. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

## 🔒 Privacidad y Datos
Todos los datos se guardan localmente en la carpeta `data/` dentro de un archivo `cuentas.db`. La aplicación no envía información a la nube, garantizando la total privacidad de tus clientes.

---
*Desarrollado con ❤️ para digitalizar negocios locales.*

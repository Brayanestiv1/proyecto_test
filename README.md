# Procesador de Archivos TXT a JSON/CSV con Django

Este proyecto fue desarrollado como parte de una **prueba técnica** para convertir archivos de texto plano con formato de **ancho fijo** a los formatos **JSON**, **CSV** y luego **insertarlos en una base de datos** usando **Django**.

---

## 📂 Estructura del Proyecto

```
proyecto_test/
├── procesador/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   ├── utils.py
│   │   ├── views.py
│   │   ├── models.py
│   │   └── urls.py
│   ├── procesador/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
├── pruebas/
│   └── PRUEBA_20250129.txt
├── salida.csv
├── salida.json
```

---

## 🌐 Requisitos Previos

- Python 3.11 instalado
- Entorno virtual activado (`python -m venv venv` + `venv\Scripts\activate`)
- Django instalado en el entorno:

```bash
pip install django
```

---

## ✅ Proceso Paso a Paso

### 1. Crear el Proyecto Django

```bash
cd Desktop
django-admin startproject procesador
cd procesador
python manage.py startapp core
```

### 2. Registrar la app `core` en `INSTALLED_APPS`:

```python
# procesador/settings.py
INSTALLED_APPS = [
    ...
    'core',
]
```

### 3. Implementar los siguientes archivos:

- `core/parser.py`: lectura y conversión del archivo
- `core/utils.py`: inserción en la base de datos
- `core/views.py`: endpoint que procesa todo
- `core/models.py`: definición del modelo `Registro`

### 4. Crear las migraciones y aplicar:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Probar el proyecto

Iniciar el servidor:

debes estar en la ruta /proyecto_test/procesador para que funcione

```bash
python manage.py runserver
```

Enviar petición:

```bash
curl -X POST http://127.0.0.1:8000/procesar/ \
  -H "Content-Type: application/json" \
  -d "{\"archivo\": \"PRUEBA_20250129.txt\"}"
```

---

## 🔍 Explicación Técnica

### Estructura del archivo TXT

- Se dividieron las líneas en bloques de **1615 caracteres**.
- Se extrajeron campos usando intervalos fijos según el PDF:

```python
INTERVALOS = [
  (0,10), (10,13), (13,28), (28,128), ..., (625,1615)
]
```

### Salidas Generadas

- `salida.csv`: con las columnas definidas en el PDF
- `salida.json`: con todos los registros en formato legible
- Base de datos (`db.sqlite3`) con tabla `core_registro`

---

## 🚀 Endpoint API

**POST** `/procesar/`

### Body (JSON):

```json
{
  "archivo": "PRUEBA_20250129.txt"
}
```

### Respuesta esperada:

```json
{
  "archivo": "PRUEBA_20250129.txt",
  "csv": "salida.csv",
  "json": "salida.json",
  "registros_procesados": 34,
  "registros_insertados": 34,
  "estado": "OK"
}
```

---

## 🔧 Tecnologías Usadas

- Python 3.11
- Django 5.2.4
- SQLite3 (por defecto)
- curl (para pruebas)

---

## 🔗 Observaciones Finales

- No se implementaron vistas ni templates, ya que el proyecto es **100% backend**.
- No se asumieron reglas adicionales fuera del PDF.
- El sistema está diseñado para funcionar sobre el archivo `PRUEBA_20250129.txt`, con estructura fija.

---

## 🚩 Autor

Brayan Vera

---

¡Proyecto completo y funcional! 🚀


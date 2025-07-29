# Imagen base oficial
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo el archivo de dependencias primero (para aprovechar caché)
COPY requirements.txt .

# Instala dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Expone el puerto de desarrollo de Django
EXPOSE 8000

# Comando por defecto para ejecutar el servidor
CMD ["python", "procesador/manage.py", "runserver", "0.0.0.0:8000"]

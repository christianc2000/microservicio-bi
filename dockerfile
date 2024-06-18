# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el contenido del directorio actual al directorio de trabajo en el contenedor
COPY . .

# Especificar el comando para ejecutar la aplicación
# Suponiendo que tu aplicación se ejecuta con un archivo app.py
CMD ["python", "app.py"]

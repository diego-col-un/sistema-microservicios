# 1. Imagen oficial de Python (version "slim" para ahorrrar espacio)
FROM python:3.12-slim

# 2. Variables de entorno: Evitar archivos .pyc y fuerza logs directos a la consola
ENV PYTHONDONTWRITENBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Dependencias del sistema para conectar con Postgres/MySQL
RUN apt-get update && apt-get install -y gcc libpq-dev default-libmysqlclient-dev pkg-config && rm -rf /var/lib/apt/lists/*

# 4. Directorio de trabajo
WORKDIR /app

# 5. COpiamos primero el archivo de requisitos (buena practica para cache)
COPY requirements.txt .

# 6. Instalamos las librerias de python
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copiamos el resto del codigo 
COPY . .

# 8. Comando Escucha en 0.0.0.0 para ser visible en la red de Docker
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


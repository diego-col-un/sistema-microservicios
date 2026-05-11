# 1. Python base 
FROM python:3.11-slim

# 2. Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Librerias para MySQL 
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc pkg-config && rm -rf /var/lib/apt/lists/*

# 4. Instalacion de dependecias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el codigo
COPY . .

# 6. COmando de ejecucion
CMD ["python", "app.py"]

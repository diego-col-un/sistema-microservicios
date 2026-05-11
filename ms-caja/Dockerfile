# 1. Imagen oficial de Node (LTS) sobre Alpine
FROM node:20-alpine

# 2. Carpeta de la app
WORKDIR /app

# 3. Copiamos los archivos de gestion de paquetes
COPY package*.json ./

# 4. Instalamos solo dependencias de produccion 
RUN npm install --only=production

# 5. Copiamos el codigo 
COPY . .

#6. Exponer el puerto
EXPOSE 8003

# 7. COmando de arranque
CMD ["node", "index.js"]
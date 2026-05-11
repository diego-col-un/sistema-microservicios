# 1. Imagen base oficial de PHP con Alpine Linux (ligera)
FROM php:8.3-fpm-alpine

# 2. Instalacion de librerias del sistema necesaria para extensiones
RUN apk add --no-cache git curl libpng-dev libxml2-dev zip unzip sqlite-dev

# 3. Instalacion de extensiones de PHP que laravel requiere para funcionar
RUN docker-php-ext-install pdo_sqlite bcmatch

# 4. Copiamos el ejecutable de Composer desde su imagen oficial (Multi-stage build)
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# 5. Definimos el directorio de trabajo dentro del contenedor
WORKDIR /var/www

# 6. Copiamos todo el contenido del proyecto al contenedor
COPY . .

# 7. Ejecutamos composer para instalar las librerias de PHP
RUN composer install --no-dev --optimize-autoloader

# 8. Ajustamos permisos para que laravel pueda escribir en logs y base de datos
RUN chown -R www-data:www-data /var/www/storage /var/www/database

# 9. Informamos que el contenedor usará el puerto 8000
EXPOSE 8000

#10. Comando para iniciar el servidor
CMD php artisan serve --host=0.0.0.0 --port=8000
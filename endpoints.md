# Endpoints del Sistema — Referencia Rápida
Base URL: `http://localhost:8000`
Headers requeridos siempre:
```
Accept: application/json
Content-Type: application/json
Authorization: Bearer <token>   ← solo en endpoints con Auth
```

---

## Auth

### POST /api/auth/register — Registrar usuario (sin auth)
```json
{
  "name": "Diego Aristizábal",
  "email": "diego1@test.com",
  "password": "password123",
  "password_confirmation": "password123",
  "security_question": "¿Cuál es el nombre de tu mascota?",
  "security_answer": "Firulais"
}
```

### POST /api/auth/login — Iniciar sesión (sin auth)
```json
{
  "email": "diego1@test.com",
  "password": "password123"
}
```

### POST /api/auth/logout — Cerrar sesión (con auth)
```
Body vacío
```

### GET /api/auth/me — Usuario actual (con auth)
```
Sin body
```

### POST /api/auth/obtener-pregunta — Obtener pregunta secreta (sin auth)
```json
{
  "email": "diego1@test.com"
}
```

### POST /api/auth/reset-password — Resetear contraseña (sin auth)
```json
{
  "email": "diego1@test.com",
  "security_answer": "Firulais",
  "password": "nuevapassword123",
  "password_confirmation": "nuevapassword123"
}
```

---

## Reservas

### GET /api/reservas/ — Listar reservas (con auth)
```
Sin body
```

### POST /api/reservas/ — Crear reserva (con auth)
```json
{
  "cliente_nombre": "Diego Aristizábal",
  "cliente_email": "diego1@test.com",
  "cliente_telefono": "3001234567",
  "vehiculo_placa": "ABC123",
  "vehiculo_marca": "Toyota",
  "vehiculo_modelo": "Corolla",
  "descripcion": "Cambio de aceite",
  "fecha_reserva": "2026-04-10T10:00:00"
}
```

### GET /api/reservas/:id/ — Obtener reserva (con auth)
```
Sin body — reemplazar :id por el id numérico, ej: /api/reservas/2/
```

### PUT /api/reservas/:id/ — Actualizar reserva (con auth)
```json
{
  "cliente_nombre": "Diego Aristizábal",
  "cliente_email": "diego1@test.com",
  "cliente_telefono": "3001234567",
  "vehiculo_placa": "ABC123",
  "vehiculo_marca": "Toyota",
  "vehiculo_modelo": "Corolla",
  "descripcion": "Cambio de aceite y filtro",
  "fecha_reserva": "2026-04-10T10:00:00"
}
```

### DELETE /api/reservas/:id/ — Eliminar reserva (con auth)
```
Sin body — reemplazar :id por el id numérico
```

### GET /api/reservas/estado/:estado/ — Filtrar por estado (con auth)
```
Sin body — estados posibles: pendiente | en_proceso | completada | cancelada
Ejemplo: /api/reservas/estado/pendiente/
```

### PUT /api/reservas/:id/estado/ — Cambiar estado (con auth)
```json
{
  "estado": "en_proceso"
}
```

---

## Repuestos

### GET /api/repuestos — Listar repuestos (con auth)
```
Sin body
```

### POST /api/repuestos — Crear repuesto (con auth)
```json
{
  "nombre": "Filtro de aceite",
  "referencia": "FA-001",
  "marca": "Bosch",
  "precio": 25000,
  "stock": 20
}
```

### GET /api/repuestos/:id — Obtener repuesto (con auth)
```
Sin body — reemplazar :id por el id numérico
```

### PUT /api/repuestos/:id — Actualizar repuesto (con auth)
```json
{
  "nombre": "Filtro de aceite",
  "referencia": "FA-001",
  "marca": "Bosch",
  "precio": 27000,
  "stock": 15
}
```

### DELETE /api/repuestos/:id — Eliminar repuesto (con auth)
```
Sin body
```

### PUT /api/repuestos/:id/stock — Actualizar stock (con auth)
```json
{
  "stock": 50
}
```

### GET /api/repuestos/stock-bajo — Repuestos bajo mínimo (con auth)
```
Sin body
```

---

## Caja

### GET /api/caja — Listar transacciones (con auth)
```
Sin body
```

### POST /api/caja — Registrar transacción (con auth)
```json
{
  "tipo": "ingreso",
  "categoria": "venta_taller",
  "descripcion": "Cambio de aceite Toyota",
  "monto": 150000,
  "usuario_id": "1"
}
```

### GET /api/caja/:id — Obtener transacción (con auth)
```
Sin body — reemplazar :id por el ObjectId de MongoDB
Ejemplo: /api/caja/69cd7feed9c87befaf399a86
```

### GET /api/caja/resumen/:fecha — Resumen del día (con auth)
```
Sin body — formato fecha: YYYY-MM-DD
Ejemplo: /api/caja/resumen/2026-04-01
```

### POST /api/caja/cierre — Cierre de caja (con auth)
```
Body vacío
```

### DELETE /api/caja/:id — Eliminar transacción (con auth)
```
Sin body — reemplazar :id por el ObjectId de MongoDB
```

---

## Menú

### GET /api/menu — Listar menú (con auth)
```
Sin body
```

### POST /api/menu — Crear item (con auth)
```json
{
  "nombre": "Perro Americano",
  "precio": 13000,
  "categoria": "Perro",
  "descripcion": "Salchicha americana, pan, tocineta, ripio, salsas"
}
```

### GET /api/menu/:id — Obtener item (con auth)
```
Sin body — reemplazar :id por el id del item
```

### PUT /api/menu/:id — Actualizar item (con auth)
```json
{
  "nombre": "Perro Americano",
  "precio": 14000,
  "categoria": "Perro",
  "descripcion": "Salchicha americana, pan, tocineta, ripio, salsas"
}
```

### DELETE /api/menu/:id — Eliminar item (con auth)
```
Sin body
```

### PUT /api/menu/:id/disponibilidad — Toggle disponibilidad (con auth)
```json
{
  "disponible": false
}
```

### GET /api/menu/categoria/:cat — Filtrar por categoría (con auth)
```
Sin body — reemplazar :cat por el nombre de la categoría
Ejemplo: /api/menu/categoria/Perro
```

---

## Empleados

### GET /api/empleados/ — Listar empleados (con auth)
```
Sin body
```

### POST /api/empleados/ — Crear empleado (con auth)
```json
{
  "nombre": "Carlos",
  "apellido": "Pérez",
  "email": "carlos2@test.com",
  "telefono": "3001234567",
  "cedula": "9876543210",
  "cargo": "mecanico",
  "area": "taller",
  "salario": 1800000,
  "fecha_ingreso": "2024-01-15"
}
```

### GET /api/empleados/:id/ — Obtener empleado (con auth)
```
Sin body — reemplazar :id por el id numérico
```

### PUT /api/empleados/:id/ — Actualizar empleado (con auth)
```json
{
  "nombre": "Carlos",
  "apellido": "Pérez",
  "email": "carlos2@test.com",
  "telefono": "3001234567",
  "cedula": "9876543210",
  "cargo": "mecanico",
  "area": "taller",
  "salario": 2000000,
  "fecha_ingreso": "2024-01-15"
}
```

### DELETE /api/empleados/:id/ — Desactivar empleado (con auth)
```
Sin body
```

### GET /api/empleados/area/:area/ — Filtrar por área (con auth)
```
Sin body — reemplazar :area por el nombre del área
Ejemplo: /api/empleados/area/taller/
```

### GET /api/empleados/nomina/ — Ver nómina total (con auth)
```
Sin body
```

## 1.  Documentación Integral de QA 
Puedes estructurar esta sección en tu informe para mostrar la trazabilidad completa del sistema:

Resumen Ejecutivo de Pruebas
Se implementó una suite de 15 tests unitarios y de integración para validar la seguridad perimetral y la integridad de los datos en una arquitectura políglota de microservicios.

A. API Gateway (Laravel) - Tests 1 al 5
Validación de Perímetro: Se confirmó que el acceso externo está protegido por Sanctum (Test 1).

Gestión de Secretos: Verificación de la existencia y estructura del GATEWAY_INTERNAL_TOKEN (Tests 2 y 4).

Orquestación: Validación de rutas de proxy hacia los microservicios y manejo de fallos/timeouts (Tests 3 y 5).

B. Microservicio de Caja (Node.js) - Tests 6 al 9
Middleware de Seguridad: Validación del bloqueo por falta de header o token incorrecto (Tests 6 y 7).

Entorno y Datos: Verificación de carga de .env y formato de respuesta JSON (Tests 8 y 9).

C. Microservicio de Repuestos (Flask/SQL) - Tests 10 y 11
Seguridad: Validación del middleware X-Gateway-Secret (Test 10).

Persistencia: Prueba de acceso exitoso a la base de datos SQLite/SQLAlchemy (Test 11).

D. Microservicio de Menú (Flask/Firebase) - Tests 12 y 13
Mocking de Firebase: Simulación de respuestas de la base de datos NoSQL para listar el catálogo (Test 12).

Consumo de Recursos: Validación de la obtención de un ítem específico por ID (Test 13).

E. Microservicio de Reservas (Django) - Tests 14 y 15
Middleware Django: Validación del flujo de denegación 403 (Test 14).

Autorización Exitosa: Confirmación de acceso mediante el secreto compartido (Test 15).

## 2. Guía de Ejecución de Tests

| Módulo | Comando | Herramienta |
|---|---|---|
| **Gateway** | `php artisan test` | PHPUnit |
| **Caja** | `npm test` | Mocha / Chai |
| **Repuestos** | `pytest test_repuestos.py` | Pytest |
| **Menú** | `pytest test_menu.py` | Pytest + Mock |
| **Reservas** | `pytest` | Pytest-Django |

## 3. Notas adicionales

Aislamiento: Los tests de los microservicios de Menú y Reservas fueron diseñados para ejecutarse de forma independiente, utilizando técnicas de Mocking y configuraciones específicas de entorno (pytest.ini) para garantizar la repetibilidad sin depender de servicios externos.

Consistencia: Todos los módulos validan el flujo de seguridad mediante el token compartido X-Gateway-Secret, asegurando la integridad de la arquitectura de microservicios planteada en la asignatura.
## 1.  Documentación Integral de QA 
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

## 🚀 Pruebas de Estrés y Carga (Stress Testing)

Para validar la resiliencia de la arquitectura políglota, se implementó una suite de pruebas utilizando **Locust**, simulando el comportamiento de usuarios concurrentes autenticados mediante el sistema de tokens (Sanctum) del API Gateway.

### 1. Matriz de Escenarios de Ejecución
Se definieron 10 configuraciones específicas para hallar los límites del sistema y la capacidad de respuesta de los microservicios:

| ID | Nombre del Test | Usuarios (Peak) | Ramp-up | Objetivo (KPI) |
| :--- | :--- | :--- | :--- | :--- |
| **ST-01** | Carga Repuestos | 50 | 2 | Estabilidad en microservicio de Inventario (Flask). |
| **ST-02** | Estrés Reservas | 150 | 5 | Validar concurrencia en microservicio de Citas (Django). |
| **ST-03** | Carga Menú | 100 | 5 | Medir persistencia y lectura en base de datos. |
| **ST-04** | Gateway Latency | 200 | 10 | Evaluación del orquestador central (Laravel). |
| **ST-05** | Caja Concurrente | 80 | 4 | Capacidad de respuesta en microservicio Financiero (Node.js). |
| **ST-06** | Security Spam | 500 | 50 | Validación de rechazo 401/403 ante peticiones sin token. |
| **ST-07** | Spike Test | 400 | 100 | Capacidad de recuperación ante aumentos súbitos de tráfico. |
| **ST-08** | Soak Test | 50 | 1 | Estabilidad de memoria en ejecución de larga duración. |
| **ST-09** | Gestión Personal | 60 | 3 | Estresar endpoint de consulta de Empleados. |
| **ST-10** | Breakpoint Test | 1000 | 20 | Punto de colapso y monitoreo de degradación. |

### 2. Resultados y Métricas Globales
Tras la ejecución de la suite completa, se consolidaron los siguientes hallazgos:

* **Tasa de Éxito:** 100% (0 fallos registrados bajo carga máxima).
* **Rendimiento (RPS):** Pico máximo de ~180 peticiones por segundo.
* **Latencia Promedio:** ~7.4 segundos en condiciones de alta concurrencia local.

### 3. Conclusiones Técnicas
1.  **Resiliencia del API Gateway:** El orquestador Laravel manejó correctamente el flujo hacia los servicios de Python y Node.js sin presentar errores de conexión.
2.  **Escalabilidad:** La arquitectura soporta el crecimiento de usuarios, aunque se identifica el hardware local como el principal cuello de botella para la latencia.
3.  **Gestión de Seguridad:** Se confirmó que el sistema protege los endpoints críticos, rechazando peticiones no autorizadas de forma eficiente bajo estrés.
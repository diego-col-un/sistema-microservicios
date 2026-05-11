from locust import HttpUser, task, between, constant
import random

class SistemaCompleto(HttpUser):
    # Entre 1 y 3 segundos para carga normal, 0 para estrés puro
    wait_time = between(0.1, 1.0) 

    def on_start(self):
        """Escenario ST-00: Autenticación obligatoria (Sanctum)"""
        response = self.client.post("/api/auth/login", json={
            "email":    "diego1@test.com",
            "password": "nueva123"
        })
        if response.status_code == 200:
            token = response.json().get('token', '')
            self.client.headers.update({
                "Authorization": f"Bearer {token}",
                "Accept":        "application/json"
            })

    # --- ESCENARIOS DE LECTURA ---
    @task(3)
    def escenario_01_03_repuestos_menu(self):
        """ST-01 y ST-03: Carga de catálogos"""
        self.client.get("/api/repuestos/", name="ST-01: Listar Repuestos")
        self.client.get("/api/menu/", name="ST-03: Listar Menú")

    @task(3)
    def escenario_09_empleados(self):
        """ST-09: Gestión de personal"""
        self.client.get("/api/empleados/", name="ST-09: Listar Empleados")

    # --- ESCENARIOS DE ESCRITURA ---
    @task(1)
    def escenario_02_reservas_post(self):
        """ST-02: Stress de inserción en Django"""
        self.client.post("/api/reservas/", json={
            "cliente_nombre":   f"User Stress {random.randint(1,1000)}",
            "cliente_email":    "test@stress.com",
            "cliente_telefono": "300000000",
            "vehiculo_placa":   "STR000",
            "vehiculo_marca":   "Tesla",
            "vehiculo_modelo":  "Model 3",
            "descripcion":      "Test de carga sostenida",
            "fecha_reserva":    "2026-05-10T10:00:00"
        }, name="ST-02: Crear Reserva")

    # --- ESCENARIOS DE FINANZAS ---
    @task(2)
    def escenario_05_caja(self):
        """ST-05: Concurrencia en microservicio Node.js"""
        self.client.get("/api/caja/", name="ST-05: Consultar Caja")

    # --- ESCENARIO DE FALLO (RESILIENCIA) ---
    @task(1)
    def escenario_06_unauthorized(self):
        """ST-06: Intento de acceso sin headers (debe dar 401/403)"""
        with self.client.get("/api/reservas/", headers={"Authorization": ""}, catch_response=True, name="ST-06: Acceso Denegado") as response:
            if response.status_code in [401, 403]:
                response.success()
from locust import HttpUser, task, between, constant

class UsuarioNormal(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
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

    @task(3)
    def listar_reservas(self):
        self.client.get("/api/reservas/")

    @task(1)
    def crear_reserva(self):
        self.client.post("/api/reservas/", json={
            "cliente_nombre":   "Cliente Test",
            "cliente_email":    "test@test.com",
            "cliente_telefono": "3001234567",
            "vehiculo_placa":   "TST001",
            "vehiculo_marca":   "Toyota",
            "vehiculo_modelo":  "Corolla",
            "descripcion":      "Prueba de carga",
            "fecha_reserva":    "2026-05-01T10:00:00"
        })

    @task(3)
    def listar_repuestos(self):
        self.client.get("/api/repuestos/")

    @task(2)
    def listar_caja(self):
        self.client.get("/api/caja/")

    @task(3)
    def listar_menu(self):
        self.client.get("/api/menu/")

    @task(2)
    def listar_empleados(self):
        self.client.get("/api/empleados/")


class UsuarioEstres(HttpUser):
    wait_time = constant(0)

    def on_start(self):
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

    @task
    def estres_reservas(self):
        self.client.get("/api/reservas/")

    @task
    def estres_repuestos(self):
        self.client.get("/api/repuestos/")

    @task
    def estres_menu(self):
        self.client.get("/api/menu/")

    @task
    def estres_caja(self):
        self.client.get("/api/caja/")
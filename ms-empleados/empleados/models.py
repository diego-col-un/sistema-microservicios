from django.db import models

class Empleado(models.Model):
    CARGO_CHOICES = [
        ('mecanico',    'Mecánico'),
        ('cajero',      'Cajero'),
        ('mesero',      'Mesero'),
        ('cocinero',    'Cocinero'),
        ('administrador', 'Administrador'),
        ('otro',        'Otro'),
    ]

    AREA_CHOICES = [
        ('taller',      'Taller'),
        ('restaurante', 'Restaurante'),
        ('ambos',       'Ambos'),
    ]

    nombre          = models.CharField(max_length=200)
    apellido        = models.CharField(max_length=200)
    email           = models.EmailField(unique=True)
    telefono        = models.CharField(max_length=20)
    cedula          = models.CharField(max_length=20, unique=True)
    cargo           = models.CharField(max_length=20, choices=CARGO_CHOICES)
    area            = models.CharField(max_length=20, choices=AREA_CHOICES)
    salario         = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ingreso   = models.DateField()
    activo          = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'empleados'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo}"
from django.db import models

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente',  'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada',  'Cancelada'),
        ('completada', 'Completada'),
    ]

    cliente_nombre  = models.CharField(max_length=200)
    cliente_email   = models.EmailField()
    cliente_telefono = models.CharField(max_length=20)
    vehiculo_placa  = models.CharField(max_length=20)
    vehiculo_marca  = models.CharField(max_length=100)
    vehiculo_modelo = models.CharField(max_length=100)
    descripcion     = models.TextField()
    estado          = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_reserva   = models.DateTimeField()
    fecha_creacion  = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reservas'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.cliente_nombre} - {self.vehiculo_placa} - {self.estado}"
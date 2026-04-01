from rest_framework import serializers
from .models import Reserva

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Reserva
        fields = '__all__'

class ReservaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Reserva
        fields = [
            'cliente_nombre', 'cliente_email', 'cliente_telefono',
            'vehiculo_placa', 'vehiculo_marca', 'vehiculo_modelo',
            'descripcion', 'fecha_reserva'
        ]
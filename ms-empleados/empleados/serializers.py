from rest_framework import serializers
from .models import Empleado

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Empleado
        fields = '__all__'

class EmpleadoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Empleado
        fields = [
            'nombre', 'apellido', 'email', 'telefono',
            'cedula', 'cargo', 'area', 'salario', 'fecha_ingreso'
        ]
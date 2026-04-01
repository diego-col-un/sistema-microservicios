from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Empleado
from .serializers import EmpleadoSerializer, EmpleadoCreateSerializer

@api_view(['GET', 'POST'])
def empleados_list(request):
    if request.method == 'GET':
        empleados  = Empleado.objects.filter(activo=True)
        serializer = EmpleadoSerializer(empleados, many=True)
        return Response({'success': True, 'data': serializer.data})

    if request.method == 'POST':
        serializer = EmpleadoCreateSerializer(data=request.data)
        if serializer.is_valid():
            empleado = serializer.save()
            return Response({
                'success': True,
                'data': EmpleadoSerializer(empleado).data
            }, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def empleado_detail(request, pk):
    try:
        empleado = Empleado.objects.get(pk=pk)
    except Empleado.DoesNotExist:
        return Response({'success': False, 'message': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response({'success': True, 'data': EmpleadoSerializer(empleado).data})

    if request.method == 'PUT':
        serializer = EmpleadoSerializer(empleado, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data})
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        empleado.activo = False
        empleado.save()
        return Response({'success': True, 'message': 'Empleado desactivado correctamente'})

@api_view(['GET'])
def empleados_por_area(request, area):
    empleados  = Empleado.objects.filter(area=area, activo=True)
    serializer = EmpleadoSerializer(empleados, many=True)
    return Response({'success': True, 'data': serializer.data})

@api_view(['GET'])
def nomina(request):
    empleados     = Empleado.objects.filter(activo=True)
    serializer    = EmpleadoSerializer(empleados, many=True)
    total_nomina  = sum(e.salario for e in empleados)
    return Response({
        'success':      True,
        'total_nomina': float(total_nomina),
        'empleados':    serializer.data
    })
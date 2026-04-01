from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Reserva
from .serializers import ReservaSerializer, ReservaCreateSerializer

# ─────────────────────────────────────────
# GET  /api/reservas/       — listar todas
# POST /api/reservas/       — crear reserva
# ─────────────────────────────────────────
@api_view(['GET', 'POST'])
def reservas_list(request):
    if request.method == 'GET':
        reservas = Reserva.objects.all()
        serializer = ReservaSerializer(reservas, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = ReservaCreateSerializer(data=request.data)
        if serializer.is_valid():
            reserva = serializer.save()
            return Response({
                'success': True,
                'data': ReservaSerializer(reserva).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# ─────────────────────────────────────────
# GET    /api/reservas/<id>/ — obtener una
# PUT    /api/reservas/<id>/ — actualizar
# DELETE /api/reservas/<id>/ — eliminar
# ─────────────────────────────────────────
@api_view(['GET', 'PUT', 'DELETE'])
def reserva_detail(request, pk):
    try:
        reserva = Reserva.objects.get(pk=pk)
    except Reserva.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Reserva no encontrada'
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReservaSerializer(reserva)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = ReservaSerializer(reserva, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        reserva.delete()
        return Response({
            'success': True,
            'message': 'Reserva eliminada correctamente'
        }, status=status.HTTP_200_OK)

# ─────────────────────────────────────────
# GET /api/reservas/estado/<estado>/
# ─────────────────────────────────────────
@api_view(['GET'])
def reservas_por_estado(request, estado):
    reservas = Reserva.objects.filter(estado=estado)
    serializer = ReservaSerializer(reservas, many=True)
    return Response({
        'success': True,
        'data': serializer.data
    }, status=status.HTTP_200_OK)

# ─────────────────────────────────────────
# PUT /api/reservas/<id>/estado/
# ─────────────────────────────────────────
@api_view(['PUT'])
def actualizar_estado(request, pk):
    try:
        reserva = Reserva.objects.get(pk=pk)
    except Reserva.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Reserva no encontrada'
        }, status=status.HTTP_404_NOT_FOUND)

    nuevo_estado = request.data.get('estado')
    estados_validos = ['pendiente', 'confirmada', 'cancelada', 'completada']

    if nuevo_estado not in estados_validos:
        return Response({
            'success': False,
            'message': f'Estado inválido. Debe ser uno de: {estados_validos}'
        }, status=status.HTTP_400_BAD_REQUEST)

    reserva.estado = nuevo_estado
    reserva.save()

    return Response({
        'success': True,
        'data': ReservaSerializer(reserva).data
    }, status=status.HTTP_200_OK)
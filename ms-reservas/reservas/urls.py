from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.reservas_list,       name='reservas-list'),
    path('<int:pk>/',               views.reserva_detail,      name='reserva-detail'),
    path('estado/<str:estado>/',    views.reservas_por_estado, name='reservas-por-estado'),
    path('<int:pk>/estado/',        views.actualizar_estado,   name='actualizar-estado'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('',              views.empleados_list,    name='empleados-list'),
    path('<int:pk>/',     views.empleado_detail,   name='empleado-detail'),
    path('area/<str:area>/', views.empleados_por_area, name='empleados-por-area'),
    path('nomina/',       views.nomina,            name='nomina'),
]
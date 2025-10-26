from django.urls import path
from . import views

app_name = 'secundarios'

urlpatterns = [
    path('mapa/', views.mapa_view, name='mapa'),
    path('login/', views.login_view, name='login'),
    path('criaConta/', views.criaConta_view, name='criaConta'),
]
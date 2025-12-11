from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'secundarios'

urlpatterns = [
    path('mapa/', views.mapa_view, name='mapa'),
    path('mapaLog/', views.mapaLog_view, name='mapaLog'),
    path('signup/', views.criaConta_view, name='criaConta'),
    path('login/', auth_views.LoginView.as_view(template_name='secundarios/login.html'), name='login'),
    path('home_conta/',views.home_conta_view, name= 'home_conta'),
    path('post/',views.post_view, name= 'post'),
    path('feed/',views.feed_view, name= 'feed'),
    path('feedLog/',views.feedLog_view, name= 'feedLog'),
    path('api/places/', views.places_api, name='places_api'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('chats/', views.chats_view, name='chats'),
    path("", views.searchf, name="busca"),
    
]
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'secundarios'

urlpatterns = [
    path('mapa/', views.mapa_view, name='mapa'),
    path('signup/', views.criaConta_view, name='criaConta'),
    path('profile/', views.perfil_view, name='perfil'),
    path('login/', auth_views.LoginView.as_view(template_name='secundarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home_conta/',views.home_conta_view, name= 'home_conta'),
    path('post/<int:post_id>',views.post_view, name= 'post'),
    path('feed/',views.feed_view, name= 'feed'),
    path('novo_post/', views.novo_post_view, name='novo_post'),
    path('api/places/', views.places_api, name='places_api'),
    path('perfil/', views.perfil_view, name='perfil'),
]
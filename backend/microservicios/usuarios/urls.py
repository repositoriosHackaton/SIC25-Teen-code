from django.urls import path
from .views import UsuarioCreateView, UsuarioListView

urlpatterns = [
    path('usuarios/', UsuarioListView.as_view(), name='listar_usuarios'),
    path('usuarios/crear/', UsuarioCreateView.as_view(), name='crear_usuario'),
]

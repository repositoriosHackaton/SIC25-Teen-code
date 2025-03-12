from rest_framework import generics
from .models import Usuario
from .serializers import UsuarioSerializer

# 📌 Crear usuario
class UsuarioCreateView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# 📌 Listar usuarios
class UsuarioListView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

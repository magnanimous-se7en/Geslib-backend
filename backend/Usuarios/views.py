from rest_framework import viewsets
from .serializers import UsuarioSerializer, PrestamoSerializer
from .models import Usuario, Prestamo


class UsuarioView(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()
    
    # El ViewSet de Django REST framework maneja automáticamente
    # todas las operaciones CRUD usando el queryset definido


class PrestamoView(viewsets.ModelViewSet):
    serializer_class = PrestamoSerializer
    queryset = Prestamo.objects.all()
    
    # El ViewSet de Django REST framework maneja automáticamente  
    # todas las operaciones CRUD usando el queryset definido




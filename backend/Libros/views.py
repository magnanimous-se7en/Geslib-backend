from rest_framework import viewsets
from .serializer import LibroSerializer
from .models import Libro


class LibroView(viewsets.ModelViewSet):
    serializer_class = LibroSerializer
    queryset = Libro.objects.all().order_by('-status', 'title')
    
    # El ViewSet de Django REST framework maneja automáticamente
    # todas las operaciones CRUD usando el queryset definido
    # Orden: prestados primero (-status), luego por título alfabéticamente

from django.apps import AppConfig


class LibrosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Libros'
    
    def ready(self):
        # Importar signals cuando la app esté lista
        import Libros.signals

from django.apps import AppConfig

class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Usuarios'

    def ready(self):
        # Importar signals cuando la app esté lista
        import Usuarios.signals

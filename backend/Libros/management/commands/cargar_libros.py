import csv
import os
from random import randint
from django.core.management.base import BaseCommand
from django.db import transaction
from Libros.models import Libro


class Command(BaseCommand):
    help = 'Cargar libros desde archivo CSV'

    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            '--file',
            type=str,
            default='data.csv',
            help='Ruta al archivo CSV (default: data.csv)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=200,
            help='Número máximo de libros a cargar (default: 200)'
        )

    def handle(self, **options):
        archivo_csv = options['file']
        limite = options['limit']
        
        if not os.path.exists(archivo_csv):
            self.stdout.write(
                self.style.ERROR(f'El archivo {archivo_csv} no existe')
            )
            return

        contador = 0
        errores = 0
        
        try:
            self.stdout.write('Usando encoding: utf-8')
            
            with open(archivo_csv, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                
                with transaction.atomic():
                    for linea in lector:
                        if contador >= limite:
                            break
                            
                        try:
                            isbn = linea['isbn10'].strip()
                            authors = linea['authors'].strip()
                            title = linea['title'].strip()
                            published_year = linea['published_year'].strip()
                            categories = linea['categories'].strip()

                            # Validar datos requeridos
                            if not all([isbn, authors, title, published_year, categories]):
                                continue

                            # Validar y convertir año
                            try:
                                year = int(float(published_year))
                            except (ValueError, TypeError):
                                continue

                            # Truncar ISBN si es muy largo
                            if len(isbn) > 8:
                                isbn = isbn[:8]
                            
                            # Verificar si el libro ya existe
                            if Libro.objects.filter(isbn=isbn).exists():
                                continue

                            # Generar fecha aleatoria
                            mes = randint(1, 12)
                            dia = randint(1, 28)
                            fecha_publicacion = f"{year}-{mes:02d}-{dia:02d}"

                            # Truncar campos si son muy largos
                            title = title[:255] if len(title) > 255 else title
                            authors = authors[:255] if len(authors) > 255 else authors
                            categories = categories[:100] if len(categories) > 100 else categories

                            # Crear el libro
                            Libro.objects.create(
                                isbn=isbn,
                                title=title,
                                author=authors,
                                gender=categories,
                                date_publication=fecha_publicacion,
                                description=linea.get('description', '').strip(),
                                status='disponible'
                            )
                            
                            contador += 1
                            if contador % 50 == 0:
                                self.stdout.write(f'Cargados {contador} libros...')

                        except Exception as e:
                            errores += 1
                            self.stdout.write(
                                self.style.WARNING(
                                    f'Error al cargar libro con ISBN {linea.get("isbn10", "N/A")}: {e}'
                                )
                            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Proceso completado: {contador} libros cargados, {errores} errores'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error general: {e}')
            )
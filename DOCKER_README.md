# GestLib - Sistema de Gestión de Biblioteca

## Requisitos previos

- Docker
- Docker Compose

## Configuración y ejecución

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd GestLib
```

### 2. Configurar variables de entorno (opcional)
El proyecto incluye un archivo `.env` preconfigurado en el directorio `backend/`. Puedes modificar las variables según tus necesidades.

### 3. Ejecutar con Docker Compose
```bash
# Navegar a la carpeta backend
cd backend

# Construir y ejecutar todos los servicios
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build
```

### 4. Acceder a la aplicación
- **Backend (Django API)**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin (usuario: admin, contraseña: admin123)

### 5. Ejecutar el frontend por separado
El frontend de React no está dockerizado. Para ejecutarlo:
```bash
cd client
npm install
npm run dev
```
- **Frontend (React)**: http://localhost:5173

### 6. Comandos útiles

```bash
# IMPORTANTE: Todos los comandos docker-compose deben ejecutarse desde la carpeta backend/
cd backend

# Ver logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Ejecutar comandos en el contenedor del backend
docker-compose exec backend python manage.py shell
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# Acceder a la base de datos PostgreSQL
docker-compose exec db psql -U gestlib_user -d gestlib_db
```

## Estructura del proyecto

```
GestLib/
├── backend/                 # Django REST API (Dockerizado)
│   ├── Dockerfile
│   ├── docker-compose.yml   # Backend + PostgreSQL
│   ├── requirements.txt
│   ├── .env
│   ├── entrypoint.sh
│   └── ...
├── client/                  # React Frontend (NO dockerizado)
│   ├── package.json
│   ├── src/
│   └── ...
```


### Reinstalar dependencias
```bash
docker-compose down
docker-compose up --build
```
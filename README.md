# SGAD – Referee Management Service

Microservicio del **SGAD (Sistema de Gestión de Árbitros y Designaciones)** encargado de la **gestión de árbitros**.  
Permite registrar árbitros, consultar su información, manejar su disponibilidad y apoyar la asignación de árbitros a partidos deportivos.

---

## 📖 Descripción

El **Referee Management Service** administra toda la información relacionada con los árbitros:  
- Registro y actualización de árbitros.  
- Consulta de la lista de árbitros disponibles.  
- Manejo de la disponibilidad y horarios de árbitros.  
- Integración con el **Match Management Service** para asignar árbitros a partidos.  

Este servicio expone **endpoints REST** que son consumidos por el **API Gateway** del sistema SGAD.

---

## 📂 Estructura del Proyecto

```
sgad-referee-management/
│── .env                  # Variables de entorno (ejemplo: URL de la base de datos)
│── requirements.txt       # Dependencias de Python
│
└── app/
    ├── __init__.py
    ├── main.py            # Punto de entrada (endpoints)
    ├── routes.py          # Rutas específicas de árbitros
    ├── database.py        # Configuración de conexión a MongoDB
    ├── models.py          # Definición de modelos
    ├── schemas.py         # Validaciones y serialización (Pydantic)
```

---

## ⚙️ Requisitos

- **Python 3.9+**
- **MongoDB** como base de datos NoSQL
- Docker (opcional, para despliegue contenerizado)

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución Local

1. Configurar las variables de entorno en un archivo `.env`:

```env
DATABASE_URL=mongodb://localhost:27017/sgad_referees
```

2. Ejecutar el servidor en modo desarrollo:

```bash
uvicorn app.main:app --reload
```

3. La API estará disponible en:

- Base URL: `http://localhost:8002`
- Documentación automática (Swagger): `http://localhost:8002/docs`

---

## 🔗 Endpoints Principales

| Método | Endpoint               | Descripción                          |
|--------|------------------------|--------------------------------------|
| GET    | `/referees`            | Listar todos los árbitros            |
| GET    | `/referees/{id}`       | Obtener información de un árbitro    |
| POST   | `/referees`            | Registrar un nuevo árbitro           |
| PUT    | `/referees/{id}`       | Actualizar datos de un árbitro       |
| DELETE | `/referees/{id}`       | Eliminar un árbitro                  |
| GET    | `/referees/available`  | Consultar árbitros disponibles       |

---

## 🐳 Despliegue con Docker

1. Crear la imagen:
```bash
docker build -t sgad-referee-management .
```

2. Ejecutar el contenedor:
```bash
docker run -d -p 8002:8000 --env-file .env sgad-referee-management
```

---

## 📡 Integración con SGAD

- Este servicio se comunica con el **API Gateway** (`sgad-api-gateway`).  
- La información de árbitros se almacena en **MongoDB** (contenedor `nosql-db` en `sgad-main`).  
- Trabaja en conjunto con el **Match Management Service** para asignar árbitros disponibles a los partidos.

---

# API RPA Empresas

## Descripción

Esta API RESTful fue desarrollada en Python usando Flask y SQLAlchemy. Es el backend de soporte para un bot de RPA que gestiona datos de empresas, permitiendo crear, consultar, actualizar estados y eliminar registros. Está documentada con Swagger y cuenta con pruebas unitarias, manejo avanzado de errores y validaciones robustas.

---

## Arquitectura

- **Lenguaje:** Python 3.13+
- **Framework:** Flask
- **Base de datos:** SQLite (se puede migrar a PostgreSQL/MySQL fácilmente)
- **ORM:** SQLAlchemy
- **Documentación:** Swagger (Flasgger)
- **Pruebas:** Pytest

### Estructura de Carpetas

```
backend-rpa/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   └── routes.py
│
├── tests/
│   └── test_routes.py
│
├── run.py
├── requirements.txt
└── README.md
```

---

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd backend-rpa
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Inicializar la base de datos

```bash
python
>>> from app import db, create_app
>>> app = create_app()
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
```

### 5. Ejecutar el servidor

```bash
python run.py
```

La API estará disponible en [http://localhost:5000](http://localhost:5000)

### 6. Acceder a la documentación Swagger

[http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)

---

## Endpoints principales

| Método | Ruta               | Descripción                                       |
|--------|--------------------|---------------------------------------------------|
| POST   | /process-data      | Crear empresa                                     |
| POST   | /update-status     | Actualizar estado de empresa                      |
| GET    | /empresas          | Listar todas las empresas                         |
| GET    | /empresa/<nit>     | Consultar empresa por NIT                         |
| DELETE | /empresa/<nit>     | Eliminar empresa por NIT                          |

---

## Pruebas

Ejecuta los tests con:

```bash
python -m pytest
```

---

## Validaciones y Manejo de Errores

- NIT debe ser numérico y tener entre 6 y 15 dígitos.
- Nombre obligatorio, no vacío.
- Campo "datos" debe ser un objeto/dict.
- Estado solo acepta "PENDIENTE", "PROCESADO" o "ERROR".
- Códigos HTTP estándar y respuestas JSON claras.
- Ante errores de usuario se retorna 400, ante recursos no encontrados 404.

---

## Decisiones técnicas y buenas prácticas

- **Modularidad:** Uso de Blueprints para separar lógica.
- **ORM:** SQLAlchemy permite migrar fácilmente de motor de base de datos.
- **Swagger:** Documentación y testing interactivo de endpoints.
- **Pruebas automáticas:** Pytest con cobertura sobre todos los endpoints y casos de error.
- **Validaciones robustas:** Todas las rutas validan datos de entrada y previenen errores comunes.
- **CRUD completo:** Integración directa y sencilla con bots RPA.

---

## Consideraciones de Escalabilidad

- Arquitectura desacoplada: La API puede crecer y migrar a motores robustos (PostgreSQL, MySQL, etc.).
- Uso de SQLAlchemy para consultas eficientes, relaciones y optimizaciones.
- Lista para despliegue en producción usando servidores WSGI como Gunicorn/Uwsgi.
- Preparada para autenticación, paginación y filtros en endpoints de consulta.
- Se puede integrar CI/CD para pruebas y despliegue automatizados.

---

## Consideraciones de Seguridad

- Nunca se exponen datos sensibles en las respuestas.
- Todas las entradas son validadas rigurosamente.
- Listo para integración de autenticación/autorización (por ejemplo, JWT).
- Se recomienda usar variables de entorno para configuración sensible en producción.
- Protege contra inyección SQL al usar ORM.

---

## Ejemplo de petición

```bash
curl -X POST http://localhost:5000/process-data \
    -H "Content-Type: application/json" \
    -d '{
        "nit": "123456789",
        "nombre": "Empresa Prueba",
        "datos": {"direccion": "Calle 123", "telefono": "1234567"}
    }'
```

---

## Mejoras y siguientes pasos recomendados

- Agregar autenticación (por ejemplo, JWT).
- Implementar paginación y filtros en los endpoints de consulta.
- Migrar a un motor de base de datos robusto para producción.
- Desplegar en la nube (Render, Railway, Heroku, etc.).
- Integrar logs avanzados y monitoreo.
- Añadir rate limiting y protección contra ataques comunes.

---

## Contacto

Camilo Ortiz  
<tu_email@dominio.com>

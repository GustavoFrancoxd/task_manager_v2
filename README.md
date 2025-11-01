# Gestor de Tareas v2

Un sistema completo de gestión de tareas desarrollado con Flask que permite a los usuarios crear, editar, eliminar y gestionar sus tareas de manera eficiente.

## 🚀 Características

- **Autenticación de usuarios**: Registro, inicio de sesión y recuperación de contraseña
- **Gestión de tareas**: Crear, editar, eliminar y cambiar estado de tareas
- **Dashboard interactivo**: Vista principal con todas las tareas del usuario
- **Historial de cambios**: Seguimiento completo de modificaciones en las tareas
- **Interfaz responsive**: Diseño adaptable con Bootstrap
- **Notificaciones por email**: Sistema de recuperación de contraseña

## 📋 Requisitos del Sistema

- Python 3.12+
- MySQL 5.7+ o MariaDB 10.3+
- Navegador web moderno

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd task_manager_v2
```

### 2. Crear entorno virtual
```bash
python -m venv venv312
```

### 3. Activar entorno virtual
```bash
# Windows
venv312\Scripts\activate

# Linux/Mac
source venv312/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar base de datos y correo
- crear variables de entorno para la base de datos
- utilizar cuenta de correo, de preferencia google, despues genenerar una llave de acceso para aplicacion
- crear las variables de entorno para el correo y otra para la llave de acceso

### 6. Ejecutar la aplicación
```bash
python main.py
```

La aplicación estará disponible en `http://localhost:5001`

## 🏗️ Estructura del Proyecto

```
task_manager_v2/
├── app/
│   ├── controllers/         # Lógica de negocio
│   ├── forms/              # Formularios WTF
│   ├── models/             # Modelos de base de datos
│   ├── routes/             # Rutas de la aplicación
│   ├── static/             # Archivos estáticos (CSS, JS, imágenes)
│   ├── templates/          # Plantillas HTML
│   └── utils/              # Utilidades (tokens, etc.)
├── venv312/                # Entorno virtual
├── main.py                 # Punto de entrada
└── requirements.txt        # Dependencias
```

## 🔧 Configuración

Edita el archivo `app/config.py` para personalizar:

- Configuración de base de datos
- Configuración de email
- Clave secreta
- Configuración del servidor

## 📖 Uso Básico

1. **Registro**: Crea una cuenta nueva
2. **Inicio de sesión**: Accede con tus credenciales
3. **Dashboard**: Ve todas tus tareas
4. **Crear tarea**: Añade nuevas tareas
5. **Gestionar tareas**: Edita, completa o elimina tareas

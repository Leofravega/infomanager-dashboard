# Barby InfoManager - BI Dashboard

Dashboard interactivo para análisis de ventas y métricas de e-commerce con carga dinámica de datos.

## 📋 Requisitos

- Python 3.8+
- pip o conda

## 🚀 Instalación Local

```bash
pip install -r requirements.txt
```

## ▶️ Ejecutar la aplicación

```bash
python src/app.py
```

La aplicación estará disponible en:
- **Local**: `http://localhost:8050`
- **Red Local**: `http://192.168.x.x:8050` (desde otro dispositivo)

## 📁 Estructura del Proyecto

```
Barby InfoManager/
├── src/
│   ├── app.py              # Aplicación principal Dash
│   ├── data_generator.py   # Cargador de datos Excel
│   └── __pycache__/        
├── uploads/                # Archivos Excel subidos (panel admin)
├── data/                   # Carpeta para datos auxiliares
├── assets/                 # CSS y recursos estáticos
├── requirements.txt        # Dependencias
├── Procfile                # Configuración para Render
├── runtime.txt             # Versión de Python para Render
├── DEPLOY.md               # Guía de despliegue en Render
└── README.md              # Este archivo
```

## 📊 Dashboards Disponibles

### 1. **Resumen Anual** 📊
- Tabla con todos los KPIs por mes
- Tarjetas de progresión anual
- Comparativa mes a mes

### 2. **Métricas Principales** 📈
- Gráficos interactivos de tendencias
- Selector de métrica
- Estadísticas (promedio, máximo, mínimo)

### 3. **Vista Mensual** 📋
- Desglose completo por mes
- Tabla ordenable

### 4. **Panel Admin** 🔐
- Carga de nuevos archivos Excel
- Regeneración automática del reporte
- Contraseña: `admin123`

## 🎨 Características

✅ Carga automática de datos desde Excel  
✅ Gráficos interactivos con Plotly  
✅ Panel admin para subir nuevos datos  
✅ Acceso desde red local  
✅ Responsive design  
✅ Formato profesional  

## 📝 Uso del Panel Admin

1. Abre la pestaña **"🔐 Admin"**
2. Ingresa la contraseña: `admin123`
3. Arrastra y suelta un archivo Excel
4. El reporte se actualiza automáticamente

## 🌐 Desplegar en Render

Ver [DEPLOY.md](DEPLOY.md) para instrucciones detalladas.

En resumen:
1. Pushea a GitHub
2. Conecta con Render
3. El dashboard está en vivo 🚀

## 📝 Notas

- El archivo Excel debe tener una hoja llamada "resumen mensual"
- Los datos se cargan automáticamente al inicio
- Los archivos subidos via admin se guardan en la carpeta `uploads/`

## 🔧 Configuración avanzada

### Cambiar contraseña admin

Edita `src/app.py`:
```python
ADMIN_PASSWORD = "tu_nueva_contraseña"
```

### Personalizar colores

En `src/app.py`, busca `style` y cambia los valores de color `#1a237e`.

---

**Versión**: 1.0  
**Última actualización**: Marzo 2026

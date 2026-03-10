# 🎯 Características Principales - Barby InfoManager

## 📊 Dashboard Interactivo

### 1️⃣ Resumen Anual
- **Tabla completa**: Todos los KPIs por mes
- **Tarjetas de progresión**: Cambio % compare (primer vs. último mes)
- **Métricas destacadas**: Inversión, Leads, Reuniones, CPL, CPR
- **Vista limpia**: Diseño profesional y responsive

### 2️⃣ Análisis de Métricas Principales
- **Selector dinámico**: Elige cualquier métrica del Excel
- **Gráfico de línea interactivo**: Evolución mensual con área sombreada
- **Estadísticas automáticas**:
  - Promedio anual
  - Valor máximo
  - Valor mínimo
  - Promedio últimos 3 meses

### 3️⃣ Vista Mensual
- **Selector de mes**: Elige cualquier mes disponible
- **Tabla ordenada**: Métricas de mayor a menor valor
- **Valores formateados**: Números con miles y decimales

### 4️⃣ Panel Administrativo 🔐
- **Protegido con contraseña**: `admin123`
- **Drag & Drop**: Arrastra archivos Excel fácilmente
- **Carga automática**: Recibe y procesa nuevos datos
- **Regeneración instantánea**: El reporte se actualiza automáticamente
- **Validación**: Verifica formato correcto del Excel

---

## 🔧 Características Técnicas

### Backend
- **Framework**: Dash (Python)
- **Visualización**: Plotly
- **Datos**: Excel (.xlsx)
- **Servidor**: Gunicorn + Python WSGI

### Frontend
- **Componentes**: HTML, CSS, JavaScript (Dash)
- **Responsivo**: Se adapta a cualquier pantalla
- **Interactivo**: Gráficos con hover, zoom, descargas

### Almacenamiento
- **Local**: Carpeta `uploads/` para archivos subidos
- **Cloud**: Compatible con Render, Cloudflare, etc.

---

## 🌐 Acceso

### Desarrollo Local
```
http://localhost:8050
http://192.168.x.x:8050  (desde otro dispositivo en la red)
```

### En Producción (Render)
```
https://barby-infomanager.onrender.com
```

---

## 📁 Estructura de Datos

### Excel requerido
```
Hoja: "resumen mensual"
Estructura:
  - Fila 0: Tasas de cambio (TC)
  - Fila 2: Nombres de meses (ENERO, FEBRERO, etc.)
  - Fila 3+: Métricas con valores por mes
```

### Métricas soportadas
✅ Inversión total  
✅ Inversión USD  
✅ Leads Ingresados  
✅ CPL (Costo por Lead)  
✅ CPL USD  
✅ Reuniones  
✅ CPR (Costo por Reunión)  
✅ CPR USD  
✅ % Lead a reunión  
✅ Cualquier otra métrica en el Excel

---

## 🚀 Flujos de Trabajo

### Flujo 1: Visualizar Datos Actuales
```
1. Abrir dashboard
2. Ver Resumen Anual
3. Explorar métricas principales
4. Analizar vista mensual
```

### Flujo 2: Cargar Nuevo Archivo
```
1. Panel Admin (pestaña 🔐)
2. Ingresar contraseña
3. Arrastra Excel o haz clic
4. Esperar validación
5. Dashboard se regenera automáticamente ✅
```

### Flujo 3: Desplegar a Producción
```
1. Preparar GitHub (QUICKSTART_DEPLOY.md)
2. Conectar con Render
3. Render descarga, instala, ejecuta
4. Dashboard en vivo en minutos 🎉
```

---

## 🔒 Seguridad

### Contraseña Admin
- Por defecto: `admin123`
- **CAMBIAR en producción** (ver DEPLOY.md)
- En Render: usar variables de entorno

### Validación de Archivos
- Solo acepta `.xlsx` o `.xls`
- Valida estructura de Excel
- Maneja errores gracefully

### Datos
- No se envían datos a terceros
- Todo se ejecuta localmente o en tu servidor Render

---

## ⚡ Performance

- **Carga rápida**: <2 segundos en conexión normal
- **Gráficos interactivos**: Responden instantáneamente
- **Escalable**: Soporta miles de filas de datos

---

## 🎨 Personalización

### Cambiar colores
Edita `src/app.py`, busca:
```python
'backgroundColor': '#1a237e'  # Azul oscuro principal
```

### Cambiar contraseña
Opción 1 (local):
```python
ADMIN_PASSWORD = "tu_nueva_pass"
```

Opción 2 (Render - recomendado):
```
Settings > Environment > ADMIN_PASSWORD=tu_pass
```

### Agregar métricas
Si el Excel tiene más métricas, aparecen automáticamente en el selector.

---

## 📞 Soporte

**¿Qué hacer si...**

❓ El Excel no carga?
- Verifica que tenga hoja "resumen mensual"
- Formatos: .xlsx o .xls

❓ La contraseña no funciona?
- Por defecto es `admin123`
- En Render, revisa variables de entorno

❓ Los gráficos no se muestran?
- Recarga la página (F5)
- Verifica conexión a internet

---

## 📊 Casos de Uso

✅ **Marketing**: Seguimiento de leads y conversiones  
✅ **Finanzas**: Control de inversiones y gastos  
✅ **Ventas**: Monitoreo de KPIs de desempeño  
✅ **Dirección**: Dashboard ejecutivo para reportes  
✅ **Operaciones**: Comparativa histórica de métricas  

---

**Versión**: 1.0  
**Última actualización**: Marzo 2026

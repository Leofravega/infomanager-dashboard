# 📚 Índice de Documentación - Barby InfoManager

## 🚀 Inicio Rápido

| Documento | Propósito |
|-----------|-----------|
| **[README.md](README.md)** | 📖 Guía general y estructura del proyecto |
| **[QUICKSTART_DEPLOY.md](QUICKSTART_DEPLOY.md)** | ⚡ Desplegar en Render en 5 minutos |
| **[FEATURES.md](FEATURES.md)** | 🎯 Lista completa de características |

---

## 📖 Documentación Detallada

### Para usuarios del Dashboard
1. Lee [README.md](README.md)
2. Ejecuta localmente: `python src/app.py`
3. Accede a `http://localhost:8050`
4. Prueba el Panel Admin (pestaña 🔐, contraseña: `admin123`)

### Para desplegar a producción
1. Lee [QUICKSTART_DEPLOY.md](QUICKSTART_DEPLOY.md) (5 min)
2. O ve a [DEPLOY.md](DEPLOY.md) para detalles completos
3. Sigue los pasos para GitHub y Render

---

## 🎯 Características Principales

El dashboard incluye:
- ✅ Carga automática de datos desde Excel
- ✅ 4 vistas diferentes (Resumen, Métricas, Mensual, Admin)
- ✅ Panel administrador con upload de archivos
- ✅ Gráficos interactivos en tiempo real
- ✅ Acceso desde red local y producción
- ✅ Responsive design (móvil, tablet, desktop)

Ver [FEATURES.md](FEATURES.md) para detalles completos.

---

## 📁 Estructura del Proyecto

```
barby-infomanager/
├── src/
│   ├── app.py                  # Aplicación principal (Dash)
│   └── data_generator.py       # Cargador de datos Excel
├── uploads/                    # Archivos Excel subidos
├── README.md                   # Documentación general
├── QUICKSTART_DEPLOY.md        # Despliegue rápido (5 min)
├── DEPLOY.md                   # Despliegue detallado
├── FEATURES.md                 # Lista de características
├── requirements.txt            # Dependencias Python
├── Procfile                    # Configuración Render
├── runtime.txt                 # Versión Python
└── INDEX.md                    # Este archivo
```

---

## 🌐 Acceso al Dashboard

### Desarrollo Local
```bash
# Instalar (primera vez)
pip install -r requirements.txt

# Ejecutar
python src/app.py

# Acceder
# Local:   http://localhost:8050
# Red:     http://192.168.x.x:8050
```

### En Producción (Render)
```
https://barby-infomanager.onrender.com
Contraseña admin: admin123
```

---

## 🔐 Panel Administrativo

### Acceso
1. Haz clic en pestaña **"🔐 Admin"**
2. Ingresa contraseña: `admin123`
3. Arrastra un archivo Excel o haz clic para seleccionar

### Resultado
- El reporte se regenera automáticamente
- Los datos se actualizan al instante
- El archivo se guarda en `uploads/`

---

## 🚀 Próximos Pasos

### Opción 1: Ejecutar Localmente
```bash
cd "c:\Projects\Barby InfoManager"
python src/app.py
# Abre http://localhost:8050
```

### Opción 2: Desplegar en Render (Recomendado)
1. Lee [QUICKSTART_DEPLOY.md](QUICKSTART_DEPLOY.md)
2. Crea repo en GitHub
3. Conecta con Render
4. ¡Listo! 🎉

### Opción 3: Despliegue Avanzado
Ver [DEPLOY.md](DEPLOY.md) para:
- Variables de entorno
- Dominios propios
- Almacenamiento en la nube
- Autenticación robusta

---

## ❓ Preguntas Frecuentes

**P: ¿Dónde cambio la contraseña admin?**  
A: En `src/app.py`, busca `ADMIN_PASSWORD = "admin123"`

**P: ¿Cómo subo un nuevo Excel?**  
A: Panel Admin → Arrastra archivo → Se regenera automático

**P: ¿Cuál es la URL en red local?**  
A: `http://192.168.1.33:8050` (o tu IP local)

**P: ¿Funciona en móvil?**  
A: Sí, es 100% responsive

**P: ¿Cómo despliegos sin pagar?**  
A: Usa Render gratis (con algunas limitaciones)

---

## 📱 Compatibilidad

| Dispositivo | Compatible |
|-------------|-----------|
| PC Windows | ✅ Totalmente |
| PC Mac | ✅ Totalmente |
| PC Linux | ✅ Totalmente |
| Móvil | ✅ Responsive |
| Tablet | ✅ Responsive |

---

## 🔗 Enlaces Útiles

- [Render.com](https://render.com) - Hosting gratuito
- [Dash Documentation](https://dash.plotly.com) - Framework
- [Plotly Charts](https://plotly.com) - Visualizaciones
- [GitHub](https://github.com) - Control de versiones

---

## 📞 Soporte

Si necesitas ayuda:
1. Revisa [FEATURES.md](FEATURES.md)
2. Consulta [DEPLOY.md](DEPLOY.md)
3. Lee los comentarios en `src/app.py`

---

**¡Estás listo para empezar! 🚀**

Comienza con [QUICKSTART_DEPLOY.md](QUICKSTART_DEPLOY.md) o ejecuta localmente.

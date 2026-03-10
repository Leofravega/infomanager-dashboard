# 🚀 Guía de Despliegue en Render

## Prerequisitos

1. Una cuenta en [Render.com](https://render.com) (gratis)
2. Tu repositorio en GitHub con el código
3. El archivo Excel original en el repo

## Pasos para desplegar

### 1. Preparar el repositorio en GitHub

```bash
# En tu máquina local
cd "c:\Projects\Barby InfoManager"
git init
git add .
git commit -m "Initial commit - Barby InfoManager"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/barby-infomanager.git
git push -u origin main
```

### 2. Crear el servicio en Render

1. Ve a [Render.com](https://render.com) y crea una cuenta
2. Haz clic en **"New +"** y selecciona **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Rellena los siguientes datos:

| Campo | Valor |
|-------|-------|
| **Name** | `barby-infomanager` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn src.app:server` |
| **Plan** | Free (o Premium si gustas) |

5. Haz clic en **"Create Web Service"**

### 3. Configurar variables de entorno (opcional)

Si quieres cambiar la contraseña del admin o usar variables secretas:

1. En el panel de Render, ve a **Settings**
2. En la sección **"Environment"**, agrega:

```
ADMIN_PASSWORD=tu_contraseña_nueva
```

3. Luego actualiza `src/app.py` para leer desde variables de entorno:

```python
import os
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
```

### 4. Esperar el despliegue

Render comenzará a:
1. Clonar tu repositorio
2. Instalar las dependencias
3. Iniciar la aplicación

Verás la URL en el formato: `https://barby-infomanager.onrender.com`

### 5. Acceder a tu dashboard

- **URL pública**: `https://barby-infomanager.onrender.com`
- **Usuario admin**: `admin123` (o tu contraseña)
- El archivo Excel se sincroniza automáticamente desde GitHub

## 📝 Notas importantes

### Almacenamiento de archivos subidos

En **Render Free**, los archivos subidos se perderán cuando se reinicie el servicio (cada 15 minutos sin actividad). Para persistencia:

1. **Opción A**: Usa **Cloudflare R2** (almacenamiento en la nube)
2. **Opción B**: Usa **PostgreSQL** para guardar los datos
3. **Opción C**: Sube archivos vía GitHub directamente

### Para sincronizar archivos vía GitHub

```bash
# En tu máquina local
# 1. Reemplaza el archivo Excel
cp "C:\ruta\al\nuevo\Resumen mensual INFOMANAGER.xlsx" .

# 2. Sube a GitHub
git add .
git commit -m "Update: Nuevo archivo de datos"
git push

# 3. En Render, redeploy automático
# (o ve a Settings > Deployments > Re-deploy latest)
```

## 🔒 Seguridad

- **Cambia la contraseña por defecto** en variables de entorno
- **No commits contraseñas** en GitHub (usa .env)
- Considera usar autenticación más robusta en producción

## ❓ Preguntas frecuentes

**P: ¿Cómo actualizar los datos?**
A: Sube un nuevo archivo Excel vía el Panel Admin, o actualiza en GitHub y hace redeploy.

**P: ¿Cómo cambio la contraseña?**
A: En Render Settings > Environment, actualiza `ADMIN_PASSWORD` y redeploy.

**P: ¿Puedo usar un dominio propio?**
A: Sí, en Render Settings > Domain Management, conecta tu dominio.

---

**¡Tu dashboard estará en vivo en minutos! 🎉**

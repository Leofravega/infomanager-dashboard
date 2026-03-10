# 🚀 Guía Rápida: GitHub → Render

## Paso 1: Preparar GitHub Desktop (o Git en terminal)

### Opción A: Con GitHub Desktop (más fácil)

1. Descarga [GitHub Desktop](https://desktop.github.com)
2. Crea un nuevo repositorio:
   - Nombre: `barby-infomanager`
   - Ruta local: `C:\Projects\Barby InfoManager`
   - Local only: desmarcar
3. Haz un nuevo commit con todos los archivos
4. Publica en GitHub

### Opción B: Con Terminal PowerShell

```powershell
cd "C:\Projects\Barby InfoManager"

# Iniciar repositorio
git init
git config user.name "Tu Nombre"
git config user.email "tu@email.com"

# Agregar archivos
git add .

# Hacer commit
git commit -m "Initial commit - Barby InfoManager with Admin Panel"

# Crear repositorio en GitHub
# 1. Ve a https://github.com/new
# 2. Nombre: barby-infomanager
# 3. Crear repositorio

# Conectar y subir (cambiar TU_USUARIO)
git branch -M main
git remote add origin https://github.com/TU_USUARIO/barby-infomanager.git
git push -u origin main
```

## Paso 2: Desplegar en Render

1. Ve a [https://render.com](https://render.com)
2. Crea una cuenta (gratis)
3. Haz clic en **"New +"** → **"Web Service"**
4. Autoriza GitHub y conecta `barby-infomanager`
5. Configura:
   - **Name**: `barby-infomanager`
   - **Runtime**: Python 3
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `gunicorn src.app:server`
   - **Plan**: Free

6. Clic en **"Create Web Service"**

## Paso 3: ¡Tu app está en vivo! 🎉

En pocos minutos tu dashboard estará disponible en:
```
https://barby-infomanager.onrender.com
```

### Cambiar contraseña admin

En GitHub:
1. Edita `src/app.py`
2. Busca `ADMIN_PASSWORD = "admin123"`
3. Cambia a tu contraseña
4. Commit y push
5. Render se redeploya automático

### Subir un nuevo archivo Excel

Opción 1: Via admin panel en vivo
- Pestaña "Admin" → Contraseña → Upload file

Opción 2: Via GitHub
- Reemplaza `Resumen mensual INFOMANAGER (1).xlsx`
- Commit y push
- Render redeploy automático

---

**¿Necesitas ayuda? Ver DEPLOY.md para más detalles**

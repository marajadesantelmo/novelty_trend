# Seguridad y Configuración 🔒

## ⚠️ IMPORTANTE: Credenciales NO Incluidas

Este repositorio **NO** incluye credenciales reales. Debes crear tus propios archivos de configuración.

## Archivos que Debes Crear

### 1. `tokens.py`
```python
url_supabase = 'https://TU-PROYECTO.supabase.co'
key_supabase = 'TU_SUPABASE_SERVICE_ROLE_KEY'
```

**Cómo obtener tus credenciales de Supabase:**
1. Ve a [supabase.com](https://supabase.com)
2. Crea un nuevo proyecto o selecciona uno existente
3. Ve a Settings → API
4. Copia la URL del proyecto y el `service_role` key

### 2. `credenciales_gsheets.json` (Opcional)
Solo necesario si usas integración con Google Sheets.

```json
{
  "type": "service_account",
  "project_id": "tu-proyecto-id",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "...",
  ...
}
```

**Cómo obtener credenciales de Google:**
1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Crea un proyecto o selecciona uno existente
3. Habilita Google Sheets API
4. Crea una Service Account
5. Descarga el archivo JSON de credenciales

### 3. `.env` (Alternativa recomendada)
```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_service_role_key
```

## Archivos Ignorados por Git

Los siguientes archivos están en `.gitignore` y **NUNCA** deben committearse:

- `tokens.py` - Credenciales de Supabase
- `credenciales_gsheets.json` - Credenciales de Google
- `.env` - Variables de entorno
- `migracion.py` - Scripts de migración específicos

## Archivos de Ejemplo Incluidos

✅ `tokens.py.example` - Template para tokens.py  
✅ `credenciales_gsheets.json.example` - Template para credenciales  
✅ `.env.template` - Template para variables de entorno

## Mejores Prácticas de Seguridad

1. **NUNCA** commitees credenciales reales
2. **NUNCA** compartas tu `service_role` key públicamente
3. Usa variables de entorno en producción
4. Rota tus keys regularmente
5. Usa diferentes credenciales para desarrollo y producción
6. Limita los permisos de las service accounts al mínimo necesario

## Rotación de Credenciales

Si accidentalmente expusiste credenciales:

### Para Supabase:
1. Ve a Settings → API en tu proyecto
2. Regenera el `service_role` key
3. Actualiza tu archivo `tokens.py` local

### Para Google Cloud:
1. Ve a IAM & Admin → Service Accounts
2. Elimina la key comprometida
3. Crea una nueva key
4. Descarga el nuevo JSON

## Contacto de Seguridad

Si encuentras algún problema de seguridad, por favor **NO** abras un issue público. Contacta directamente al mantenedor del repositorio.

---
**Última actualización:** 24/10/2025

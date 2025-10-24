# 🚀 INICIO RÁPIDO - NOVELTY TREND ERP

## Configuración en 5 Pasos

### 1️⃣ Configurar Supabase (5 minutos)

1. Ir a https://supabase.com y crear cuenta
2. Crear nuevo proyecto
3. Ir a **SQL Editor** (icono en sidebar)
4. Copiar TODO el contenido de `create_tables.sql`
5. Pegar y ejecutar (botón RUN)
6. Verificar que se crearon las tablas en **Table Editor**

### 2️⃣ Obtener Credenciales (2 minutos)

1. En Supabase, ir a **Settings** → **API**
2. Copiar:
   - **Project URL** (ej: https://xxxxx.supabase.co)
   - **anon/public key** (cadena larga que empieza con "eyJ...")

### 3️⃣ Configurar Proyecto Local (3 minutos)

1. Crear archivo `.env` en la raíz del proyecto:

```env
url_supabase=TU_PROJECT_URL_AQUI
key_supabase=TU_ANON_KEY_AQUI
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

### 4️⃣ Crear Usuario de Prueba (2 minutos)

1. En Supabase, ir a **Authentication** → **Users**
2. Click en **Add user** → **Create new user**
3. Ingresar:
   - Email: admin@noveltytrend.com
   - Password: (tu contraseña segura)
4. Click **Create user**

### 5️⃣ Ejecutar Aplicación (1 minuto)

```bash
streamlit run app_streamlit.py
```

Se abrirá automáticamente en http://localhost:8501

## 🎯 Primer Uso

### Orden Recomendado de Carga de Datos:

1. **Proveedores** → Crear 1-2 proveedores
2. **Contenedores** → Crear contenedor de prueba
3. **Stock** → Registrar 5-10 rollos
4. **Clientes** → Crear 2-3 clientes
5. **Costos** → Asignar costos al contenedor
6. **Ventas** → Crear un remito de prueba
7. **Cobranzas** → Registrar un pago
8. **Dashboard** → Ver las métricas

## ✅ Verificación

Si todo funciona correctamente:
- ✅ Ves el login al abrir la app
- ✅ Puedes iniciar sesión
- ✅ Ves 7 opciones en el menú lateral
- ✅ Cada página carga sin errores
- ✅ Puedes crear registros en cada módulo

## ❌ Problemas Comunes

### Error: "No module named 'supabase'"
**Solución:** `pip install -r requirements.txt`

### Error: "Invalid API key"
**Solución:** Verificar que el .env tenga las credenciales correctas

### Error: "relation does not exist"
**Solución:** Ejecutar create_tables.sql en Supabase

### Error al iniciar sesión
**Solución:** Verificar que creaste el usuario en Supabase Authentication

## 📞 Ayuda

Consultar documentación completa en `README.md`

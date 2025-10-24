# NOVELTY TREND ERP - SISTEMA DE GESTIÓN TEXTIL

## 📋 Resumen del Proyecto

Sistema ERP completo para la gestión de una empresa textil que comercializa rollos de tela importados. El sistema maneja inventario, ventas, clientes, cobranzas, proveedores y análisis de costos.

---

## 🗄️ ESTRUCTURA DE BASE DE DATOS

### Tablas Principales

1. **Clientes** - Gestión de clientes con cuentas corrientes en ARS y USD
2. **Proveedores** - Información de proveedores internacionales
3. **Contenedores** - Contenedores (CTN) que agrupan rollos importados
4. **Tipos_Tela** - Catálogo de tipos de tela
5. **Colores** - Catálogo de colores disponibles
6. **Rollos** - Inventario individual de cada rollo con código de barras único
7. **Remitos** - Notas de despacho/ventas
8. **Remitos_Detalle** - Líneas de detalle de cada remito
9. **Pagos** - Registro de pagos de clientes
10. **Cuentas_Corrientes** - Movimientos de cuenta corriente
11. **Costos_Contenedor** - Costos asociados a cada contenedor
12. **Costos_Rollo** - Asignación de costos por rollo
13. **Tipos_Cambio** - Registro histórico de tipos de cambio
14. **Auditoria** - Registro de cambios en el sistema

### Vistas Útiles

- **Vista_Stock_Disponible** - Stock agrupado por tipo y color
- **Vista_Ventas_Por_Cliente** - Resumen de ventas por cliente
- **Vista_Saldos_Clientes** - Saldos y vencimientos por cliente

---

## 🚀 INSTALACIÓN Y CONFIGURACIÓN

### 1. Configurar Base de Datos Supabase

```sql
-- Ejecutar el archivo create_tables.sql en Supabase SQL Editor
-- Este archivo contiene:
-- - Creación de todas las tablas
-- - Relaciones y claves foráneas
-- - Índices para optimización
-- - Vistas para consultas rápidas
-- - Datos de ejemplo para testing
```

### 2. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
url_supabase=https://tu-proyecto.supabase.co
key_supabase=tu-api-key-aqui
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación

```bash
streamlit run app_streamlit.py
```

---

## 📱 MÓDULOS DEL SISTEMA

### 1. Dashboard (dashboard.py)
- **KPIs principales**: Stock, ventas, clientes, cuentas por cobrar
- **Gráficos de ventas**: Evolución temporal y por cliente
- **Análisis de productos**: Stock y ventas por tipo de tela
- **Estado de cobranzas**: Vencimientos y pagos
- **Rotación de stock**: Tiempo promedio de permanencia

### 2. Stock (stock.py)
**Funcionalidades:**
- ✅ Ver stock disponible con filtros por tipo, color y estado
- ✅ Registrar nuevos rollos con código de barras
- ✅ Gestión por contenedor
- ✅ Búsqueda rápida por código de barras
- ✅ Métricas de inventario (cantidad, peso, valor)
- ✅ Resumen por tipo y color

### 3. Ventas (ventas.py)
**Funcionalidades:**
- ✅ Crear remitos con carrito de compras
- ✅ Selección de rollos disponibles
- ✅ Aplicar descuentos por cliente
- ✅ Ventas en ARS o USD con tipo de cambio
- ✅ Actualización automática de stock
- ✅ Registro en cuenta corriente
- ✅ Listado y filtrado de remitos
- ✅ Estadísticas de ventas

### 4. Clientes (clientes.py)
**Funcionalidades:**
- ✅ CRUD completo de clientes
- ✅ Gestión de saldos en ARS y USD
- ✅ Condiciones de pago y descuentos
- ✅ Tipo de cambio personalizado
- ✅ Estadísticas por cliente
- ✅ Top clientes por volumen

### 5. Cobranzas (cobranzas.py)
**Funcionalidades:**
- ✅ Registrar pagos (efectivo, transferencia, cheque, tarjeta)
- ✅ Asociar pagos a remitos
- ✅ Historial de pagos
- ✅ Consulta de cuenta corriente
- ✅ Alertas de vencimientos
- ✅ Seguimiento de cheques diferidos

### 6. Proveedores (proveedores.py)
**Funcionalidades:**
- ✅ Gestión de proveedores internacionales
- ✅ Registro de contenedores (CTN)
- ✅ Información de arribos y puertos
- ✅ Trazabilidad de rollos por proveedor

### 7. Costos (costos.py)
**Funcionalidades:**
- ✅ Registro de costos por contenedor
- ✅ Desglose de costos: mercadería, flete, seguro, importación
- ✅ Cálculo de costo por kilogramo
- ✅ Conversión USD a ARS
- ✅ Análisis de rentabilidad
- ✅ Cálculo de márgenes de ganancia

---

## 🔑 CARACTERÍSTICAS PRINCIPALES

### Gestión de Inventario
- ✅ Código de barras único por rollo
- ✅ Trazabilidad por contenedor
- ✅ Control de ubicación física
- ✅ Estados: Disponible, Vendido, Reservado, Defectuoso
- ✅ Registro de peso inicial y actual

### Sistema de Ventas
- ✅ Carrito de compras interactivo
- ✅ Precios modificables por venta
- ✅ Descuentos automáticos por cliente
- ✅ Generación automática de número de remito
- ✅ Actualización de stock en tiempo real

### Cuentas Corrientes
- ✅ Soporte para ARS y USD
- ✅ Tipos de cambio configurables
- ✅ Registro de débitos y créditos
- ✅ Cálculo automático de saldos
- ✅ Alertas de vencimientos

### Análisis y Reportes
- ✅ Dashboard ejecutivo con KPIs
- ✅ Gráficos interactivos (Plotly)
- ✅ Análisis de rentabilidad
- ✅ Rotación de stock
- ✅ Top clientes y productos

---

## 🔐 SEGURIDAD

- ✅ Autenticación via Supabase Auth
- ✅ Control de acceso por usuario
- ✅ Registro de auditoría de operaciones
- ✅ Variables de entorno para credenciales

---

## 📊 FLUJOS DE TRABAJO PRINCIPALES

### Flujo de Importación
1. Registrar proveedor
2. Crear contenedor (CTN)
3. Registrar costos del contenedor
4. Cargar rollos individuales con código de barras
5. Asignar ubicación en depósito

### Flujo de Venta
1. Seleccionar cliente
2. Agregar rollos al carrito
3. Ajustar precios si es necesario
4. Generar remito
5. Actualización automática de:
   - Stock (rollos → vendidos)
   - Cuenta corriente (débito)
   - Saldo del cliente

### Flujo de Cobranza
1. Registrar pago del cliente
2. Asociar a remito (opcional)
3. Actualización automática de:
   - Saldo del cliente (crédito)
   - Cuenta corriente
   - Estado de vencimientos

---

## 📈 MÉTRICAS Y KPIs

### Operacionales
- Stock disponible (kg y unidades)
- Ventas del período (ARS y USD)
- Clientes activos
- Cuentas por cobrar

### Financieros
- Margen de ganancia por producto
- Costo promedio por kg
- Rentabilidad por tipo de tela
- Valor del inventario

### Gestión
- Tiempo de rotación de stock
- Performance de cobranzas
- Top clientes
- Productos más vendidos

---

## 🛠️ TECNOLOGÍAS UTILIZADAS

- **Frontend**: Streamlit (Python)
- **Backend**: Supabase (PostgreSQL)
- **Autenticación**: Supabase Auth
- **Visualización**: Plotly
- **Gestión de Datos**: Pandas

---

## 📝 NOTAS TÉCNICAS

### Nomenclatura de Columnas
- Se utiliza formato Title Case ("Nombre", "Saldo_ARS") para facilitar visualización en Streamlit
- Las relaciones usan formato "Id_Tabla" (ej: "Id_Cliente")

### Validaciones Implementadas
- ✅ Códigos de barras únicos
- ✅ Montos positivos
- ✅ Estados válidos
- ✅ Integridad referencial

### Optimizaciones
- Índices en campos de búsqueda frecuente
- Vistas pre-calculadas para reportes
- Carga lazy de datos pesados

---

## 🔄 PRÓXIMAS MEJORAS SUGERIDAS

### Funcionalidades
- [ ] Exportación a Excel/PDF
- [ ] Notificaciones por email de vencimientos
- [ ] Gestión de usuarios y permisos
- [ ] Módulo de facturación electrónica
- [ ] Integración con AFIP (Argentina)
- [ ] App móvil para escaneo de códigos de barras

### Reportes Adicionales
- [ ] Análisis de tendencias de venta
- [ ] Predicción de demanda
- [ ] Comparativas período anterior
- [ ] Ranking de rentabilidad

### Optimizaciones
- [ ] Cache de consultas frecuentes
- [ ] Paginación en tablas grandes
- [ ] Búsqueda full-text
- [ ] Backup automático

---

## 👥 ROLES Y PERMISOS SUGERIDOS

### Administrador
- Acceso completo a todos los módulos
- Gestión de usuarios
- Configuración del sistema

### Ventas
- Dashboard
- Stock (solo lectura)
- Ventas (completo)
- Clientes (completo)

### Cobranzas
- Dashboard
- Clientes (lectura)
- Cobranzas (completo)

### Almacén
- Stock (completo)
- Ventas (lectura)

---

## 📞 SOPORTE Y MANTENIMIENTO

### Backup de Datos
- Configurar backup automático diario en Supabase
- Exportar datos críticos semanalmente

### Monitoreo
- Revisar logs de Supabase
- Monitorear performance de consultas
- Verificar integridad de datos mensualmente

---

## 📄 LICENCIA

Desarrollado para Novelty Trend - Sistema Propietario

---

## 🎯 CONCLUSIÓN

Este sistema ERP proporciona una solución completa para la gestión de un negocio textil, desde la importación de rollos hasta la venta final y cobranza, con control financiero en múltiples monedas y análisis detallado de rentabilidad.

**Características destacadas:**
✅ Gestión completa del ciclo de negocio
✅ Soporte multi-moneda (ARS/USD)
✅ Trazabilidad completa de productos
✅ Análisis financiero detallado
✅ Interfaz intuitiva y moderna
✅ Base de datos robusta y escalable

---

**Fecha de Creación:** 24 de Octubre, 2025  
**Versión:** 1.0  
**Desarrollado para:** Novelty Trend

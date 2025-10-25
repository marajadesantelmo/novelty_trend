# Propuesta Comercial - Sistema ERP Novelty Trend

**Fecha:** 25 de Octubre de 2025  
**Cliente:** Novelty Trend S.A.  
**Proveedor:** Pymetech
**Validez de la Propuesta:** 30 días

---

## 1. Resumen Ejecutivo

Presentamos una propuesta integral para el desarrollo de un Sistema de Gestión Empresarial (ERP) personalizado para Novelty Trend. 

El sistema permitirá gestionar de manera eficiente y centralizada las operaciones de inventario, ventas, cobranzas, proveedores y análisis financiero, mejorando significativamente la toma de decisiones y la productividad operativa.

### Inversión Total
**U$D 4.000** (Cuatro mil dólares estadounidenses)
a
### Tecnologías Propuestas
- **Prototipado Rápido:** Streamlit (Python) para validación de funcionalidades
- **Aplicación de Producción:** TypeScript con Lovable para desarrollo web profesional
- **Base de Datos:** PostgreSQL en Supabase (escalable y segura)
- **Integración Hardware:** Sistema de escaneo de códigos de barras

---

## 2. Alcance del Proyecto

### 2.1. Objetivos del Sistema

1. **Centralizar** la información de stock, ventas, clientes y proveedores
2. **Automatizar** procesos de facturación, cobranzas y gestión de inventario
3. **Optimizar** el control de costos y rentabilidad por producto
4. **Mejorar** la trazabilidad de rollos de tela desde contenedor hasta venta final
5. **Facilitar** la toma de decisiones mediante dashboards ejecutivos en tiempo real

### 2.2. Usuarios del Sistema

- **Administración:** Acceso completo a reportes financieros y KPIs
- **Ventas:** Gestión de remitos, clientes y cuenta corriente
- **Depósito:** Control de stock, ubicaciones y movimientos de inventario
- **Compras:** Gestión de proveedores y costos de importación

---

## 3. Metodología de Desarrollo

### Enfoque Dual de Desarrollo

**1. Streamlit (Prototipado)**
- Desarrollo ágil de prototipos funcionales
- Validación rápida de requerimientos con el cliente
- Iteraciones semanales con feedback continuo
- Entrega de MVP (Producto Mínimo Viable) funcional

**2. TypeScript + Lovable (Producción)**
- Desarrollo simultáneo de la versión de producción
- Interfaz profesional responsive (web/mobile)
- Rendimiento optimizado y mejor experiencia de usuario
- Código mantenible y escalable a largo plazo

**3. Base de Datos Unificada**
- PostgreSQL en Supabase para ambas versiones
- Esquema único garantiza consistencia de datos
- Migración transparente de prototipo a producción
- Backups automáticos y alta disponibilidad

---

## 4. Plan de Trabajo - Fases y Entregables

### **FASE 1: Módulos Operativos Principales**
**Duración:** 4 semanas  
**Inversión:** U$D 1.200

#### Entregables

** Dashboard Ejecutivo**
- KPIs principales: Ventas del mes, Stock valorizado, Cuentas por cobrar
- Gráficos de tendencias de ventas por cliente y tipo de tela
- Alertas de stock bajo y vencimientos próximos
- Filtros por período y moneda (ARS/USD)

**📦 Módulo de Stock**
- Clasificación por tipo de tela, color y contenedor
- Estados: Disponible, Reservado, Vendido
- Búsqueda rápida por código de barras
- Control de ubicaciones en depósito
- Historial de movimientos de inventario

**💰 Módulo de Ventas**
- Emisión de remitos digitales
- Carrito de venta con selección de rollos
- Cálculo automático de totales en ARS/USD
- Actualización automática de stock
- Registro de ventas con tipo de cambio del día
- Generación de PDF de remitos

**👥 Módulo de Clientes**
- Ficha completa de cliente (CUIT, Condición IVA, domicilio)
- Gestión de condiciones de pago
- Tipo de cambio preferencial por cliente
- Saldo en cuenta corriente (ARS y USD separados)
- Historial de compras y estadísticas

**💵 Módulo de Cobranzas**
- Registro de pagos (Efectivo, Transferencia, Cheque, Tarjeta)
- Aplicación de pagos a remitos pendientes
- Actualización automática de cuenta corriente
- Alertas de vencimientos próximos
- Reporte de deuda vencida por cliente
- Historial completo de cobranzas

**✅ Criterios de Aceptación Fase 1:**
- Sistema funcional en Streamlit para pruebas internas
- Base de datos PostgreSQL implementada y poblada con datos reales en base a los arhivos excel que utiliza actualmente la empresa
- Inicio del desarrollo de la versión TypeScript
- Capacitación inicial al equipo

---

### **FASE 2: Gestión de Proveedores y Compras**
**Duración:** 4 semanas  
**Inversión:** U$D 1.000

#### Entregables

**🏭 Módulo de Proveedores**
- Alta, baja y modificación de proveedores
- Datos de contacto y condiciones comerciales
- Historial de compras por proveedor

**📦 Gestión de Contenedores (CTN)**
- Registro de contenedores importados
- Asociación contenedor ↔ proveedor ↔ rollos
- Fecha de arribo y datos de tracking
- Distribución de rollos por contenedor
- Reportes de costos por contenedor y por rollos asociados al contenedor

**💳 Módulo de Cuentas por Pagar**
- Registro de obligaciones con proveedores
- Vencimientos y pagos programados
- Control de saldos por proveedor
- Conciliación de pagos

---

### **FASE 3: Análisis Financiero y Rentabilidad**
**Duración:** 4 semanas  
**Inversión:** U$D 1.000

#### Entregables

**📈 Módulo de Costos**
- Registro de costos por contenedor:
  - Flete internacional (USD)
  - Despacho de aduana (ARS)
  - Gastos portuarios y logística
  - Otros gastos asociados
- Prorrateo automático de costos por rollo según peso
- Cálculo de costo por Kg de cada rollo
- Margen de ganancia por venta (precio venta - costo)
- Análisis de rentabilidad por:
  - Tipo de tela
  - Proveedor
  - Cliente
  - Período

**💹 Estado de Resultados**
- Ingresos por ventas (ARS/USD)
- Costo de mercadería vendida
- Margen bruto
- Gastos operativos
- Resultado neto del período
- Comparativas mensuales/anuales
- Gráficos de evolución de rentabilidad
- Exportación a Excel/PDF

**📊 Reportes Avanzados**
- Stock valorizado a costo y precio de venta
- Rotación de inventario
- Productos más rentables
- Análisis ABC de clientes
- Proyección de flujo de caja

---

### **FASE 4: Integración Hardware y Optimización**
**Duración:** 2 semanas  
**Inversión:** U$D 800

#### Entregables

**📱 Sistema de Escaneo de Códigos de Barras**
- Generación automática de códigos
- Impresión de etiquetas adhesivas para rollos
- Escaneo rápido para:
  - Ingreso de stock
  - Búsqueda instantánea de rollos
  - Inventario físico
- Soporte para lectores móviles (smartphones)

**🚀 Optimización y Puesta en Producción**
- Migración completa a versión TypeScript de producción
- Optimización de rendimiento y carga de datos
- Testing exhaustivo de todos los módulos
- Configuración de dominio y SSL
- Deploy en infraestructura de producción
- Migración de datos reales desde sistemas anteriores

---

## 5. Cronograma General

| Fase | Descripción | Duración | Semanas |
|------|-------------|----------|---------|
| **Fase 1** | Dashboard, Stock, Ventas, Clientes, Cobranzas | 4 semanas | S1-S4 |
| **Fase 2** | Proveedores, Contenedores, Cuentas por Pagar | 3 semanas | S5-S7 |
| **Fase 3** | Costos, Estados de Resultados, Reportes | 3 semanas | S8-S10 |
| **Fase 4** | Códigos de barras, Optimización, Deploy | 2 semanas | S11-S12 |

**Duración Total del Proyecto:** 12 semanas (3 meses)

---

## 6. Esquema de Pagos

### Inversión Inicial: U$D 4.000

| Hito | Monto | Momento de Pago |
|------|-------|----------------|
| **Pago 1 - Inicio del Proyecto** | U$D 1.200 (30%) | Al firmar contrato |
| **Pago 2 - Finalización Fase 1** | U$D 1.000 (25%) | Entrega y aprobación Fase 1 |
| **Pago 3 - Finalización Fase 2** | U$D 800 (20%) | Entrega y aprobación Fase 2 |
| **Pago 4 - Finalización Fase 3** | U$D 600 (15%) | Entrega y aprobación Fase 3 |
| **Pago 5 - Deploy Final** | U$D 400 (10%) | Puesta en producción |

**Total:** U$D 4.000

---

## 7. Mantenimiento y Soporte Post-Implementación

### Servicio de Mantenimiento Mensual: U$D 200

**Incluye:**

✅ **Soporte Técnico**
- Atención de consultas por email/WhatsApp (horario laboral)
- Resolución de incidencias en menos de 24 horas
- Soporte remoto cuando sea necesario

✅ **Mantenimiento Preventivo**
- Actualización de librerías y dependencias
- Monitoreo de rendimiento del sistema
- Optimización de base de datos
- Revisión de seguridad mensual

✅ **Hosting y Infraestructura**
- Servidor de aplicación
- Base de datos PostgreSQL en Supabase
- Dominio y certificado SSL
- Backups automáticos diarios
- Disponibilidad del 99.5%

✅ **Mejoras y Nuevas Funcionalidades**
- Hasta 8 horas/mes de desarrollo de mejoras menores
- Ajustes en reportes existentes
- Nuevos filtros o campos en módulos actuales

✅ **Capacitación Continua**
- 2 horas/mes de capacitación a nuevos usuarios
- Actualización de documentación

**Condiciones:**
- Contrato mínimo: 6 meses
- Renovación automática mensual
- Pago anticipado los primeros 5 días de cada mes
- Desarrollos mayores se cotizan aparte

---

##  Próximos Pasos

1. **Revisión de la Propuesta:** Análisis y consultas sobre el alcance
2. **Reunión de Kick-off:** Definición de detalles finales y cronograma
3. **Firma de Contrato:** Formalización del acuerdo
4. **Inicio del Proyecto:** Pago inicial y comienzo Fase 1

---

## Contacto

**Pymetech** 
Desarrollo a cargo de Facundo Lastra
Email: [facundo@pymetech.com.ar]  
Teléfono: [+1151128207]  
LinkedIn: [[click aquí](https://www.linkedin.com/in/facundo-lastra-b205511aa)]


---

**Validez de la Propuesta:** 30 días calendario desde la fecha de emisión

---


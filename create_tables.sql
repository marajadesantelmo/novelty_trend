-- ============================================
-- NOVELTY TREND - SISTEMA ERP TEXTIL
-- Base de datos para gestión de stock, ventas, clientes y costos
-- Fecha de creación: 24/10/2025
-- ============================================

-- ============================================
-- TABLAS MAESTRAS
-- ============================================

-- Tabla: Clientes
-- Almacena información de clientes con saldos en ARS y USD
CREATE TABLE "novelty_Clientes" (
    "Id" SERIAL PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "Razon_Social" VARCHAR(255),
    "CUIT" VARCHAR(13) UNIQUE,
    "Direccion" TEXT,
    "Telefono" VARCHAR(50),
    "Email" VARCHAR(255),
    "Condicion_Pago" VARCHAR(50) DEFAULT 'Contado', -- Contado, 30 días, 60 días, etc.
    "Descuento_Porcentaje" NUMERIC(5,2) DEFAULT 0,
    "Tipo_Cambio" VARCHAR(50) DEFAULT 'Celeste', -- Celeste (entre blue y oficial)
    "Estado" VARCHAR(20) DEFAULT 'Activo', -- Activo, Inactivo, Moroso
    "Fecha_Alta" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "Notas" TEXT
);

-- Tabla: Proveedores
-- Almacena información de proveedores que suministran rollos
CREATE TABLE "novelty_Proveedores" (
    "Id" SERIAL PRIMARY KEY,
    "Nombre" VARCHAR(255) NOT NULL,
    "Razon_Social" VARCHAR(255),
    "CUIT" VARCHAR(13) UNIQUE,
    "Pais_Origen" VARCHAR(100),
    "Direccion" TEXT,
    "Telefono" VARCHAR(50),
    "Email" VARCHAR(255),
    "Contacto" VARCHAR(255),
    "Condiciones_Pago" TEXT,
    "Estado" VARCHAR(20) DEFAULT 'Activo',
    "Fecha_Alta" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "Notas" TEXT
);

-- Tabla: Tipos_Tela
-- Catálogo de tipos de tela disponibles
CREATE TABLE "novelty_Tipos_Tela" (
    "Id" SERIAL PRIMARY KEY,
    "Nombre" VARCHAR(100) NOT NULL UNIQUE,
    "Descripcion" TEXT,
    "Composicion" VARCHAR(255), -- Ej: 100% Algodón, Poliéster 65% Algodón 35%
    "Ancho_Metros" NUMERIC(5,2),
    "Gramaje" NUMERIC(6,2), -- Gramos por metro cuadrado
    "Uso_Sugerido" TEXT,
    "Estado" VARCHAR(20) DEFAULT 'Activo'
);

-- Tabla: Colores
-- Catálogo de colores disponibles
CREATE TABLE "novelty_Colores" (
    "Id" SERIAL PRIMARY KEY,
    "Nombre" VARCHAR(100) NOT NULL UNIQUE,
    "Codigo_Hex" VARCHAR(7), -- Código hexadecimal del color (#FFFFFF)
    "Codigo_Pantone" VARCHAR(20),
    "Descripcion" TEXT,
    "Estado" VARCHAR(20) DEFAULT 'Activo'
);

-- Tabla: Contenedores
-- Información de contenedores (CTN) que agrupan rollos
CREATE TABLE "novelty_Contenedores" (
    "Id" SERIAL PRIMARY KEY,
    "Numero_CTN" VARCHAR(50) NOT NULL UNIQUE,
    "Id_Proveedor" INTEGER REFERENCES "novelty_Proveedores"("Id") ON DELETE SET NULL,
    "Fecha_Arribo" DATE,
    "Puerto_Origen" VARCHAR(100),
    "Puerto_Destino" VARCHAR(100),
    "Peso_Total_Kg" NUMERIC(12,2),
    "Cantidad_Rollos" INTEGER DEFAULT 0,
    "Estado" VARCHAR(50) DEFAULT 'En Tránsito', -- En Tránsito, Arribado, Despachado
    "Notas" TEXT,
    "Fecha_Registro" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- MÓDULO DE STOCK/INVENTARIO
-- ============================================

-- Tabla: Rollos
-- Almacena información individual de cada rollo de tela
CREATE TABLE "novelty_Rollos" (
    "Id" SERIAL PRIMARY KEY,
    "Codigo_Barras" VARCHAR(100) NOT NULL UNIQUE,
    "Numero_Rollo" VARCHAR(50) NOT NULL,
    "Id_Contenedor" INTEGER REFERENCES "novelty_Contenedores"("Id") ON DELETE SET NULL,
    "Id_Tipo_Tela" INTEGER REFERENCES "novelty_Tipos_Tela"("Id") ON DELETE SET NULL,
    "Id_Color" INTEGER REFERENCES "novelty_Colores"("Id") ON DELETE SET NULL,
    "Peso_Kg" NUMERIC(10,2) NOT NULL,
    "Peso_Inicial_Kg" NUMERIC(10,2), -- Peso original del rollo
    "Metros" NUMERIC(10,2),
    "Ubicacion" VARCHAR(100), -- Ubicación física en el depósito
    "Estado" VARCHAR(50) DEFAULT 'Disponible', -- Disponible, Vendido, Reservado, Defectuoso
    "Precio_Costo_Por_Kg" NUMERIC(10,2),
    "Precio_Venta_Por_Kg" NUMERIC(10,2),
    "Lote" VARCHAR(50),
    "Fecha_Ingreso" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "Fecha_Venta" TIMESTAMP,
    "Notas" TEXT
);

-- Índices para mejorar búsquedas
CREATE INDEX idx_rollos_estado ON "novelty_Rollos"("Estado");
CREATE INDEX idx_rollos_contenedor ON "novelty_Rollos"("Id_Contenedor");
CREATE INDEX idx_rollos_tipo_color ON "novelty_Rollos"("Id_Tipo_Tela", "Id_Color");

-- ============================================
-- MÓDULO DE VENTAS
-- ============================================

-- Tabla: Remitos
-- Registro de notas de despacho/ventas
CREATE TABLE "novelty_Remitos" (
    "Id" SERIAL PRIMARY KEY,
    "Numero_Remito" VARCHAR(50) NOT NULL UNIQUE,
    "Id_Cliente" INTEGER REFERENCES "novelty_Clientes"("Id") ON DELETE SET NULL,
    "Fecha_Emision" DATE NOT NULL DEFAULT CURRENT_DATE,
    "Fecha_Entrega" DATE,
    "Total_Kg" NUMERIC(12,2) DEFAULT 0,
    "Total_Rollos" INTEGER DEFAULT 0,
    "Subtotal_ARS" NUMERIC(12,2) DEFAULT 0,
    "Subtotal_USD" NUMERIC(12,2) DEFAULT 0,
    "Descuento_Porcentaje" NUMERIC(5,2) DEFAULT 0,
    "Descuento_Monto" NUMERIC(12,2) DEFAULT 0,
    "Total_ARS" NUMERIC(12,2) DEFAULT 0,
    "Total_USD" NUMERIC(12,2) DEFAULT 0,
    "Moneda" VARCHAR(10) DEFAULT 'ARS', -- ARS o USD
    "Tipo_Cambio_Aplicado" NUMERIC(10,2),
    "Estado" VARCHAR(50) DEFAULT 'Pendiente', -- Pendiente, Entregado, Facturado, Cancelado
    "Observaciones" TEXT,
    "Usuario_Creacion" VARCHAR(100),
    "Fecha_Creacion" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: Remitos_Detalle
-- Detalle de rollos incluidos en cada remito
CREATE TABLE "novelty_Remitos_Detalle" (
    "Id" SERIAL PRIMARY KEY,
    "Id_Remito" INTEGER REFERENCES "novelty_Remitos"("Id") ON DELETE CASCADE,
    "Id_Rollo" INTEGER REFERENCES "novelty_Rollos"("Id") ON DELETE SET NULL,
    "Codigo_Barras" VARCHAR(100), -- Guardamos copia por si se elimina el rollo
    "Tipo_Tela" VARCHAR(100),
    "Color" VARCHAR(100),
    "Peso_Kg" NUMERIC(10,2) NOT NULL,
    "Precio_Por_Kg" NUMERIC(10,2) NOT NULL,
    "Subtotal" NUMERIC(12,2) NOT NULL,
    "Descuento_Aplicado" NUMERIC(5,2) DEFAULT 0,
    "Total" NUMERIC(12,2) NOT NULL
);

-- Índices para ventas
CREATE INDEX idx_remitos_cliente ON "novelty_Remitos"("Id_Cliente");
CREATE INDEX idx_remitos_fecha ON "novelty_Remitos"("Fecha_Emision");
CREATE INDEX idx_remitos_detalle_remito ON "novelty_Remitos_Detalle"("Id_Remito");

-- ============================================
-- MÓDULO DE COBRANZAS
-- ============================================

-- Tabla: Pagos
-- Registro de pagos realizados por clientes
CREATE TABLE "novelty_Pagos" (
    "Id" SERIAL PRIMARY KEY,
    "Id_Cliente" INTEGER REFERENCES "novelty_Clientes"("Id") ON DELETE SET NULL,
    "Id_Remito" INTEGER REFERENCES "novelty_Remitos"("Id") ON DELETE SET NULL,
    "Numero_Recibo" VARCHAR(50) UNIQUE,
    "Fecha_Pago" DATE NOT NULL DEFAULT CURRENT_DATE,
    "Monto_ARS" NUMERIC(12,2) DEFAULT 0,
    "Monto_USD" NUMERIC(12,2) DEFAULT 0,
    "Moneda" VARCHAR(10) NOT NULL, -- ARS o USD
    "Tipo_Cambio" NUMERIC(10,2),
    "Metodo_Pago" VARCHAR(50), -- Efectivo, Transferencia, Cheque, Tarjeta
    "Referencia" VARCHAR(100), -- Número de cheque, transferencia, etc.
    "Estado" VARCHAR(50) DEFAULT 'Confirmado', -- Pendiente, Confirmado, Rechazado
    "Fecha_Vencimiento" DATE, -- Para cheques diferidos
    "Observaciones" TEXT,
    "Usuario_Registro" VARCHAR(100),
    "Fecha_Registro" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: Cuentas_Corrientes
-- Movimientos de cuenta corriente de clientes
CREATE TABLE "novelty_Cuentas_Corrientes" (
    "Id" SERIAL PRIMARY KEY,
    "Id_Cliente" INTEGER REFERENCES "novelty_Clientes"("Id") ON DELETE CASCADE,
    "Fecha" DATE NOT NULL DEFAULT CURRENT_DATE,
    "Tipo_Movimiento" VARCHAR(50) NOT NULL, -- Salida o Ingreso
    "Categoria" VARCHAR(50) NOT NULL, -- Cobranza, Rentabilidad, Otros Ingresos, Comex, Proveedores, Caja chica, Retiros, Gastos, Otras salidas, Comision, Entregas
    "Id_Remito" INTEGER REFERENCES "novelty_Remitos"("Id") ON DELETE SET NULL,
    "Id_Pago" INTEGER REFERENCES "novelty_Pagos"("Id") ON DELETE SET NULL,
    "Moneda" TEXT NOT NULL, -- ARS o USD
    "Tipo de Cambio" NUMERIC(10,2),
    "Debe_USD" NUMERIC(12,2) DEFAULT 0,
    "Haber_USD" NUMERIC(12,2) DEFAULT 0,
    "Saldo_USD" NUMERIC(12,2) DEFAULT 0,
    "Descripcion" TEXT,
    "Fecha_Vencimiento" DATE,
    "Estado" VARCHAR(50) DEFAULT 'Pendiente', -- Pendiente, Vencido, Pagado
    "Fecha_Registro" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para cobranzas
CREATE INDEX idx_pagos_cliente ON "novelty_Pagos"("Id_Cliente");
CREATE INDEX idx_pagos_fecha ON "novelty_Pagos"("Fecha_Pago");
CREATE INDEX idx_cuentas_corrientes_cliente ON "novelty_Cuentas_Corrientes"("Id_Cliente");

-- ============================================
-- MÓDULO DE COSTOS
-- ============================================

-- Tabla: Costos_Contenedor
-- Costos asociados a cada contenedor
CREATE TABLE "novelty_Costos_Contenedor" (
    "Id" SERIAL PRIMARY KEY,
    "Id_Contenedor" INTEGER REFERENCES "novelty_Contenedores"("Id") ON DELETE CASCADE,
    "Costo_Mercaderia_USD" NUMERIC(12,2) DEFAULT 0,
    "Costo_Flete_USD" NUMERIC(12,2) DEFAULT 0,
    "Costo_Seguro_USD" NUMERIC(12,2) DEFAULT 0,
    "Derechos_Importacion_USD" NUMERIC(12,2) DEFAULT 0,
    "Gastos_Despacho_USD" NUMERIC(12,2) DEFAULT 0,
    "Otros_Gastos_USD" NUMERIC(12,2) DEFAULT 0,
    "Total_Costos_USD" NUMERIC(12,2) DEFAULT 0,
    "Costo_Por_Kg_USD" NUMERIC(10,4), -- Calculado automáticamente
    "Tipo_Cambio_Compra" NUMERIC(10,2),
    "Total_Costos_ARS" NUMERIC(12,2) DEFAULT 0,
    "Fecha_Registro" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "Notas" TEXT
);

-- Tabla: Costos_Rollo
-- Asignación de costos específicos por rollo (opcional)
CREATE TABLE "novelty_Costos_Rollo" (
    "Id" SERIAL PRIMARY KEY,
    "Id_Rollo" INTEGER REFERENCES "novelty_Rollos"("Id") ON DELETE CASCADE,
    "Costo_Unitario_USD" NUMERIC(10,4),
    "Costo_Por_Kg_USD" NUMERIC(10,4),
    "Costo_Total_USD" NUMERIC(12,2),
    "Tipo_Cambio" NUMERIC(10,2),
    "Costo_Total_ARS" NUMERIC(12,2),
    "Margen_Ganancia_Porcentaje" NUMERIC(5,2),
    "Precio_Venta_Sugerido_Por_Kg" NUMERIC(10,2),
    "Fecha_Calculo" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "Notas" TEXT
);

-- ============================================
-- TABLAS DE CONFIGURACIÓN Y AUDITORÍA
-- ============================================

-- Tabla: Tipos_Cambio
-- Registro histórico de tipos de cambio
CREATE TABLE "novelty_Tipos_Cambio" (
    "Id" SERIAL PRIMARY KEY,
    "Fecha" DATE NOT NULL,
    "Tipo" VARCHAR(50) NOT NULL, -- Oficial, Blue, Celeste, MEP, etc.
    "Valor_Compra" NUMERIC(10,2),
    "Valor_Venta" NUMERIC(10,2),
    "Valor_Promedio" NUMERIC(10,2),
    "Fecha_Registro" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE("Fecha", "Tipo")
);

-- Tabla: Auditoria
-- Registro de cambios importantes en el sistema
CREATE TABLE "novelty_Auditoria" (
    "Id" SERIAL PRIMARY KEY,
    "Tabla" VARCHAR(100) NOT NULL,
    "Id_Registro" INTEGER,
    "Accion" VARCHAR(50) NOT NULL, -- INSERT, UPDATE, DELETE
    "Usuario" VARCHAR(100),
    "Datos_Anteriores" JSONB,
    "Datos_Nuevos" JSONB,
    "Fecha" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "IP_Address" VARCHAR(50)
);

-- ============================================
-- VISTAS ÚTILES
-- ============================================

-- Vista: Stock disponible por tipo y color
CREATE VIEW "Vista_Stock_Disponible" AS
SELECT 
    tt."Nombre" AS "Tipo_Tela",
    c."Nombre" AS "Color",
    COUNT(r."Id") AS "Cantidad_Rollos",
    SUM(r."Peso_Kg") AS "Total_Kg",
    AVG(r."Precio_Venta_Por_Kg") AS "Precio_Promedio_Por_Kg",
    MIN(r."Fecha_Ingreso") AS "Fecha_Ingreso_Mas_Antigua"
FROM "Rollos" r
LEFT JOIN "Tipos_Tela" tt ON r."Id_Tipo_Tela" = tt."Id"
LEFT JOIN "Colores" c ON r."Id_Color" = c."Id"
WHERE r."Estado" = 'Disponible'
GROUP BY tt."Nombre", c."Nombre"
ORDER BY tt."Nombre", c."Nombre";

-- Vista: Resumen de ventas por cliente
CREATE VIEW "Vista_Ventas_Por_Cliente" AS
SELECT 
    cl."Id" AS "Id_Cliente",
    cl."Nombre" AS "Cliente",
    COUNT(DISTINCT r."Id") AS "Total_Remitos",
    SUM(r."Total_Kg") AS "Total_Kg_Vendidos",
    SUM(r."Total_ARS") AS "Total_Ventas_ARS",
    SUM(r."Total_USD") AS "Total_Ventas_USD",
    MAX(r."Fecha_Emision") AS "Ultima_Venta"
FROM "Clientes" cl
LEFT JOIN "Remitos" r ON cl."Id" = r."Id_Cliente"
GROUP BY cl."Id", cl."Nombre"
ORDER BY SUM(r."Total_ARS" + r."Total_USD") DESC;

-- Vista: Saldos de clientes
CREATE VIEW "Vista_Saldos_Clientes" AS
SELECT 
    c."Id",
    c."Nombre",
    c."Razon_Social",
    c."Saldo_ARS",
    c."Saldo_USD",
    c."Estado",
    COUNT(DISTINCT cc."Id") AS "Movimientos_Pendientes",
    MIN(cc."Fecha_Vencimiento") AS "Vencimiento_Mas_Proximo"
FROM "Clientes" c
LEFT JOIN "Cuentas_Corrientes" cc ON c."Id" = cc."Id_Cliente" 
    AND cc."Estado" = 'Pendiente'
GROUP BY c."Id", c."Nombre", c."Razon_Social", c."Saldo_ARS", c."Saldo_USD", c."Estado"
ORDER BY c."Nombre";

-- ============================================
-- DATOS DE EJEMPLO PARA TESTING
-- ============================================

-- Insertar tipos de tela de ejemplo
INSERT INTO "novelty_Tipos_Tela" ("Nombre", "Descripcion", "Composicion", "Ancho_Metros") VALUES
('Jersey', 'Tela de punto suave y elástica', '100% Algodón', 1.80),
('Poplin', 'Tela plana de tejido fino', '65% Poliéster 35% Algodón', 1.50),
('Gabardina', 'Tela resistente de sarga', '100% Poliéster', 1.50),
('Lycra', 'Tela elástica', '92% Poliéster 8% Spandex', 1.70),
('Polar', 'Tela térmica suave', '100% Poliéster', 1.60);

-- Insertar colores de ejemplo
INSERT INTO "novelty_Colores" ("Nombre", "Codigo_Hex") VALUES
('Blanco', '#FFFFFF'),
('Negro', '#000000'),
('Rojo', '#FF0000'),
('Azul Marino', '#000080'),
('Gris', '#808080'),
('Verde', '#008000'),
('Amarillo', '#FFFF00'),
('Rosa', '#FFC0CB'),
('Beige', '#F5F5DC'),
('Celeste', '#87CEEB');

-- Insertar tipo de cambio de ejemplo
INSERT INTO "novelty_Tipos_Cambio" ("Fecha", "Tipo", "Valor_Compra", "Valor_Venta", "Valor_Promedio") VALUES
(CURRENT_DATE, 'Oficial', 1455.00, 1505.00, 1480.00),
(CURRENT_DATE, 'Blue', 1500.00, 1520.00, 1510.00),
(CURRENT_DATE, 'Celeste', 1477.50, 1512.50, 1495.00);

-- Insertar cliente de ejemplo --> Desde script migracion.py

-- Insertar proveedor de ejemplo
INSERT INTO "novelty_Proveedores" ("Nombre", "Razon_Social", "Pais_Origen", "Email") VALUES
('TextiChina Ltd.', 'TextiChina Import Export Ltd.', 'China', 'info@textichina.com'),
('IndiaTextiles Co.', 'India Textiles Company', 'India', 'sales@indiatextiles.in');
-- ============================================
-- COMENTARIOS FINALES
-- ============================================
-- Este esquema proporciona:
-- 1. Gestión completa de inventario con trazabilidad por rollo y contenedor
-- 2. Sistema de ventas con remitos y detalle de productos
-- 3. Cuentas corrientes de clientes en ARS y USD
-- 4. Control de cobranzas con fechas de vencimiento
-- 5. Cálculo de costos por contenedor y por rollo
-- 6. Auditoría de operaciones
-- 7. Vistas para reportes rápidos
--
-- Consideraciones de escalabilidad:
-- - Índices en campos de búsqueda frecuente
-- - Claves foráneas con acciones ON DELETE apropiadas
-- - Campos de estado para soft-delete
-- - Campos de auditoría (fechas, usuarios)
-- - Uso de NUMERIC para valores monetarios (evita errores de redondeo)
-- ============================================


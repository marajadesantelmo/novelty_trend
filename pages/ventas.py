"""
MÓDULO DE VENTAS Y REMITOS
Gestión de notas de despacho, ventas de rollos y facturación
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from supabase_connection import supabase_client

def show():
    st.title("🛒 Ventas y Remitos")
    
    tab1, tab2, tab3 = st.tabs([
        "📝 Nuevo Remito",
        "📋 Listado de Remitos",
        "📊 Estadísticas de Ventas"
    ])
    
    # ============================================
    # TAB 1: CREAR NUEVO REMITO
    # ============================================
    with tab1:
        st.subheader("Crear Nuevo Remito")
        
        # Inicializar carrito en session_state
        if 'carrito' not in st.session_state:
            st.session_state['carrito'] = []
        
        # Selector de cliente
        clientes = supabase_client.table("novelty_Clientes").select("*").eq("Estado", "Activo").execute()
        cliente_options = {f"{c['Nombre']} - {c.get('Razon_Social', '')}": c for c in clientes.data}
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            cliente_selected = st.selectbox(
                "Seleccionar Cliente *",
                ["Seleccionar..."] + list(cliente_options.keys())
            )
        
        with col2:
            fecha_emision = st.date_input("Fecha de Emisión", value=date.today())
        
        if cliente_selected != "Seleccionar...":
            cliente = cliente_options[cliente_selected]
            
            # Información del cliente
            st.info(f"""
            **Cliente:** {cliente['Nombre']}  
            **Condición de Pago:** {cliente.get('Condicion_Pago', 'N/A')}  
            **Descuento:** {cliente.get('Descuento_Porcentaje', 0)}%  
            **Saldo ARS:** ${cliente.get('Saldo_ARS', 0):,.2f} | **Saldo USD:** ${cliente.get('Saldo_USD', 0):,.2f}
            """)
            
            st.markdown("---")
            
            # Selección de rollos
            st.subheader("Agregar Rollos al Remito")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                # Obtener tipos de tela
                tipos_tela = supabase_client.table("novelty_Tipos_Tela").select("*").eq("Estado", "Activo").execute()
                tipo_options = ["Todos"] + [t["Nombre"] for t in tipos_tela.data]
                tipo_filter = st.selectbox("Tipo de Tela", tipo_options, key="tipo_venta")
            
            with col_b:
                # Obtener colores
                colores = supabase_client.table("novelty_Colores").select("*").eq("Estado", "Activo").execute()
                color_options = ["Todos"] + [c["Nombre"] for c in colores.data]
                color_filter = st.selectbox("Color", color_options, key="color_venta")
            
            with col_c:
                codigo_buscar = st.text_input("Código de Barras", placeholder="Escanear")
            
            # Consultar rollos disponibles
            try:
                query = supabase_client.table("novelty_Rollos").select("""
                    *,
                    Tipos_Tela:Id_Tipo_Tela(Nombre),
                    Colores:Id_Color(Nombre),
                    Contenedores:Id_Contenedor(Numero_CTN)
                """).eq("Estado", "Disponible")
                
                if tipo_filter != "Todos":
                    tipo_id = next((t["Id"] for t in tipos_tela.data if t["Nombre"] == tipo_filter), None)
                    if tipo_id:
                        query = query.eq("Id_Tipo_Tela", tipo_id)
                
                if color_filter != "Todos":
                    color_id = next((c["Id"] for c in colores.data if c["Nombre"] == color_filter), None)
                    if color_id:
                        query = query.eq("Id_Color", color_id)
                
                if codigo_buscar:
                    query = query.ilike("Codigo_Barras", f"%{codigo_buscar}%")
                
                rollos_disponibles = query.execute()
                
                if rollos_disponibles.data:
                    st.write(f"**{len(rollos_disponibles.data)} rollos disponibles**")
                    
                    # Mostrar rollos disponibles
                    for rollo in rollos_disponibles.data[:10]:  # Limitar a 10 para no saturar
                        col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
                        
                        with col1:
                            st.text(rollo['Codigo_Barras'])
                        with col2:
                            tipo = rollo['Tipos_Tela']['Nombre'] if rollo.get('Tipos_Tela') else 'N/A'
                            color = rollo['Colores']['Nombre'] if rollo.get('Colores') else 'N/A'
                            st.text(f"{tipo} - {color}")
                        with col3:
                            st.text(f"{rollo['Peso_Kg']} kg")
                        with col4:
                            precio = rollo.get('Precio_Venta_Por_Kg', 0)
                            st.text(f"${precio:.2f}/kg")
                        with col5:
                            if st.button("➕", key=f"add_{rollo['Id']}"):
                                # Agregar al carrito
                                item = {
                                    'id': rollo['Id'],
                                    'codigo': rollo['Codigo_Barras'],
                                    'tipo': tipo,
                                    'color': color,
                                    'peso': rollo['Peso_Kg'],
                                    'precio_kg': precio,
                                    'subtotal': rollo['Peso_Kg'] * precio
                                }
                                st.session_state['carrito'].append(item)
                                st.success(f"✅ Agregado: {rollo['Codigo_Barras']}")
                                st.rerun()
                
                else:
                    st.warning("No hay rollos disponibles con esos filtros")
            
            except Exception as e:
                st.error(f"Error al buscar rollos: {str(e)}")
            
            # Mostrar carrito
            st.markdown("---")
            st.subheader("🛒 Carrito de Venta")
            
            if st.session_state['carrito']:
                df_carrito = pd.DataFrame(st.session_state['carrito'])
                
                # Permitir editar precios
                st.write("**Detalle de Items:**")
                
                for idx, item in enumerate(st.session_state['carrito']):
                    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1, 1, 1, 1])
                    
                    with col1:
                        st.text(item['codigo'])
                    with col2:
                        st.text(f"{item['tipo']} - {item['color']}")
                    with col3:
                        st.text(f"{item['peso']} kg")
                    with col4:
                        # Permitir modificar precio
                        nuevo_precio = st.number_input(
                            "$/kg",
                            value=float(item['precio_kg']),
                            min_value=0.0,
                            step=0.01,
                            key=f"precio_{idx}",
                            label_visibility="collapsed"
                        )
                        st.session_state['carrito'][idx]['precio_kg'] = nuevo_precio
                        st.session_state['carrito'][idx]['subtotal'] = item['peso'] * nuevo_precio
                    with col5:
                        st.text(f"${item['subtotal']:,.2f}")
                    with col6:
                        if st.button("🗑️", key=f"remove_{idx}"):
                            st.session_state['carrito'].pop(idx)
                            st.rerun()
                
                # Totales
                st.markdown("---")
                
                subtotal = sum([item['subtotal'] for item in st.session_state['carrito']])
                total_kg = sum([item['peso'] for item in st.session_state['carrito']])
                descuento_pct = cliente.get('Descuento_Porcentaje', 0)
                descuento_monto = subtotal * (descuento_pct / 100)
                total = subtotal - descuento_monto
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Rollos", len(st.session_state['carrito']))
                with col2:
                    st.metric("Total Kg", f"{total_kg:.2f}")
                with col3:
                    st.metric("Subtotal", f"${subtotal:,.2f}")
                with col4:
                    st.metric("Total", f"${total:,.2f}", 
                             delta=f"-{descuento_pct}%" if descuento_pct > 0 else None)
                
                # Opciones de venta
                col_m1, col_m2 = st.columns(2)
                
                with col_m1:
                    moneda = st.selectbox("Moneda", ["ARS", "USD"])
                
                with col_m2:
                    if moneda == "USD":
                        # Obtener tipo de cambio
                        tc_result = supabase_client.table("novelty_Tipos_Cambio").select("*").eq("Tipo", cliente.get('Tipo_Cambio', 'Celeste')).order("Fecha", desc=True).limit(1).execute()
                        if tc_result.data:
                            tc_default = tc_result.data[0]['Valor_Promedio']
                        else:
                            tc_default = 1000.0
                        tipo_cambio = st.number_input("Tipo de Cambio", value=float(tc_default), min_value=0.0)
                    else:
                        tipo_cambio = 1.0
                
                observaciones = st.text_area("Observaciones")
                
                # Botones de acción
                col_b1, col_b2, col_b3 = st.columns(3)
                
                with col_b1:
                    if st.button("🗑️ Limpiar Carrito", use_container_width=True):
                        st.session_state['carrito'] = []
                        st.rerun()
                
                with col_b3:
                    if st.button("💾 Guardar Remito", type="primary", use_container_width=True):
                        try:
                            # Generar número de remito
                            ultimo_remito = supabase_client.table("novelty_Remitos").select("Numero_Remito").order("Id", desc=True).limit(1).execute()
                            if ultimo_remito.data:
                                ultimo_num = int(ultimo_remito.data[0]['Numero_Remito'].split('-')[-1])
                                nuevo_num = f"REM-{ultimo_num + 1:06d}"
                            else:
                                nuevo_num = "REM-000001"
                            
                            # Crear remito
                            remito_data = {
                                "Numero_Remito": nuevo_num,
                                "Id_Cliente": cliente['Id'],
                                "Fecha_Emision": fecha_emision.isoformat(),
                                "Total_Kg": total_kg,
                                "Total_Rollos": len(st.session_state['carrito']),
                                "Subtotal_ARS": subtotal if moneda == "ARS" else 0,
                                "Subtotal_USD": subtotal if moneda == "USD" else 0,
                                "Descuento_Porcentaje": descuento_pct,
                                "Descuento_Monto": descuento_monto,
                                "Total_ARS": total if moneda == "ARS" else 0,
                                "Total_USD": total if moneda == "USD" else 0,
                                "Moneda": moneda,
                                "Tipo_Cambio_Aplicado": tipo_cambio if moneda == "USD" else None,
                                "Estado": "Pendiente",
                                "Observaciones": observaciones,
                                "Usuario_Creacion": st.session_state.get('user', {}).email if hasattr(st.session_state.get('user'), 'email') else 'Sistema'
                            }
                            
                            remito_result = supabase_client.table("novelty_Remitos").insert(remito_data).execute()
                            
                            if remito_result.data:
                                remito_id = remito_result.data[0]['Id']
                                
                                # Insertar detalles
                                for item in st.session_state['carrito']:
                                    detalle = {
                                        "Id_Remito": remito_id,
                                        "Id_Rollo": item['id'],
                                        "Codigo_Barras": item['codigo'],
                                        "Tipo_Tela": item['tipo'],
                                        "Color": item['color'],
                                        "Peso_Kg": item['peso'],
                                        "Precio_Por_Kg": item['precio_kg'],
                                        "Subtotal": item['subtotal'],
                                        "Descuento_Aplicado": descuento_pct,
                                        "Total": item['subtotal'] * (1 - descuento_pct / 100)
                                    }
                                    supabase_client.table("novelty_Remitos_Detalle").insert(detalle).execute()
                                    
                                    # Actualizar estado del rollo
                                    supabase_client.table("novelty_Rollos").update({
                                        "Estado": "Vendido",
                                        "Fecha_Venta": datetime.now().isoformat()
                                    }).eq("Id", item['id']).execute()
                                
                                # Actualizar saldo del cliente
                                if moneda == "ARS":
                                    nuevo_saldo_ars = cliente.get('Saldo_ARS', 0) + total
                                    supabase_client.table("novelty_Clientes").update({
                                        "Saldo_ARS": nuevo_saldo_ars
                                    }).eq("Id", cliente['Id']).execute()
                                else:
                                    nuevo_saldo_usd = cliente.get('Saldo_USD', 0) + total
                                    supabase_client.table("novelty_Clientes").update({
                                        "Saldo_USD": nuevo_saldo_usd
                                    }).eq("Id", cliente['Id']).execute()
                                
                                # Registrar en cuenta corriente
                                cc_data = {
                                    "Id_Cliente": cliente['Id'],
                                    "Fecha": fecha_emision.isoformat(),
                                    "Tipo_Movimiento": "Venta",
                                    "Id_Remito": remito_id,
                                    "Debe_ARS": total if moneda == "ARS" else 0,
                                    "Debe_USD": total if moneda == "USD" else 0,
                                    "Haber_ARS": 0,
                                    "Haber_USD": 0,
                                    "Saldo_ARS": cliente.get('Saldo_ARS', 0) + (total if moneda == "ARS" else 0),
                                    "Saldo_USD": cliente.get('Saldo_USD', 0) + (total if moneda == "USD" else 0),
                                    "Descripcion": f"Venta - Remito {nuevo_num}",
                                    "Estado": "Pendiente"
                                }
                                supabase_client.table("novelty_Cuentas_Corrientes").insert(cc_data).execute()
                                
                                st.success(f"✅ Remito {nuevo_num} creado exitosamente!")
                                st.balloons()
                                st.session_state['carrito'] = []
                                st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error al guardar remito: {str(e)}")
            
            else:
                st.info("El carrito está vacío. Agregue rollos para crear un remito.")
        
        else:
            st.info("👆 Seleccione un cliente para comenzar")
    
    # ============================================
    # TAB 2: LISTADO DE REMITOS
    # ============================================
    with tab2:
        st.subheader("Listado de Remitos")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            clientes = supabase_client.table("novelty_Clientes").select("*").execute()
            cliente_filter_options = ["Todos"] + [c['Nombre'] for c in clientes.data]
            cliente_filter = st.selectbox("Cliente", cliente_filter_options)
        
        with col2:
            estado_filter = st.selectbox("Estado", ["Todos", "Pendiente", "Entregado", "Facturado", "Cancelado"])
        
        with col3:
            fecha_desde = st.date_input("Desde", value=date(2024, 1, 1))
        
        try:
            query = supabase_client.table("novelty_Remitos").select("""
                *,
                Clientes:Id_Cliente(Nombre)
            """).gte("Fecha_Emision", fecha_desde.isoformat())
            
            if cliente_filter != "Todos":
                cliente_id = next((c["Id"] for c in clientes.data if c["Nombre"] == cliente_filter), None)
                if cliente_id:
                    query = query.eq("Id_Cliente", cliente_id)
            
            if estado_filter != "Todos":
                query = query.eq("Estado", estado_filter)
            
            remitos = query.order("Fecha_Emision", desc=True).execute()
            
            if remitos.data:
                df = pd.DataFrame(remitos.data)
                df["Cliente"] = df["Clientes"].apply(lambda x: x["Nombre"] if x else "N/A")
                
                display_df = df[[
                    "Numero_Remito", "Cliente", "Fecha_Emision", "Total_Kg", "Total_Rollos",
                    "Total_ARS", "Total_USD", "Moneda", "Estado"
                ]]
                
                st.dataframe(display_df, use_container_width=True, height=400)
                
                # Totales
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Remitos", len(df))
                with col2:
                    st.metric("Total Kg", f"{df['Total_Kg'].sum():.2f}")
                with col3:
                    st.metric("Total ARS", f"${df['Total_ARS'].sum():,.2f}")
                with col4:
                    st.metric("Total USD", f"${df['Total_USD'].sum():,.2f}")
            
            else:
                st.info("No se encontraron remitos")
        
        except Exception as e:
            st.error(f"Error al consultar remitos: {str(e)}")
    
    # ============================================
    # TAB 3: ESTADÍSTICAS DE VENTAS
    # ============================================
    with tab3:
        st.subheader("📊 Estadísticas de Ventas")
        
        try:
            # Ventas por tipo de tela
            st.write("**Ventas por Tipo de Tela**")
            
            ventas_tipo = supabase_client.table("novelty_Remitos_Detalle").select("Tipo_Tela, Peso_Kg, Total").execute()
            
            if ventas_tipo.data:
                df_tipo = pd.DataFrame(ventas_tipo.data)
                resumen_tipo = df_tipo.groupby("Tipo_Tela").agg({
                    "Peso_Kg": "sum",
                    "Total": "sum"
                }).reset_index()
                resumen_tipo.columns = ["Tipo de Tela", "Kg Vendidos", "Total Vendido"]
                
                st.dataframe(resumen_tipo, use_container_width=True)
                
                # Gráfico
                st.bar_chart(resumen_tipo.set_index("Tipo de Tela")["Kg Vendidos"])
            
            else:
                st.info("No hay datos de ventas aún")
        
        except Exception as e:
            st.error(f"Error al generar estadísticas: {str(e)}")


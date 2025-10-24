"""
MÓDULO DE CLIENTES
Gestión de clientes, cuentas corrientes y estadísticas
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from supabase_connection import supabase_client

def show():
    st.title("👥 Gestión de Clientes")
    
    tab1, tab2, tab3 = st.tabs([
        "📋 Listado de Clientes",
        "➕ Nuevo Cliente",
        "📊 Estadísticas por Cliente"
    ])
    
    # ============================================
    # TAB 1: LISTADO DE CLIENTES
    # ============================================
    with tab1:
        st.subheader("Clientes Registrados")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            estado_filter = st.selectbox("Estado", ["Todos", "Activo", "Inactivo", "Moroso"])
        with col2:
            buscar = st.text_input("Buscar por nombre", placeholder="Nombre del cliente")
        
        try:
            query = supabase_client.table("novelty_Clientes").select("*")
            
            if estado_filter != "Todos":
                query = query.eq("Estado", estado_filter)
            
            if buscar:
                query = query.ilike("Nombre", f"%{buscar}%")
            
            clientes = query.order("Nombre").execute()
            
            if clientes.data:
                df = pd.DataFrame(clientes.data)
                
                # Métricas
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Clientes", len(df))
                with col2:
                    activos = len(df[df["Estado"] == "Activo"])
                    st.metric("Activos", activos)
                with col3:
                    saldo_total_ars = df["Saldo_ARS"].sum()
                    st.metric("Saldo Total ARS", f"${saldo_total_ars:,.2f}")
                with col4:
                    saldo_total_usd = df["Saldo_USD"].sum()
                    st.metric("Saldo Total USD", f"${saldo_total_usd:,.2f}")
                
                # Tabla de clientes
                display_df = df[[
                    "Nombre", "Razon_Social", "CUIT", "Condicion_Pago",
                    "Descuento_Porcentaje", "Saldo_ARS", "Saldo_USD", "Estado"
                ]]
                
                st.dataframe(display_df, use_container_width=True, height=400)
                
                # Detalles de cliente seleccionado
                st.markdown("---")
                st.subheader("Detalles del Cliente")
                
                cliente_ver = st.selectbox(
                    "Seleccionar cliente para ver detalles",
                    df["Nombre"].tolist()
                )
                
                if cliente_ver:
                    cliente_data = df[df["Nombre"] == cliente_ver].iloc[0]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Nombre:** {cliente_data['Nombre']}")
                        st.write(f"**Razón Social:** {cliente_data.get('Razon_Social', 'N/A')}")
                        st.write(f"**CUIT:** {cliente_data.get('CUIT', 'N/A')}")
                        st.write(f"**Email:** {cliente_data.get('Email', 'N/A')}")
                        st.write(f"**Teléfono:** {cliente_data.get('Telefono', 'N/A')}")
                    
                    with col2:
                        st.write(f"**Condición de Pago:** {cliente_data.get('Condicion_Pago', 'N/A')}")
                        st.write(f"**Descuento:** {cliente_data.get('Descuento_Porcentaje', 0)}%")
                        st.write(f"**Tipo de Cambio:** {cliente_data.get('Tipo_Cambio', 'N/A')}")
                        st.write(f"**Estado:** {cliente_data['Estado']}")
                        st.write(f"**Fecha Alta:** {cliente_data.get('Fecha_Alta', 'N/A')}")
                    
                    # Saldos destacados
                    col_s1, col_s2 = st.columns(2)
                    with col_s1:
                        st.metric("Saldo ARS", f"${cliente_data['Saldo_ARS']:,.2f}")
                    with col_s2:
                        st.metric("Saldo USD", f"${cliente_data['Saldo_USD']:,.2f}")
                    
                    if cliente_data.get('Notas'):
                        st.info(f"**Notas:** {cliente_data['Notas']}")
            
            else:
                st.info("No se encontraron clientes")
        
        except Exception as e:
            st.error(f"Error al consultar clientes: {str(e)}")
    
    # ============================================
    # TAB 2: NUEVO CLIENTE
    # ============================================
    with tab2:
        st.subheader("Registrar Nuevo Cliente")
        
        with st.form("form_nuevo_cliente"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre *")
                razon_social = st.text_input("Razón Social")
                cuit = st.text_input("CUIT", placeholder="XX-XXXXXXXX-X")
                email = st.text_input("Email")
                telefono = st.text_input("Teléfono")
            
            with col2:
                direccion = st.text_area("Dirección")
                condicion_pago = st.selectbox(
                    "Condición de Pago",
                    ["Contado", "15 días", "30 días", "60 días", "90 días"]
                )
                descuento = st.number_input("Descuento (%)", min_value=0.0, max_value=100.0, step=0.5)
                tipo_cambio = st.selectbox(
                    "Tipo de Cambio",
                    ["Celeste", "Oficial", "Blue", "MEP"]
                )
                estado = st.selectbox("Estado", ["Activo", "Inactivo"])
            
            notas = st.text_area("Notas")
            
            submitted = st.form_submit_button("💾 Registrar Cliente", use_container_width=True)
            
            if submitted:
                if not nombre:
                    st.error("❌ El nombre es obligatorio")
                else:
                    try:
                        nuevo_cliente = {
                            "Nombre": nombre,
                            "Razon_Social": razon_social if razon_social else None,
                            "CUIT": cuit if cuit else None,
                            "Direccion": direccion if direccion else None,
                            "Telefono": telefono if telefono else None,
                            "Email": email if email else None,
                            "Condicion_Pago": condicion_pago,
                            "Descuento_Porcentaje": descuento,
                            "Tipo_Cambio": tipo_cambio,
                            "Estado": estado,
                            "Notas": notas if notas else None
                        }
                        
                        result = supabase_client.table("novelty_Clientes").insert(nuevo_cliente).execute()
                        
                        if result.data:
                            st.success(f"✅ Cliente {nombre} registrado exitosamente!")
                            st.balloons()
                        else:
                            st.error("❌ Error al registrar el cliente")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # ============================================
    # TAB 3: ESTADÍSTICAS POR CLIENTE
    # ============================================
    with tab3:
        st.subheader("📊 Estadísticas por Cliente")
        
        try:
            # Obtener datos de la vista
            ventas_cliente = supabase_client.table("novelty_Vista_Ventas_Por_Cliente").select("*").execute()
            
            if ventas_cliente.data:
                df = pd.DataFrame(ventas_cliente.data)
                
                # Top clientes por ventas
                st.write("**Top 10 Clientes por Volumen de Ventas**")
                
                df_sorted = df.sort_values("Total_Ventas_ARS", ascending=False).head(10)
                
                st.dataframe(df_sorted[[
                    "Cliente", "Total_Remitos", "Total_Kg_Vendidos",
                    "Total_Ventas_ARS", "Total_Ventas_USD", "Ultima_Venta"
                ]], use_container_width=True)
                
                # Gráfico de barras
                st.bar_chart(df_sorted.set_index("Cliente")["Total_Kg_Vendidos"])
            
            else:
                st.info("No hay datos de ventas aún")
        
        except Exception as e:
            st.error(f"Error al generar estadísticas: {str(e)}")


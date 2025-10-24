"""
MÓDULO DE DASHBOARD
Panel principal con métricas y visualizaciones del negocio
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from supabase_connection import supabase_client

def show():
    st.title("📊 Dashboard Ejecutivo - Novelty Trend")
    
    # Selector de período
    col_period1, col_period2, col_period3 = st.columns([1, 1, 2])
    
    with col_period1:
        fecha_desde = st.date_input("Desde", value=date.today() - timedelta(days=30))
    with col_period2:
        fecha_hasta = st.date_input("Hasta", value=date.today())
    
    st.markdown("---")
    
    # ============================================
    # SECCIÓN 1: KPIs PRINCIPALES
    # ============================================
    st.subheader("📈 Indicadores Clave")
    
    try:
        # Stock disponible
        stock_disponible = supabase_client.table("novelty_Rollos").select("Peso_Kg, Precio_Venta_Por_Kg").eq("Estado", "Disponible").execute()
        
        # Ventas del período
        ventas_periodo = supabase_client.table("novelty_Remitos").select("*").gte("Fecha_Emision", fecha_desde.isoformat()).lte("Fecha_Emision", fecha_hasta.isoformat()).execute()
        
        # Clientes activos
        clientes_activos = supabase_client.table("novelty_Clientes").select("*").eq("Estado", "Activo").execute()
        
        # Cuentas por cobrar
        saldos_clientes = supabase_client.table("novelty_Vista_Saldos_Clientes").select("*").execute()
        
        # Calcular métricas
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if stock_disponible.data:
                df_stock = pd.DataFrame(stock_disponible.data)
                total_kg = df_stock['Peso_Kg'].sum()
                st.metric("Stock Disponible", f"{total_kg:,.0f} Kg", delta=f"{len(df_stock)} rollos")
            else:
                st.metric("Stock Disponible", "0 Kg")
        
        with col2:
            if ventas_periodo.data:
                df_ventas = pd.DataFrame(ventas_periodo.data)
                total_ventas_ars = df_ventas['Total_ARS'].sum()
                st.metric("Ventas ARS", f"${total_ventas_ars:,.0f}", delta=f"{len(df_ventas)} remitos")
            else:
                st.metric("Ventas ARS", "$0")
        
        with col3:
            if ventas_periodo.data:
                total_ventas_usd = df_ventas['Total_USD'].sum()
                st.metric("Ventas USD", f"${total_ventas_usd:,.0f}")
            else:
                st.metric("Ventas USD", "$0")
        
        with col4:
            if clientes_activos.data:
                st.metric("Clientes Activos", len(clientes_activos.data))
            else:
                st.metric("Clientes Activos", "0")
        
        with col5:
            if saldos_clientes.data:
                df_saldos = pd.DataFrame(saldos_clientes.data)
                total_por_cobrar_ars = df_saldos['Saldo_ARS'].sum()
                total_por_cobrar_usd = df_saldos['Saldo_USD'].sum()
                st.metric("Por Cobrar ARS", f"${total_por_cobrar_ars:,.0f}")
            else:
                st.metric("Por Cobrar", "$0")
        
    except Exception as e:
        st.error(f"Error al cargar KPIs: {str(e)}")
    
    st.markdown("---")
    
    # ============================================
    # SECCIÓN 2: VENTAS POR PERÍODO
    # ============================================
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.subheader("📅 Ventas por Fecha")
        
        try:
            if ventas_periodo.data and len(ventas_periodo.data) > 0:
                df_ventas_fecha = pd.DataFrame(ventas_periodo.data)
                df_ventas_fecha['Fecha'] = pd.to_datetime(df_ventas_fecha['Fecha_Emision'])
                
                ventas_diarias = df_ventas_fecha.groupby('Fecha').agg({
                    'Total_ARS': 'sum',
                    'Total_USD': 'sum',
                    'Total_Kg': 'sum'
                }).reset_index()
                
                fig_ventas = px.line(
                    ventas_diarias,
                    x='Fecha',
                    y='Total_ARS',
                    title='Evolución de Ventas (ARS)',
                    labels={'Total_ARS': 'Ventas (ARS)', 'Fecha': 'Fecha'}
                )
                fig_ventas.update_traces(line_color='#1f77b4', line_width=3)
                st.plotly_chart(fig_ventas, use_container_width=True)
            else:
                st.info("No hay datos de ventas en el período seleccionado")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with col_v2:
        st.subheader("🎯 Top 5 Clientes del Período")
        
        try:
            if ventas_periodo.data and len(ventas_periodo.data) > 0:
                df_ventas_cliente = pd.DataFrame(ventas_periodo.data)
                
                # Obtener nombres de clientes
                clientes_dict = {}
                for venta in ventas_periodo.data:
                    if venta.get('Id_Cliente') and venta['Id_Cliente'] not in clientes_dict:
                        cliente_data = supabase_client.table("novelty_Clientes").select("Nombre").eq("Id", venta['Id_Cliente']).execute()
                        if cliente_data.data:
                            clientes_dict[venta['Id_Cliente']] = cliente_data.data[0]['Nombre']
                
                df_ventas_cliente['Cliente'] = df_ventas_cliente['Id_Cliente'].map(clientes_dict)
                
                top_clientes = df_ventas_cliente.groupby('Cliente').agg({
                    'Total_ARS': 'sum',
                    'Total_USD': 'sum',
                    'Total_Kg': 'sum'
                }).reset_index().sort_values('Total_ARS', ascending=False).head(5)
                
                fig_clientes = px.bar(
                    top_clientes,
                    x='Cliente',
                    y='Total_ARS',
                    title='Ventas por Cliente (ARS)',
                    labels={'Total_ARS': 'Ventas (ARS)', 'Cliente': 'Cliente'},
                    color='Total_ARS',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_clientes, use_container_width=True)
            else:
                st.info("No hay datos de ventas por cliente")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    
    # ============================================
    # SECCIÓN 3: ANÁLISIS DE PRODUCTOS
    # ============================================
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.subheader("📦 Stock por Tipo de Tela")
        
        try:
            stock_vista = supabase_client.table("novelty_Vista_Stock_Disponible").select("*").execute()
            
            if stock_vista.data:
                df_stock_tipo = pd.DataFrame(stock_vista.data)
                
                # Agrupar por tipo
                stock_por_tipo = df_stock_tipo.groupby('Tipo_Tela').agg({
                    'Cantidad_Rollos': 'sum',
                    'Total_Kg': 'sum'
                }).reset_index()
                
                fig_stock = px.pie(
                    stock_por_tipo,
                    values='Total_Kg',
                    names='Tipo_Tela',
                    title='Distribución de Stock (Kg)',
                    color_discrete_sequence=px.colors.sequential.Blues_r
                )
                st.plotly_chart(fig_stock, use_container_width=True)
            else:
                st.info("No hay stock disponible")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with col_p2:
        st.subheader("🛒 Ventas por Tipo de Tela")
        
        try:
            ventas_detalle = supabase_client.table("novelty_Remitos_Detalle").select("*").execute()
            
            if ventas_detalle.data:
                df_detalle = pd.DataFrame(ventas_detalle.data)
                
                ventas_por_tipo = df_detalle.groupby('Tipo_Tela').agg({
                    'Peso_Kg': 'sum',
                    'Total': 'sum'
                }).reset_index().sort_values('Total', ascending=False)
                
                fig_ventas_tipo = px.bar(
                    ventas_por_tipo,
                    x='Tipo_Tela',
                    y='Peso_Kg',
                    title='Kg Vendidos por Tipo',
                    labels={'Peso_Kg': 'Kilogramos', 'Tipo_Tela': 'Tipo de Tela'},
                    color='Peso_Kg',
                    color_continuous_scale='Greens'
                )
                st.plotly_chart(fig_ventas_tipo, use_container_width=True)
            else:
                st.info("No hay ventas registradas")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    
    # ============================================
    # SECCIÓN 4: ESTADO DE COBRANZAS
    # ============================================
    st.subheader("💰 Estado de Cobranzas")
    
    try:
        col_c1, col_c2, col_c3 = st.columns(3)
        
        # Cuentas vencidas
        hoy = date.today()
        cuentas_vencidas = supabase_client.table("novelty_Cuentas_Corrientes").select("*").eq("Estado", "Pendiente").lt("Fecha_Vencimiento", hoy.isoformat()).execute()
        
        # Cuentas por vencer (próximos 7 días)
        proximo_semana = hoy + timedelta(days=7)
        cuentas_por_vencer = supabase_client.table("novelty_Cuentas_Corrientes").select("*").eq("Estado", "Pendiente").gte("Fecha_Vencimiento", hoy.isoformat()).lte("Fecha_Vencimiento", proximo_semana.isoformat()).execute()
        
        # Pagos del mes
        primer_dia_mes = date(hoy.year, hoy.month, 1)
        pagos_mes = supabase_client.table("novelty_Pagos").select("*").gte("Fecha_Pago", primer_dia_mes.isoformat()).execute()
        
        with col_c1:
            if cuentas_vencidas.data:
                df_vencidas = pd.DataFrame(cuentas_vencidas.data)
                total_vencido_ars = df_vencidas['Debe_ARS'].sum()
                total_vencido_usd = df_vencidas['Debe_USD'].sum()
                st.error(f"**🚨 Vencidas**\n\n{len(df_vencidas)} cuentas\n\nARS: ${total_vencido_ars:,.0f}\n\nUSD: ${total_vencido_usd:,.0f}")
            else:
                st.success("✅ Sin cuentas vencidas")
        
        with col_c2:
            if cuentas_por_vencer.data:
                df_por_vencer = pd.DataFrame(cuentas_por_vencer.data)
                total_por_vencer_ars = df_por_vencer['Debe_ARS'].sum()
                total_por_vencer_usd = df_por_vencer['Debe_USD'].sum()
                st.warning(f"**⚠️ Próximos 7 días**\n\n{len(df_por_vencer)} cuentas\n\nARS: ${total_por_vencer_ars:,.0f}\n\nUSD: ${total_por_vencer_usd:,.0f}")
            else:
                st.info("📅 Sin vencimientos próximos")
        
        with col_c3:
            if pagos_mes.data:
                df_pagos = pd.DataFrame(pagos_mes.data)
                total_cobrado_ars = df_pagos['Monto_ARS'].sum()
                total_cobrado_usd = df_pagos['Monto_USD'].sum()
                st.success(f"**💵 Cobrado (mes actual)**\n\n{len(df_pagos)} pagos\n\nARS: ${total_cobrado_ars:,.0f}\n\nUSD: ${total_cobrado_usd:,.0f}")
            else:
                st.info("Sin pagos este mes")
    
    except Exception as e:
        st.error(f"Error al cargar estado de cobranzas: {str(e)}")
    
    st.markdown("---")
    
    # ============================================
    # SECCIÓN 5: ANÁLISIS DE ROTACIÓN
    # ============================================
    st.subheader("⏱️ Tiempo de Rotación de Stock")
    
    try:
        # Calcular tiempo promedio en stock
        rollos_vendidos = supabase_client.table("novelty_Rollos").select("Fecha_Ingreso, Fecha_Venta").eq("Estado", "Vendido").execute()
        
        if rollos_vendidos.data:
            df_rotacion = pd.DataFrame(rollos_vendidos.data)
            df_rotacion['Fecha_Ingreso'] = pd.to_datetime(df_rotacion['Fecha_Ingreso'])
            df_rotacion['Fecha_Venta'] = pd.to_datetime(df_rotacion['Fecha_Venta'])
            df_rotacion['Dias_Stock'] = (df_rotacion['Fecha_Venta'] - df_rotacion['Fecha_Ingreso']).dt.days
            
            # Filtrar valores válidos
            df_rotacion = df_rotacion[df_rotacion['Dias_Stock'] >= 0]
            
            if len(df_rotacion) > 0:
                col_r1, col_r2, col_r3 = st.columns(3)
                
                with col_r1:
                    promedio_dias = df_rotacion['Dias_Stock'].mean()
                    st.metric("Tiempo Promedio en Stock", f"{promedio_dias:.0f} días")
                
                with col_r2:
                    minimo_dias = df_rotacion['Dias_Stock'].min()
                    st.metric("Rotación Mínima", f"{minimo_dias:.0f} días")
                
                with col_r3:
                    maximo_dias = df_rotacion['Dias_Stock'].max()
                    st.metric("Rotación Máxima", f"{maximo_dias:.0f} días")
                
                # Histograma de rotación
                fig_rotacion = px.histogram(
                    df_rotacion,
                    x='Dias_Stock',
                    nbins=20,
                    title='Distribución del Tiempo de Rotación',
                    labels={'Dias_Stock': 'Días en Stock', 'count': 'Cantidad de Rollos'},
                    color_discrete_sequence=['#17becf']
                )
                st.plotly_chart(fig_rotacion, use_container_width=True)
            else:
                st.info("No hay datos suficientes para calcular rotación")
        else:
            st.info("No hay rollos vendidos para analizar rotación")
    
    except Exception as e:
        st.error(f"Error al calcular rotación: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.caption(f"Dashboard actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")


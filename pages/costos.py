"""
MÓDULO DE COSTOS
Gestión de costos por contenedor y cálculo de precios
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from supabase_connection import supabase_client

def show():
    st.title("💲 Gestión de Costos")
    
    tab1, tab2, tab3 = st.tabs([
        "📦 Costos por Contenedor",
        "➕ Registrar Costos",
        "📊 Análisis de Rentabilidad"
    ])
    
    # ============================================
    # TAB 1: COSTOS POR CONTENEDOR
    # ============================================
    with tab1:
        st.subheader("Costos por Contenedor")
        
        try:
            # Obtener contenedores con costos
            costos = supabase_client.table("novelty_Costos_Contenedor").select("""
                *,
                Contenedores:Id_Contenedor(Numero_CTN, Peso_Total_Kg, Cantidad_Rollos)
            """).execute()
            
            if costos.data:
                df = pd.DataFrame(costos.data)
                
                for idx, costo in df.iterrows():
                    ctn = costo["Contenedores"]
                    
                    with st.expander(f"📦 {ctn['Numero_CTN']}", expanded=False):
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Peso Total", f"{ctn.get('Peso_Total_Kg', 0):.2f} Kg")
                        with col2:
                            st.metric("Cantidad Rollos", ctn.get('Cantidad_Rollos', 0))
                        with col3:
                            st.metric("Total Costos USD", f"${costo['Total_Costos_USD']:,.2f}")
                        with col4:
                            st.metric("Costo/Kg USD", f"${costo.get('Costo_Por_Kg_USD', 0):.4f}")
                        
                        st.markdown("---")
                        
                        # Desglose de costos
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.write("**Desglose de Costos (USD):**")
                            st.write(f"- Mercadería: ${costo.get('Costo_Mercaderia_USD', 0):,.2f}")
                            st.write(f"- Flete: ${costo.get('Costo_Flete_USD', 0):,.2f}")
                            st.write(f"- Seguro: ${costo.get('Costo_Seguro_USD', 0):,.2f}")
                            st.write(f"- Derechos Importación: ${costo.get('Derechos_Importacion_USD', 0):,.2f}")
                            st.write(f"- Gastos Despacho: ${costo.get('Gastos_Despacho_USD', 0):,.2f}")
                            st.write(f"- Otros: ${costo.get('Otros_Gastos_USD', 0):,.2f}")
                        
                        with col_b:
                            st.write("**Conversión a ARS:**")
                            tc = costo.get('Tipo_Cambio_Compra', 1)
                            st.write(f"- Tipo de Cambio: ${tc:,.2f}")
                            st.write(f"- Total ARS: ${costo.get('Total_Costos_ARS', 0):,.2f}")
                            
                            if ctn.get('Peso_Total_Kg', 0) > 0:
                                costo_kg_ars = costo.get('Total_Costos_ARS', 0) / ctn['Peso_Total_Kg']
                                st.write(f"- Costo/Kg ARS: ${costo_kg_ars:,.2f}")
                        
                        if costo.get('Notas'):
                            st.info(f"**Notas:** {costo['Notas']}")
            
            else:
                st.info("No hay costos registrados")
        
        except Exception as e:
            st.error(f"Error al consultar costos: {str(e)}")
    
    # ============================================
    # TAB 2: REGISTRAR COSTOS
    # ============================================
    with tab2:
        st.subheader("Registrar Costos de Contenedor")
        
        # Obtener contenedores sin costos asignados
        contenedores = supabase_client.table("novelty_Contenedores").select("*").execute()
        
        ctn_options = {}
        for ctn in contenedores.data:
            # Verificar si ya tiene costos
            costo_existente = supabase_client.table("novelty_Costos_Contenedor").select("Id").eq("Id_Contenedor", ctn['Id']).execute()
            if not costo_existente.data:
                ctn_options[f"{ctn['Numero_CTN']} ({ctn.get('Peso_Total_Kg', 0)} Kg)"] = ctn
        
        if ctn_options:
            with st.form("form_costos"):
                ctn_selected = st.selectbox("Seleccionar Contenedor", list(ctn_options.keys()))
                
                if ctn_selected:
                    contenedor = ctn_options[ctn_selected]
                    
                    st.info(f"""
                    **Contenedor:** {contenedor['Numero_CTN']}  
                    **Peso Total:** {contenedor.get('Peso_Total_Kg', 0)} Kg  
                    **Cantidad Rollos:** {contenedor.get('Cantidad_Rollos', 0)}
                    """)
                    
                    st.markdown("---")
                    st.write("### Costos en USD")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        costo_mercaderia = st.number_input("Costo Mercadería (USD)", min_value=0.0, step=100.0)
                        costo_flete = st.number_input("Costo Flete (USD)", min_value=0.0, step=100.0)
                        costo_seguro = st.number_input("Costo Seguro (USD)", min_value=0.0, step=100.0)
                    
                    with col2:
                        derechos_import = st.number_input("Derechos de Importación (USD)", min_value=0.0, step=100.0)
                        gastos_despacho = st.number_input("Gastos de Despacho (USD)", min_value=0.0, step=100.0)
                        otros_gastos = st.number_input("Otros Gastos (USD)", min_value=0.0, step=100.0)
                    
                    # Calcular total
                    total_usd = (costo_mercaderia + costo_flete + costo_seguro + 
                                derechos_import + gastos_despacho + otros_gastos)
                    
                    st.metric("**Total Costos USD**", f"${total_usd:,.2f}")
                    
                    # Tipo de cambio
                    tc_result = supabase_client.table("novelty_Tipos_Cambio").select("*").eq("Tipo", "Oficial").order("Fecha", desc=True).limit(1).execute()
                    tc_default = tc_result.data[0]['Valor_Promedio'] if tc_result.data else 1000.0
                    
                    tipo_cambio = st.number_input("Tipo de Cambio Compra", value=float(tc_default), min_value=0.0)
                    
                    total_ars = total_usd * tipo_cambio
                    st.metric("**Total Costos ARS**", f"${total_ars:,.2f}")
                    
                    # Costo por Kg
                    if contenedor.get('Peso_Total_Kg', 0) > 0:
                        costo_kg_usd = total_usd / contenedor['Peso_Total_Kg']
                        costo_kg_ars = total_ars / contenedor['Peso_Total_Kg']
                        
                        col_k1, col_k2 = st.columns(2)
                        with col_k1:
                            st.metric("Costo por Kg USD", f"${costo_kg_usd:.4f}")
                        with col_k2:
                            st.metric("Costo por Kg ARS", f"${costo_kg_ars:,.2f}")
                    
                    notas = st.text_area("Notas")
                    
                    submitted = st.form_submit_button("💾 Guardar Costos", use_container_width=True)
                    
                    if submitted:
                        try:
                            costos_data = {
                                "Id_Contenedor": contenedor['Id'],
                                "Costo_Mercaderia_USD": costo_mercaderia,
                                "Costo_Flete_USD": costo_flete,
                                "Costo_Seguro_USD": costo_seguro,
                                "Derechos_Importacion_USD": derechos_import,
                                "Gastos_Despacho_USD": gastos_despacho,
                                "Otros_Gastos_USD": otros_gastos,
                                "Total_Costos_USD": total_usd,
                                "Costo_Por_Kg_USD": costo_kg_usd if contenedor.get('Peso_Total_Kg', 0) > 0 else None,
                                "Tipo_Cambio_Compra": tipo_cambio,
                                "Total_Costos_ARS": total_ars,
                                "Notas": notas if notas else None
                            }
                            
                            result = supabase_client.table("novelty_Costos_Contenedor").insert(costos_data).execute()
                            
                            if result.data:
                                st.success(f"✅ Costos del contenedor {contenedor['Numero_CTN']} registrados!")
                                
                                # Actualizar precio de costo en rollos
                                if contenedor.get('Peso_Total_Kg', 0) > 0:
                                    supabase_client.table("novelty_Rollos").update({
                                        "Precio_Costo_Por_Kg": costo_kg_usd
                                    }).eq("Id_Contenedor", contenedor['Id']).execute()
                                
                                st.balloons()
                        
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        
        else:
            st.warning("⚠️ No hay contenedores disponibles para asignar costos")
            st.info("Todos los contenedores ya tienen costos asignados o no hay contenedores registrados")
    
    # ============================================
    # TAB 3: ANÁLISIS DE RENTABILIDAD
    # ============================================
    with tab3:
        st.subheader("📊 Análisis de Rentabilidad")
        
        try:
            # Obtener rollos vendidos con sus costos
            rollos_vendidos = supabase_client.table("novelty_Rollos").select("""
                *,
                Tipos_Tela:Id_Tipo_Tela(Nombre),
                Colores:Id_Color(Nombre)
            """).eq("Estado", "Vendido").execute()
            
            if rollos_vendidos.data:
                df = pd.DataFrame(rollos_vendidos.data)
                
                # Calcular rentabilidad
                df['Costo_Total'] = df['Peso_Kg'] * df['Precio_Costo_Por_Kg'].fillna(0)
                df['Venta_Total'] = df['Peso_Kg'] * df['Precio_Venta_Por_Kg'].fillna(0)
                df['Ganancia'] = df['Venta_Total'] - df['Costo_Total']
                df['Margen_Pct'] = ((df['Ganancia'] / df['Venta_Total']) * 100).fillna(0)
                
                # Métricas generales
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Rollos Vendidos", len(df))
                with col2:
                    st.metric("Costo Total", f"${df['Costo_Total'].sum():,.2f}")
                with col3:
                    st.metric("Venta Total", f"${df['Venta_Total'].sum():,.2f}")
                with col4:
                    ganancia_total = df['Ganancia'].sum()
                    margen_prom = (ganancia_total / df['Venta_Total'].sum() * 100) if df['Venta_Total'].sum() > 0 else 0
                    st.metric("Ganancia", f"${ganancia_total:,.2f}", delta=f"{margen_prom:.1f}%")
                
                # Rentabilidad por tipo de tela
                st.markdown("---")
                st.write("**Rentabilidad por Tipo de Tela**")
                
                df['Tipo'] = df['Tipos_Tela'].apply(lambda x: x['Nombre'] if x else 'N/A')
                
                rentabilidad_tipo = df.groupby('Tipo').agg({
                    'Id': 'count',
                    'Peso_Kg': 'sum',
                    'Costo_Total': 'sum',
                    'Venta_Total': 'sum',
                    'Ganancia': 'sum'
                }).reset_index()
                
                rentabilidad_tipo.columns = ['Tipo', 'Cantidad', 'Kg Vendidos', 'Costo', 'Venta', 'Ganancia']
                rentabilidad_tipo['Margen %'] = ((rentabilidad_tipo['Ganancia'] / rentabilidad_tipo['Venta']) * 100).round(2)
                
                st.dataframe(rentabilidad_tipo, use_container_width=True)
                
                # Gráfico
                st.bar_chart(rentabilidad_tipo.set_index('Tipo')[['Costo', 'Venta']])
            
            else:
                st.info("No hay rollos vendidos para analizar")
        
        except Exception as e:
            st.error(f"Error al generar análisis: {str(e)}")


"""
MÓDULO DE STOCK/INVENTARIO
Gestión de rollos de tela, códigos de barras, contenedores y stock disponible
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from supabase_connection import supabase_client

def show():
    st.title("📦 Gestión de Stock e Inventario")
    
    # Tabs para diferentes funcionalidades
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Ver Stock", 
        "➕ Registrar Rollos", 
        "📊 Por Contenedor",
        "🔍 Búsqueda por Código"
    ])
    
    # ============================================
    # TAB 1: VER STOCK DISPONIBLE
    # ============================================
    with tab1:
        st.subheader("Stock Disponible")
        
        col1, col2, col3 = st.columns(3)
        
        # Filtros
        with col1:
            # Obtener tipos de tela
            tipos_tela = supabase_client.table("novelty_Tipos_Tela").select("*").eq("Estado", "Activo").execute()
            tipos_options = ["Todos"] + [t["Nombre"] for t in tipos_tela.data]
            tipo_filter = st.selectbox("Filtrar por Tipo de Tela", tipos_options)
        
        with col2:
            # Obtener colores
            colores = supabase_client.table("novelty_Colores").select("*").eq("Estado", "Activo").execute()
            colores_options = ["Todos"] + [c["Nombre"] for c in colores.data]
            color_filter = st.selectbox("Filtrar por Color", colores_options)
        
        with col3:
            estado_filter = st.selectbox("Estado", ["Todos", "Disponible", "Reservado", "Vendido"])
        
        # Consultar stock
        try:
            query = supabase_client.table("novelty_Rollos").select("""
                *,
                novelty_Tipos_Tela:Id_Tipo_Tela(Nombre),
                novelty_Colores:Id_Color(Nombre),
                novelty_Contenedores:Id_Contenedor(Numero_CTN)
            """)
            
            if tipo_filter != "Todos":
                # Buscar ID del tipo
                tipo_id = next((t["Id"] for t in tipos_tela.data if t["Nombre"] == tipo_filter), None)
                if tipo_id:
                    query = query.eq("Id_Tipo_Tela", tipo_id)
            
            if color_filter != "Todos":
                # Buscar ID del color
                color_id = next((c["Id"] for c in colores.data if c["Nombre"] == color_filter), None)
                if color_id:
                    query = query.eq("Id_Color", color_id)
            
            if estado_filter != "Todos":
                query = query.eq("Estado", estado_filter)
            
            result = query.execute()
            
            if result.data:
                # Transformar datos para mejor visualización
                df = pd.DataFrame(result.data)
                
                # Extraer nombres de las relaciones
                df["Tipo_Tela"] = df["Tipos_Tela"].apply(lambda x: x["Nombre"] if x else "N/A")
                df["Color"] = df["Colores"].apply(lambda x: x["Nombre"] if x else "N/A")
                df["CTN"] = df["Contenedores"].apply(lambda x: x["Numero_CTN"] if x else "N/A")
                
                # Seleccionar columnas relevantes
                display_df = df[[
                    "Codigo_Barras", "Numero_Rollo", "Tipo_Tela", "Color", 
                    "Peso_Kg", "CTN", "Ubicacion", "Estado"
                ]]
                
                # Métricas generales
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Rollos", len(df))
                with col2:
                    st.metric("Peso Total (Kg)", f"{df['Peso_Kg'].sum():.2f}")
                with col3:
                    disponibles = len(df[df["Estado"] == "Disponible"])
                    st.metric("Disponibles", disponibles)
                with col4:
                    if df["Precio_Venta_Por_Kg"].notna().any():
                        valor_estimado = (df["Peso_Kg"] * df["Precio_Venta_Por_Kg"]).sum()
                        st.metric("Valor Estimado", f"${valor_estimado:,.2f}")
                
                st.dataframe(display_df, use_container_width=True, height=400)
                
                # Resumen por tipo y color
                st.subheader("📊 Resumen por Tipo y Color")
                resumen = df.groupby(["Tipo_Tela", "Color"]).agg({
                    "Id": "count",
                    "Peso_Kg": "sum"
                }).rename(columns={"Id": "Cantidad", "Peso_Kg": "Total_Kg"}).reset_index()
                st.dataframe(resumen, use_container_width=True)
                
            else:
                st.info("No se encontraron rollos con los filtros seleccionados")
                
        except Exception as e:
            st.error(f"Error al consultar stock: {str(e)}")
    
    # ============================================
    # TAB 2: REGISTRAR NUEVOS ROLLOS
    # ============================================
    with tab2:
        st.subheader("Registrar Nuevos Rollos")
        
        with st.form("form_nuevo_rollo"):
            col1, col2 = st.columns(2)
            
            with col1:
                codigo_barras = st.text_input("Código de Barras *", placeholder="Escanear o ingresar")
                numero_rollo = st.text_input("Número de Rollo *")
                
                # Obtener contenedores
                contenedores = supabase_client.table("novelty_Contenedores").select("Id, Numero_CTN").execute()
                contenedor_options = {f"{c['Numero_CTN']}": c["Id"] for c in contenedores.data}
                contenedor_selected = st.selectbox("Contenedor (CTN) *", ["Seleccionar..."] + list(contenedor_options.keys()))
                
                # Tipos de tela
                tipos_tela = supabase_client.table("novelty_Tipos_Tela").select("*").eq("Estado", "Activo").execute()
                tipo_options = {t["Nombre"]: t["Id"] for t in tipos_tela.data}
                tipo_selected = st.selectbox("Tipo de Tela *", ["Seleccionar..."] + list(tipo_options.keys()))
            
            with col2:
                # Colores
                colores = supabase_client.table("novelty_Colores").select("*").eq("Estado", "Activo").execute()
                color_options = {c["Nombre"]: c["Id"] for c in colores.data}
                color_selected = st.selectbox("Color *", ["Seleccionar..."] + list(color_options.keys()))
                
                peso_kg = st.number_input("Peso (Kg) *", min_value=0.01, step=0.01)
                metros = st.number_input("Metros", min_value=0.0, step=0.1)
                ubicacion = st.text_input("Ubicación en Depósito", placeholder="Ej: Estante A-3")
                
            col3, col4 = st.columns(2)
            with col3:
                precio_costo = st.number_input("Precio Costo por Kg", min_value=0.0, step=0.01)
            with col4:
                precio_venta = st.number_input("Precio Venta por Kg", min_value=0.0, step=0.01)
            
            lote = st.text_input("Lote/Batch")
            notas = st.text_area("Notas")
            
            submitted = st.form_submit_button("💾 Registrar Rollo", use_container_width=True)
            
            if submitted:
                # Validaciones
                if not codigo_barras or not numero_rollo:
                    st.error("❌ Código de barras y número de rollo son obligatorios")
                elif contenedor_selected == "Seleccionar..." or tipo_selected == "Seleccionar..." or color_selected == "Seleccionar...":
                    st.error("❌ Debe seleccionar contenedor, tipo de tela y color")
                elif peso_kg <= 0:
                    st.error("❌ El peso debe ser mayor a 0")
                else:
                    try:
                        # Verificar si el código de barras ya existe
                        check = supabase_client.table("novelty_Rollos").select("Id").eq("Codigo_Barras", codigo_barras).execute()
                        if check.data:
                            st.error(f"❌ Ya existe un rollo con el código de barras {codigo_barras}")
                        else:
                            # Insertar rollo
                            nuevo_rollo = {
                                "Codigo_Barras": codigo_barras,
                                "Numero_Rollo": numero_rollo,
                                "Id_Contenedor": contenedor_options[contenedor_selected],
                                "Id_Tipo_Tela": tipo_options[tipo_selected],
                                "Id_Color": color_options[color_selected],
                                "Peso_Kg": peso_kg,
                                "Peso_Inicial_Kg": peso_kg,
                                "Metros": metros if metros > 0 else None,
                                "Ubicacion": ubicacion,
                                "Estado": "Disponible",
                                "Precio_Costo_Por_Kg": precio_costo if precio_costo > 0 else None,
                                "Precio_Venta_Por_Kg": precio_venta if precio_venta > 0 else None,
                                "Lote": lote if lote else None,
                                "Notas": notas if notas else None
                            }
                            
                            result = supabase_client.table("novelty_Rollos").insert(nuevo_rollo).execute()
                            
                            if result.data:
                                st.success(f"✅ Rollo {codigo_barras} registrado exitosamente!")
                                st.balloons()
                                
                                # Actualizar contador de rollos en contenedor
                                update_container_count(contenedor_options[contenedor_selected])
                            else:
                                st.error("❌ Error al registrar el rollo")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # ============================================
    # TAB 3: STOCK POR CONTENEDOR
    # ============================================
    with tab3:
        st.subheader("Stock por Contenedor")
        
        try:
            # Obtener contenedores con información
            contenedores = supabase_client.table("novelty_Contenedores").select("""
                *,
                novelty_Proveedores:Id_Proveedor(Nombre)
            """).execute()
            
            if contenedores.data:
                for ctn in contenedores.data:
                    prov_nombre = ctn.get('novelty_Proveedores', {}).get('Nombre', 'Sin proveedor')
                    with st.expander(f"📦 {ctn['Numero_CTN']} - {prov_nombre}"):
                        col1, col2, col3, col4 = st.columns(4)
                        
                        # Obtener rollos del contenedor
                        rollos = supabase_client.table("novelty_Rollos").select("*").eq("Id_Contenedor", ctn["Id"]).execute()
                        
                        disponibles = len([r for r in rollos.data if r["Estado"] == "Disponible"])
                        vendidos = len([r for r in rollos.data if r["Estado"] == "Vendido"])
                        peso_total = sum([r["Peso_Kg"] for r in rollos.data])
                        
                        with col1:
                            st.metric("Total Rollos", len(rollos.data))
                        with col2:
                            st.metric("Disponibles", disponibles)
                        with col3:
                            st.metric("Vendidos", vendidos)
                        with col4:
                            st.metric("Peso Total (Kg)", f"{peso_total:.2f}")
                        
                        # Información del contenedor
                        st.write(f"**Proveedor:** {ctn['Proveedores']['Nombre'] if ctn.get('Proveedores') else 'N/A'}")
                        st.write(f"**Fecha Arribo:** {ctn.get('Fecha_Arribo', 'N/A')}")
                        st.write(f"**Puerto Origen:** {ctn.get('Puerto_Origen', 'N/A')}")
                        
                        if rollos.data:
                            df_rollos = pd.DataFrame(rollos.data)
                            st.dataframe(
                                df_rollos[["Codigo_Barras", "Numero_Rollo", "Peso_Kg", "Estado", "Ubicacion"]],
                                use_container_width=True
                            )
            else:
                st.info("No hay contenedores registrados")
        
        except Exception as e:
            st.error(f"Error al consultar contenedores: {str(e)}")
    
    # ============================================
    # TAB 4: BÚSQUEDA POR CÓDIGO DE BARRAS
    # ============================================
    with tab4:
        st.subheader("🔍 Búsqueda Rápida por Código de Barras")
        
        codigo_buscar = st.text_input("Ingrese código de barras", placeholder="Escanear o escribir código")
        
        if codigo_buscar:
            try:
                result = supabase_client.table("novelty_Rollos").select("""
                    *,
                    novelty_Tipos_Tela:Id_Tipo_Tela(Nombre, Descripcion),
                    novelty_Colores:Id_Color(Nombre),
                    novelty_Contenedores:Id_Contenedor(Numero_CTN, Fecha_Arribo)
                """).eq("Codigo_Barras", codigo_buscar).execute()
                
                if result.data:
                    rollo = result.data[0]
                    
                    # Mostrar información en cards
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.info(f"""
                        **Código:** {rollo['Codigo_Barras']}  
                        **Rollo #:** {rollo['Numero_Rollo']}  
                        **Estado:** {rollo['Estado']}
                        """)
                    
                    with col2:
                        st.success(f"""
                        **Tipo:** {rollo['Tipos_Tela']['Nombre'] if rollo.get('Tipos_Tela') else 'N/A'}  
                        **Color:** {rollo['Colores']['Nombre'] if rollo.get('Colores') else 'N/A'}  
                        **Peso:** {rollo['Peso_Kg']} Kg
                        """)
                    
                    with col3:
                        st.warning(f"""
                        **CTN:** {rollo['Contenedores']['Numero_CTN'] if rollo.get('Contenedores') else 'N/A'}  
                        **Ubicación:** {rollo.get('Ubicacion', 'N/A')}  
                        **Precio/Kg:** ${rollo.get('Precio_Venta_Por_Kg', 0):.2f}
                        """)
                    
                    # Opciones de acción
                    st.markdown("---")
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        if st.button("✏️ Editar Rollo", use_container_width=True):
                            st.session_state['editing_rollo'] = rollo['Id']
                            st.info("Función de edición en desarrollo")
                    
                    with col_b:
                        if rollo['Estado'] == 'Disponible':
                            if st.button("🛒 Marcar como Vendido", use_container_width=True):
                                st.info("Use el módulo de Ventas para registrar la venta")
                    
                    with col_c:
                        if st.button("🗑️ Eliminar Rollo", use_container_width=True):
                            st.warning("⚠️ Esta acción requiere confirmación")
                
                else:
                    st.warning(f"No se encontró ningún rollo con el código {codigo_buscar}")
            
            except Exception as e:
                st.error(f"Error en la búsqueda: {str(e)}")


def update_container_count(contenedor_id):
    """Actualiza el contador de rollos en un contenedor"""
    try:
        # Contar rollos del contenedor
        rollos = supabase_client.table("novelty_Rollos").select("Peso_Kg").eq("Id_Contenedor", contenedor_id).execute()
        
        cantidad = len(rollos.data)
        peso_total = sum([r["Peso_Kg"] for r in rollos.data])
        
        # Actualizar contenedor
        supabase_client.table("novelty_Contenedores").update({
            "Cantidad_Rollos": cantidad,
            "Peso_Total_Kg": peso_total
        }).eq("Id", contenedor_id).execute()
    except Exception as e:
        print(f"Error actualizando contador de contenedor: {e}")

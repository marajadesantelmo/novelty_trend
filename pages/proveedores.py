"""
MÓDULO DE PROVEEDORES
Gestión de proveedores y carga de datos de origen
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from supabase_connection import supabase_client

def show():
    st.title("🚚 Gestión de Proveedores")
    
    tab1, tab2, tab3 = st.tabs([
        "📋 Proveedores",
        "➕ Nuevo Proveedor",
        "📦 Contenedores"
    ])
    
    # ============================================
    # TAB 1: LISTADO DE PROVEEDORES
    # ============================================
    with tab1:
        st.subheader("Proveedores Registrados")
        
        try:
            proveedores = supabase_client.table("novelty_Proveedores").select("*").order("Nombre").execute()
            
            if proveedores.data:
                df = pd.DataFrame(proveedores.data)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Proveedores", len(df))
                with col2:
                    activos = len(df[df["Estado"] == "Activo"])
                    st.metric("Activos", activos)
                
                display_df = df[[
                    "Nombre", "Razon_Social", "Pais_Origen", "Email", "Telefono", "Estado"
                ]]
                
                st.dataframe(display_df, use_container_width=True, height=300)
                
                # Detalles
                st.markdown("---")
                proveedor_ver = st.selectbox("Ver detalles de", df["Nombre"].tolist())
                
                if proveedor_ver:
                    prov_data = df[df["Nombre"] == proveedor_ver].iloc[0]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Nombre:** {prov_data['Nombre']}")
                        st.write(f"**Razón Social:** {prov_data.get('Razon_Social', 'N/A')}")
                        st.write(f"**CUIT:** {prov_data.get('CUIT', 'N/A')}")
                        st.write(f"**País:** {prov_data.get('Pais_Origen', 'N/A')}")
                    
                    with col2:
                        st.write(f"**Email:** {prov_data.get('Email', 'N/A')}")
                        st.write(f"**Teléfono:** {prov_data.get('Telefono', 'N/A')}")
                        st.write(f"**Contacto:** {prov_data.get('Contacto', 'N/A')}")
                        st.write(f"**Estado:** {prov_data['Estado']}")
                    
                    # Contenedores del proveedor
                    contenedores = supabase_client.table("novelty_Contenedores").select("*").eq("Id_Proveedor", prov_data['Id']).execute()
                    
                    if contenedores.data:
                        st.write(f"**Contenedores del proveedor:** {len(contenedores.data)}")
                        df_ctn = pd.DataFrame(contenedores.data)
                        st.dataframe(df_ctn[["Numero_CTN", "Fecha_Arribo", "Cantidad_Rollos", "Peso_Total_Kg", "Estado"]], use_container_width=True)
            
            else:
                st.info("No hay proveedores registrados")
        
        except Exception as e:
            st.error(f"Error al consultar proveedores: {str(e)}")
    
    # ============================================
    # TAB 2: NUEVO PROVEEDOR
    # ============================================
    with tab2:
        st.subheader("Registrar Nuevo Proveedor")
        
        with st.form("form_proveedor"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre *")
                razon_social = st.text_input("Razón Social")
                cuit = st.text_input("CUIT")
                pais_origen = st.text_input("País de Origen")
            
            with col2:
                email = st.text_input("Email")
                telefono = st.text_input("Teléfono")
                contacto = st.text_input("Persona de Contacto")
                estado = st.selectbox("Estado", ["Activo", "Inactivo"])
            
            direccion = st.text_area("Dirección")
            condiciones_pago = st.text_area("Condiciones de Pago")
            notas = st.text_area("Notas")
            
            submitted = st.form_submit_button("💾 Registrar Proveedor", use_container_width=True)
            
            if submitted:
                if not nombre:
                    st.error("❌ El nombre es obligatorio")
                else:
                    try:
                        nuevo_prov = {
                            "Nombre": nombre,
                            "Razon_Social": razon_social if razon_social else None,
                            "CUIT": cuit if cuit else None,
                            "Pais_Origen": pais_origen if pais_origen else None,
                            "Direccion": direccion if direccion else None,
                            "Telefono": telefono if telefono else None,
                            "Email": email if email else None,
                            "Contacto": contacto if contacto else None,
                            "Condiciones_Pago": condiciones_pago if condiciones_pago else None,
                            "Estado": estado,
                            "Notas": notas if notas else None
                        }
                        
                        result = supabase_client.table("novelty_Proveedores").insert(nuevo_prov).execute()
                        
                        if result.data:
                            st.success(f"✅ Proveedor {nombre} registrado exitosamente!")
                            st.balloons()
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # ============================================
    # TAB 3: GESTIÓN DE CONTENEDORES
    # ============================================
    with tab3:
        st.subheader("Gestión de Contenedores")
        
        col_tab1, col_tab2 = st.columns([1, 1])
        
        with col_tab1:
            st.write("### Registrar Nuevo Contenedor")
            
            with st.form("form_contenedor"):
                numero_ctn = st.text_input("Número CTN *")
                
                proveedores = supabase_client.table("novelty_Proveedores").select("*").eq("Estado", "Activo").execute()
                prov_options = {p["Nombre"]: p["Id"] for p in proveedores.data}
                proveedor_sel = st.selectbox("Proveedor", list(prov_options.keys()))
                
                fecha_arribo = st.date_input("Fecha de Arribo")
                puerto_origen = st.text_input("Puerto de Origen")
                puerto_destino = st.text_input("Puerto de Destino")
                estado_ctn = st.selectbox("Estado", ["En Tránsito", "Arribado", "Despachado"])
                notas_ctn = st.text_area("Notas")
                
                submit_ctn = st.form_submit_button("💾 Registrar Contenedor", use_container_width=True)
                
                if submit_ctn:
                    if not numero_ctn:
                        st.error("❌ El número CTN es obligatorio")
                    else:
                        try:
                            nuevo_ctn = {
                                "Numero_CTN": numero_ctn,
                                "Id_Proveedor": prov_options[proveedor_sel],
                                "Fecha_Arribo": fecha_arribo.isoformat(),
                                "Puerto_Origen": puerto_origen if puerto_origen else None,
                                "Puerto_Destino": puerto_destino if puerto_destino else None,
                                "Estado": estado_ctn,
                                "Notas": notas_ctn if notas_ctn else None
                            }
                            
                            result = supabase_client.table("novelty_Contenedores").insert(nuevo_ctn).execute()
                            
                            if result.data:
                                st.success(f"✅ Contenedor {numero_ctn} registrado!")
                                st.balloons()
                        
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        
        with col_tab2:
            st.write("### Listado de Contenedores")
            
            try:
                contenedores = supabase_client.table("novelty_Contenedores").select("""
                    *,
                    Proveedores:Id_Proveedor(Nombre)
                """).order("Fecha_Arribo", desc=True).execute()
                
                if contenedores.data:
                    df_ctn = pd.DataFrame(contenedores.data)
                    df_ctn["Proveedor"] = df_ctn["Proveedores"].apply(lambda x: x["Nombre"] if x else "N/A")
                    
                    display_ctn = df_ctn[[
                        "Numero_CTN", "Proveedor", "Fecha_Arribo", "Cantidad_Rollos", "Estado"
                    ]]
                    
                    st.dataframe(display_ctn, use_container_width=True, height=400)
                
                else:
                    st.info("No hay contenedores registrados")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")


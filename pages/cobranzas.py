"""
MÓDULO DE COBRANZAS
Gestión de pagos, cuentas corrientes y seguimiento de vencimientos
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from supabase_connection import supabase_client

def show():
    st.title("💰 Gestión de Cobranzas")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "💵 Registrar Pago",
        "📋 Historial de Pagos",
        "📊 Cuenta Corriente",
        "⚠️ Vencimientos"
    ])
    
    # ============================================
    # TAB 1: REGISTRAR PAGO
    # ============================================
    with tab1:
        st.subheader("Registrar Nuevo Pago")
        
        # Selector de cliente
        clientes = supabase_client.table("novelty_Clientes").select("*").eq("Estado", "Activo").execute()
        cliente_options = {f"{c['Nombre']} (ARS: ${c.get('Saldo_ARS', 0):,.2f} | USD: ${c.get('Saldo_USD', 0):,.2f})": c for c in clientes.data}
        
        cliente_selected = st.selectbox(
            "Seleccionar Cliente *",
            ["Seleccionar..."] + list(cliente_options.keys())
        )
        
        if cliente_selected != "Seleccionar...":
            cliente = cliente_options[cliente_selected]
            
            # Mostrar saldos
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Saldo ARS", f"${cliente.get('Saldo_ARS', 0):,.2f}")
            with col2:
                st.metric("Saldo USD", f"${cliente.get('Saldo_USD', 0):,.2f}")
            
            st.markdown("---")
            
            with st.form("form_pago"):
                col1, col2 = st.columns(2)
                
                with col1:
                    fecha_pago = st.date_input("Fecha de Pago", value=date.today())
                    moneda = st.selectbox("Moneda *", ["ARS", "USD"])
                    monto = st.number_input(f"Monto ({moneda}) *", min_value=0.01, step=0.01)
                    
                    if moneda == "USD":
                        tc_result = supabase_client.table("novelty_Tipos_Cambio").select("*").eq("Tipo", "Celeste").order("Fecha", desc=True).limit(1).execute()
                        tc_default = tc_result.data[0]['Valor_Promedio'] if tc_result.data else 1000.0
                        tipo_cambio = st.number_input("Tipo de Cambio", value=float(tc_default), min_value=0.0)
                    else:
                        tipo_cambio = None
                
                with col2:
                    metodo_pago = st.selectbox(
                        "Método de Pago *",
                        ["Efectivo", "Transferencia", "Cheque", "Tarjeta de Crédito", "Tarjeta de Débito"]
                    )
                    referencia = st.text_input("Referencia", placeholder="Nº de cheque, transferencia, etc.")
                    
                    if metodo_pago == "Cheque":
                        fecha_vencimiento = st.date_input("Fecha de Vencimiento")
                    else:
                        fecha_vencimiento = None
                    
                    estado_pago = st.selectbox("Estado", ["Confirmado", "Pendiente", "Rechazado"])
                
                # Remitos pendientes del cliente
                remitos_pendientes = supabase_client.table("novelty_Remitos").select("*").eq("Id_Cliente", cliente['Id']).in_("Estado", ["Pendiente", "Entregado"]).execute()
                
                if remitos_pendientes.data:
                    st.write("**Remitos Pendientes:**")
                    remito_options = {f"{r['Numero_Remito']} - ${r.get('Total_ARS', 0) + r.get('Total_USD', 0):,.2f}": r for r in remitos_pendientes.data}
                    remito_selected = st.selectbox("Asociar a Remito (opcional)", ["Ninguno"] + list(remito_options.keys()))
                else:
                    remito_selected = "Ninguno"
                
                observaciones = st.text_area("Observaciones")
                
                submitted = st.form_submit_button("💾 Registrar Pago", use_container_width=True)
                
                if submitted:
                    if monto <= 0:
                        st.error("❌ El monto debe ser mayor a 0")
                    else:
                        try:
                            # Generar número de recibo
                            ultimo_pago = supabase_client.table("novelty_Pagos").select("Numero_Recibo").order("Id", desc=True).limit(1).execute()
                            if ultimo_pago.data and ultimo_pago.data[0].get('Numero_Recibo'):
                                ultimo_num = int(ultimo_pago.data[0]['Numero_Recibo'].split('-')[-1])
                                nuevo_recibo = f"REC-{ultimo_num + 1:06d}"
                            else:
                                nuevo_recibo = "REC-000001"
                            
                            # Obtener ID del remito si fue seleccionado
                            id_remito = None
                            if remito_selected != "Ninguno":
                                id_remito = remito_options[remito_selected]['Id']
                            
                            # Insertar pago
                            pago_data = {
                                "Id_Cliente": cliente['Id'],
                                "Id_Remito": id_remito,
                                "Numero_Recibo": nuevo_recibo,
                                "Fecha_Pago": fecha_pago.isoformat(),
                                "Monto_ARS": monto if moneda == "ARS" else 0,
                                "Monto_USD": monto if moneda == "USD" else 0,
                                "Moneda": moneda,
                                "Tipo_Cambio": tipo_cambio,
                                "Metodo_Pago": metodo_pago,
                                "Referencia": referencia if referencia else None,
                                "Estado": estado_pago,
                                "Fecha_Vencimiento": fecha_vencimiento.isoformat() if fecha_vencimiento else None,
                                "Observaciones": observaciones if observaciones else None,
                                "Usuario_Registro": st.session_state.get('user', {}).email if hasattr(st.session_state.get('user'), 'email') else 'Sistema'
                            }
                            
                            pago_result = supabase_client.table("novelty_Pagos").insert(pago_data).execute()
                            
                            if pago_result.data:
                                # Actualizar saldo del cliente
                                if moneda == "ARS":
                                    nuevo_saldo = cliente.get('Saldo_ARS', 0) - monto
                                    supabase_client.table("novelty_Clientes").update({
                                        "Saldo_ARS": nuevo_saldo
                                    }).eq("Id", cliente['Id']).execute()
                                else:
                                    nuevo_saldo = cliente.get('Saldo_USD', 0) - monto
                                    supabase_client.table("novelty_Clientes").update({
                                        "Saldo_USD": nuevo_saldo
                                    }).eq("Id", cliente['Id']).execute()
                                
                                # Registrar en cuenta corriente
                                cc_data = {
                                    "Id_Cliente": cliente['Id'],
                                    "Fecha": fecha_pago.isoformat(),
                                    "Tipo_Movimiento": "Pago",
                                    "Id_Pago": pago_result.data[0]['Id'],
                                    "Debe_ARS": 0,
                                    "Haber_ARS": monto if moneda == "ARS" else 0,
                                    "Debe_USD": 0,
                                    "Haber_USD": monto if moneda == "USD" else 0,
                                    "Saldo_ARS": cliente.get('Saldo_ARS', 0) - (monto if moneda == "ARS" else 0),
                                    "Saldo_USD": cliente.get('Saldo_USD', 0) - (monto if moneda == "USD" else 0),
                                    "Descripcion": f"Pago - Recibo {nuevo_recibo}",
                                    "Estado": "Pagado"
                                }
                                supabase_client.table("novelty_Cuentas_Corrientes").insert(cc_data).execute()
                                
                                st.success(f"✅ Pago {nuevo_recibo} registrado exitosamente!")
                                st.balloons()
                        
                        except Exception as e:
                            st.error(f"❌ Error al registrar pago: {str(e)}")
        
        else:
            st.info("👆 Seleccione un cliente para registrar un pago")
    
    # ============================================
    # TAB 2: HISTORIAL DE PAGOS
    # ============================================
    with tab2:
        st.subheader("Historial de Pagos")
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_desde = st.date_input("Desde", value=date.today() - timedelta(days=30))
        with col2:
            estado_filter = st.selectbox("Estado", ["Todos", "Confirmado", "Pendiente", "Rechazado"], key="estado_pago")
        
        try:
            query = supabase_client.table("novelty_Pagos").select("""
                *,
                Clientes:Id_Cliente(Nombre)
            """).gte("Fecha_Pago", fecha_desde.isoformat())
            
            if estado_filter != "Todos":
                query = query.eq("Estado", estado_filter)
            
            pagos = query.order("Fecha_Pago", desc=True).execute()
            
            if pagos.data:
                df = pd.DataFrame(pagos.data)
                df["Cliente"] = df["Clientes"].apply(lambda x: x["Nombre"] if x else "N/A")
                
                display_df = df[[
                    "Numero_Recibo", "Cliente", "Fecha_Pago", "Monto_ARS", "Monto_USD",
                    "Moneda", "Metodo_Pago", "Estado"
                ]]
                
                st.dataframe(display_df, use_container_width=True, height=400)
                
                # Totales
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Pagos", len(df))
                with col2:
                    st.metric("Total ARS", f"${df['Monto_ARS'].sum():,.2f}")
                with col3:
                    st.metric("Total USD", f"${df['Monto_USD'].sum():,.2f}")
            
            else:
                st.info("No se encontraron pagos")
        
        except Exception as e:
            st.error(f"Error al consultar pagos: {str(e)}")
    
    # ============================================
    # TAB 3: CUENTA CORRIENTE
    # ============================================
    with tab3:
        st.subheader("Consulta de Cuenta Corriente")
        
        clientes = supabase_client.table("novelty_Clientes").select("*").execute()
        cliente_cc_options = {c['Nombre']: c for c in clientes.data}
        
        cliente_cc = st.selectbox("Seleccionar Cliente", list(cliente_cc_options.keys()))
        
        if cliente_cc:
            cliente_data = cliente_cc_options[cliente_cc]
            
            # Saldos actuales
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Saldo Actual ARS", f"${cliente_data.get('Saldo_ARS', 0):,.2f}")
            with col2:
                st.metric("Saldo Actual USD", f"${cliente_data.get('Saldo_USD', 0):,.2f}")
            
            # Movimientos
            try:
                movimientos = supabase_client.table("novelty_Cuentas_Corrientes").select("*").eq("Id_Cliente", cliente_data['Id']).order("Fecha", desc=True).execute()
                
                if movimientos.data:
                    df_mov = pd.DataFrame(movimientos.data)
                    
                    display_df_mov = df_mov[[
                        "Fecha", "Tipo_Movimiento", "Descripcion",
                        "Debe_ARS", "Haber_ARS", "Saldo_ARS",
                        "Debe_USD", "Haber_USD", "Saldo_USD", "Estado"
                    ]]
                    
                    st.dataframe(display_df_mov, use_container_width=True, height=400)
                
                else:
                    st.info("No hay movimientos en la cuenta corriente")
            
            except Exception as e:
                st.error(f"Error al consultar cuenta corriente: {str(e)}")
    
    # ============================================
    # TAB 4: VENCIMIENTOS
    # ============================================
    with tab4:
        st.subheader("⚠️ Seguimiento de Vencimientos")
        
        try:
            # Cuentas pendientes con vencimiento próximo
            hoy = date.today()
            proximo_mes = hoy + timedelta(days=30)
            
            vencimientos = supabase_client.table("novelty_Cuentas_Corrientes").select("""
                *,
                Clientes:Id_Cliente(Nombre, Telefono, Email)
            """).eq("Estado", "Pendiente").lte("Fecha_Vencimiento", proximo_mes.isoformat()).order("Fecha_Vencimiento").execute()
            
            if vencimientos.data:
                df_venc = pd.DataFrame(vencimientos.data)
                df_venc["Cliente"] = df_venc["Clientes"].apply(lambda x: x["Nombre"] if x else "N/A")
                df_venc["Dias_Hasta_Venc"] = pd.to_datetime(df_venc["Fecha_Vencimiento"]).apply(
                    lambda x: (x.date() - hoy).days if pd.notna(x) else None
                )
                
                # Vencidos
                vencidos = df_venc[df_venc["Dias_Hasta_Venc"] < 0]
                if not vencidos.empty:
                    st.error(f"🚨 **{len(vencidos)} cuentas vencidas**")
                    st.dataframe(vencidos[[
                        "Cliente", "Descripcion", "Fecha_Vencimiento", "Debe_ARS", "Debe_USD", "Dias_Hasta_Venc"
                    ]], use_container_width=True)
                
                # Por vencer
                por_vencer = df_venc[(df_venc["Dias_Hasta_Venc"] >= 0) & (df_venc["Dias_Hasta_Venc"] <= 7)]
                if not por_vencer.empty:
                    st.warning(f"⚠️ **{len(por_vencer)} cuentas vencen en los próximos 7 días**")
                    st.dataframe(por_vencer[[
                        "Cliente", "Descripcion", "Fecha_Vencimiento", "Debe_ARS", "Debe_USD", "Dias_Hasta_Venc"
                    ]], use_container_width=True)
                
                # Próximos 30 días
                proximos = df_venc[df_venc["Dias_Hasta_Venc"] > 7]
                if not proximos.empty:
                    st.info(f"📅 **{len(proximos)} cuentas vencen en los próximos 30 días**")
                    st.dataframe(proximos[[
                        "Cliente", "Descripcion", "Fecha_Vencimiento", "Debe_ARS", "Debe_USD", "Dias_Hasta_Venc"
                    ]], use_container_width=True)
            
            else:
                st.success("✅ No hay vencimientos próximos")
        
        except Exception as e:
            st.error(f"Error al consultar vencimientos: {str(e)}")


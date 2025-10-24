import streamlit as st
from supabase_connection import login_user, logout_user

# Configuración de la página
st.set_page_config(
    page_title="Novelty Trend | ERP",
    page_icon="📊",
    layout="wide"
)

# Inicialización de estado de sesión
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None
 

def handle_logout():
    st.session_state['authenticated'] = False
    st.session_state['user'] = None
    logout_user()

# Página de login
if not st.session_state['authenticated']:
    st.title("🔐 Acceso al Sistema")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar Sesión")

    if submitted:
        try:
            user = login_user(email, password)
            if user:
                st.session_state['authenticated'] = True
                st.session_state['user'] = user
                st.success('Login exitoso!')
                st.rerun()
            else:
                st.error('Credenciales incorrectas')
        except Exception as e:
            st.error(f'Error al iniciar sesión: {str(e)}')

else:
    # Menú de navegación actualizado para ERP Textil
    NAV_ITEMS = {
        "Dashboard": {
            "icon": "📊",
        },
        "Stock": {
            "icon": "📦",
        },
        "Ventas": {
            "icon": "🛒",
        },
        "Clientes": {
            "icon": "👥",
        },
        "Cobranzas": {
            "icon": "💰",
        },
        "Proveedores": {
            "icon": "🚚",
        },
        "Costos": {
            "icon": "💲",
        },
    }

    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "Dashboard"

    sidebar_css = """
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #101e3a 0%, #142542 55%, #1c2f53 100%);
        color: #f5f7ff;
    }
    [data-testid="stSidebar"] * {
        color: #f5f7ff !important;
    }
    .user-card {
        border: 1px solid rgba(255, 255, 255, 0.18);
        background: rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 18px;
    }
    .user-card .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        margin-right: 10px;
    }
    .user-card .meta {
        display: flex;
        flex-direction: column;
        gap: 2px;
        font-size: 0.85rem;
    }
    .nav-wrapper {
        border-radius: 16px;
        padding: 14px 12px;
        background: rgba(0, 0, 0, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .nav-wrapper h3 {
        font-size: 0.95rem;
        margin-bottom: 12px;
        letter-spacing: 0.02em;
    }
    .nav-wrapper div[data-baseweb="radio"] > div {
        gap: 0.45rem;
    }
    .nav-wrapper div[data-baseweb="radio"] label {
        border: 1px solid rgba(255, 255, 255, 0.18);
        background: rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 0.65rem 0.75rem;
        transition: all 0.2s ease;
    }
    .nav-wrapper div[data-baseweb="radio"] label:hover {
        border-color: rgba(255, 255, 255, 0.35);
        background: rgba(255, 255, 255, 0.12);
    }
    .nav-wrapper div[data-baseweb="radio"] input:checked + div {
        border: 1px solid #7aa5ff;
        background: rgba(122, 165, 255, 0.16);
        box-shadow: 0 0 0 1px rgba(122, 165, 255, 0.3);
    }
    .nav-wrapper .nav-caption {
        margin-top: 10px;
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.75) !important;
    }
    </style>
    """
    st.sidebar.markdown(sidebar_css, unsafe_allow_html=True)

    user_email = getattr(st.session_state["user"], "email", "Usuario")
    user_initials = user_email[:2].upper()
    with st.sidebar:
        st.markdown(
            f"""
            <div class="user-card">
                <div style="display:flex; align-items:center;">
                    <div class="avatar">{user_initials}</div>
                    <div class="meta">
                        <span style="font-weight:600;">{user_email}</span>
                        <span style="color:rgba(255,255,255,0.7);">Usuario autorizado</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    nav_container = st.sidebar.container()
    with nav_container:
        st.markdown('<div class="nav-wrapper"><h3>🧭 Paneles disponibles</h3>', unsafe_allow_html=True)
        option_labels = [f"{item['icon']}  {title}" for title, item in NAV_ITEMS.items()]
        label_to_title = dict(zip(option_labels, NAV_ITEMS.keys()))
        default_label = f"{NAV_ITEMS[st.session_state['selected_page']]['icon']}  {st.session_state['selected_page']}"

        selected_label = st.radio(
            "Seleccionar página",
            option_labels,
            index=option_labels.index(default_label),
            label_visibility="collapsed",
            key="nav_radio",
        )

        st.markdown("</div>", unsafe_allow_html=True)

    selected_page = label_to_title[selected_label]
    st.session_state['selected_page'] = selected_page
    st.sidebar.markdown(
        f"<div class='nav-caption'>{NAV_ITEMS[selected_page]['icon']} {selected_page}</div>",
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("<hr style='margin-top:3rem;'>", unsafe_allow_html=True)
    _, logout_col, _ = st.sidebar.columns([1, 2, 1])
    with logout_col:
        st.sidebar.button("Cerrar Sesión", on_click=handle_logout, use_container_width=True)

    # ============================================
    # RENDERIZADO DE PÁGINAS SEGÚN SELECCIÓN
    # ============================================
    
    # Importar las páginas
    try:
        if selected_page == "Dashboard":
            from pages import dashboard
            dashboard.show()
        elif selected_page == "Stock":
            from pages import stock
            stock.show()
        elif selected_page == "Ventas":
            from pages import ventas
            ventas.show()
        elif selected_page == "Clientes":
            from pages import clientes
            clientes.show()
        elif selected_page == "Cobranzas":
            from pages import cobranzas
            cobranzas.show()
        elif selected_page == "Proveedores":
            from pages import proveedores
            proveedores.show()
        elif selected_page == "Costos":
            from pages import costos
            costos.show()
    except ImportError as e:
        st.error(f"⚠️ Error al cargar la página {selected_page}: {str(e)}")
        st.info("Asegúrate de que exista el archivo correspondiente en la carpeta 'pages/'")
    except Exception as e:
        st.error(f"❌ Error inesperado: {str(e)}")

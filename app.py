import os
from urllib.parse import quote as urllib_quote
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="HASSELTH GLOBAL | Catálogo de Casacas",
    page_icon="🧥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- DISEÑO CSS ---
st.markdown(
    """
    <style>
    .main { background-color: #f8fafc; }
    .product-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .header-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 30px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .price-tag { font-size: 1.35rem; font-weight: 700; color: #0ea5e9; }
    </style>
""",
    unsafe_allow_html=True,
)

# --- CONEXIÓN A GOOGLE SHEETS ---
# Usaremos una conexión pública o mediante caché para leer la hoja de cálculo de forma fluida.
SHEET_URL = st.text_input(
    "Pega aquí el enlace de tu Google Sheet (solo la primera vez)",
    value="",
    type="default",
)


@st.cache_data(ttl=60)
def cargar_datos_google_sheet(url):
    if not url:
        return pd.DataFrame()
    try:
        # Configuración para leer hojas públicas de Google Sheets vía Pandas
        csv_url = url.replace("/edit?usp=sharing", "/export?format=csv").replace(
            "/edit#gid=0", "/export?format=csv"
        )
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        st.error(
            f"Error al conectar con la hoja de Google: Asegúrate de que sea pública."
        )
        return pd.DataFrame()


# Cargar los datos
if SHEET_URL:
    df_productos = cargar_datos_google_sheet(SHEET_URL)
else:
    # Datos por defecto si aún no ponen el enlace
    df_productos = pd.DataFrame(
        {
            "ID": [1, 2],
            "Nombre_Casaca": [
                "Casaca Impermeable Urbana",
                "Casaca de Cuero Clásica",
            ],
            "Estilo": ["Impermeable", "Cuero"],
            "Precio": [150.00, 280.00],
            "Tallas": ["S, M, L, XL", "M, L, XL"],
            "Foto": ["", ""],
            "Descripcion": [
                "Ideal para invierno",
                "Cuero sintético duradero",
            ],
        }
    )

# --- PANEL DE ADMINISTRACIÓN (Protegido por contraseña) ---
st.sidebar.markdown("## 🔒 Panel de Administración")
PASSWORD_ADMIN = "hasselth2026"
password_ingresada = st.sidebar.text_input(
    "Contraseña de Administrador", type="password"
)

modo_gestion = False
if password_ingresada == PASSWORD_ADMIN:
    st.sidebar.success("✅ Modo Administrador Activo")
    modo_gestion = True
elif password_ingresada:
    st.sidebar.error("❌ Contraseña incorrecta")

# Filtro lateral por estilo
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filtrar Catálogo")
if not df_productos.empty and "Estilo" in df_productos.columns:
    estilos_disponibles = ["Todos"] + list(df_productos["Estilo"].unique())
else:
    estilos_disponibles = ["Todos"]

filtro_estilo = st.sidebar.selectbox(
    "Selecciona un estilo", estilos_disponibles
)

# --- CABECERA ---
st.markdown(
    """
    <div class="header-container">
        <h1>🧥 HASSELTH GLOBAL</h1>
        <p>Catálogo Exclusivo de Casacas • Sincronizado con Google Sheets</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Filtrar productos
if not df_productos.empty:
    productos_a_mostrar = df_productos
    if filtro_estilo != "Todos":
        productos_a_mostrar = df_productos[
            df_productos["Estilo"] == filtro_estilo
        ]

    # --- MOSTRAR PRODUCTOS EN CUADRÍCULA ---
    columnas = st.columns(3)

    for idx, row in productos_a_mostrar.iterrows():
        columna_actual = columnas[idx % 3]
        with columna_actual:
            with st.container():
                st.markdown(
                    f"""
                    <div class="product-card">
                        <h3 style="margin-top:0; color:#1e293b; font-size:1.25rem;"><b>{row['Nombre_Casaca']}</b></h3>
                        <p style="color:#64748b; font-size:0.9rem; margin-bottom: 5px;"><b>Estilo:</b> {row['Estilo']}</p>
                """,
                    unsafe_allow_html=True,
                )

                # Mostrar imagen si hay URL válida
                foto_val = (
                    str(row["Foto"])
                    if pd.notna(row["Foto"])
                    else "Sin imagen"
                )
                if foto_val.startswith("http"):
                    st.image(foto_val, use_container_width=True)
                else:
                    st.markdown(
                        "<div style='background:#f1f5f9; padding:30px; text-align:center; color:#94a3b8; border-radius:8px; margin-bottom:10px;'>🧥 <i>Imagen desde Google Sheets</i></div>",
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"""
                    <p style="color:#334155; font-size:0.95rem; min-height:40px;">{row['Descripcion']}</p>
                    <p style="color:#475569; font-size:0.85rem; margin-bottom:5px;"><b>Tallas:</b> {row['Tallas']}</p>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:15px; margin-bottom:15px;">
                        <span class="price-tag">S/ {float(row['Precio']):.2f}</span>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

                # Botón WhatsApp
                numero_whatsapp = "51900000000"
                mensaje = f"Hola, deseo consultar por la casaca *{row['Nombre_Casaca']}* de HASSELTH GLOBAL."
                link_wa = (
                    f"https://wa.me/{numero_whatsapp}?text={urllib_quote(mensaje)}"
                )

                st.markdown(
                    f'<a href="{link_wa}" target="_blank"><button style="background-color:#16a34a; color:white; padding:10px 16px; border:none; border-radius:8px; cursor:pointer; width:100%; font-weight:600; font-size:0.95rem;">💬 Consultar / Comprar</button></a>',
                    unsafe_allow_html=True,
                )

                st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info(
        "Por favor ingresa el enlace de tu Google Sheet en la barra lateral para cargar los productos."
    )

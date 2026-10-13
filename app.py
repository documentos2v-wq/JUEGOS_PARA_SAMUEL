import os
from urllib.parse import quote as urllib_quote
import pandas as pd
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

# --- ENLACE PERMANENTE DE TU GOOGLE SHEET ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RC8pD13DcSFtiCMoYoV8NXdsjRydzNr3MTHtMQePS0E/edit?usp=sharing"


@st.cache_data(ttl=5)
def cargar_datos_hoja(url):
    try:
        csv_url = url.replace("/edit?usp=sharing", "/export?format=csv").replace(
            "/edit#gid=0", "/export?format=csv"
        )
        df = pd.read_csv(csv_url)
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        # Datos de respaldo por seguridad si la red falla
        return pd.DataFrame(
            {
                "Nombre_Casaca": ["Casaca Impermeable Urbana"],
                "Estilo": ["Impermeable"],
                "Precio": [150.00],
                "Tallas": ["S, M, L, XL"],
                "Foto": [""],
                "Descripcion": ["Ideal para invierno."],
            }
        )


# Cargar datos en la sesión
if "df_casacas" not in st.session_state:
    st.session_state.df_casacas = cargar_data_hoja(SHEET_URL)

df_productos = st.session_state.df_casacas

# --- BARRA LATERAL: Filtros públicos ---
st.sidebar.markdown("## 🔍 Filtrar Catálogo")
col_estilo = next(
    (c for c in df_productos.columns if "estilo" in c.lower()),
    df_productos.columns[1] if len(df_productos.columns) > 1 else None,
)
estilos_disponibles = (
    ["Todos"] + list(df_productos[col_estilo].unique())
    if col_estilo
    else ["Todos"]
)
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
productos_a_mostrar = df_productos
if filtro_estilo != "Todos" and col_estilo:
    productos_a_mostrar = df_productos[
        df_productos[col_estilo] == filtro_estilo
    ]

# Mapeo flexible de columnas
c_nombre = next(
    (c for c in df_productos.columns if "nombre" in c.lower()),
    df_productos.columns[0],
)
c_estilo = col_estilo
c_precio = next(
    (c for c in df_productos.columns if "precio" in c.lower()),
    df_productos.columns[2],
)
c_tallas = next(
    (c for c in df_productos.columns if "talla" in c.lower()),
    df_productos.columns[3],
)
c_foto = next(
    (c for c in df_productos.columns if "foto" in c.lower()),
    df_productos.columns[4],
)
c_desc = next(
    (c for c in df_productos.columns if "desc" in c.lower()),
    df_productos.columns[5],
)

# --- CUADRÍCULA DE PRODUCTOS ---
columnas = st.columns(3)

for idx, row in productos_a_mostrar.iterrows():
    columna_actual = columnas[idx % 3]
    with columna_actual:
        with st.container():
            val_nombre = str(row[c_nombre]) if c_nombre else "Casaca"
            val_estilo = str(row[c_estilo]) if c_estilo else "General"
            val_precio = (
                float(row[c_precio])
                if c_precio and pd.notna(row[c_precio])
                else 0.0
            )
            val_tallas = str(row[c_tallas]) if c_tallas else "S, M, L"
            val_desc = (
                str(row[c_desc]) if c_desc and pd.notna(row[c_desc]) else ""
            )
            val_foto = (
                str(row[c_foto]) if c_foto and pd.notna(row[c_foto]) else ""
            )

            st.markdown(
                f"""
                <div class="product-card">
                    <h3 style="margin-top:0; color:#1e293b; font-size:1.25rem;"><b>{val_nombre}</b></h3>
                    <p style="color:#64748b; font-size:0.9rem; margin-bottom: 5px;"><b>Estilo:</b> {val_estilo}</p>
            """,
                unsafe_allow_html=True,
            )

            if val_foto.startswith("http"):
                st.image(val_foto, use_container_width=True)
            else:
                st.markdown(
                    "<div style='background:#f1f5f9; padding:30px; text-align:center; color:#94a3b8; border-radius:8px; margin-bottom:10px;'>🧥 <i>HASSELTH GLOBAL</i></div>",
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"""
                <p style="color:#334155; font-size:0.95rem; min-height:40px;">{val_desc}</p>
                <p style="color:#475569; font-size:0.85rem; margin-bottom:5px;"><b>Tallas:</b> {val_tallas}</p>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:15px; margin-bottom:15px;">
                    <span class="price-tag">S/ {val_precio:.2f}</span>
                </div>
            """,
                unsafe_allow_html=True,
            )

            # Botón WhatsApp
            numero_whatsapp = "51900000000"
            mensaje = f"Hola, deseo consultar por la casaca *{val_nombre}* de HASSELTH GLOBAL."
            link_wa = (
                f"https://wa.me/{numero_whatsapp}?text={urllib_quote(mensaje)}"
            )

            st.markdown(
                f'<a href="{link_wa}" target="_blank"><button style="background-color:#16a34a; color:white; padding:10px 16px; border:none; border-radius:8px; cursor:pointer; width:100%; font-weight:600; font-size:0.95rem;">💬 Consultar / Comprar</button></a>',
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)


# --- BARRA LATERAL (Zona de Gestión / Admin abajo del todo) ---
st.sidebar.markdown("---")
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Zona de Gestión (Admin)")

PASSWORD_ADMIN = "hasselth2026"
password_ingresada = st.sidebar.text_input(
    "Contraseña de Administrador", type="password", key="pwd_admin_key"
)

if password_ingresada == PASSWORD_ADMIN:
    st.sidebar.success("✅ Acceso de Administrador Concedido")

    with st.sidebar.expander("➕ Agregar Nueva Casaca"):
        with st.form("form_agregar_sheet", clear_on_submit=True):
            f_nombre = st.text_input("Nombre de la casaca")
            f_estilo = st.selectbox(
                "Estilo",
                [
                    "Impermeable",
                    "Cuero",
                    "Térmica",
                    "Cortaviento",
                    "Casual",
                ],
            )
            f_precio = st.number_input("Precio (S/)", min_value=0.0, value=120.0)
            f_tallas = st.text_input("Tallas (ej: S, M, L)", value="S, M, L")
            f_desc = st.text_area("Descripción")
            f_foto = st.text_input("URL de la foto (opcional)")

            btn_enviar = st.form_submit_button(
                "Añadir al Catálogo (Guardar cambios)"
            )
            if btn_enviar:
                if f_nombre:
                    nueva_fila = pd.DataFrame(
                        [
                            {
                                c_nombre: f_nombre,
                                c_estilo: f_estilo,
                                c_precio: float(f_precio),
                                c_tallas: f_tallas,
                                c_foto: f_foto,
                                c_desc: f_desc,
                            }
                        ]
                    )
                    st.session_state.df_casacas = pd.concat(
                        [st.session_state.df_casacas, nueva_fila],
                        ignore_index=True,
                    )
                    st.success(
                        "¡Casaca agregada! (Actualiza tu Google Sheet con estos mismos datos para persistencia absoluta)."
                    )
                    st.rerun()
                else:
                    st.error("Debes ingresar el nombre de la casaca.")

    st.sidebar.markdown(
        "💡 *Tip:* Para cambios definitivos y masivos, edita directamente tu **Google Sheet** y los cambios se reflejarán automáticamente en esta web al recargar."
    )

elif password_ingresada:
    st.sidebar.error("❌ Contraseña incorrecta")

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

# --- INICIALIZAR BASE DE DATOS EN SESIÓN ---
if "productos_db" not in st.session_state:
    st.session_state.productos_db = [
        {
            "id": 1,
            "nombre": "Casaca Impermeable Urbana",
            "estilo": "Impermeable",
            "precio": 150.00,
            "tallas": "S, M, L, XL",
            "foto": "",
            "descripcion": (
                "Ideal para la temporada de invierno, abrigadora y moderna."
            ),
        },
        {
            "id": 2,
            "nombre": "Casaca de Cuero Clásica",
            "estilo": "Cuero",
            "precio": 280.00,
            "tallas": "M, L, XL",
            "foto": "",
            "descripcion": (
                "Cuero sintético de alta durabilidad y diseño ejecutivo."
            ),
        },
        {
            "id": 3,
            "nombre": "Casaca Térmica Acolchada",
            "estilo": "Térmica",
            "precio": 190.00,
            "tallas": "S, M, L",
            "foto": "",
            "descripcion": "Diseño ligero con retención de calor avanzada.",
        },
        {
            "id": 4,
            "nombre": "Casaca Cortaviento Sport",
            "estilo": "Cortaviento",
            "precio": 130.00,
            "tallas": "M, L, XL, XXL",
            "foto": "",
            "descripcion": "Perfecta para running y actividades al aire libre.",
        },
    ]

# Convertir a DataFrame para manejo interno
df_productos = pd.DataFrame(st.session_state.productos_db)

# --- BARRA LATERAL (Parte Superior: Filtros públicos) ---
st.sidebar.markdown("## 🔍 Filtrar Catálogo")
estilos_disponibles = ["Todos"] + list(df_productos["estilo"].unique())
filtro_estilo = st.sidebar.selectbox(
    "Selecciona un estilo", estilos_disponibles
)

# --- CABECERA ---
st.markdown(
    """
    <div class="header-container">
        <h1>🧥 HASSELTH GLOBAL</h1>
        <p>Catálogo Exclusivo de Casacas • Estilo, Calidad y Confort</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Filtrar productos
productos_a_mostrar = df_productos
if filtro_estilo != "Todos":
    productos_a_mostrar = df_productos[
        df_productos["estilo"] == filtro_estilo
    ]

# --- CUADRÍCULA DE PRODUCTOS ---
columnas = st.columns(3)

for idx, row in productos_a_mostrar.iterrows():
    columna_actual = columnas[idx % 3]
    with columna_actual:
        with st.container():
            st.markdown(
                f"""
                <div class="product-card">
                    <h3 style="margin-top:0; color:#1e293b; font-size:1.25rem;"><b>{row['nombre']}</b></h3>
                    <p style="color:#64748b; font-size:0.9rem; margin-bottom: 5px;"><b>Estilo:</b> {row['estilo']}</p>
            """,
                unsafe_allow_html=True,
            )

            if row["foto"] and str(row["foto"]).startswith("http"):
                st.image(row["foto"], use_container_width=True)
            else:
                st.markdown(
                    "<div style='background:#f1f5f9; padding:30px; text-align:center; color:#94a3b8; border-radius:8px; margin-bottom:10px;'>🧥 <i>HASSELTH GLOBAL</i></div>",
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"""
                <p style="color:#334155; font-size:0.95rem; min-height:40px;">{row['descripcion']}</p>
                <p style="color:#475569; font-size:0.85rem; margin-bottom:5px;"><b>Tallas:</b> {row['tallas']}</p>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:15px; margin-bottom:15px;">
                    <span class="price-tag">S/ {float(row['precio']):.2f}</span>
                </div>
            """,
                unsafe_allow_html=True,
            )

            # Botón WhatsApp
            numero_whatsapp = "51900000000"
            mensaje = f"Hola, deseo consultar por la casaca *{row['nombre']}* de HASSELTH GLOBAL."
            link_wa = (
                f"https://wa.me/{numero_whatsapp}?text={urllib_quote(mensaje)}"
            )

            st.markdown(
                f'<a href="{link_wa}" target="_blank"><button style="background-color:#16a34a; color:white; padding:10px 16px; border:none; border-radius:8px; cursor:pointer; width:100%; font-weight:600; font-size:0.95rem;">💬 Consultar / Comprar</button></a>',
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)


# --- BARRA LATERAL (Parte Inferior: Administración y Enlace movidos abajo) ---
st.sidebar.markdown("---")
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Zona de Gestión (Admin)")

PASSWORD_ADMIN = "hasselth2026"
password_ingresada = st.sidebar.text_input(
    "Contraseña de Administrador", type="password", key="admin_pwd_input"
)

if password_ingresada == PASSWORD_ADMIN:
    st.sidebar.success("✅ Acceso concedido")

    with st.sidebar.expander("➕ Agregar Nueva Casaca"):
        with st.form("form_nueva", clear_on_submit=True):
            n_nombre = st.text_input("Nombre de la casaca")
            n_estilo = st.selectbox(
                "Estilo",
                [
                    "Impermeable",
                    "Cuero",
                    "Térmica",
                    "Cortaviento",
                    "Casual",
                ],
            )
            n_precio = st.number_input("Precio (S/)", min_value=0.0, value=120.0)
            n_tallas = st.text_input("Tallas (ej: S, M, L)", value="S, M, L")
            n_desc = st.text_area("Descripción")
            n_foto = st.text_input("URL de la foto (opcional)")

            submitted = st.form_submit_button("Guardar Producto")
            if submitted:
                if n_nombre:
                    nuevo_id = (
                        max([p["id"] for p in st.session_state.productos_db])
                        + 1
                        if st.session_state.productos_db
                        else 1
                    )
                    st.session_state.productos_db.append(
                        {
                            "id": nuevo_id,
                            "nombre": n_nombre,
                            "estilo": n_estilo,
                            "precio": float(n_precio),
                            "tallas": n_tallas,
                            "foto": n_foto,
                            "descripcion": n_desc,
                        }
                    )
                    st.success("¡Casaca agregada con éxito!")
                    st.rerun()
                else:
                    st.error("Ingresa el nombre del producto.")

    st.sidebar.markdown("#### 🗑️ Eliminar Producto")
    ids_nombres = {
        p["nombre"]: p["id"] for p in st.session_state.productos_db
    }
    prod_a_borrar = st.sidebar.selectbox(
        "Selecciona casaca a borrar",
        ["-- Seleccionar --"] + list(ids_nombres.keys()),
    )
    if prod_a_borrar != "-- Seleccionar --":
        if st.sidebar.button("Borrar producto seleccionado"):
            st.session_state.productos_db = [
                p
                for p in st.session_state.productos_db
                if p["nombre"] != prod_a_borrar
            ]
            st.success(f"Se eliminó: {prod_a_borrar}")
            st.rerun()

elif password_ingresada:
    st.sidebar.error("❌ Contraseña incorrecta")

# Enlace de Google Sheets reubicado abajo del todo
st.sidebar.markdown("---")
sheet_url_input = st.sidebar.text_input(
    "Enlace Google Sheet (Opcional)",
    value="",
    placeholder="Pega tu enlace aquí...",
)

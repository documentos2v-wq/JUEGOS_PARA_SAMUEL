import os
from urllib.parse import quote as urllib_quote
import streamlit as st

# Configuración de la página con diseño ancho y moderno
st.set_page_config(
    page_title="HASSELTH GLOBAL | Catálogo de Casacas",
    page_icon="🧥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- DISEÑO CSS PERSONALIZADO ---
st.markdown(
    """
    <style>
    .main {
        background-color: #f8fafc;
    }
    .product-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 20px;
    }
    .product-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .header-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 30px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .header-container h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.025em;
    }
    .header-container p {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-top: 10px;
    }
    .price-tag {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0ea5e9;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- CARPETA PARA GUARDAR FOTOS ---
UPLOAD_DIR = "imagenes_casacas"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- INICIALIZAR BASE DE DATOS DE LA SESIÓN ---
if "productos" not in st.session_state:
    st.session_state.productos = [
        {
            "id": 1,
            "nombre": "Casaca Impermeable Urbana",
            "estilo": "Impermeable",
            "precio": 150.00,
            "tallas": ["S", "M", "L", "XL"],
            "descripcion": "Ideal para la temporada de invierno, abrigadora y moderna.",
            "imagen": None,
        },
        {
            "id": 2,
            "nombre": "Casaca de Cuero Clásica",
            "estilo": "Cuero",
            "precio": 280.00,
            "tallas": ["M", "L", "XL"],
            "descripcion": "Cuero sintético de alta durabilidad y diseño ejecutivo.",
            "imagen": None,
        },
        {
            "id": 3,
            "nombre": "Casaca Térmica Acolchada",
            "estilo": "Térmica / Deportiva",
            "precio": 190.00,
            "tallas": ["S", "M", "L"],
            "descripcion": "Diseño ligero con retención de calor avanzada.",
            "imagen": None,
        },
    ]

# --- BARRA LATERAL CON ACCESO RESTRINGIDO (ADMIN) ---
st.sidebar.markdown("## 🔒 Panel de Administración")
st.sidebar.markdown("Acceso exclusivo para administradores de la tienda.")

# Configura tu contraseña secreta aquí (puedes cambiar "hasselth2026" por la que prefieras)
PASSWORD_ADMIN = "hasselth2026"

password_ingresada = st.sidebar.text_input(
    "Contraseña de Administrador", type="password"
)

if password_ingresada == PASSWORD_ADMIN:
    st.sidebar.success("✅ Acceso concedido")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Administrar Catálogo")

    with st.sidebar.expander("➕ Agregar Nueva Casaca"):
        with st.form("form_nueva_casaca", clear_on_submit=True):
            nuevo_nombre = st.text_input("Nombre de la casaca")
            nuevo_estilo = st.selectbox(
                "Estilo",
                [
                    "Impermeable",
                    "Cuero",
                    "Térmica / Deportiva",
                    "Casual",
                    "Cortaviento",
                ],
            )
            nuevo_precio = st.number_input(
                "Precio (S/)", min_value=0.0, value=120.0, step=10.0
            )
            nuevas_tallas = st.multiselect(
                "Tallas disponibles",
                ["S", "M", "L", "XL", "XXL"],
                default=["M", "L"],
            )
            nueva_desc = st.text_area("Breve descripción")
            archivo_foto = st.file_uploader(
                "Foto de la casaca", type=["jpg", "jpeg", "png"]
            )

            submit_btn = st.form_submit_button("Guardar en el Catálogo")

            if submit_btn:
                if nuevo_nombre:
                    ruta_imagen = None
                    if archivo_foto is not None:
                        ruta_imagen = os.path.join(UPLOAD_DIR, archivo_foto.name)
                        with open(ruta_imagen, "wb") as f:
                            f.write(archivo_foto.getbuffer())

                    nuevo_id = (
                        max([p["id"] for p in st.session_state.productos]) + 1
                        if st.session_state.productos
                        else 1
                    )
                    st.session_state.productos.append(
                        {
                            "id": nuevo_id,
                            "nombre": nuevo_nombre,
                            "estilo": nuevo_estilo,
                            "precio": float(nuevo_precio),
                            "tallas": nuevas_tallas,
                            "descripcion": nueva_desc,
                            "imagen": ruta_imagen,
                        }
                    )
                    st.success(f"¡{nuevo_nombre} agregada correctamente!")
                    st.rerun()
                else:
                    st.error("Por favor ingresa al menos el nombre del producto.")
    
    modo_gestion_activo = True
else:
    if password_ingresada:
        st.sidebar.error("❌ Contraseña incorrecta")
    st.sidebar.info(
        "💡 Los clientes solo pueden ver el catálogo y comprar. El panel de edición está bloqueado."
    )
    modo_gestion_activo = False

# Filtro lateral público por estilo (visible para todos)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filtrar Catálogo")
estilos_disponibles = ["Todos"] + list(
    set([p["estilo"] for p in st.session_state.productos])
)
filtro_estilo = st.sidebar.selectbox(
    "Selecciona un estilo", estilos_disponibles
)

# --- CABECERA VISUAL DE LA TIENDA ---
st.markdown(
    """
    <div class="header-container">
        <h1>🧥 HASSELTH GLOBAL</h1>
        <p>Catálogo Exclusivo de Casacas • Estilo, Calidad y Confort</p>
    </div>
""",
    unsafe_allow_html=True,
)

# --- FILTRADO DE PRODUCTOS ---
productos_a_mostrar = st.session_state.productos
if filtro_estilo != "Todos":
    productos_a_mostrar = [
        p for p in productos_a_mostrar if p["estilo"] == filtro_estilo
    ]

if not productos_a_mostrar:
    st.info("No hay casacas registradas bajo este filtro.")

# --- CUADRÍCULA DE PRODUCTOS ---
columnas = st.columns(3)

for idx, producto in enumerate(productos_a_mostrar):
    columna_actual = columnas[idx % 3]
    with columna_actual:
        with st.container():
            st.markdown(
                f"""
                <div class="product-card">
                    <h3 style="margin-top:0; color:#1e293b; font-size:1.25rem;"><b>{producto['nombre']}</b></h3>
                    <p style="color:#64748b; font-size:0.9rem; margin-bottom: 5px;"><b>Estilo:</b> {producto['estilo']}</p>
            """,
                unsafe_allow_html=True,
            )

            if producto["imagen"] and os.path.exists(producto["imagen"]):
                st.image(producto["imagen"], use_container_width=True)
            else:
                st.markdown(
                    "<div style='background:#f1f5f9; padding:40px; text-align:center; color:#94a3b8; border-radius:8px; margin-bottom:10px;'>🧥 <i>Sin imagen cargada</i></div>",
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"""
                <p style="color:#334155; font-size:0.95rem; min-height:40px;">{producto['descripcion']}</p>
                <p style="color:#475569; font-size:0.85rem; margin-bottom:5px;"><b>Tallas:</b> {', '.join(producto['tallas'])}</p>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:15px; margin-bottom:15px;">
                    <span class="price-tag">S/ {producto['precio']:.2f}</span>
                </div>
            """,
                unsafe_allow_html=True,
            )

            numero_whatsapp = "51900000000"  # Cambia por tu número real
            mensaje = f"Hola, deseo comprar o consultar por la casaca *{producto['nombre']}* de HASSELTH GLOBAL."
            link_wa = f"https://wa.me/{numero_whatsapp}?text={urllib_quote(mensaje)}"

            st.markdown(
                f'<a href="{link_wa}" target="_blank"><button style="background-color:#16a34a; color:white; padding:10px 16px; border:none; border-radius:8px; cursor:pointer; width:100%; font-weight:600; font-size:0.95rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">💬 Consultar / Comprar</button></a>',
                unsafe_allow_html=True,
            )

            # Opciones de borrado solo si el administrador puso la clave correcta
            if modo_gestion_activo:
                if st.checkbox(
                    f"Modo gestión", value=False, key=f"chk_{producto['id']}"
                ):
                    if st.button(
                        f"🗑️ Eliminar {producto['nombre']}",
                        key=f"del_{producto['id']}",
                    ):
                        st.session_state.productos = [
                            p
                            for p in st.session_state.productos
                            if p["id"] != producto["id"]
                        ]
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

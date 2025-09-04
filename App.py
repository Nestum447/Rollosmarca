import streamlit as st
from streamlit_image_annotation import point_canvas
from PIL import Image

st.set_page_config(page_title="Contador de Rollos", layout="wide")

st.title("📸 Contador manual de rollos")

# Subir imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # Herramienta interactiva para clicks en la imagen
    puntos = point_canvas(
        image=image,
        key="rollos",
        point_color="red",   # Color de los puntos
        stroke_width=5       # Tamaño del punto
    )

    # Mostrar conteo
    if puntos is not None:
        st.success(f"🔴 Rollos marcados: {len(puntos)}")

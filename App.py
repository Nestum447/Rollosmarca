import streamlit as st
from streamlit_image_annotation import image_annotation
from PIL import Image

st.set_page_config(page_title="Contador de Rollos", layout="wide")

st.title("📸 Contador manual de rollos")

# Subir imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # Herramienta interactiva para clicks
    puntos = image_annotation(
        image,
        key="rollos",
        box_color="red",
        single_class=True,
    )

    # Mostrar conteo
    if puntos:
        st.success(f"🔴 Rollos marcados: {len(puntos)}")

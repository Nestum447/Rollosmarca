import streamlit as st
from streamlit_image_annotation import pointdet
from PIL import Image

st.set_page_config(page_title="Contador de Rollos", layout="wide")
st.title("📸 Contador manual de rollos")

# Subida de imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # Herramienta interactiva con pointdet
    puntos = pointdet(
        image_path=None,               # No usar, vamos con PIL
        label_list=["rollo"],          # Solo una clase: rollo
        points=None,                   # Sin puntos iniciales
        labels=None,
        height=600,                    # Por ejemplo
        width=800,                     # Ajusta según sea conveniente
        point_width=5,
        use_space=True,
        key="rollos"
    )

    # Mostrar conteo
    if puntos is not None:
        st.success(f"🔴 Rollos marcados: {len(puntos)}")
        st.write(puntos)  # Muestra datos de puntos si quieres

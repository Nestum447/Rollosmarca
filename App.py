import streamlit as st
from PIL import Image
import pandas as pd
from streamlit_clickable_image import clickable_image

st.set_page_config(page_title="Contador de Rollos", layout="wide")
st.title("📸 Contador manual de rollos")

# Subida de imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["png","jpg","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Imagen cargada", use_column_width=True)

    st.write("Haz clic sobre cada rollo para marcarlo:")

    # Guardar coordenadas de clics
    if "points" not in st.session_state:
        st.session_state.points = []

    # Capturar clics con clickable_image
    clicked = clickable_image(image=image, key="click_image")
    if clicked:
        st.session_state.points.append(clicked)

    # Mostrar resultados
    if st.session_state.points:
        st.success(f"🔴 Rollos marcados: {len(st.session_state.points)}")
        df = pd.DataFrame(st.session_state.points, columns=["x","y"])
        st.dataframe(df)

        # Descargar CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Descargar coordenadas CSV",
            data=csv,
            file_name="rollos.csv",
            mime="text/csv"
        )

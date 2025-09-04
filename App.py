import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Contador de Rollos", layout="wide")
st.title("📸 Contador manual de rollos")

# Subir imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Imagen cargada", use_column_width=True)

    st.write("Haz clic sobre cada rollo para marcarlo:")

    # Guardar puntos en session_state
    if "points" not in st.session_state:
        st.session_state.points = []

    # Capturar coordenadas relativas de clics
    click = st.experimental_get_query_params().get("click")
    # Si quieres capturar clics dinámicos en Cloud, esto se hace con st.image + JS
    # Pero para simplicidad, agregamos un botón que simula clics manuales por coordenadas
    with st.form("add_point_form"):
        x = st.number_input("Coordenada X (px)", min_value=0, max_value=image.width, step=1)
        y = st.number_input("Coordenada Y (px)", min_value=0, max_value=image.height, step=1)
        submit = st.form_submit_button("Agregar rollo")
        if submit:
            st.session_state.points.append((x, y))

    # Mostrar resultados
    if st.session_state.points:
        st.success(f"🔴 Rollos marcados: {len(st.session_state.points)}")
        df = pd.DataFrame(st.session_state.points, columns=["x", "y"])
        st.dataframe(df)

        # Descargar CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Descargar coordenadas CSV",
            data=csv,
            file_name="rollos.csv",
            mime="text/csv"
        )

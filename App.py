import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import pandas as pd

st.set_page_config(page_title="Contador de Rollos", layout="wide")
st.title("📸 Contador interactivo de rollos")

# Subir imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["png","jpg","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Imagen cargada", use_container_width=True)

    # Canvas sobre la imagen
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.5)",  # color de los puntos
        stroke_width=5,
        stroke_color="red",
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",  # solo puntos
        key="canvas"
    )

    # Extraer puntos y mostrar conteo
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        st.success(f"🔴 Rollos marcados: {len(objects)}")

        # Crear DataFrame con coordenadas
        coords = [(int(obj["left"]), int(obj["top"])) for obj in objects]
        if coords:
            df = pd.DataFrame(coords, columns=["x","y"])
            st.dataframe(df)

            # Descargar CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Descargar coordenadas CSV",
                data=csv,
                file_name="rollos.csv",
                mime="text/csv"
            )

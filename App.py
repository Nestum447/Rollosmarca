import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import pandas as pd

st.set_page_config(page_title="Contador de Rollos", layout="wide")
st.title("📸 Contador manual de rollos")

# Subida de imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)

    # Canvas interactivo
    canvas_result = st_canvas(
        background_image=image,
        drawing_mode="point",        # Dibujar solo puntos
        point_display_radius=6,      # Tamaño del punto
        stroke_color="red",          # Color de los puntos
        update_streamlit=True,
        height=image.height,
        width=image.width,
        key="canvas"
    )

    # Extraer puntos
    puntos = []
    if canvas_result.json_data:
        for obj in canvas_result.json_data["objects"]:
            if obj.get("type") == "circle":
                puntos.append((obj["left"], obj["top"]))

    # Mostrar resultados
    if puntos:
        st.success(f"🔴 Rollos marcados: {len(puntos)}")

        df = pd.DataFrame(puntos, columns=["x", "y"])
        st.dataframe(df)

        # Botón para exportar
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Descargar coordenadas en CSV",
            data=csv,
            file_name="rollos_marcados.csv",
            mime="text/csv",
        )

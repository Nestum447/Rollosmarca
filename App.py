import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.title("Contador manual de rollos")

uploaded_file = st.file_uploader("Sube imagen", type=["png","jpg","jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGBA")

    # Redimensionar si es muy grande
    max_width = 800
    if image.width > max_width:
        ratio = max_width / image.width
        new_height = int(image.height * ratio)
        image = image.resize((max_width, new_height))

    canvas_result = st_canvas(
        background_image=image,
        drawing_mode="point",
        point_display_radius=6,
        stroke_color="red",
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

    if puntos:
        st.success(f"🔴 Rollos marcados: {len(puntos)}")

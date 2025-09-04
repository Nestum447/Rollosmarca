import streamlit as st
from PIL import Image
import pandas as pd
from io import BytesIO
import base64
from streamlit_javascript import st_javascript

st.set_page_config(page_title="Contador de Rollos", layout="wide")
st.title("📸 Contador interactivo de rollos")

# Subir imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    width, height = image.size

    # Convertir imagen a base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Inicializar lista de puntos
    if "points" not in st.session_state:
        st.session_state.points = []

    # Mostrar imagen y capturar clics con JS
    js_code = f"""
    const img = document.createElement('img');
    img.src = "data:image/png;base64,{img_base64}";
    img.style.width = "{width}px";
    img.style.height = "{height}px";
    img.style.position = "relative";
    document.body.appendChild(img);

    img.addEventListener('click', function(e) {{
        const rect = img.getBoundingClientRect();
        const x = Math.round(e.clientX - rect.left);
        const y = Math.round(e.clientY - rect.top);
        return [x, y];
    }});
    """
    # Ejecutar JS y obtener coordenadas
    clicked_point = st_javascript(js_code, key="js_click")

    # Guardar clic en session_state si existe
    if clicked_point:
        st.session_state.points.append(tuple(clicked_point))

    # Mostrar conteo automático
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

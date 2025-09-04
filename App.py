import streamlit as st
from PIL import Image
import pandas as pd
import base64
from io import BytesIO

st.set_page_config(page_title="Contador de Rollos", layout="wide")
st.title("📸 Contador de rollos interactivo")

# Subir imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    width, height = image.size

    # Convertir imagen a base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Inicializar puntos en session_state
    if "points" not in st.session_state:
        st.session_state.points = []

    # HTML + JS para capturar clics
    html_code = f"""
    <div style="position: relative; display: inline-block;">
        <img id="img" src="data:image/png;base64,{img_base64}" width="{width}" height="{height}" style="display:block;">
        <canvas id="canvas" width="{width}" height="{height}" style="position:absolute; top:0; left:0;"></canvas>
    </div>
    <script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    canvas.addEventListener('click', function(e) {{
        const rect = canvas.getBoundingClientRect();
        const x = Math.round(e.clientX - rect.left);
        const y = Math.round(e.clientY - rect.top);
        ctx.fillStyle = 'red';
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, 2 * Math.PI);
        ctx.fill();
        // Enviar coordenadas a Streamlit mediante console (placeholder, se puede mejorar con streamlit-events)
        console.log(x, y);
    }});
    </script>
    """

    st.components.v1.html(html_code, height=height + 20, scrolling=True)

    # Formulario para agregar puntos manualmente
    with st.form("manual_point_form"):
        x = st.number_input("Coordenada X (px)", min_value=0, max_value=width, step=1)
        y = st.number_input("Coordenada Y (px)", min_value=0, max_value=height, step=1)
        submit = st.form_submit_button("Agregar rollo")
        if submit:
            st.session_state.points.append((x, y))

    # Mostrar resultados
    if st.session_state.points:
        st.success(f"🔴 Rollos marcados: {len(st.session_state.points)}")
        df = pd.DataFrame(st.session_state.points, columns=["x","y"])
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Descargar coordenadas CSV",
            data=csv,
            file_name="rollos.csv",
            mime="text/csv"
        )

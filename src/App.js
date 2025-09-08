import React, { useState, useRef, useEffect } from "react";
import { CSVLink } from "react-csv";

function App() {
  const [points, setPoints] = useState([]);
  const [image, setImage] = useState(null);
  const canvasRef = useRef(null);

  // Subir imagen
  const handleImageUpload = (e) => {
    setImage(URL.createObjectURL(e.target.files[0]));
    setPoints([]);
  };

  // Agregar puntos con mouse o touch
  const handleCanvasClick = (e) => {
    const rect = canvasRef.current.getBoundingClientRect();
    let x, y;

    if (e.touches) {
      // Evento táctil
      x = Math.round(e.touches[0].clientX - rect.left);
      y = Math.round(e.touches[0].clientY - rect.top);
    } else {
      // Evento de mouse
      x = Math.round(e.clientX - rect.left);
      y = Math.round(e.clientY - rect.top);
    }

    setPoints((prev) => [...prev, { x, y }]);
  };

  // Revertir último punto
  const handleUndo = () => {
    if (points.length > 0) {
      setPoints(points.slice(0, -1));
    }
  };

  // Limpiar todos los puntos
  const handleClear = () => {
    setPoints([]);
  };

  // Dibujar puntos rojos sobre la imagen
  useEffect(() => {
    if (canvasRef.current && image) {
      const ctx = canvasRef.current.getContext("2d");
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      ctx.fillStyle = "red";
      points.forEach((p) => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, 6, 0, 2 * Math.PI);
        ctx.fill();
      });
    }
  }, [points, image]);

  return (
    <div style={{ padding: "20px" }}>
      <h1>📸 Contador interactivo de rollos</h1>

      {/* Subir imagen */}
      <input type="file" accept="image/*" onChange={handleImageUpload} />

      {image && (
        <div style={{ position: "relative", display: "inline-block" }}>
          {/* Imagen */}
          <img
            src={image}
            alt="Subida"
            style={{ display: "block", maxWidth: "600px", maxHeight: "400px" }}
          />
          {/* Canvas sobre la imagen */}
          <canvas
            ref={canvasRef}
            width={600}
            height={400}
            style={{ position: "absolute", top: 0, left: 0 }}
            onClick={handleCanvasClick}
            onTouchStart={handleCanvasClick} // soporte táctil
          />
        </div>
      )}

      {/* Conteo */}
      <h2>Rollos marcados: {points.length}</h2>

      {/* Botones de control */}
      {points.length > 0 && (
        <div style={{ marginBottom: "15px" }}>
          <button
            onClick={handleUndo}
            style={{
              padding: "10px 15px",
              marginRight: "10px",
              background: "orange",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
              color: "white",
              fontWeight: "bold",
            }}
          >
            🔄 Revertir último
          </button>

          <button
            onClick={handleClear}
            style={{
              padding: "10px 15px",
              background: "red",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
              color: "white",
              fontWeight: "bold",
            }}
          >
            🗑️ Limpiar todos
          </button>
        </div>
      )}

      {/* Tabla y CSV */}
      {points.length > 0 && (
        <>
          <table border="1" cellPadding="5">
            <thead>
              <tr>
                <th>X</th>
                <th>Y</th>
              </tr>
            </thead>
            <tbody>
              {points.map((p, i) => (
                <tr key={i}>
                  <td>{p.x}</td>
                  <td>{p.y}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <CSVLink
            data={points}
            filename={"rollos.csv"}
            style={{
              display: "inline-block",
              marginTop: "10px",
              padding: "10px",
              background: "green",
              color: "white",
              textDecoration: "none",
              borderRadius: "5px",
            }}
          >
            📥 Descargar CSV
          </CSVLink>
        </>
      )}
    </div>
  );
}

export default App;

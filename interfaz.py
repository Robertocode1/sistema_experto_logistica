import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any
from motor import MotorInferencia


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Experto Logístico en Tiempo Real</title>
    <style>
        :root {
            --bg: #f8fafc;
            --surface: #ffffff;
            --text: #0f172a;
            --muted: #64748b;
            --border: #e2e8f0;
            --primary: #2563eb;
            --primary-light: #eff6ff;
            --success: #166534;
            --success-bg: #f0fdf4;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.5;
            padding: 2rem 1rem;
        }
        .container { max-width: 1100px; margin: 0 auto; }
        header {
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }
        header h1 { font-size: 1.4rem; font-weight: 600; }
        header p { color: var(--muted); font-size: 0.9rem; }
        
        .layout {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }
        @media (max-width: 768px) {
            .layout { grid-template-columns: 1fr; }
        }
        
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            margin-bottom: 1rem;
        }
        .card-title {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .form-group {
            margin-bottom: 0.9rem;
        }
        .form-group label {
            display: block;
            font-size: 0.82rem;
            font-weight: 500;
            color: var(--muted);
            margin-bottom: 0.3rem;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 0.55rem 0.75rem;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 0.9rem;
            background: #fff;
            color: var(--text);
            transition: border-color 0.15s;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
        
        .result-section {
            background: var(--primary-light);
            border: 1px solid #bfdbfe;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.75rem;
        }
        .result-section h4 {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--primary);
            margin-bottom: 0.4rem;
        }
        .result-item {
            font-size: 0.9rem;
            margin-bottom: 0.3rem;
        }
        .result-item span { color: var(--muted); font-size: 0.8rem; display: inline-block; width: 130px; }
        .result-item strong { color: var(--text); font-weight: 600; }
        
        .trace-box {
            font-size: 0.85rem;
            padding: 0.6rem 0.8rem;
            background: #f8fafc;
            border-left: 3px solid var(--primary);
            margin-bottom: 0.5rem;
            border-radius: 0 6px 6px 0;
        }
        .trace-box strong { color: var(--primary); }
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1>Sistema Experto de Logística Nacional</h1>
        <p>Motor de Inferencia en Tiempo Real · Actualización dinámica según los parámetros del paquete</p>
    </header>

    <div class="layout">
        <!-- COLUMNA IZQUIERDA: PREGUNTAS / VARIABLES DE ENTRADA -->
        <div class="card">
            <div class="card-title">📝 Parámetros del Paquete (Preguntas Clave)</div>
            
            <div class="form-group">
                <label>ID del Paquete</label>
                <input type="text" id="id_paquete" value="PAQ-105" oninput="evaluarEnTiempoReal()">
            </div>
            <div class="form-group">
                <label>Tienda de Origen (First-Mile)</label>
                <input type="text" id="tienda_origen" value="Sucursal Metrocentro" oninput="evaluarEnTiempoReal()">
            </div>
            <div class="form-group">
                <label>Municipio / Destino de Entrega</label>
                <input type="text" id="destino" value="Santa Ana" oninput="evaluarEnTiempoReal()">
            </div>
            <div class="form-group">
                <label>Distancia desde Bodega Central (km)</label>
                <input type="number" id="distancia_km" value="65" min="1" oninput="evaluarEnTiempoReal()">
            </div>
            <div class="form-group">
                <label>Peso del Paquete (kg)</label>
                <input type="number" id="peso_kg" value="25" min="0.1" step="0.5" oninput="evaluarEnTiempoReal()">
            </div>
            <div class="form-group">
                <label>Nivel de Urgencia</label>
                <select id="urgencia" onchange="evaluarEnTiempoReal()">
                    <option value="baja">Baja</option>
                    <option value="media" selected>Media</option>
                    <option value="alta">Alta (Express)</option>
                </select>
            </div>
            <div class="form-group">
                <label>Nivel de Fragilidad</label>
                <select id="fragilidad" onchange="evaluarEnTiempoReal()">
                    <option value="baja">Baja</option>
                    <option value="media">Media</option>
                    <option value="alta" selected>Alta (Frágil)</option>
                </select>
            </div>
            <div class="form-group">
                <label>Valor Declarado de la Mercancía ($ USD)</label>
                <input type="number" id="valor_usd" value="1200" min="1" oninput="evaluarEnTiempoReal()">
            </div>
        </div>

        <!-- COLUMNA DERECHA: RESPUESTAS ORDENADAS EN TIEMPO REAL -->
        <div>
            <div class="card">
                <div class="card-title">📦 Dictamen Logístico Ordenado</div>
                
                <div class="result-section">
                    <h4>1. Primera Milla (Recolección en Tienda)</h4>
                    <div class="result-item"><span>Prioridad:</span> <strong id="res_recoleccion">-</strong></div>
                    <div class="result-item"><span>Flujo en Bodega:</span> <strong id="res_flujo">-</strong></div>
                </div>

                <div class="result-section">
                    <h4>2. Cross-Docking y Organización en Bodega</h4>
                    <div class="result-item"><span>Zona Logística:</span> <strong id="res_zona">-</strong></div>
                    <div class="result-item"><span>Andén Asignado:</span> <strong id="res_anden">-</strong></div>
                    <div class="result-item"><span>Estiba en Jaula:</span> <strong id="res_estiba">-</strong></div>
                    <div class="result-item"><span>Seguridad/Custodia:</span> <strong id="res_seguridad">-</strong></div>
                </div>

                <div class="result-section">
                    <h4>3. Última Milla (Diseño de Ruta)</h4>
                    <div class="result-item"><span>Vehículo Ruta:</span> <strong id="res_vehiculo" style="color:var(--primary)">-</strong></div>
                    <div class="result-item"><span>Estrategia:</span> <strong id="res_estrategia">-</strong></div>
                    <div class="result-item"><span>Requisito Entrega:</span> <strong id="res_entrega">-</strong></div>
                </div>
            </div>

            <div class="card">
                <div class="card-title">🔍 Trazabilidad Experta (¿Por qué se decidió?)</div>
                <div id="contenedor-traza">
                    <p style="color:var(--muted); font-size:0.85rem;">Modifique cualquier campo a la izquierda para ver las reglas activadas instantáneamente.</p>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
async function evaluarEnTiempoReal() {
    const payload = {
        id_paquete: document.getElementById('id_paquete').value,
        tienda_origen: document.getElementById('tienda_origen').value,
        destino: document.getElementById('destino').value,
        estado_paquete: "en_tienda",
        distancia_km: parseFloat(document.getElementById('distancia_km').value) || 0,
        peso_kg: parseFloat(document.getElementById('peso_kg').value) || 0,
        urgencia: document.getElementById('urgencia').value,
        fragilidad: document.getElementById('fragilidad').value,
        valor_usd: parseFloat(document.getElementById('valor_usd').value) || 0
    };

    try {
        const res = await fetch('/api/evaluar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        const r = data.resultado;

        // Actualizar campos ordenados
        document.getElementById('res_recoleccion').innerText = r.prioridad_recoleccion || 'Estándar';
        document.getElementById('res_flujo').innerText = r.flujo_bodega || 'Consolidación por destino';
        document.getElementById('res_zona').innerText = r.zona_destino || 'ZONA-ESTANDAR';
        document.getElementById('res_anden').innerText = r.anden_bodega || 'Andén General';
        document.getElementById('res_estiba').innerText = r.ubicacion_jaula || 'Estiba Estándar';
        document.getElementById('res_seguridad').innerText = r.seguridad_bodega || 'Custodia Estándar';
        document.getElementById('res_vehiculo').innerText = r.vehiculo_ruta || 'Panel Estándar';
        document.getElementById('res_estrategia').innerText = r.estrategia_ruta || 'Ruta Estándar';
        document.getElementById('res_entrega').innerText = r.requisito_entrega || 'Firma de recibido';

        // Actualizar trazabilidad paso a paso
        let trazaHtml = '';
        if (data.traza && data.traza.length > 0) {
            data.traza.forEach((t, idx) => {
                trazaHtml += `
                    <div class="trace-box">
                        <strong>[${t.regla_id}] ${t.name || t.nombre}</strong><br>
                        <span>${t.explicacion}</span>
                    </div>
                `;
            });
        } else {
            trazaHtml = '<p style="color:var(--muted); font-size:0.85rem;">Ninguna regla activada con los parámetros actuales.</p>';
        }
        document.getElementById('contenedor-traza').innerHTML = trazaHtml;

    } catch (e) {
        console.error("Error al comunicar con el motor:", e);
    }
}

// Ejecutar al cargar la página
window.onload = () => evaluarEnTiempoReal();
</script>
</body>
</html>
"""


class InterfazCLI:
    """Implementa la interfaz web reactiva en tiempo real manteniendo la compatibilidad con main.py."""

    def __init__(self, motor: MotorInferencia, puerto: int = 8000):
        self.motor = motor
        self.puerto = puerto

    def iniciar_menu(self) -> None:
        motor_ref = self.motor

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: Any) -> None:
                pass  # Silenciar logs en consola para mantenerla limpia

            def do_GET(self) -> None:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(HTML_TEMPLATE.encode("utf-8"))

            def do_POST(self) -> None:
                if self.path == "/api/evaluar":
                    length = int(self.headers.get("Content-Length", 0))
                    body = json.loads(self.rfile.read(length).decode("utf-8"))
                    resultado = motor_ref.encadenamiento_adelante(body)
                    respuesta = {
                        "resultado": resultado,
                        "traza": motor_ref.explicador.traza
                    }
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps(respuesta, ensure_ascii=False).encode("utf-8"))

        url = f"http://localhost:{self.puerto}"
        servidor = HTTPServer(("127.0.0.1", self.puerto), Handler)
        print(f"\n  ✔ Interfaz Web Interactiva en Tiempo Real activa en: {url}")
        print("  ✔ El navegador se abrirá automáticamente. Presione Ctrl + C en la terminal para salir.\n")
        webbrowser.open(url)
        servidor.serve_forever()

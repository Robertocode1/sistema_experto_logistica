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
        .container { max-width: 1200px; margin: 0 auto; }
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
            word-break: break-word;
        }
        .result-item span { color: var(--muted); font-size: 0.8rem; display: inline-block; width: 150px; }
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
        <!-- COLUMNA IZQUIERDA: PARÁMETROS DE ENTRADA -->
        <div class="card">
            <div class="card-title">📝 Parámetros del Paquete (Hechos)</div>
            
            <div class="form-group">
                <label>Estado del Paquete / Tienda</label>
                <select id="estado_paquete" onchange="evaluarEnTiempoReal()">
                    <option value="registrado_tienda" selected>Registrado en Tienda</option>
                    <option value="en_bodega">En Bodega</option>
                </select>
            </div>
            <div class="form-group">
                <label>Paquetes acumulados en Tienda (First-Mile)</label>
                <input type="number" id="paquetes_en_tienda" value="6" min="0" oninput="evaluarEnTiempoReal()">
            </div>
            <div class="form-group">
                <label>Zona de Destino</label>
                <select id="zona_destino" onchange="evaluarEnTiempoReal()">
                    <option value="central" selected>Central (San Salvador)</option>
                    <option value="occidental">Occidental (Santa Ana)</option>
                    <option value="oriental">Oriental (San Miguel)</option>
                </select>
            </div>
            <div class="form-group">
                <label>Peso del Paquete (kg)</label>
                <input type="number" id="peso_kg" value="12" min="0.1" step="0.5" oninput="evaluarEnTiempoReal()">
            </div>
            <div class="form-group">
                <label>Tipo de Pago</label>
                <select id="tipo_pago" onchange="evaluarEnTiempoReal()">
                    <option value="contra_entrega" selected>Contra Entrega (COD)</option>
                    <option value="pagado_tienda">Pagado en Tienda</option>
                </select>
            </div>
            <div class="form-group">
                <label>Maneja Carga Frágil (Regla R11)</label>
                <select id="maneja_fragil" onchange="evaluarEnTiempoReal()">
                    <option value="true" selected>Sí (Frágil)</option>
                    <option value="false">No</option>
                </select>
            </div>
            <div class="form-group">
                <label>Estado de Entrega (Regla R10)</label>
                <select id="estado_entrega" onchange="evaluarEnTiempoReal()">
                    <option value="entregado">Entregado</option>
                    <option value="no_entregado" selected>No Entregado (Falla)</option>
                    <option value="normal">Normal</option>
                </select>
            </div>
            <div class="form-group">
                <label>Motivo de Falla de Entrega</label>
                <select id="motivo_falla" onchange="evaluarEnTiempoReal()">
                    <option value="cliente_ausente" selected>Cliente Ausente</option>
                    <option value="direccion_incorrecta">Dirección Incorrecta</option>
                </select>
            </div>
            <div class="form-group">
                <label>Intentos Realizados</label>
                <input type="number" id="intentos_realizados" value="1" min="0" oninput="evaluarEnTiempoReal()">
            </div>
        </div>

        <!-- COLUMNA DERECHA: RESULTADOS DINÁMICOS -->
        <div>
            <div class="card">
                <div class="card-title">📦 Dictamen Logístico Inferido</div>
                
                <div class="result-section">
                    <h4>Asignación Operativa y Bodega</h4>
                    <div class="result-item"><span>Acción Recolección:</span> <strong id="res_accion_recoleccion">-</strong></div>
                    <div class="result-item"><span>Bodega Destino:</span> <strong id="res_bodega_destino">-</strong></div>
                    <div class="result-item"><span>Hub Regional:</span> <strong id="res_hub_regional">-</strong></div>
                </div>

                <div class="result-section">
                    <h4>Flota y Tipo de Reparto</h4>
                    <div class="result-item"><span>Vehículo Asignado:</span> <strong id="res_vehiculo_asignado" style="color:var(--primary)">-</strong></div>
                    <div class="result-item"><span>Tipo Reparto:</span> <strong id="res_tipo_reparto">-</strong></div>
                </div>

                <div class="result-section">
                    <h4>Gestión Financiera y Excepciones</h4>
                    <div class="result-item"><span>Proceso Financiero:</span> <strong id="res_proceso_financiero">-</strong></div>
                    <div class="result-item"><span>Acción Operativa:</span> <strong id="res_accion_operativa">-</strong></div>
                    <div class="result-item"><span>Etiquetado Especial:</span> <strong id="res_etiquetado_especial">-</strong></div>
                </div>
            </div>

            <div class="card">
                <div class="card-title">🔍 Trazabilidad Experta (Reglas Disparadas)</div>
                <div id="contenedor-traza">
                    <p style="color:var(--muted); font-size:0.85rem;">Modifique los parámetros para ver las reglas activarse en tiempo real.</p>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
async function evaluarEnTiempoReal() {
    const payload = {
        estado_paquete: document.getElementById('estado_paquete').value,
        paquetes_en_tienda: parseInt(document.getElementById('paquetes_en_tienda').value) || 0,
        zona_destino: document.getElementById('zona_destino').value,
        peso_kg: parseFloat(document.getElementById('peso_kg').value) || 0,
        tipo_pago: document.getElementById('tipo_pago').value,
        maneja_fragil: document.getElementById('maneja_fragil').value === 'true',
        estado_entrega: document.getElementById('estado_entrega').value,
        motivo_falla: document.getElementById('motivo_falla').value,
        intentos_realizados: parseInt(document.getElementById('intentos_realizados').value) || 0,
        volumen_alto: false
    };

    try {
        const res = await fetch('/api/evaluar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        const r = data.resultado;

        // Actualizar interfaz con los valores devueltos por el motor
        document.getElementById('res_accion_recoleccion').innerText = r.accion_recoleccion || 'Pendiente';
        document.getElementById('res_bodega_destino').innerText = r.bodega_destino || 'Por definir';
        document.getElementById('res_hub_regional').innerText = r.hub_regional || 'N/A';
        document.getElementById('res_vehiculo_asignado').innerText = r.vehiculo_asignado || 'Sin asignar';
        document.getElementById('res_tipo_reparto').innerText = r.tipo_reparto || 'Estándar';
        document.getElementById('res_proceso_financiero').innerText = r.proceso_financiero || 'N/A';
        document.getElementById('res_accion_operativa').innerText = r.accion_operativa || 'Ninguna';
        document.getElementById('res_etiquetado_especial').innerText = r.etiquetado_especial || 'Estándar';

        // Trazabilidad paso a paso
        let trazaHtml = '';
        if (data.traza && data.traza.length > 0) {
            data.traza.forEach((t) => {
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

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from motor import MotorInferencia


class TestSistemaExpertoLogistica(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        ruta_reglas = os.path.join(ruta_base, "conocimiento", "reglas.json")
        cls.motor = MotorInferencia(ruta_reglas)

    def test_01_recoleccion_tienda_y_moto_express(self):
        paquete = {
            "id_paquete": "PAQ-001",
            "tienda_origen": "Sucursal Escalón",
            "destino": "San Salvador Centro",
            "estado_paquete": "en_tienda",
            "peso_kg": 5.0,
            "fragilidad": "baja",
            "urgencia": "alta",
            "distancia_km": 12,
            "valor_usd": 120.0
        }
        res = self.motor.encadenamiento_adelante(paquete)
        self.assertEqual(res.get("zona_destino"), "ZONA-URBANA")
        self.assertEqual(res.get("flujo_bodega"), "Cross-Docking Directo")
        self.assertEqual(res.get("vehiculo_ruta"), "Motocicleta de Reparto")

    def test_02_distribucion_urbana_panel_consolidado(self):
        paquete = {
            "id_paquete": "PAQ-002",
            "tienda_origen": "Tienda Soyapango",
            "destino": "Santa Tecla",
            "estado_paquete": "en_tienda",
            "peso_kg": 45.0,
            "fragilidad": "media",
            "urgencia": "media",
            "distancia_km": 18,
            "valor_usd": 200.0
        }
        res = self.motor.encadenamiento_adelante(paquete)
        self.assertEqual(res.get("zona_destino"), "ZONA-URBANA")
        self.assertEqual(res.get("flujo_bodega"), "Consolidación por Destino")
        self.assertEqual(res.get("vehiculo_ruta"), "Panel / Furgoneta (1.5 Toneladas)")

    def test_03_ruta_regional_fragil_y_alto_valor(self):
        paquete = {
            "id_paquete": "PAQ-003",
            "tienda_origen": "Tienda Multiplaza",
            "destino": "Santa Ana",
            "estado_paquete": "en_tienda",
            "peso_kg": 30.0,
            "fragilidad": "alta",
            "urgencia": "media",
            "distancia_km": 65,
            "valor_usd": 1500.0
        }
        res = self.motor.encadenamiento_adelante(paquete)
        self.assertEqual(res.get("zona_destino"), "ZONA-REGIONAL")
        self.assertEqual(res.get("anden_bodega"), "Andén B (Jaulas de Ruta Departamental)")
        self.assertEqual(res.get("ubicacion_jaula"), "Nivel Superior (No apilar carga encima)")
        self.assertIn("Candado", res.get("seguridad_bodega", ""))
        self.assertEqual(res.get("vehiculo_ruta"), "Camión Furgón (3.5 Toneladas)")

    def test_04_ruta_troncal_nacional_larga_distancia(self):
        paquete = {
            "id_paquete": "PAQ-004",
            "tienda_origen": "Tienda Centro",
            "destino": "San Miguel",
            "estado_paquete": "en_tienda",
            "peso_kg": 300.0,
            "fragilidad": "baja",
            "urgencia": "baja",
            "distancia_km": 138,
            "valor_usd": 500.0
        }
        res = self.motor.encadenamiento_adelante(paquete)
        self.assertEqual(res.get("zona_destino"), "ZONA-NACIONAL-LEJANA")
        self.assertEqual(res.get("anden_bodega"), "Andén C (Plataformas de Ruta Troncal)")
        self.assertEqual(res.get("vehiculo_ruta"), "Camión Rígido (8 Toneladas)")

    def test_05_agrupacion_bodega_por_destino(self):
        lote_tiendas = [
            {
                "id_paquete": "PAQ-101",
                "tienda_origen": "Tienda Soyapango",
                "destino": "Santa Ana",
                "estado_paquete": "en_tienda",
                "peso_kg": 40.0,
                "fragilidad": "alta",
                "urgencia": "media",
                "distancia_km": 65,
                "valor_usd": 300.0
            },
            {
                "id_paquete": "PAQ-102",
                "tienda_origen": "Tienda Merliot",
                "destino": "Santa Ana",
                "estado_paquete": "en_tienda",
                "peso_kg": 85.0,
                "fragilidad": "baja",
                "urgencia": "baja",
                "distancia_km": 65,
                "valor_usd": 150.0
            }
        ]
        consolidado = self.motor.agrupar_lote_por_destino(lote_tiendas)
        self.assertIn("Santa Ana", consolidado)
        self.assertEqual(consolidado["Santa Ana"]["total_paquetes"], 2)
        self.assertEqual(consolidado["Santa Ana"]["peso_acumulado_kg"], 125.0)
        self.assertEqual(consolidado["Santa Ana"]["anden_bodega"], "Andén B (Jaulas de Ruta Departamental)")

    def test_06_modulo_explicacion_por_que(self):
        paquete = {
            "id_paquete": "PAQ-006",
            "tienda_origen": "Sucursal Escalón",
            "destino": "Antiguo Cuscatlan",
            "estado_paquete": "en_tienda",
            "peso_kg": 3.0,
            "fragilidad": "baja",
            "urgencia": "alta",
            "distancia_km": 8,
            "valor_usd": 90.0
        }
        self.motor.encadenamiento_adelante(paquete)
        explicacion = self.motor.explicador.responder_por_que()
        self.assertIn("R01", explicacion)
        self.assertIn("R03", explicacion)
        self.assertIn("R08", explicacion)


if __name__ == "__main__":
    unittest.main()

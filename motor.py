import json
import operator
from collections import defaultdict
from typing import Dict, List, Any
from explicacion import ModuloExplicacion

class MotorInferencia:
    OPERADORES = {
        "==": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le
    }

    def __init__(self, ruta_reglas: str = "conocimiento/reglas.json"):
        self.ruta_reglas = ruta_reglas
        self.reglas = self._cargar_reglas()
        self.explicador = ModuloExplicacion()

    def _cargar_reglas(self) -> List[Dict[str, Any]]:
        with open(self.ruta_reglas, mode="r", encoding="utf-8") as archivo:
            reglas = json.load(archivo)
        return sorted(reglas, key=lambda r: r.get("prioridad", 100))

    def _evaluar_condicion(self, condicion: Dict[str, Any], hechos: Dict[str, Any]) -> bool:
        variable = condicion["variable"]
        if variable not in hechos:
            return False

        op_func = self.OPERADORES.get(condicion["operador"])
        if not op_func:
            raise ValueError(f"Operador no válido: {condicion['operador']}")

        return op_func(hechos[variable], condicion["valor"])

    def encadenamiento_adelante(self, hechos_iniciales: Dict[str, Any]) -> Dict[str, Any]:
        hechos = hechos_iniciales.copy()
        self.explicador.limpiar()
        reglas_disparadas = set()
        cambio_en_memoria = True

        while cambio_en_memoria:
            cambio_en_memoria = False
            for regla in self.reglas:
                regla_id = regla["id"]
                if regla_id in reglas_disparadas:
                    continue

                # Soporte flexible para "condiciones" (formato antiguo) o "si" (formato nuevo)
                condiciones_regla = regla.get("condiciones") or regla.get("si", [])

                if all(self._evaluar_condicion(c, hechos) for c in condiciones_regla):
                    # Soporte flexible para "conclusiones" (antiguo) o "entonces" (nuevo)
                    conclusiones_regla = regla.get("conclusiones") or regla.get("entonces", {})
                    
                    for clave, valor in conclusiones_regla.items():
                        if clave not in hechos:
                            hechos[clave] = valor

                    reglas_disparadas.add(regla_id)
                    self.explicador.registrar_paso(regla, hechos)
                    cambio_en_memoria = True

        return hechos

    def agrupar_lote_por_destino(self, paquetes: List[Dict[str, Any]]) -> Dict[str, Any]:
        grupos_bodega = defaultdict(lambda: {
            "zona_destino": "",
            "anden_bodega": "",
            "vehiculo_ruta": "",
            "estrategia_ruta": "",
            "total_paquetes": 0,
            "peso_acumulado_kg": 0.0,
            "paquetes": []
        })

        for paq in paquetes:
            resultado = self.encadenamiento_adelante(paq)
            destino = resultado.get("destino", "DESTINO_GENERAL")
            
            grupo = grupos_bodega[destino]
            grupo["zona_destino"] = resultado.get("zona_destino", "N/A")
            grupo["anden_bodega"] = resultado.get("anden_bodega", "Andén General")
            grupo["vehiculo_ruta"] = resultado.get("vehiculo_ruta", "Por asignar")
            grupo["estrategia_ruta"] = resultado.get("estrategia_ruta", "Estándar")
            grupo["total_paquetes"] += 1
            grupo["peso_acumulado_kg"] += float(resultado.get("peso_kg", 0))
            grupo["paquetes"].append({
                "id": resultado.get("id_paquete", "S/N"),
                "tienda_origen": resultado.get("tienda_origen", "Tienda"),
                "prioridad_recoleccion": resultado.get("prioridad_recoleccion"),
                "ubicacion_jaula": resultado.get("ubicacion_jaula", "Estiba Estándar")
            })

        return dict(grupos_bodega)
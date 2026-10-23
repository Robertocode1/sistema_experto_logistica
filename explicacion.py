from typing import List, Dict, Any

class ModuloExplicacion:
    def __init__(self):
        self.traza: List[Dict[str, Any]] = []

    def limpiar(self) -> None:
        self.traza.clear()

    def registrar_paso(self, regla: Dict[str, Any], hechos_evaluados: Dict[str, Any]) -> None:
        # Soporte flexible: lee "condiciones" o "si"
        condiciones_regla = regla.get("condiciones") or regla.get("si", [])
        # Soporte flexible: lee "conclusiones" o "entonces"
        conclusiones_regla = regla.get("conclusiones") or regla.get("entonces", {})

        condiciones_cumplidas = []
        for cond in condiciones_regla:
            var = cond["variable"]
            val_actual = hechos_evaluados.get(var)
            condiciones_cumplidas.append(
                f"{var} ({val_actual}) {cond['operador']} {cond['valor']}"
            )

        self.traza.append({
            "regla_id": regla["id"],
            "nombre": regla["nombre"],
            "condiciones_activadas": condiciones_cumplidas,
            "conclusiones": conclusiones_regla,
            "explicacion": regla["explicacion"]
        })

    def responder_por_que(self) -> str:
        if not self.traza:
            return "No se activó ninguna regla de la base de conocimiento para este paquete."

        lineas = ["\n=================================================================="]
        lineas.append("   EXPLICACIÓN DEL SISTEMA EXPERTO (¿POR QUÉ SE TOMÓ LA DECISIÓN?)")
        lineas.append("==================================================================")
        
        for i, paso in enumerate(self.traza, start=1):
            lineas.append(f"\n[Paso {i}] Regla Activada: {paso['regla_id']} - {paso['nombre']}")
            lineas.append(f"  ├─ Condiciones cumplidas : {', '.join(paso['condiciones_activadas'])}")
            lineas.append(f"  ├─ Decisión inferida     : {paso['conclusiones']}")
            lineas.append(f"  └─ Justificación experta : {paso['explicacion']}")
            
        return "\n".join(lineas)
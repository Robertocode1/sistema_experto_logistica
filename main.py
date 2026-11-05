import os
import sys
from motor import MotorInferencia
from interfaz import InterfazCLI


def main() -> None:
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_reglas = os.path.join(ruta_base, "conocimiento", "reglas.json")

    if not os.path.exists(ruta_reglas):
        print(f"[ERROR CRÍTICO] No se encontró la base de conocimiento en: {ruta_reglas}")
        sys.exit(1)

    try:
        motor = MotorInferencia(ruta_reglas=ruta_reglas)
        cli = InterfazCLI(motor=motor)
        cli.iniciar_menu()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupción detectada por el usuario. Saliendo del sistema...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR EN EJECUCIÓN] Ocurrió un problema inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
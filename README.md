# SISTEMA EXPERTO EN OPTIMIZACION Y GESTION LOGISTICA

* Sistema experto basado en reglas heuristicas y tecnicas de inferencia logica, disenado para la toma de decisiones automatizada en la gestion de la cadena de suministro, distribucion y transporte de mercancias.

### DESCRIPCION GENERAL Y ALCANCE

* El sistema formaliza y automatiza el conocimiento operativo de especialistas en transporte y almacenamiento. A traves de un motor de inferencia desacoplado de la base de conocimiento, evalua hechos contextuales ingresados por el operador y deduce acciones recomendadas para cuatro areas criticas del flujo logistico.

# MODULOS FUNCIONALES

### OPTIMIZADOR DE RUTAS DE ENTREGA

* Variables de entrada: distancia, trafico vehicular, ventanas de tiempo de entrega y capacidad del vehiculo (peso y volumen).

* Logica heuristica: consolidacion de envios por densidad de paradas (ejemplo: si hay mas de 5 entregas en una misma zona, agruparlas en la misma ruta), priorizacion de franjas horarias estrictas y minimizacion de tiempos en transito.

### GESTION DE INVENTARIO PREDICTIVO

* Variables de entrada: historico de demanda, estacionalidad, tendencias de consumo y tiempo de reposicion de proveedores.

* Logica heuristica: calculo de puntos de reorden, sugerencia de cantidades optimas de pedido y emision de alertas tempranas sobre riesgo de quiebre de stock o sobrecostos por exceso de inventario.

### CLASIFICADOR DE PRIORIDADES DE ENVIO

* Variables de entrada: tipo de producto (perecedero, fragil, estandar, peligroso), valor declarado, destino y nivel de servicio pactado (SLA).

* Logica heuristica: determinacion del metodo de transporte optimo (aereo, terrestre, maritimo o multimodal) evaluando la relacion costo-beneficio frente a la urgencia requerida.

### DIAGNOSTICO DE CUELLOS DE BOTELLA

* Variables de entrada: tiempos de proceso en recepcion, almacenamiento, preparacion de pedidos (picking/packing), despacho y transito.

* Logica heuristica: medicion de desviaciones sobre la linea base operativa, identificacion de fases saturadas y recomendacion de redistribucion de recursos basada en patrones historicos.


### REGLAS AGREGADAS EN EL PARCIAL
## Regla 1: Protocolo de Segundo Intento por Ausencia del Cliente
* SI: estado_entrega == "no_entregado" Y motivo_falla == "cliente_ausente" Y intentos_realizados == 1

* ENTONCES:

* accion_operativa = "Reprogramar para Día Siguiente"

* notificacion_cliente = "Enviar enlace de confirmación de franja horaria"

* Explicación: Si un paquete no pudo entregarse en el primer intento por ausencia del receptor, el sistema lo reprograma * automáticamente para el día siguiente y le notifica al cliente para asegurar su presencia.

## Regla 2: Control de Carga Frágil o Especial
* SI: maneja_fragil == true O requiere_refrigeracion == true

* ENTONCES:

* etiquetado_especial = "Sello de Manipulación Cuidadosa"

* restriccion_carga = "No apilar / Cargar en sección superior"

* Explicación: Las mercancías frágiles o con requerimientos especiales de conservación reciben marcas distintivas y restricciones de estiba para evitar daños durante el transporte.


### INSTRUCCIONES DE EJECUCION

## Requisitos:

* Python 3.10 o superior instalado.

* Ejecutar la aplicacion interactiva:

* python3 main.py


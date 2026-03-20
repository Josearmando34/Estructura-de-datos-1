"""
Backend - Sistema de Gestión de Vuelos en Aeropuerto
Lógica de negocio: Colas circulares, gestión de pistas y lista de espera
con sistema de ticks, tiempos de preparación y límite de espera.
"""

import random


# ─────────────────────────────────────────────
#  ESTRUCTURA: Vuelo
# ─────────────────────────────────────────────

class Vuelo:
    """
    Representa un vuelo con su nombre, tiempo de preparación restante
    y tiempo acumulado en lista de espera.
    
    Decisión de diseño: encapsular el estado temporal del vuelo en su propia
    clase en lugar de usar diccionarios, facilita comparaciones y logs claros.
    """

    TIEMPO_MIN = 2   # ticks mínimos de preparación
    TIEMPO_MAX = 5   # ticks máximos de preparación

    def __init__(self, nombre: str):
        self.nombre = nombre
        # Tiempo de preparación aleatorio en pista antes de poder despegar
        self.ticks_restantes: int = random.randint(self.TIEMPO_MIN, self.TIEMPO_MAX)
        # Ticks acumulados en lista de espera (informativo)
        self.ticks_en_espera: int = 0

    def listo_para_despegar(self) -> bool:
        """Retorna True si el vuelo completó su preparación."""
        return self.ticks_restantes <= 0

    def tick_pista(self):
        """Descuenta un tick de preparación (mínimo 0)."""
        if self.ticks_restantes > 0:
            self.ticks_restantes -= 1

    def tick_espera(self):
        """Incrementa el tiempo acumulado en lista de espera."""
        self.ticks_en_espera += 1

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return f"Vuelo({self.nombre}, ticks={self.ticks_restantes})"


# ─────────────────────────────────────────────
#  ESTRUCTURA: Cola Circular
# ─────────────────────────────────────────────

class ColaCircular:
    """
    Cola circular de capacidad fija que almacena objetos Vuelo.
    
    Decisión de diseño: los slots ahora guardan instancias de Vuelo (no strings),
    lo que permite acceder al estado temporal de cada vuelo desde la pista.
    Los métodos get_slots() y siguiente() siguen siendo públicos para el frontend.
    """

    def __init__(self, capacidad: int, nombre: str):
        self.capacidad = capacidad
        self.nombre = nombre
        self.datos: list[Vuelo | None] = [None] * capacidad
        self.frente = 0
        self.final = 0
        self.tamaño = 0

    def esta_llena(self) -> bool:
        return self.tamaño == self.capacidad

    def esta_vacia(self) -> bool:
        return self.tamaño == 0

    def encolar(self, vuelo: Vuelo) -> bool:
        """Agrega un vuelo al final de la cola. Retorna False si está llena."""
        if self.esta_llena():
            return False
        self.datos[self.final] = vuelo
        self.final = (self.final + 1) % self.capacidad
        self.tamaño += 1
        return True

    def desencolar(self) -> Vuelo | None:
        """Retira el vuelo del frente si está listo. Retorna None si no."""
        if self.esta_vacia():
            return None
        vuelo = self.datos[self.frente]
        self.datos[self.frente] = None
        self.frente = (self.frente + 1) % self.capacidad
        self.tamaño -= 1
        return vuelo

    def siguiente(self) -> Vuelo | None:
        """Retorna el vuelo en el frente sin retirarlo."""
        if self.esta_vacia():
            return None
        return self.datos[self.frente]

    def get_slots(self) -> list[Vuelo | None]:
        """Retorna copia de los slots para visualización."""
        return list(self.datos)

    def tick(self) -> list[Vuelo]:
        """
        Avanza un tick en todos los vuelos de esta pista.
        Retorna lista de vuelos que despegaron en este tick.
        
        Decisión de diseño: solo el vuelo del frente puede despegar;
        los demás se preparan pero esperan su turno en la cola.
        """
        despegados = []

        # Descontar ticks a todos los vuelos en la pista
        for slot in self.datos:
            if slot is not None:
                slot.tick_pista()

        # El vuelo del frente despega si su tiempo llegó a 0
        frente = self.siguiente()
        if frente is not None and frente.listo_para_despegar():
            vuelo = self.desencolar()
            despegados.append(vuelo)

        return despegados


# ─────────────────────────────────────────────
#  MANAGER: Lógica de Negocio
# ─────────────────────────────────────────────

class AeropuertoManager:
    """
    Gestor del aeropuerto. Administra pistas, lista de espera y ciclos de simulación.
    
    Nuevas responsabilidades respecto a la versión anterior:
    - Mantener límite máximo en lista de espera (MAX_ESPERA)
    - Rechazar vuelos cuando lista de espera esté llena
    - Procesar ticks: descontar tiempos, disparar despegues automáticos,
      mover vuelos desde espera a pistas liberadas
    - Llevar log de eventos por tick para el frontend
    """

    NUM_PISTAS      = 3
    CAPACIDAD_PISTA = 5
    MAX_ESPERA      = 8   # Límite configurable de lista de espera

    def __init__(self):
        self.pistas: list[ColaCircular] = [
            ColaCircular(self.CAPACIDAD_PISTA, f"Pista {i+1}")
            for i in range(self.NUM_PISTAS)
        ]
        self.lista_espera: list[Vuelo] = []
        self.contador_vuelo = 1
        self.contador_pista_despegue = 0  # Para Round-Robin
        self.tick_actual = 0
        # Log de eventos del último tick (para el frontend)
        self.eventos_ultimo_tick: list[tuple[str, str]] = []

    # ── Generación de datos ────────────────

    def generar_nombre_vuelo(self) -> str:
        """Genera el siguiente nombre de vuelo (ej: MX001, AM002)."""
        prefijos = ["MX", "AM", "VB", "LA", "AV"]
        nombre = f"{random.choice(prefijos)}{self.contador_vuelo:03d}"
        self.contador_vuelo += 1
        return nombre

    # ── Búsqueda y selección ───────────────

    def obtener_pista_menos_ocupada(self) -> ColaCircular | None:
        """Retorna la pista con menor cantidad de vuelos que no esté llena."""
        no_llenas = [p for p in self.pistas if not p.esta_llena()]
        if not no_llenas:
            return None
        return min(no_llenas, key=lambda p: p.tamaño)

    def obtener_primera_pista_con_vuelos(self) -> ColaCircular | None:
        """Retorna la primera pista que tenga vuelos."""
        for p in self.pistas:
            if not p.esta_vacia():
                return p
        return None

    def obtener_siguiente_pista_roundrobin(self) -> ColaCircular | None:
        """Retorna la siguiente pista en Round-Robin que tenga vuelos."""
        inicio = self.contador_pista_despegue
        for i in range(self.NUM_PISTAS):
            idx = (inicio + i) % self.NUM_PISTAS
            if not self.pistas[idx].esta_vacia():
                self.contador_pista_despegue = (idx + 1) % self.NUM_PISTAS
                return self.pistas[idx]
        return None

    def espera_llena(self) -> bool:
        """Retorna True si la lista de espera alcanzó su límite."""
        return len(self.lista_espera) >= self.MAX_ESPERA

    # ── Operaciones de vuelos ──────────────

    def registrar_vuelo(self) -> tuple[Vuelo, ColaCircular | None, bool]:
        """
        Genera y registra un nuevo vuelo.
        Retorna: (vuelo, pista_asignada, rechazado)
        - Si hay pista disponible: (vuelo, pista, False)
        - Si va a espera:          (vuelo, None, False)
        - Si es rechazado:         (vuelo, None, True)
        
        Decisión de diseño: retornar una tupla de 3 elementos en lugar de 2
        para que el frontend pueda distinguir entre "en espera" y "rechazado"
        sin lógica adicional.
        """
        vuelo = Vuelo(self.generar_nombre_vuelo())
        pista = self.obtener_pista_menos_ocupada()

        if pista:
            pista.encolar(vuelo)
            return (vuelo, pista, False)
        elif not self.espera_llena():
            self.lista_espera.append(vuelo)
            return (vuelo, None, False)
        else:
            # Vuelo rechazado: lista de espera llena
            return (vuelo, None, True)

    def despegar_vuelo(self, pista_idx: int | None = None) -> tuple[Vuelo | None, Vuelo | None]:
        """
        Despega manualmente el vuelo del frente de la pista (sin respetar ticks).
        Usado solo para acción manual desde el frontend.
        Retorna: (vuelo_despegado, vuelo_que_entra_de_espera)
        """
        if pista_idx is None:
            pista = self.obtener_siguiente_pista_roundrobin()
        else:
            pista = self.pistas[pista_idx]

        if pista is None or pista.esta_vacia():
            return (None, None)

        vuelo_despegado = pista.desencolar()

        vuelo_de_espera = None
        if self.lista_espera:
            vuelo_de_espera = self.lista_espera.pop(0)
            pista.encolar(vuelo_de_espera)

        return (vuelo_despegado, vuelo_de_espera)

    def avanzar_tick(self) -> list[tuple[str, str]]:
        """
        Avanza un ciclo de simulación (tick).
        En cada tick:
          1. Descuenta ticks de preparación a todos los vuelos en pistas.
          2. Despega automáticamente los vuelos listos (frente de cola con ticks=0).
          3. Incrementa ticks_en_espera de vuelos en lista de espera.
          4. Mueve vuelos desde lista de espera a pistas liberadas (FIFO).
        
        Retorna lista de eventos (mensaje, tag) ocurridos en este tick.
        
        Decisión de diseño: un único método de tick centraliza toda la lógica
        temporal, facilitando la simulación automática y el modo manual.
        """
        self.tick_actual += 1
        eventos: list[tuple[str, str]] = [
            (f"── Tick {self.tick_actual} ──", "sim")
        ]

        # 1 & 2: Tick en pistas → despegar listos
        for pista in self.pistas:
            despegados = pista.tick()
            for v in despegados:
                eventos.append((f"[🛫] {v.nombre} despegó de {pista.nombre} (esperó {v.ticks_en_espera} ticks en espera)", "dep"))

        # 3: Incrementar tiempo de espera en lista general
        for vuelo in self.lista_espera:
            vuelo.tick_espera()

        # 4: Mover desde espera a pistas liberadas (FIFO)
        while self.lista_espera:
            pista = self.obtener_pista_menos_ocupada()
            if pista is None:
                break
            vuelo = self.lista_espera.pop(0)
            pista.encolar(vuelo)
            eventos.append((
                f"[→] {vuelo.nombre} pasó de Espera → {pista.nombre} "
                f"(estuvo {vuelo.ticks_en_espera} ticks esperando)",
                "esp"
            ))

        self.eventos_ultimo_tick = eventos
        return eventos

    # ── Getters para Frontend ──────────────

    def get_pistas(self) -> list[ColaCircular]:
        return self.pistas

    def get_lista_espera(self) -> list[Vuelo]:
        return list(self.lista_espera)

    def get_contador_vuelo(self) -> int:
        return self.contador_vuelo

    def get_tick_actual(self) -> int:
        return self.tick_actual

    def get_max_espera(self) -> int:
        return self.MAX_ESPERA
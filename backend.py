"""
Backend - Sistema de Gestión de Vuelos en Aeropuerto
Lógica de negocio: Colas circulares, gestión de pistas y lista de espera
"""

import random


# ─────────────────────────────────────────────
#  ESTRUCTURA: Cola Circular
# ─────────────────────────────────────────────

class ColaCircular:
    def __init__(self, capacidad: int, nombre: str):
        self.capacidad = capacidad
        self.nombre = nombre
        self.datos = [None] * capacidad
        self.frente = 0
        self.final = 0
        self.tamaño = 0

    def esta_llena(self) -> bool:
        return self.tamaño == self.capacidad

    def esta_vacia(self) -> bool:
        return self.tamaño == 0

    def encolar(self, vuelo: str) -> bool:
        if self.esta_llena():
            return False
        self.datos[self.final] = vuelo
        self.final = (self.final + 1) % self.capacidad
        self.tamaño += 1
        return True

    def desencolar(self) -> str | None:
        if self.esta_vacia():
            return None
        vuelo = self.datos[self.frente]
        self.datos[self.frente] = None
        self.frente = (self.frente + 1) % self.capacidad
        self.tamaño -= 1
        
        # Resetear punteros si la cola quedó vacía
        if self.esta_vacia():
            self.frente = 0
            self.final = 0
        
        return vuelo

    def siguiente(self) -> str | None:
        if self.esta_vacia():
            return None
        return self.datos[self.frente]

    def get_slots(self) -> list:
        return list(self.datos)


# ─────────────────────────────────────────────
#  MANAGER: Lógica de Negocio
# ─────────────────────────────────────────────

class AeropuertoManager:
    """
    Gestor del aeropuerto: administra pistas y lista de espera.
    Responsabilidades:
    - Crear y mantener N colas circulares (pistas)
    - Generar nombres de vuelos
    - Asignar vuelos a la pista menos ocupada
    - Gestionar lista de espera
    - Despejar vuelos
    """

    NUM_PISTAS = 3
    CAPACIDAD_PISTA = 5

    def __init__(self):
        self.pistas = [
            ColaCircular(self.CAPACIDAD_PISTA, f"Pista {i+1}")
            for i in range(self.NUM_PISTAS)
        ]
        self.lista_espera = []
        self.contador_vuelo = 1

    # ── Generación de datos ────────────────

    def generar_nombre_vuelo(self) -> str:
        """Genera el siguiente nombre de vuelo (ej: MX001, AM002, etc)"""
        prefijos = ["MX", "AM", "VB", "LA", "AV"]
        nombre = f"{random.choice(prefijos)}{self.contador_vuelo:03d}"
        self.contador_vuelo += 1
        return nombre

    # ── Búsqueda y selección ───────────────

    def obtener_pista_menos_ocupada(self) -> ColaCircular | None:
        """Retorna la pista con menor cantidad de vuelos (que no esté llena)"""
        no_llenas = [p for p in self.pistas if not p.esta_llena()]
        if not no_llenas:
            return None
        return min(no_llenas, key=lambda p: p.tamaño)

    def obtener_primera_pista_con_vuelos(self) -> ColaCircular | None:
        """Retorna la primera pista que tenga vuelos"""
        for p in self.pistas:
            if not p.esta_vacia():
                return p
        return None

    # ── Operaciones de vuelos ──────────────

    def registrar_vuelo(self) -> tuple[str, ColaCircular | None]:
        """
        Genera y registra un nuevo vuelo.
        Retorna: (nombre_vuelo, pista_asignada)
        - Si hay pista disponible: (vuelo, pista)
        - Si no: (vuelo, None) → va a lista de espera
        """
        vuelo = self.generar_nombre_vuelo()
        pista = self.obtener_pista_menos_ocupada()
        
        if pista:
            pista.encolar(vuelo)
            return (vuelo, pista)
        else:
            self.lista_espera.append(vuelo)
            return (vuelo, None)

    def despegar_vuelo(self, pista_idx: int | None = None) -> tuple[str | None, str | None]:
        """
        Despega un vuelo de la pista indicada (o auto si pista_idx=None).
        Retorna: (vuelo_despegado, vuelo_que_entra_de_espera)
        - vuelo_despegado: nombre del vuelo que se fue
        - vuelo_que_entra_de_espera: nombre del vuelo que pasó de espera a pista (o None)
        """
        if pista_idx is None:
            # Auto: primera pista con vuelos
            pista = self.obtener_primera_pista_con_vuelos()
        else:
            pista = self.pistas[pista_idx]

        if pista is None or pista.esta_vacia():
            return (None, None)

        # Despegar
        vuelo_despegado = pista.desencolar()

        # Intentar mover de espera a la pista
        vuelo_de_espera = None
        if self.lista_espera:
            vuelo_de_espera = self.lista_espera.pop(0)
            pista.encolar(vuelo_de_espera)

        return (vuelo_despegado, vuelo_de_espera)

    # ── Getters para Frontend ──────────────

    def get_pistas(self) -> list[ColaCircular]:
        """Retorna lista de pistas"""
        return self.pistas

    def get_lista_espera(self) -> list[str]:
        """Retorna copia de lista de espera"""
        return list(self.lista_espera)

    def get_contador_vuelo(self) -> int:
        """Retorna el contador actual de vuelos"""
        return self.contador_vuelo
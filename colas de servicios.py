from collections import deque
from datetime import datetime

SERVICES = {
    1: {"name": "Nuevas Pólizas",    "prefix": "NP"},
    2: {"name": "Renovaciones",      "prefix": "RN"},
    3: {"name": "Siniestros",        "prefix": "SI"},
    4: {"name": "Cobros y Pagos",    "prefix": "CP"},
    5: {"name": "Información Gral.", "prefix": "IG"},
}

class Cola:
    def __init__(self, service_id: int):
        self.service_id = service_id
        self.name       = SERVICES[service_id]["name"]
        self.prefix     = SERVICES[service_id]["prefix"]
        self._elementos: deque = deque()
        self._contador  = 0

    def encolar(self) -> str:
        self._contador += 1
        ticket = f"{self.prefix}-{self._contador:03d}"
        self._elementos.append(ticket)
        return ticket

    def desencolar(self):
        if self._elementos:
            return self._elementos.popleft()
        return None

    def proximo(self):
        if self._elementos:
            return self._elementos[0]
        return None

    def esta_vacia(self):
        return len(self._elementos) == 0

    def tamanio(self):
        return len(self._elementos)

    def lista_tickets(self):
        return list(self._elementos)

class SistemaColas:
    def __init__(self):
        self.colas = {sid: Cola(sid) for sid in SERVICES}
        self.historial = []

    def _log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.historial.append(f"[{ts}] {msg}")

    def llega_cliente(self, service_id):
        if service_id not in self.colas:
            return None

        cola = self.colas[service_id]
        ticket = cola.encolar()
        pos = cola.tamanio()

        self._log(f"LLEGADA · Servicio {service_id} ({cola.name}) → ticket {ticket} (posición {pos})")

        return ticket

    def atender(self, service_id):
        if service_id not in self.colas:
            return None

        cola = self.colas[service_id]
        ticket = cola.desencolar()

        if ticket:
            self._log(f"ATENCIÓN · Servicio {service_id} ({cola.name}) ← llamando {ticket}")

        return ticket

    def estado(self):
        return {
            sid: {
                "name": cola.name,
                "size": cola.tamanio(),
                "next": cola.proximo(),
                "tickets": cola.lista_tickets(),
            }
            for sid, cola in self.colas.items()
        }


def mostrar_estado(sistema):
    print("\nEstado de las colas\n")

    estado = sistema.estado()

    for sid, info in estado.items():
        print(f"{sid} - {info['name']}")
        print(f"Clientes en cola: {info['size']}")
        print(f"Próximo: {info['next']}")
        print()


def mostrar_historial(sistema):
    print("\nHistorial\n")

    if not sistema.historial:
        print("Sin eventos")
    else:
        for evento in sistema.historial:
            print(evento)

def main():

    sistema = SistemaColas()

    print("Sistema de Colas - Compañía de Seguros")
    print("Comandos:")
    print("C<n> llegada de cliente")
    print("A<n> atender cliente")
    print("L ver colas")
    print("H historial")
    print("Q salir")

    while True:

        comando = input("\n> ").upper()

        if comando == "Q":
            break

        elif comando == "L":
            mostrar_estado(sistema)

        elif comando == "H":
            mostrar_historial(sistema)

        elif comando.startswith("C") and comando[1:].isdigit():

            servicio = int(comando[1:])
            ticket = sistema.llega_cliente(servicio)

            if ticket:
                print("Ticket asignado:", ticket)
            else:
                print("Servicio no válido")

        elif comando.startswith("A") and comando[1:].isdigit():

            servicio = int(comando[1:])
            ticket = sistema.atender(servicio)

            if ticket:
                print("Atendiendo ticket:", ticket)
            else:
                print("Cola vacía")

        else:
            print("Comando inválido")

if __name__ == "__main__":
    main()

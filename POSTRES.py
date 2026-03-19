import bisect

POSTRES = [
    ("Brownie",     ["chocolate", "harina", "azúcar", "huevo", "mantequilla"]),
    ("Cheesecake",  ["queso crema", "galleta", "mantequilla", "azúcar", "huevo"]),
    ("Flan",        ["leche", "huevo", "azúcar", "vainilla"]),
    ("Gelatina",    ["gelatina en polvo", "agua", "azúcar"]),
    ("Tiramisu",    ["mascarpone", "café", "bizcocho", "huevo", "azúcar", "cocoa"]),
]

def _nombres() -> list[str]:
    return [p[0] for p in POSTRES]


def _buscar(nombre: str) -> int:
    nombres = [p[0].lower() for p in POSTRES]
    idx = bisect.bisect_left(nombres, nombre.lower())
    if idx < len(POSTRES) and POSTRES[idx][0].lower() == nombre.lower():
        return idx
    return -1


def _punto_insercion(nombre: str) -> int:
    nombres = [p[0].lower() for p in POSTRES]
    return bisect.bisect_left(nombres, nombre.lower())


def mostrar_ingredientes(nombre: str) -> None:
    idx = _buscar(nombre)

    if idx == -1:
        print(f"  ✗ El postre '{nombre}' no existe en el arreglo.")
        return

    postre, ingredientes = POSTRES[idx]
    print(f"\n  Ingredientes de '{postre}':")
    for i, ing in enumerate(ingredientes, 1):
        print(f"    {i}. {ing}")


def insertar_ingredientes(nombre: str, nuevos: list[str]) -> None:
    if not nuevos:
        print("  ✗ No se proporcionaron ingredientes.")
        return

    idx = _buscar(nombre)
    if idx == -1:
        print(f"  ✗ El postre '{nombre}' no existe.")
        return

    postre, ingredientes = POSTRES[idx]
    ings_lower = [i.lower() for i in ingredientes]

    for nuevo in nuevos:
        if nuevo.lower() not in ings_lower:
            ingredientes.append(nuevo)

    print(f"  ✔ Ingredientes agregados a '{postre}'.")


def eliminar_ingrediente(nombre: str, ingrediente: str) -> None:
    idx = _buscar(nombre)
    if idx == -1:
        print(f"  ✗ El postre '{nombre}' no existe.")
        return

    postre, ingredientes = POSTRES[idx]
    if ingrediente in ingredientes:
        ingredientes.remove(ingrediente)
        print(f"  ✔ Ingrediente eliminado.")
    else:
        print(f"  ✗ No existe ese ingrediente.")


# ✅ AQUÍ ESTÁ EL CAMBIO (YA PERMITE REPETIDOS)
def alta_postre(nombre: str, ingredientes: list[str]) -> None:
    nombre = nombre.strip()
    if not nombre:
        print("  ✗ Nombre vacío.")
        return

    idx = _punto_insercion(nombre)
    POSTRES.insert(idx, (nombre, ingredientes))
    print(f"  ✔ Postre '{nombre}' agregado.")


def baja_postre(nombre: str) -> None:
    idx = _buscar(nombre)
    if idx == -1:
        print(f"  ✗ No existe.")
        return

    POSTRES.pop(idx)
    print(f"  ✔ Eliminado.")


def eliminar_repetidos() -> None:
    vistos = set()
    i = 0

    while i < len(POSTRES):
        nombre = POSTRES[i][0].lower()
        if nombre in vistos:
            POSTRES.pop(i)
        else:
            vistos.add(nombre)
            i += 1

    print("  ✔ Repetidos eliminados.")


def mostrar_todos() -> None:
    print("\nPOSTRES:")
    for i, (p, ing) in enumerate(POSTRES, 1):
        print(i, p, "-", ", ".join(ing))


MENU = """
╔══════════════════════════════════════════╗
║         GESTIÓN DE POSTRES               ║
╠══════════════════════════════════════════╣
║  1. Ver ingredientes de un postre        ║
║  2. Agregar ingredientes a un postre     ║
║  3. Eliminar un ingrediente de un postre ║
║  4. Alta de postre                       ║
║  5. Baja de postre                       ║
║  6. Eliminar postres repetidos           ║
║  7. Mostrar todos los postres            ║
║  0. Salir                                ║
╚══════════════════════════════════════════╝
"""


def main():
    while True:
        print(MENU)
        op = input("Opción: ")

        if op == "1":
            mostrar_ingredientes(input("Postre: "))

        elif op == "2":
            nombre = input("Postre: ")
            nuevos = input("Ingredientes: ").split(",")
            insertar_ingredientes(nombre, nuevos)

        elif op == "3":
            eliminar_ingrediente(input("Postre: "), input("Ingrediente: "))

        elif op == "4":
            nombre = input("Nuevo postre: ")
            ings = input("Ingredientes: ").split(",")
            alta_postre(nombre, ings)

        elif op == "5":
            baja_postre(input("Postre: "))

        elif op == "6":
            eliminar_repetidos()

        elif op == "7":
            mostrar_todos()

        elif op == "0":
            break


if __name__ == "__main__":
    main()
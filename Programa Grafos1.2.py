import heapq
import math
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

ESTADOS = [
    "Yucatán", "Campeche", "Quintana Roo",
    "Tabasco", "Chiapas", "Veracruz", "Oaxaca"
]

ABREV = {
    "Yucatán":      "YUC",
    "Campeche":     "CAM",
    "Quintana Roo": "QROO",
    "Tabasco":      "TAB",
    "Chiapas":      "CHIS",
    "Veracruz":     "VER",
    "Oaxaca":       "OAX",
}

POS = {
    "Yucatán":      (5.5,  7.3),
    "Campeche":     (3.4,  5.8),
    "Quintana Roo": (7.6,  5.9),
    "Tabasco":      (2.2,  4.0),
    "Chiapas":      (3.8,  2.4),
    "Veracruz":     (0.8,  3.5),
    "Oaxaca":       (1.2,  1.2),
}


ARISTAS = [
    ("Yucatán",      "Campeche",     204),
    ("Yucatán",      "Quintana Roo", 320),
    ("Campeche",     "Quintana Roo", 380),
    ("Campeche",     "Tabasco",      444),
    ("Campeche",     "Chiapas",      530),
    ("Quintana Roo", "Chiapas",      620),
    ("Tabasco",      "Chiapas",      290),
    ("Tabasco",      "Veracruz",     355),
    ("Chiapas",      "Oaxaca",       510),
    ("Veracruz",     "Oaxaca",       350),
    ("Veracruz",     "Tabasco",      355),
]

def construir_grafo():
    """Devuelve un diccionario {nodo: {vecino: peso}}."""
    g = {e: {} for e in ESTADOS}
    for u, v, w in ARISTAS:
        g[u][v] = w
        g[v][u] = w
    return g

def dijkstra(grafo, origen):
    """
    Distancias mínimas desde 'origen' a todos los demás nodos.
    Retorna (dist, prev) donde prev permite reconstruir el camino.
    """
    dist = {n: math.inf for n in grafo}
    prev = {n: None for n in grafo}
    dist[origen] = 0
    heap = [(0, origen)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in grafo[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

    return dist, prev


def reconstruir_ruta(prev, origen, destino):
    """Traza la ruta desde 'destino' hacia 'origen' siguiendo prev."""
    ruta, cur = [], destino
    while cur:
        ruta.append(cur)
        cur = prev[cur]
    ruta.reverse()
    return ruta if ruta[0] == origen else []

def camino_hamiltoniano(grafo):
    """
    Busca el camino hamiltoniano de menor costo:
    visita los 7 estados exactamente una vez.
    Usa backtracking con poda por costo.
    """
    mejor = {"costo": math.inf, "camino": None}

    def bt(actual, visitados, camino, costo):
        
        if costo >= mejor["costo"]:
            return
        if len(visitados) == len(ESTADOS):
            mejor["costo"] = costo
            mejor["camino"] = list(camino)
            return
        for v, w in sorted(grafo[actual].items(), key=lambda x: x[1]):
            if v not in visitados:
                visitados.add(v)
                camino.append(v)
                bt(v, visitados, camino, costo + w)
                camino.pop()
                visitados.remove(v)

    for inicio in ESTADOS:
        bt(inicio, {inicio}, [inicio], 0)

    return mejor["camino"], mejor["costo"]

def recorrido_con_repeticion(grafo):
    """
    Recorre los 7 estados repitiendo Campeche (hub natural).
    Orden lógico: Oaxaca→Veracruz→Tabasco→Chiapas→Campeche
                  →Yucatán→Campeche→Quintana Roo
    Cada tramo usa la ruta más corta (Dijkstra).
    """

    dist_min, prev_min = {}, {}
    for e in ESTADOS:
        dist_min[e], prev_min[e] = dijkstra(grafo, e)

    orden = [
        "Oaxaca", "Veracruz", "Tabasco", "Chiapas",
        "Campeche", "Yucatán", "Campeche", "Quintana Roo"
    ]

    ruta_completa = [orden[0]]
    costo_total   = 0

    for i in range(len(orden) - 1):
        tramo = reconstruir_ruta(prev_min[orden[i]], orden[i], orden[i+1])
        ruta_completa.extend(tramo[1:])          # evitar duplicar el nodo de inicio
        costo_total += dist_min[orden[i]][orden[i+1]]

    return ruta_completa, costo_total, orden


PALETA = {
    "fondo":      "#0d1117",
    "panel":      "#161b22",
    "borde":      "#30363d",
    "arista":     "#334155",
    "arista_act": "#3b82f6",
    "nodo_base":  "#1e293b",
    "nodo_ruta":  "#1d4ed8",
    "nodo_rep":   "#d97706",
    "texto_prim": "#e2e8f0",
    "texto_sec":  "#94a3b8",
    "texto_km":   "#64748b",
    "titulo":     "#93c5fd",
    "costo":      "#34d399",
    "num":        "#fbbf24",
}

def _dibujar_panel(ax, grafo, titulo, ruta=None, subtitulo=None):
    ax.set_facecolor(PALETA["panel"])
    for spine in ax.spines.values():
        spine.set_edgecolor(PALETA["borde"])
        spine.set_linewidth(0.8)
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.2, 8.6)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])

    ax.text(5.0, 8.3, titulo,
            fontsize=9.5, fontweight="bold",
            color=PALETA["titulo"], ha="center", va="center",
            fontfamily="monospace")
    if subtitulo:
        ax.text(5.0, 7.85, subtitulo,
                fontsize=8, color=PALETA["costo"], ha="center",
                fontfamily="monospace")

    aristas_act = set()
    if ruta:
        for i in range(len(ruta) - 1):
            aristas_act.add((ruta[i], ruta[i+1]))
            aristas_act.add((ruta[i+1], ruta[i]))

   
    for u, v, w in ARISTAS:
        x0, y0 = POS[u]
        x1, y1 = POS[v]
        activa = (u, v) in aristas_act

        color = PALETA["arista_act"] if activa else PALETA["arista"]
        lw    = 2.5 if activa else 1.0
        alpha = 1.0 if activa else 0.55
        ls    = "-" if activa else "--"

        ax.plot([x0, x1], [y0, y1],
                color=color, lw=lw, alpha=alpha,
                linestyle=ls, zorder=2, solid_capstyle="round")

        mx, my = (x0+x1)/2, (y0+y1)/2
        fc_km = PALETA["arista_act"] if activa else PALETA["texto_km"]
        ax.text(mx, my, f"{w} km",
                fontsize=7.5 if activa else 7.0,
                color=fc_km,
                fontweight="bold" if activa else "normal",
                ha="center", va="bottom",
                fontfamily="monospace",
                bbox=dict(boxstyle="round,pad=0.18",
                          fc=PALETA["panel"], ec="none", alpha=0.85),
                zorder=3)

    conteos = {}
    if ruta:
        for e in ruta:
            conteos[e] = conteos.get(e, 0) + 1


    for est in ESTADOS:
        cx, cy = POS[est]
        repetido = conteos.get(est, 0) > 1
        en_ruta  = conteos.get(est, 0) >= 1

        fc = (PALETA["nodo_rep"]  if repetido else
              PALETA["nodo_ruta"] if en_ruta  else
              PALETA["nodo_base"])
        ec = "#f59e0b" if repetido else ("#60a5fa" if en_ruta else PALETA["borde"])
        lw = 2.0 if (en_ruta or repetido) else 1.0

        circle = plt.Circle((cx, cy), 0.52, fc=fc, ec=ec, lw=lw, zorder=5)
        ax.add_patch(circle)

        ax.text(cx, cy + 0.08, ABREV[est],
                fontsize=8, fontweight="bold", color="#ffffff",
                ha="center", va="center",
                fontfamily="monospace", zorder=6)
        ax.text(cx, cy - 0.22, est,
                fontsize=6.2, color=PALETA["texto_sec"],
                ha="center", va="top",
                fontfamily="monospace", zorder=6)

    
    if ruta:
        for i, est in enumerate(ruta):
            cx, cy = POS[est]
            ax.text(cx + 0.54, cy + 0.48, str(i+1),
                    fontsize=7.5, fontweight="bold",
                    color=PALETA["num"],
                    fontfamily="monospace", zorder=7)


def _panel_relaciones(ax, grafo):
    ax.set_facecolor(PALETA["panel"])
    for spine in ax.spines.values():
        spine.set_edgecolor(PALETA["borde"])
        spine.set_linewidth(0.8)
    ax.axis("off")

    ax.text(0.5, 0.97, "ESTADOS Y RELACIONES",
            transform=ax.transAxes,
            fontsize=10, fontweight="bold",
            color=PALETA["titulo"], ha="center", va="top",
            fontfamily="monospace")

    encabezados = ["Estado", "Abrev.", "Vecinos directos (km)"]
    col_x = [0.01, 0.18, 0.30]
    y0 = 0.88

    for txt, x in zip(encabezados, col_x):
        ax.text(x, y0, txt, transform=ax.transAxes,
                fontsize=8, fontweight="bold",
                color=PALETA["texto_prim"],
                fontfamily="monospace", va="top")

    ax.plot([0.01, 0.99], [y0-0.04, y0-0.04],
            transform=ax.transAxes,
            color=PALETA["borde"], lw=0.8)

    y    = y0 - 0.09
    dy   = 0.107
    alts = ["#1a2233", "#161b22"]

    for idx, est in enumerate(ESTADOS):
        rect = mpatches.FancyBboxPatch(
            (0.0, y - 0.025), 1.0, dy - 0.01,
            boxstyle="square,pad=0", transform=ax.transAxes,
            fc=alts[idx % 2], ec="none", zorder=0)
        ax.add_patch(rect)

        vecinos_txt = "  •  ".join(
            f"{v} ({w} km)"
            for v, w in sorted(grafo[est].items(), key=lambda x: x[1]))

        ax.text(col_x[0], y, est, transform=ax.transAxes,
                fontsize=7.8, color=PALETA["texto_prim"],
                fontfamily="monospace", va="center")
        ax.text(col_x[1], y, ABREV[est], transform=ax.transAxes,
                fontsize=7.8, color=PALETA["titulo"],
                fontfamily="monospace", va="center")
        ax.text(col_x[2], y, vecinos_txt, transform=ax.transAxes,
                fontsize=7.0, color=PALETA["texto_sec"],
                fontfamily="monospace", va="center")
        y -= dy

    ax.text(0.5, 0.03,
            f"Total: {len(ESTADOS)} estados  |  {len(ARISTAS)} aristas  |  "
            "Grafo no dirigido y ponderado",
            transform=ax.transAxes,
            fontsize=7, color=PALETA["texto_km"],
            ha="center", fontfamily="monospace")

def visualizar(grafo, ruta_a, costo_a, ruta_b, costo_b):
    fig = plt.figure(figsize=(20, 14), facecolor=PALETA["fondo"])
    fig.patch.set_facecolor(PALETA["fondo"])

    fig.text(0.5, 0.97,
             "GRAFO DE ESTADOS DE MÉXICO — SURESTE Y SUR",
             ha="center", fontsize=15, fontweight="bold",
             color=PALETA["texto_prim"], fontfamily="monospace")
    fig.text(0.5, 0.945,
             "Yucatán  •  Campeche  •  Quintana Roo  •  Tabasco  "
             "•  Chiapas  •  Veracruz  •  Oaxaca",
             ha="center", fontsize=9,
             color=PALETA["texto_sec"], fontfamily="monospace")

    gs = fig.add_gridspec(
        2, 3,
        top=0.93, bottom=0.04,
        left=0.02, right=0.98,
        hspace=0.08, wspace=0.06,
        height_ratios=[1.6, 1]
    )

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    ax4 = fig.add_subplot(gs[1, :])

    _dibujar_panel(ax1, grafo, "GRAFO COMPLETO",
                   subtitulo=f"{len(ESTADOS)} estados  •  {len(ARISTAS)} aristas")

    _dibujar_panel(ax2, grafo,
                   "INCISO A) — SIN REPETIR ESTADOS",
                   ruta=ruta_a,
                   subtitulo=f"Camino hamiltoniano  •  Costo: {costo_a} km")

    _dibujar_panel(ax3, grafo,
                   "INCISO B) — CON REPETICIÓN",
                   ruta=ruta_b,
                   subtitulo=f"Campeche repetido (naranja)  •  Costo: {costo_b} km")

    _panel_relaciones(ax4, grafo)

    leyenda = [
        mpatches.Patch(fc=PALETA["nodo_base"], ec=PALETA["borde"],  label="Estado sin recorrer"),
        mpatches.Patch(fc=PALETA["nodo_ruta"], ec="#60a5fa",        label="Estado en ruta"),
        mpatches.Patch(fc=PALETA["nodo_rep"],  ec="#f59e0b",        label="Estado repetido"),
        mpatches.Patch(fc=PALETA["arista_act"],ec="none",           label="Arista activa"),
        mpatches.Patch(fc=PALETA["arista"],    ec="none",           label="Arista inactiva"),
    ]
    fig.legend(handles=leyenda,
               loc="lower center", ncol=5,
               frameon=True, framealpha=0.15,
               facecolor=PALETA["panel"],
               edgecolor=PALETA["borde"],
               fontsize=8,
               labelcolor=PALETA["texto_sec"],
               bbox_to_anchor=(0.5, -0.005))

    ruta_img = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "grafo_estados_mexico.png")
    plt.savefig(ruta_img, dpi=160, bbox_inches="tight",
                facecolor=PALETA["fondo"])
    print(f"  [✓] Imagen guardada: {ruta_img}")
    plt.show()
    plt.close()

def imprimir_relaciones(grafo):
    sep = "─" * 70
    print(f"\n{'ESTADOS Y SUS RELACIONES':^70}")
    print(sep)
    print(f"  {'Estado':<16}  Vecinos directos (ordenados por distancia)")
    print(sep)
    for est in ESTADOS:
        vecinos = sorted(grafo[est].items(), key=lambda x: x[1])
        linea   = ",   ".join(f"{v} ({w} km)" for v, w in vecinos)
        print(f"  {est:<16}  ──▶  {linea}")
    print(sep)


def imprimir_ruta(ruta, costo, titulo, grafo):
    sep = "─" * 70
    print(f"\n  {titulo}")
    print(sep)
    for i in range(len(ruta)):
        est = ruta[i]
        if i < len(ruta) - 1:
            sig = ruta[i+1]
            km  = grafo[est].get(sig, None)
            if km:
                tramo = f"──({km:>4} km)──▶  {sig}"
            else:
                tramo = f"──(vía ruta)──▶  {sig}"
            rep = "  ★ REPETIDO" if ruta[:i].count(est) > 0 else ""
            print(f"  {i+1:>2}. {est:<16}{tramo}{rep}")
        else:
            rep = "  ★ REPETIDO" if ruta[:i].count(est) > 0 else ""
            print(f"  {i+1:>2}. {est}{rep}")
    print(sep)
    print(f"  💰  COSTO TOTAL: {costo} km")
    print(sep)


def main():
    sep = "═" * 70
    print(sep)
    print(f"{'GRAFO — ESTADOS DE MÉXICO':^70}")
    print(f"{'Sureste y Sur de la República Mexicana':^70}")
    print(sep)

    grafo = construir_grafo()

  
    print("\n  [*] Calculando camino hamiltoniano (inciso A)…")
    ruta_a, costo_a = camino_hamiltoniano(grafo)
    print(f"  [✓] Camino encontrado: {' → '.join(ruta_a)}")
    print(f"  [✓] Costo: {costo_a} km")

  
    print("\n  [*] Construyendo recorrido con repetición (inciso B)…")
    ruta_b, costo_b, orden_b = recorrido_con_repeticion(grafo)
    print(f"  [✓] Orden de visita: {' → '.join(orden_b)}")
    print(f"  [✓] Costo: {costo_b} km")

    print("\n  [*] Generando imagen del grafo…")
    visualizar(grafo, ruta_a, costo_a, ruta_b, costo_b)

    imprimir_relaciones(grafo)

    imprimir_ruta(ruta_a, costo_a,
                  "INCISO A) CAMINO HAMILTONIANO — visita los 7 estados sin repetir",
                  grafo)

    imprimir_ruta(ruta_b, costo_b,
                  "INCISO B) RECORRIDO CON REPETICIÓN — Campeche aparece 2 veces",
                  grafo)

    estados_rep = sorted({e for e in ruta_b if ruta_b.count(e) > 1})
    print(f"\n  ★  Estado(s) repetido(s) en inciso B: {', '.join(estados_rep)}")

    print(f"\n{sep}")
    print(f"  RESUMEN FINAL")
    print(f"  {'Inciso A (sin repetir)':<30}: {costo_a} km — {len(ruta_a)} estados visitados")
    print(f"  {'Inciso B (con repetición)':<30}: {costo_b} km — {len(set(ruta_b))} únicos "
          f"({len(ruta_b)} paradas totales)")
    print(f"  {'Diferencia de costo':<30}: +{costo_b - costo_a} km por la repetición")
    print(sep)


if __name__ == "__main__":
    main()
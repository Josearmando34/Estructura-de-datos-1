import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.widgets import Button
import numpy as np

# ══════════════════════════════════════════════
#  PALETA DE COLORES
# ══════════════════════════════════════════════
BG       = "#0d1117"
PANEL    = "#161b22"
BORDER   = "#21262d"
TEXT     = "#e6edf3"
MUTED    = "#7d8590"
ACCENT   = ["#58a6ff", "#3fb950", "#d29922", "#bc8cff"]  # por pista
ACCENT_D = ["#1f3d6b", "#1a4726", "#4a3519", "#3d2c6b"]
WARN     = "#d29922"
SUCCESS  = "#3fb950"
DANGER   = "#f85149"
WHITE    = "#ffffff"

# ══════════════════════════════════════════════
#  COLA CIRCULAR
# ══════════════════════════════════════════════
class ColaCircular:
    def __init__(self, capacidad, pista_id, nombre):
        self.capacidad    = capacidad
        self.cola         = [None] * capacidad
        self.frente       = 0
        self.final        = 0
        self.size         = 0
        self.pista_id     = pista_id
        self.nombre       = nombre
        self.total_dep    = 0

    def esta_llena(self): return self.size == self.capacidad
    def esta_vacia(self): return self.size == 0

    def encolar(self, vuelo):
        if self.esta_llena(): return False
        self.cola[self.final] = vuelo
        self.final = (self.final + 1) % self.capacidad
        self.size += 1
        return True

    def desencolar(self):
        if self.esta_vacia(): return None
        v = self.cola[self.frente]
        self.cola[self.frente] = None
        self.frente = (self.frente + 1) % self.capacidad
        self.size -= 1
        self.total_dep += 1
        return v

    def orden(self):
        return [self.cola[(self.frente + i) % self.capacidad]
                for i in range(self.size)]


# ══════════════════════════════════════════════
#  ESTADO GLOBAL
# ══════════════════════════════════════════════
VUELOS = [
    "AV-101","IB-202","AM-303","LA-404","AA-505",
    "DL-606","UA-707","BA-808","AF-909","KL-010",
    "QR-111","EK-212","TK-313","LH-414","AC-515",
]

state = {
    "pistas"      : [],
    "espera"      : [],
    "queue"       : [],
    "total_dep"   : 0,
    "log"         : [],
    "sim_done"    : False,
}

def reset_state():
    state["pistas"]    = [ColaCircular(4, i, n)
                          for i, n in enumerate(["09L","27R","18C","36R"])]
    state["espera"]    = []
    state["queue"]     = list(VUELOS)
    state["total_dep"] = 0
    state["log"]       = ["[SYS] Sistema inicializado — 4 pistas, cap 4"]
    state["sim_done"]  = False

def add_log(msg):
    state["log"].append(msg)
    if len(state["log"]) > 18:
        state["log"] = state["log"][-18:]

def asignar(vuelo):
    avail = [p for p in state["pistas"] if not p.esta_llena()]
    if not avail:
        state["espera"].append(vuelo)
        add_log(f"WAIT {vuelo} → lista de espera")
        return
    p = min(avail, key=lambda x: x.size)
    p.encolar(vuelo)
    add_log(f" OK  {vuelo} → Pista {p.nombre} [{p.size}/4]")

def despachar():
    con = [p for p in state["pistas"] if not p.esta_vacia()]
    if not con:
        add_log("— No hay vuelos para despachar")
        return
    p = max(con, key=lambda x: x.size)
    v = p.desencolar()
    state["total_dep"] += 1
    add_log(f"DESP {v} despegó de Pista {p.nombre} · #{state['total_dep']}")
    if state["espera"]:
        s = state["espera"].pop(0)
        add_log(f" <-   {s} sale de espera → reasignando")
        asignar(s)


# ══════════════════════════════════════════════
#  HELPERS DE DIBUJO
# ══════════════════════════════════════════════
def rounded_box(ax, x, y, w, h, color, alpha=1.0, lw=0.8, ec=None):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02",
        facecolor=color, edgecolor=ec or color,
        linewidth=lw, alpha=alpha,
        zorder=3
    )
    ax.add_patch(box)
    return box

def draw_slot(ax, x, y, w, h, vuelo, idx, is_head, is_tail, color, dark):
    has_flight = vuelo is not None
    fc  = color if has_flight else PANEL
    ec  = color if has_flight else BORDER
    lw  = 1.2 if has_flight else 0.5

    rounded_box(ax, x, y, w, h, fc, alpha=0.3 if has_flight else 1.0, lw=lw, ec=ec)
    if has_flight:
        rounded_box(ax, x, y, w, h, color, alpha=0.12, lw=0, ec=None)

    # índice
    ax.text(x + w/2, y + h - 0.04, f"[{idx}]",
            ha='center', va='top', fontsize=6.5, color=MUTED,
            fontfamily='monospace', zorder=4)

    # vuelo
    label = vuelo[:6] if vuelo else "·  ·  ·"
    fc2   = WHITE if has_flight else MUTED
    ax.text(x + w/2, y + h/2, label,
            ha='center', va='center', fontsize=8,
            fontweight='bold' if has_flight else 'normal',
            color=fc2, fontfamily='monospace', zorder=4)

    # marcadores HEAD/TAIL
    markers = []
    if is_head: markers.append(("H", SUCCESS))
    if is_tail: markers.append(("T", WARN))
    for mi, (m, mc) in enumerate(markers):
        ax.text(x + w/2, y - 0.045 - mi*0.06, m,
                ha='center', va='top', fontsize=7, color=mc,
                fontweight='bold', zorder=4)


# ══════════════════════════════════════════════
#  RENDER PRINCIPAL
# ══════════════════════════════════════════════
def draw(fig, axes):
    for ax in axes.values():
        ax.cla()
        ax.set_facecolor(PANEL)
        for sp in ax.spines.values():
            sp.set_edgecolor(BORDER)
            sp.set_linewidth(0.5)
        ax.set_xticks([])
        ax.set_yticks([])

    draw_runways(axes["runways"])
    draw_diagram(axes["diagram"])
    draw_stats(axes["stats"])
    draw_waiting(axes["waiting"])
    draw_log(axes["log"])
    fig.canvas.draw_idle()


def draw_runways(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Pistas de despegue", color=MUTED, fontsize=8,
                 loc='left', pad=6, fontfamily='monospace')

    slot_w, slot_h = 0.17, 0.18
    col_gap = 0.02
    row_h   = 0.46
    cols    = [0.01, 0.52]   # izq / der

    for i, pista in enumerate(state["pistas"]):
        col = i % 2
        row = i // 2
        ox  = cols[col]
        oy  = 0.96 - row * row_h

        clr = ACCENT[i]
        # encabezado
        ax.text(ox, oy, f"Pista {pista.nombre}", color=clr,
                fontsize=8.5, fontweight='bold', va='top',
                fontfamily='monospace', zorder=4)

        pct = pista.size / pista.capacidad
        bar_lbl_color = DANGER if pct == 1 else (WARN if pct >= .75 else SUCCESS)
        ax.text(ox + 0.44, oy, f"{pista.size}/4",
                color=bar_lbl_color, fontsize=8, va='top',
                ha='right', fontfamily='monospace', zorder=4)

        # barra de ocupación
        bary = oy - 0.065
        rounded_box(ax, ox, bary, 0.44, 0.025, BORDER, lw=0)
        if pct > 0:
            fc = DANGER if pct == 1 else (WARN if pct >= .75 else clr)
            rounded_box(ax, ox, bary, 0.44 * pct, 0.025, fc, lw=0)

        # slots
        sy = bary - 0.1
        for j in range(4):
            sx  = ox + j * (slot_w + col_gap)
            v   = pista.cola[j]
            is_h = not pista.esta_vacia() and j == pista.frente
            is_t = j == pista.final % 4
            draw_slot(ax, sx, sy, slot_w, slot_h, v, j,
                      is_h, is_t, clr, ACCENT_D[i])

        # orden de despegue
        orden = pista.orden()
        orden_str = " → ".join(orden) if orden else "(vacía)"
        ax.text(ox, sy - 0.07, f"↗ {orden_str}",
                color=MUTED, fontsize=6.5, va='top',
                fontfamily='monospace', zorder=4,
                bbox=dict(boxstyle='round,pad=0.15', fc=BG, ec=BORDER, lw=0.4))

        # info técnica
        ax.text(ox, sy - 0.12,
                f"frente={pista.frente}  final={pista.final}  ✈{pista.total_dep}",
                color=MUTED, fontsize=6, va='top', fontfamily='monospace', zorder=4)


def draw_diagram(ax):
    """Diagrama de cola circular — estado de Pista 09L."""
    p   = state["pistas"][0]
    clr = ACCENT[0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Cola circular — Pista 09L (estructura interna)",
                 color=MUTED, fontsize=7.5, loc='left', pad=6,
                 fontfamily='monospace')

    cap   = p.capacidad
    sw    = 0.17
    gap   = 0.035
    total = cap * sw + (cap - 1) * gap
    ox    = (1 - total) / 2
    cy    = 0.55

    for i in range(cap):
        x   = ox + i * (sw + gap)
        v   = p.cola[i]
        is_h = not p.esta_vacia() and i == p.frente
        is_t = i == p.final % cap
        draw_slot(ax, x, cy - 0.18, sw, 0.36, v, i,
                  is_h, is_t, clr, ACCENT_D[0])

        # flecha circular entre celdas
        if i < cap - 1:
            ax.annotate("",
                xy=(x + sw + gap, cy),
                xytext=(x + sw, cy),
                arrowprops=dict(arrowstyle="->", color=BORDER,
                                lw=0.8, connectionstyle="arc3,rad=0"))

    # flecha de wrap-around
    ax.annotate("",
        xy=(ox, cy + 0.22),
        xytext=(ox + (cap-1)*(sw+gap) + sw, cy + 0.22),
        arrowprops=dict(arrowstyle="->", color=ACCENT[0],
                        lw=1, connectionstyle="arc3,rad=0.4",
                        alpha=0.5))
    ax.text(0.5, 0.92, "(frente+1) % capacidad  —  comportamiento circular",
            ha='center', va='center', color=MUTED,
            fontsize=7, fontfamily='monospace', zorder=4)

    # leyenda HEAD/TAIL
    ax.text(0.02, 0.1, "H = HEAD (frente, primer en salir)",
            color=SUCCESS, fontsize=7, fontfamily='monospace')
    ax.text(0.55, 0.1, "T = TAIL (final, próxima posición libre)",
            color=WARN, fontsize=7, fontfamily='monospace')


def draw_stats(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    in_q   = sum(p.size for p in state["pistas"])
    waited = len(state["espera"])
    dep    = state["total_dep"]
    arr    = 15 - len(state["queue"])

    stats = [
        ("Llegados",   arr,   ACCENT[0]),
        ("En pistas",  in_q,  ACCENT[1]),
        ("En espera",  waited, WARN),
        ("Despegados", dep,   SUCCESS),
    ]
    bw, bh = 0.22, 0.6
    gap = (1 - 4*bw) / 5
    for j, (lbl, val, clr) in enumerate(stats):
        x = gap + j * (bw + gap)
        rounded_box(ax, x, 0.2, bw, bh, BORDER, lw=0.4, ec=clr)
        ax.text(x + bw/2, 0.72, str(val),
                ha='center', va='center', color=clr,
                fontsize=18, fontweight='bold', fontfamily='monospace', zorder=4)
        ax.text(x + bw/2, 0.34, lbl,
                ha='center', va='center', color=MUTED,
                fontsize=7.5, fontfamily='monospace', zorder=4)


def draw_waiting(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Lista de espera general", color=MUTED, fontsize=8,
                 loc='left', pad=5, fontfamily='monospace')

    if not state["espera"]:
        ax.text(0.5, 0.5, "Sin vuelos en espera", ha='center', va='center',
                color=MUTED, fontsize=8, fontfamily='monospace')
        return

    sw, sh = 0.12, 0.3
    gap = 0.015
    ox  = 0.02
    for j, v in enumerate(state["espera"]):
        x = ox + j * (sw + gap)
        if x + sw > 0.98: break
        rounded_box(ax, x, 0.35, sw, sh, BG, lw=0.8, ec=WARN)
        ax.text(x + sw/2, 0.5, v[:6],
                ha='center', va='center', color=WARN,
                fontsize=7.5, fontweight='bold',
                fontfamily='monospace', zorder=4)


def draw_log(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Registro de operaciones", color=MUTED, fontsize=8,
                 loc='left', pad=5, fontfamily='monospace')

    entries = state["log"][-14:]
    n       = len(entries)
    for j, msg in enumerate(reversed(entries)):
        y = 0.06 + j * (0.88 / max(n, 1))
        if   " OK " in msg: clr = SUCCESS
        elif "DESP" in msg: clr = ACCENT[0]
        elif "WAIT" in msg: clr = WARN
        elif " <- "  in msg: clr = WARN
        elif "DONE" in msg: clr = SUCCESS
        else:              clr = MUTED
        ax.text(0.02, y, msg, va='bottom', color=clr,
                fontsize=7, fontfamily='monospace', zorder=4,
                clip_on=True)


# ══════════════════════════════════════════════
#  SIMULACIÓN AUTOMÁTICA (paso a paso con timer)
# ══════════════════════════════════════════════
sim_gen  = None
sim_timer = None

def sim_step(fig, axes):
    global sim_gen, sim_timer
    try:
        next(sim_gen)
        draw(fig, axes)
        sim_timer = fig.canvas.new_timer(interval=500)
        sim_timer.add_callback(sim_step, fig, axes)
        sim_timer.single_shot = True
        sim_timer.start()
    except StopIteration:
        add_log("DONE Simulación completa")
        state["sim_done"] = True
        draw(fig, axes)
        sim_gen = None

def sim_generator():
    while state["queue"]:
        asignar(state["queue"].pop(0))
        yield
    yield  # pausa
    while any(not p.esta_vacia() for p in state["pistas"]) or state["espera"]:
        despachar()
        yield


# ══════════════════════════════════════════════
#  INTERFAZ PRINCIPAL
# ══════════════════════════════════════════════
def build_ui():
    global sim_gen, sim_timer

    reset_state()

    plt.rcParams.update({
        'figure.facecolor'  : BG,
        'axes.facecolor'    : PANEL,
        'text.color'        : TEXT,
        'axes.labelcolor'   : TEXT,
        'xtick.color'       : TEXT,
        'ytick.color'       : TEXT,
        'axes.edgecolor'    : BORDER,
        'font.family'       : 'monospace',
    })

    fig = plt.figure(figsize=(15, 9), facecolor=BG)
    fig.canvas.manager.set_window_title("✈ Aeropuerto — Colas Circulares")

    # ── Layout con GridSpec ──────────────────────
    gs_top  = gridspec.GridSpec(1, 3, figure=fig,
                                left=0.02, right=0.98,
                                top=0.96, bottom=0.72,
                                wspace=0.03)
    gs_mid  = gridspec.GridSpec(1, 2, figure=fig,
                                left=0.02, right=0.98,
                                top=0.70, bottom=0.46,
                                wspace=0.03)
    gs_bot  = gridspec.GridSpec(1, 2, figure=fig,
                                left=0.02, right=0.98,
                                top=0.43, bottom=0.12,
                                wspace=0.03)
    gs_btn  = gridspec.GridSpec(1, 5, figure=fig,
                                left=0.02, right=0.98,
                                top=0.10, bottom=0.02,
                                wspace=0.04)

    ax_stats   = fig.add_subplot(gs_top[0, 0:2])
    ax_wait    = fig.add_subplot(gs_top[0, 2])
    ax_runways = fig.add_subplot(gs_mid[0, 0])
    ax_diagram = fig.add_subplot(gs_mid[0, 1])
    ax_log     = fig.add_subplot(gs_bot[0, 0:2])

    for ax in [ax_stats, ax_wait, ax_runways, ax_diagram, ax_log]:
        ax.set_facecolor(PANEL)
        for sp in ax.spines.values():
            sp.set_edgecolor(BORDER)
            sp.set_linewidth(0.5)
        ax.set_xticks([])
        ax.set_yticks([])

    axes = {
        "stats"  : ax_stats,
        "waiting": ax_wait,
        "runways": ax_runways,
        "diagram": ax_diagram,
        "log"    : ax_log,
    }

    # Título
    fig.text(0.5, 0.985, "✈  SISTEMA DE GESTIÓN DE VUELOS — COLA CIRCULAR",
             ha='center', va='top', fontsize=11,
             color=ACCENT[0], fontfamily='monospace', fontweight='bold')

    # ── Botones ──────────────────────────────────
    btn_style = dict(
        color=PANEL, hovercolor=BORDER
    )

    ax_b1 = fig.add_subplot(gs_btn[0, 0])
    ax_b2 = fig.add_subplot(gs_btn[0, 1])
    ax_b3 = fig.add_subplot(gs_btn[0, 2])
    ax_b4 = fig.add_subplot(gs_btn[0, 3])
    ax_b5 = fig.add_subplot(gs_btn[0, 4])

    b_arrive  = Button(ax_b1, "+ Llegar vuelo",  **btn_style)
    b_depart  = Button(ax_b2, "^ Despachar",     **btn_style)
    b_sim     = Button(ax_b3, "> Simular todo",  **btn_style)
    b_reset   = Button(ax_b4, "R Reiniciar",     **btn_style)
    b_close   = Button(ax_b5, "X Cerrar",        **btn_style)

    for btn, clr in [(b_arrive, ACCENT[1]), (b_depart, ACCENT[0]),
                     (b_sim, ACCENT[3]), (b_reset, MUTED), (b_close, DANGER)]:
        btn.label.set_color(clr)
        btn.label.set_fontfamily('monospace')
        btn.label.set_fontsize(9)

    def on_arrive(_):
        if state["queue"]:
            asignar(state["queue"].pop(0))
        else:
            add_log("— No quedan vuelos por llegar")
        draw(fig, axes)

    def on_depart(_):
        despachar()
        draw(fig, axes)

    def on_sim(_):
        global sim_gen, sim_timer
        if sim_gen is not None: return
        sim_gen = sim_generator()
        sim_step(fig, axes)

    def on_reset(_):
        global sim_gen, sim_timer
        if sim_timer: sim_timer.stop()
        sim_gen = None
        reset_state()
        draw(fig, axes)

    def on_close(_): plt.close(fig)

    b_arrive.on_clicked(on_arrive)
    b_depart.on_clicked(on_depart)
    b_sim.on_clicked(on_sim)
    b_reset.on_clicked(on_reset)
    b_close.on_clicked(on_close)

    draw(fig, axes)
    plt.show()

if __name__ == "__main__":
    build_ui()
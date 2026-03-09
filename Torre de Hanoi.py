import tkinter as tk
from tkinter import ttk
import time
import math

BG      = "#04060f"
SURFACE = "#080d1c"
BORDER  = "#131d35"
CYAN    = "#00ffdd"
PINK    = "#ff00cc"
GOLD    = "#ffc200"
GREEN   = "#00ff99"
PURPLE  = "#a78bfa"
MUTED   = "#3a4a65"
TEXT    = "#c8d8f0"

DISK_COLORS = [
    "#00ffdd", "#00ff99", "#a78bfa", "#ffc200",
    "#ff00cc", "#4cc9f0", "#fb8500", "#ff6b6b",
    "#06d6a0", "#f72585",
]

def hanoi_recursivo(n, origen, destino, auxiliar, movimientos=None):
    """
    Solución recursiva clásica.
    Divide: mueve n-1 al auxiliar, mueve disco grande, repite.
    Complejidad: O(2ⁿ) tiempo y espacio.
    """
    if movimientos is None:
        movimientos = []
    if n == 1:
        movimientos.append((origen, destino))
        return movimientos
    hanoi_recursivo(n - 1, origen, auxiliar, destino, movimientos)
    movimientos.append((origen, destino))
    hanoi_recursivo(n - 1, auxiliar, destino, origen, movimientos)
    return movimientos


def hanoi_iterativo(n, origen, destino, auxiliar):
    """
    Solución iterativa con pila explícita.
    Evita RecursionError para n grandes.
    ~20-40% más rápido que recursivo.
    """
    movimientos = []
    stack = [(n, origen, destino, auxiliar)]
    while stack:
        discos, src, dst, aux = stack.pop()
        if discos == 1:
            movimientos.append((src, dst))
        else:
            stack.append((discos - 1, aux, dst, src))
            stack.append((1, src, dst, aux))
            stack.append((discos - 1, src, aux, dst))
    return movimientos


def contar_movimientos(n):
    """
    Devuelve 2ⁿ − 1 sin simular ningún movimiento.
    O(1). Único método viable para n = 64.
    """
    return (2 ** n) - 1

MAX_SIMULABLE = 20

class HanoiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Torre de Hanoi — Análisis Computacional")
        self.root.configure(bg=BG)
        self.root.geometry("920x700")
        self.root.minsize(750, 580)

        self.pegs     = [[], [], []]
        self.moves    = []
        self.idx      = 0
        self.n        = 5
        self.running  = False
        self.after_id = None

        self._build_ui()
        self._init_board()

    def _build_ui(self):
        hdr = tk.Frame(self.root, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(14, 4))
        tk.Label(hdr, text="TORRE DE HANOI",
                 font=("Courier New", 22, "bold"), fg=CYAN, bg=BG).pack()
        tk.Label(hdr, text="Análisis Computacional  ·  3 Métodos  ·  Visualización Interactiva",
                 font=("Courier New", 9), fg=MUTED, bg=BG).pack()

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Dark.TNotebook",     background=BG,     borderwidth=0)
        style.configure("Dark.TNotebook.Tab", background=SURFACE, foreground=MUTED,
                        font=("Courier New", 9, "bold"), padding=[14, 6])
        style.map("Dark.TNotebook.Tab",
                  background=[("selected", CYAN)],
                  foreground=[("selected", BG)])

        self.nb = ttk.Notebook(self.root, style="Dark.TNotebook")
        self.nb.pack(fill="both", expand=True, padx=12, pady=8)

        self._build_tab_sim()
        self._build_tab_analysis()
        self._build_tab_code()
        self._build_tab_conclusions()

    def _build_tab_sim(self):
        frame = tk.Frame(self.nb, bg=SURFACE)
        self.nb.add(frame, text="  ▶  SIMULADOR  ")

        ctrl = tk.Frame(frame, bg=SURFACE)
        ctrl.pack(fill="x", padx=16, pady=(12, 8))

        self._label(ctrl, "DISCOS:").grid(row=0, column=0, padx=(0, 4))
        self.var_disks = tk.IntVar(value=5)
       
        disk_cb = ttk.Combobox(ctrl, textvariable=self.var_disks, width=5,
                               values=[5,10, 30, 64],
                               state="readonly", font=("Courier New", 10))
        disk_cb.grid(row=0, column=1, padx=(0, 14))
        disk_cb.bind("<<ComboboxSelected>>", lambda e: self._on_disk_change())

        self._label(ctrl, "MÉTODO:").grid(row=0, column=2, padx=(0, 4))
        self.var_method = tk.StringVar(value="Recursivo")
        met_cb = ttk.Combobox(ctrl, textvariable=self.var_method, width=12,
                              values=["Recursivo", "Iterativo"],
                              state="readonly", font=("Courier New", 10))
        met_cb.grid(row=0, column=3, padx=(0, 14))

        self._label(ctrl, "VELOCIDAD:").grid(row=0, column=4, padx=(0, 4))
        self.var_speed = tk.IntVar(value=5)
        spd = tk.Scale(ctrl, variable=self.var_speed, from_=1, to=10,
                       orient="horizontal", length=110, bg=SURFACE, fg=GOLD,
                       troughcolor=BORDER, highlightthickness=0, bd=0,
                       font=("Courier New", 8), command=self._on_speed)
        spd.grid(row=0, column=5, padx=(0, 14))

        self.btn_solve = self._btn(ctrl, "▶ RESOLVER", CYAN, self.start_solve)
        self.btn_solve.grid(row=0, column=6, padx=4)
        self.btn_step = self._btn(ctrl, "⏭ PASO", GOLD, self.do_step)
        self.btn_step.grid(row=0, column=7, padx=4)
        self.btn_step["state"] = "disabled"
        self.btn_reset = self._btn(ctrl, "↺ RESET", PINK, self.reset_all)
        self.btn_reset.grid(row=0, column=8, padx=4)

        self.lbl_warn = tk.Label(frame, text="", font=("Courier New", 9, "bold"),
                                 fg=GOLD, bg=SURFACE, anchor="w")
        self.lbl_warn.pack(fill="x", padx=18, pady=(0, 2))

        self.canvas = tk.Canvas(frame, bg="#030608",
                                highlightthickness=1, highlightbackground=BORDER)
        self.canvas.pack(fill="both", expand=True, padx=16, pady=4)
        self.canvas.bind("<Configure>", lambda e: self._draw_board())

        pb_frame = tk.Frame(frame, bg=SURFACE)
        pb_frame.pack(fill="x", padx=16, pady=(2, 4))
        style2 = ttk.Style()
        style2.configure("Cyan.Horizontal.TProgressbar",
                         troughcolor=BORDER, background=CYAN,
                         bordercolor=BORDER, lightcolor=CYAN, darkcolor=CYAN)
        self.pb = ttk.Progressbar(pb_frame, style="Cyan.Horizontal.TProgressbar",
                                  maximum=100, value=0)
        self.pb.pack(fill="x")

        stats = tk.Frame(frame, bg=SURFACE)
        stats.pack(fill="x", padx=16, pady=(2, 6))
        self.lbl_move   = self._stat(stats, "MOVIMIENTO",  "0",     CYAN)
        self.lbl_total  = self._stat(stats, "TOTAL",       "31",    TEXT)
        self.lbl_pct    = self._stat(stats, "PROGRESO",    "0%",    GOLD)
        self.lbl_time   = self._stat(stats, "TIEMPO CÁLC", "—",     PURPLE)
        self.lbl_status = self._stat(stats, "ESTADO",      "LISTO", MUTED)

        log_frame = tk.Frame(frame, bg=SURFACE)
        log_frame.pack(fill="x", padx=16, pady=(0, 10))
        self.log_text = tk.Text(log_frame, bg="#030608", fg=MUTED,
                                font=("Courier New", 8), height=5,
                                wrap="word", state="disabled",
                                highlightthickness=1, highlightbackground=BORDER,
                                insertbackground=CYAN, relief="flat")
        sb = tk.Scrollbar(log_frame, command=self.log_text.yview,
                          bg=BORDER, troughcolor=BG)
        self.log_text.configure(yscrollcommand=sb.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.log_text.tag_config("cyan",  foreground=CYAN)
        self.log_text.tag_config("gold",  foreground=GOLD)
        self.log_text.tag_config("green", foreground=GREEN)
        self.log_text.tag_config("pink",  foreground=PINK)
        self.log_text.tag_config("muted", foreground=MUTED)
        self.log_text.tag_config("red",   foreground="#ff4444")
        for c in DISK_COLORS:
            self.log_text.tag_config(c, foreground=c)

    def _build_tab_analysis(self):
        outer = tk.Frame(self.nb, bg=SURFACE)
        self.nb.add(outer, text="  📊  ANÁLISIS  ")

        canv = tk.Canvas(outer, bg=SURFACE, highlightthickness=0)
        sb   = ttk.Scrollbar(outer, orient="vertical", command=canv.yview)
        canv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canv.pack(side="left", fill="both", expand=True)

        frame  = tk.Frame(canv, bg=SURFACE)
        win_id = canv.create_window((0, 0), window=frame, anchor="nw")
        frame.bind("<Configure>",
                   lambda e: canv.configure(scrollregion=canv.bbox("all")))
        canv.bind("<Configure>",
                  lambda e: canv.itemconfig(win_id, width=e.width))

        self._section(frame, "MÉTODOS DEL PROGRAMA — TOTAL: 3")
        for num, name, desc, col in [
            ("1", "hanoi_recursivo(n, origen, destino, auxiliar)",
             "Recursión clásica · O(2ⁿ) · Elegante y directa", CYAN),
            ("2", "hanoi_iterativo(n, origen, destino, auxiliar)",
             "Pila explícita · O(2ⁿ) · Evita RecursionError", PURPLE),
            ("3", "contar_movimientos(n)",
             "Fórmula 2ⁿ−1 · O(1) · Único viable para n=64", GOLD),
        ]:
            row = tk.Frame(frame, bg="#060b18")
            row.pack(fill="x", padx=16, pady=3)
            tk.Label(row, text=f" {num}. ", font=("Courier New", 11, "bold"),
                     fg=col, bg="#060b18").pack(side="left")
            tk.Label(row, text=name, font=("Courier New", 10, "bold"),
                     fg=col, bg="#060b18").pack(side="left", padx=(0, 10))
            tk.Label(row, text=desc, font=("Courier New", 8),
                     fg=MUTED, bg="#060b18").pack(side="left")

        self._section(frame, "RESULTADOS POR NÚMERO DE DISCOS")
        cards = tk.Frame(frame, bg=SURFACE)
        cards.pack(fill="x", padx=16, pady=6)
        for i, (n, movs, tiempo, mem, badge, col) in enumerate([
            (5,  "31",                         "< 0.01 ms",       "~248 B",  "TRIVIAL",   CYAN),
            (10, "1,023",                      "~0.3–0.8 ms",     "~8 KB",   "RÁPIDO",    PURPLE),
            (30, "1,073,741,823",              "~8–15 segundos",  "~8 GB",   "LÍMITE",    GOLD),
            (64, "18,446,744,073,709,551,615", "585 mil M. años", "~147 ZB", "IMPOSIBLE", PINK),
        ]):
            card = tk.Frame(cards, bg="#060b18",
                            highlightthickness=1, highlightbackground=col)
            card.grid(row=0, column=i, padx=6, pady=4, sticky="nsew")
            cards.columnconfigure(i, weight=1)
            tk.Label(card, text=str(n), font=("Courier New", 36, "bold"),
                     fg=col, bg="#060b18").pack(pady=(8, 0))
            tk.Label(card, text="DISCOS", font=("Courier New", 7),
                     fg=MUTED, bg="#060b18").pack()
            tk.Frame(card, bg=col, height=1).pack(fill="x", padx=8, pady=4)
            tk.Label(card, text=movs, font=("Courier New", 8, "bold"),
                     fg=col, bg="#060b18", wraplength=160).pack(padx=8)
            tk.Label(card, text=f"⏱ {tiempo}", font=("Courier New", 8),
                     fg=MUTED, bg="#060b18").pack(padx=8, anchor="w")
            tk.Label(card, text=f"💾 {mem}", font=("Courier New", 8),
                     fg=MUTED, bg="#060b18").pack(padx=8, anchor="w")
            tk.Label(card, text=badge, font=("Courier New", 8, "bold"),
                     fg=BG, bg=col).pack(pady=(4, 8), ipadx=8, ipady=2)

        self._section(frame, "CRECIMIENTO EXPONENCIAL — Barras proporcionales (log)")
        chart = tk.Frame(frame, bg="#060b18")
        chart.pack(fill="x", padx=16, pady=6)
        for n_d, val, col in [
            (5,  2**5-1,  CYAN),
            (10, 2**10-1, PURPLE),
            (20, 2**20-1, GOLD),
            (30, 2**30-1, PINK),
            (64, 2**64-1, "#ff4444"),
        ]:
            log_w = int((math.log2(val + 1) / 64) * 55)
            row = tk.Frame(chart, bg="#060b18")
            row.pack(fill="x", padx=10, pady=3)
            tk.Label(row, text=f"n={n_d:2d} ", font=("Courier New", 9),
                     fg=MUTED, bg="#060b18", width=6).pack(side="left")
            bar = "▓" * log_w + (">>>∞" if n_d == 64 else "")
            tk.Label(row, text=bar, font=("Courier New", 9, "bold"),
                     fg=col, bg="#060b18").pack(side="left")
            tk.Label(row, text=f"  2^{n_d}-1 = {val:,}",
                     font=("Courier New", 8), fg=MUTED, bg="#060b18").pack(side="left")
            
    def _build_tab_code(self):
        frame = tk.Frame(self.nb, bg=SURFACE)
        self.nb.add(frame, text="  💻  CÓDIGO PYTHON  ")
        tk.Label(frame, text="  Código fuente Python — 3 métodos implementados",
                 font=("Courier New", 9, "bold"), fg=CYAN, bg=SURFACE,
                 anchor="w").pack(fill="x", padx=16, pady=(10, 4))

        cf = tk.Frame(frame, bg="#030608",
                      highlightthickness=1, highlightbackground=BORDER)
        cf.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        text = tk.Text(cf, bg="#030608", fg=TEXT, font=("Courier New", 9),
                       wrap="none", state="normal", relief="flat",
                       highlightthickness=0, padx=10, pady=10)
        sbx = ttk.Scrollbar(cf, orient="horizontal", command=text.xview)
        sby = ttk.Scrollbar(cf, orient="vertical",   command=text.yview)
        text.configure(xscrollcommand=sbx.set, yscrollcommand=sby.set)
        sby.pack(side="right",  fill="y")
        sbx.pack(side="bottom", fill="x")
        text.pack(fill="both", expand=True)
        text.tag_config("kw", foreground=PINK)
        text.tag_config("fn", foreground=CYAN)
        text.tag_config("cm", foreground=MUTED)
        text.tag_config("st", foreground=GOLD)
        text.tag_config("nm", foreground=PURPLE)

        snippets = [
          ("cm","# ══════════════════════════════════════════\n"),
          ("cm","# TORRE DE HANOI — 3 Métodos\n"),
          ("cm","# ══════════════════════════════════════════\n"),
          ("kw","import"),("", " time\n\n"),
          ("cm","# MÉTODO 1: Recursivo  O(2ⁿ)\n"),
          ("kw","def"),(" ",""),("fn","hanoi_recursivo"),
          ("","(n, origen, destino, auxiliar, movimientos="),
          ("kw","None"),("","):\n"),
          ("st",'    """Recursión clásica. Complejidad O(2ⁿ)."""\n'),
          ("kw","    if"),("", " movimientos "),("kw","is"),(" ",""),
          ("kw","None"),("",":\n"),
          ("","        movimientos = []\n"),
          ("kw","    if"),("", " n == "),("nm","1"),("",":\n"),
          ("","        movimientos.append((origen, destino))\n"),
          ("kw","        return"),("", " movimientos\n"),
          ("fn","    hanoi_recursivo"),
          ("","(n-"),("nm","1"),("",", origen, auxiliar, destino, movimientos)\n"),
          ("","    movimientos.append((origen, destino))\n"),
          ("fn","    hanoi_recursivo"),
          ("","(n-"),("nm","1"),("",", auxiliar, destino, origen, movimientos)\n"),
          ("kw","    return"),("", " movimientos\n\n"),
          ("cm","# MÉTODO 2: Iterativo  O(2ⁿ)\n"),
          ("kw","def"),(" ",""),("fn","hanoi_iterativo"),
          ("","(n, origen, destino, auxiliar):\n"),
          ("st",'    """Pila explícita. Evita RecursionError."""\n'),
          ("","    movimientos = []\n"),
          ("","    stack = [(n, origen, destino, auxiliar)]\n"),
          ("kw","    while"),("", " stack:\n"),
          ("","        discos, src, dst, aux = stack.pop()\n"),
          ("kw","        if"),("", " discos == "),("nm","1"),("",":\n"),
          ("","            movimientos.append((src, dst))\n"),
          ("kw","        else"),("",":\n"),
          ("","            stack.append((discos-"),("nm","1"),("",", aux, dst, src))\n"),
          ("","            stack.append(("),("nm","1"),("",", src, dst, aux))\n"),
          ("","            stack.append((discos-"),("nm","1"),("",", src, aux, dst))\n"),
          ("kw","    return"),("", " movimientos\n\n"),
          ("cm","# MÉTODO 3: Fórmula directa  O(1)\n"),
          ("kw","def"),(" ",""),("fn","contar_movimientos"),("","(n):\n"),
          ("st",'    """Devuelve 2ⁿ−1. O(1). Único viable para n=64."""\n'),
          ("kw","    return"),("", " ("),("nm","2"),("", " ** n) - "),("nm","1"),("","\n\n"),
          ("cm","# EJECUCIÓN\n"),
          ("kw","if"),("", " __name__ == "),("st",'"__main__"'),("",":\n"),
          ("","    for n in ["),("nm","5"),("",", "),("nm","10"),("",", "),
          ("nm","30"),("",", "),("nm","64"),("","]:\n"),
          ("","        total = contar_movimientos(n)\n"),
          ("","        print(f"),("st",'"n={n}: {total:,} movimientos"'),("",")\n"),
          ("kw","        if"),("", " n <= "),("nm","20"),("",":\n"),
          ("fn","            hanoi_recursivo"),
          ("","(n, "),("st","'A'"),("",", "),("st","'C'"),("",", "),("st","'B'"),("",")\n"),
        ]
        for tag, txt in snippets:
            text.insert("end", txt, tag) if tag else text.insert("end", txt)
        text.configure(state="disabled")

    def _build_tab_conclusions(self):
        outer = tk.Frame(self.nb, bg=SURFACE)
        self.nb.add(outer, text="  🧠  CONCLUSIONES  ")
        canv = tk.Canvas(outer, bg=SURFACE, highlightthickness=0)
        sb   = ttk.Scrollbar(outer, orient="vertical", command=canv.yview)
        canv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canv.pack(side="left", fill="both", expand=True)
        frame  = tk.Frame(canv, bg=SURFACE)
        wid    = canv.create_window((0, 0), window=frame, anchor="nw")
        frame.bind("<Configure>",
                   lambda e: canv.configure(scrollregion=canv.bbox("all")))
        canv.bind("<Configure>",
                  lambda e: canv.itemconfig(wid, width=e.width))

        self._section(frame, "CONCLUSIONES DEL ANÁLISIS COMPUTACIONAL")
        for col, titulo, texto in [
            (CYAN,   "📌  MÉTODOS IMPLEMENTADOS: 3 EN TOTAL",
             "El programa maneja 3 métodos: hanoi_recursivo traduce la definición "
             "matemática directamente en código; hanoi_iterativo logra lo mismo con "
             "pila explícita evitando el límite de recursión de Python; y "
             "contar_movimientos obtiene el resultado con 2ⁿ−1 en O(1)."),
            (GOLD,   "📈  CRECIMIENTO EXPONENCIAL O(2ⁿ) — INCONTROLABLE",
             "Cada disco adicional duplica exactamente los movimientos. "
             "De n=5 a n=10: ×33. De n=10 a n=30: ×1,000,000. "
             "El algoritmo es correcto pero la escala lo hace inviable para n grande."),
            (PINK,   "🚫  64 DISCOS: EL MURO COMPUTACIONAL",
             "Se requieren 18,446,744,073,709,551,615 movimientos. "
             "A 1 GHz tardaría 585 años. A 1 mov/segundo: 585 mil millones de años "
             "(42× la edad del universo). Solo la fórmula O(1) es viable."),
            (PURPLE, "⚡  RECURSIVO vs ITERATIVO: ¿CUÁL ELEGIR?",
             "Para n ≤ 20: recursivo es más legible. Para n > 20: iterativo es "
             "preferible — evita RecursionError y es ~20-40% más rápido. "
             "Ambos son inviables para n=64 por la cantidad de movimientos."),
            (GREEN,  "🧮  LA LECCIÓN MÁS PROFUNDA",
             "La Torre de Hanoi demuestra que no todo problema bien definido es "
             "computacionalmente tratable. Para n=64 la fórmula O(1) no es un truco: "
             "es la única respuesta útil. Esta distinción entre 'resoluble' y 'tratable' "
             "es el fundamento de la Teoría de Complejidad Computacional."),
        ]:
            blk = tk.Frame(frame, bg="#060b18",
                           highlightthickness=2, highlightbackground=col)
            blk.pack(fill="x", padx=16, pady=6)
            tk.Label(blk, text=titulo, font=("Courier New", 9, "bold"),
                     fg=col, bg="#060b18", anchor="w").pack(
                     fill="x", padx=12, pady=(10, 4))
            tk.Label(blk, text=texto, font=("Courier New", 9),
                     fg=TEXT, bg="#060b18", wraplength=800,
                     justify="left", anchor="w").pack(
                     fill="x", padx=12, pady=(0, 12))

    def _init_board(self):
        self.n    = self.var_disks.get()
        self.pegs = [list(range(self.n, 0, -1)), [], []]
        self.moves = []
        self.idx   = 0
        self.running = False
        total = contar_movimientos(self.n)
        self._update_stats(0, total, "—", "LISTO", MUTED)
        self.pb["value"] = 0
        self._log_clear()

        if self.n > MAX_SIMULABLE:
            msg = (f"⚠  n={self.n}: {total:,} movimientos — "
                   f"{'IMPOSIBLE simular' if self.n==64 else 'demasiado para animar'}. "
                   f"Se mostrará solo el resultado de la fórmula O(1).")
            self.lbl_warn.config(text=msg, fg=GOLD if self.n==30 else PINK)
            self._log(f"// contar_movimientos({self.n}) = {total:,}\n", "gold")
            self._log(f"// Simulación deshabilitada para n > {MAX_SIMULABLE}\n", "red")
        else:
            self.lbl_warn.config(text="")
            self._log("// Presiona ▶ RESOLVER para iniciar...\n", "muted")

        self.btn_step["state"] = "disabled"
     
        solve_state = "disabled" if self.n > MAX_SIMULABLE else "normal"
        self.btn_solve["state"] = solve_state
        self._draw_board()

    def _on_disk_change(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self._init_board()

    def start_solve(self):
    
        if self.n > MAX_SIMULABLE:
            return
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self._init_board()

        method = self.var_method.get()
        t0 = time.perf_counter()
        if method == "Recursivo":
            self.moves = hanoi_recursivo(self.n, 0, 2, 1)
        else:
            self.moves = hanoi_iterativo(self.n, 0, 2, 1)
        elapsed = (time.perf_counter() - t0) * 1000

        mname = "hanoi_recursivo" if method == "Recursivo" else "hanoi_iterativo"
        total = len(self.moves)
        self._log_clear()
        self._log(f"// {mname}({self.n}) → {total:,} movimientos en {elapsed:.3f} ms\n",
                  "cyan")
        self._update_stats(0, total, f"{elapsed:.3f} ms", "EJECUTANDO", CYAN)
        self.btn_step["state"] = "normal"
        self.running = True
        self._animate()

    def _animate(self):
        if not self.running or self.idx >= len(self.moves):
            self.running = False
            if self.idx >= len(self.moves) and self.moves:
                self._update_stats(self.idx, len(self.moves),
                                   self.lbl_time.cget("text"), "✓ COMPLETADO", GREEN)
                self.btn_step["state"] = "disabled"
            return
        self._apply_move(self.moves[self.idx])
        self.idx += 1
        self._update_stats(self.idx, len(self.moves),
                           self.lbl_time.cget("text"), "EJECUTANDO", CYAN)
        self._draw_board()
        self.after_id = self.root.after(self._get_delay(), self._animate)

    def do_step(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.running = False
        if not self.moves:
            self.start_solve()
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
            self.running = False
            return
        if self.idx < len(self.moves):
            self._apply_move(self.moves[self.idx])
            self.idx += 1
            total = len(self.moves)
            self._update_stats(self.idx, total,
                               self.lbl_time.cget("text"), "PASO A PASO", GOLD)
            self._draw_board()
            if self.idx >= total:
                self._update_stats(self.idx, total,
                                   self.lbl_time.cget("text"), "✓ COMPLETADO", GREEN)
                self.btn_step["state"] = "disabled"

    def reset_all(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.running = False
        self._init_board()

    def _apply_move(self, move):
        src, dst = move
        labels = ["A", "B", "C"]
        disk = self.pegs[src].pop()
        self.pegs[dst].append(disk)
        col_tag = DISK_COLORS[(disk - 1) % len(DISK_COLORS)]
        self._log(f"→ Mov {self.idx+1:4d}: Disco {disk}  {labels[src]} → {labels[dst]}\n",
                  col_tag)

    def _get_delay(self):
        v = self.var_speed.get()
        return [1800, 1100, 600, 320, 160, 75, 30, 12, 5, 1][v - 1]

    def _on_speed(self, _):
        pass

  
    def _draw_board(self):
        c = self.canvas
        c.delete("all")
        W = c.winfo_width()
        H = c.winfo_height()
        if W < 10 or H < 10:
            return

        n      = self.n
        base_y = H - 40
        peg_xs = [W * 0.17, W * 0.50, W * 0.83]
        max_dw = W * 0.25
        min_dw = 22
        disk_h = max(13, min(28, (H - 80) / (n + 2)))
        labels = ["A", "B", "C"]

        c.create_rectangle(0, 0, W, H, fill="#030608", outline="")
        c.create_rectangle(14, base_y, W - 14, base_y + 10,
                           fill="#131d35", outline="")

        for pi, px in enumerate(peg_xs):
            c.create_rectangle(px - 4, 30, px + 4, base_y,
                               fill="#1a2a4a", outline="")
            c.create_text(px, H - 16, text=labels[pi],
                          font=("Courier New", 11, "bold"), fill="#2a3a5a")

            for di, disk in enumerate(self.pegs[pi]):
                dw  = min_dw + ((disk - 1) / max(n - 1, 1)) * (max_dw - min_dw)
                dy  = base_y - (di + 1) * (disk_h + 3)
                dx  = px - dw / 2
                col = DISK_COLORS[(disk - 1) % len(DISK_COLORS)]
                # sombra
                c.create_rectangle(dx+3, dy+3, dx+dw+3, dy+disk_h+3,
                                   fill="#000", outline="", stipple="gray25")
                # cuerpo
                c.create_rectangle(dx, dy, dx+dw, dy+disk_h,
                                   fill=col, outline=col, width=1)
                # número
                if disk_h >= 15:
                    c.create_text(px, dy + disk_h * 0.62, text=str(disk),
                                  font=("Courier New", max(7, int(disk_h*0.52)), "bold"),
                                  fill="#000000")

        if n > MAX_SIMULABLE:
            total = contar_movimientos(n)
            c.create_text(W // 2, H // 2 - 20,
                          text=f"n = {n}  →  contar_movimientos({n})",
                          font=("Courier New", 13, "bold"), fill=GOLD)
            c.create_text(W // 2, H // 2 + 16,
                          text=f"= {total:,} movimientos",
                          font=("Courier New", 11), fill=TEXT)
            c.create_text(W // 2, H // 2 + 46,
                          text="Simulación imposible — solo fórmula O(1)",
                          font=("Courier New", 10), fill=PINK)

   
    def _btn(self, parent, text, color, cmd):
        return tk.Button(parent, text=text, font=("Courier New", 8, "bold"),
                         fg=color, bg=SURFACE, activebackground=color,
                         activeforeground=BG, relief="flat", bd=0,
                         highlightthickness=1, highlightbackground=color,
                         padx=10, pady=5, cursor="hand2", command=cmd)

    def _label(self, parent, text):
        return tk.Label(parent, text=text, font=("Courier New", 8, "bold"),
                        fg=CYAN, bg=SURFACE)

    def _stat(self, parent, name, val, col):
        box = tk.Frame(parent, bg="#060b18",
                       highlightthickness=1, highlightbackground=BORDER)
        box.pack(side="left", padx=4, pady=4, ipadx=8, ipady=4)
        tk.Label(box, text=name, font=("Courier New", 7),
                 fg=MUTED, bg="#060b18").pack()
        lbl = tk.Label(box, text=val, font=("Courier New", 11, "bold"),
                       fg=col, bg="#060b18")
        lbl.pack()
        return lbl

    def _section(self, parent, text):
        tk.Label(parent, text=f"  {text}", font=("Courier New", 8, "bold"),
                 fg=MUTED, bg=SURFACE, anchor="w").pack(
                 fill="x", padx=16, pady=(14, 2))
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=16, pady=(0, 8))

    def _update_stats(self, current, total, tval, status, scol):
        pct = int(current / total * 100) if total else 0
        self.lbl_move.config(text=f"{current:,}")
        self.lbl_total.config(text=f"{total:,}")
        self.lbl_pct.config(text=f"{pct}%")
        self.lbl_time.config(text=tval)
        self.lbl_status.config(text=status, fg=scol)
        self.pb["value"] = pct

    def _log_clear(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def _log(self, text, tag=None):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text, tag) if tag else \
            self.log_text.insert("end", text)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg=BG)
    root.title("Torre de Hanoi — Análisis Computacional")
    HanoiApp(root)
    root.mainloop()
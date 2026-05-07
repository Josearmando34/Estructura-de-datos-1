"""
╔══════════════════════════════════════════════════════╗
║   MÉTODOS DE ORDENAMIENTO — VISUALIZADOR GRÁFICO     ║
║   Desarrollado en Python + Tkinter                   ║
║   1. Intercalación                                   ║
║   2. Mezcla Directa (Merge Sort)                     ║
║   3. Mezcla Equilibrada                              ║
╚══════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import random

# ─────────────────────────────────────────────────────────
#  COLORES Y ESTILOS
# ─────────────────────────────────────────────────────────
BG        = "#0F1117"
BG2       = "#1A1D2E"
BG3       = "#252840"
ACCENT    = "#6C63FF"
ACCENT2   = "#FF6584"
GREEN     = "#43E97B"
YELLOW    = "#FFD166"
CYAN      = "#38BDF8"
TEXT      = "#E8E8F0"
TEXT2     = "#8888AA"
FONT_TIT  = ("Consolas", 20, "bold")
FONT_SUB  = ("Consolas", 11)
FONT_BTN  = ("Consolas", 12, "bold")
FONT_SM   = ("Consolas", 9)

DELAY = 0.35   # segundos entre pasos de animación

# ─────────────────────────────────────────────────────────
#  PALETAS DE BARRAS POR MÉTODO
# ─────────────────────────────────────────────────────────
PALETAS = {
    "intercalacion": {"normal": ACCENT,  "activo": ACCENT2, "listo": GREEN},
    "directa":       {"normal": CYAN,    "activo": YELLOW,  "listo": GREEN},
    "equilibrada":   {"normal": ACCENT2, "activo": YELLOW,  "listo": GREEN},
}

# ─────────────────────────────────────────────────────────
#  LÓGICA DE ALGORITMOS (con callbacks para animación)
# ─────────────────────────────────────────────────────────

def intercalacion_pasos(a, b):
    """Genera lista de estados (resultado, i, j) para animar."""
    pasos = []
    resultado = []
    i = j = 0
    while i < len(a) and j < len(b):
        pasos.append(("cmp", list(resultado), i, j))
        if a[i] <= b[j]:
            resultado.append(a[i]); i += 1
        else:
            resultado.append(b[j]); j += 1
        pasos.append(("add", list(resultado), i, j))
    while i < len(a):
        resultado.append(a[i]); i += 1
        pasos.append(("add", list(resultado), i, j))
    while j < len(b):
        resultado.append(b[j]); j += 1
        pasos.append(("add", list(resultado), i, j))
    pasos.append(("done", list(resultado), i, j))
    return resultado, pasos


def mezcla_directa_pasos(lista):
    """Merge sort con registro de cada fusión."""
    pasos = []
    arr = list(lista)

    def merge_sort(a):
        if len(a) <= 1:
            return a
        m = len(a) // 2
        L = merge_sort(a[:m])
        R = merge_sort(a[m:])
        return merge(L, R)

    def merge(L, R):
        res = []
        i = j = 0
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                res.append(L[i]); i += 1
            else:
                res.append(R[j]); j += 1
            pasos.append(list(res) + L[i:] + R[j:])
        res += L[i:] + R[j:]
        pasos.append(list(res))
        return res

    resultado = merge_sort(arr)
    pasos.append(list(resultado))
    return resultado, pasos


def mezcla_equilibrada_pasos(lista, k=3):
    """Mezcla equilibrada con registro de rondas."""
    pasos = []
    sublistas = [[] for _ in range(k)]
    for idx, el in enumerate(lista):
        sublistas[idx % k].append(el)
    sublistas = [sorted(s) for s in sublistas if s]
    pasos.append(("split", [item for s in sublistas for item in s]))

    def merge2(a, b):
        res, i, j = [], 0, 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]: res.append(a[i]); i += 1
            else:             res.append(b[j]); j += 1
        return res + a[i:] + b[j:]

    while len(sublistas) > 1:
        nueva = []
        for i in range(0, len(sublistas), 2):
            if i + 1 < len(sublistas):
                m = merge2(sublistas[i], sublistas[i+1])
                nueva.append(m)
            else:
                nueva.append(sublistas[i])
        sublistas = nueva
        pasos.append(("merge", sublistas[0] if len(sublistas) == 1
                      else [x for s in sublistas for x in s]))

    resultado = sublistas[0]
    pasos.append(("done", list(resultado)))
    return resultado, pasos


# ─────────────────────────────────────────────────────────
#  CLASE PRINCIPAL DE LA APP
# ─────────────────────────────────────────────────────────

class OrdenamientoApp:

    EJERCICIOS = {
        "intercalacion": [
            {"titulo": "Números pares e impares",
             "a": [1, 3, 5, 7, 9], "b": [2, 4, 6, 8, 10]},
            {"titulo": "Listas de diferente tamaño",
             "a": [10, 20, 30], "b": [5, 15, 25, 35]},
            {"titulo": "Nombres de alumnos",
             "a": ["Ana", "Carlos", "Luis"],
             "b": ["Beto", "Diana", "Zoe"]},
        ],
        "directa": [
            {"titulo": "Números desordenados",
             "datos": [38, 27, 43, 3, 9, 82, 10]},
            {"titulo": "Calificaciones de alumnos",
             "datos": [85, 42, 91, 67, 23, 78, 55]},
            {"titulo": "Temperaturas corporales",
             "datos": [36.5, 37.2, 35.8, 38.1, 36.9]},
        ],
        "equilibrada": [
            {"titulo": "10 números (k=3 vías)",
             "datos": [15, 3, 22, 8, 47, 1, 35, 12, 9, 28], "k": 3},
            {"titulo": "Edades de personas (k=4)",
             "datos": [20, 35, 18, 42, 27, 31, 19, 45], "k": 4},
            {"titulo": "Precios de productos (k=2)",
             "datos": [199, 45, 320, 89, 150, 275, 60], "k": 2},
        ],
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Métodos de Ordenamiento — Visualizador")
        self.root.configure(bg=BG)
        self.root.geometry("960x700")
        self.root.resizable(True, True)
        self.animando = False
        self._build_ui()

    # ── CONSTRUCCIÓN DE LA INTERFAZ ──────────────────────

    def _build_ui(self):
        # ── Encabezado
        hdr = tk.Frame(self.root, bg=BG, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="⬡  MÉTODOS DE ORDENAMIENTO",
                 font=FONT_TIT, fg=ACCENT, bg=BG).pack()
        tk.Label(hdr, text="Selecciona un método y un ejercicio para visualizar",
                 font=FONT_SUB, fg=TEXT2, bg=BG).pack(pady=2)

        # ── Separador
        tk.Frame(self.root, bg=ACCENT, height=2).pack(fill="x", padx=20)

        # ── Cuerpo principal (sidebar + contenido)
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=12)

        self._build_sidebar(body)
        self._build_main(body)

    def _build_sidebar(self, parent):
        side = tk.Frame(parent, bg=BG2, width=240,
                        highlightbackground=BG3, highlightthickness=1)
        side.pack(side="left", fill="y", padx=(0, 12))
        side.pack_propagate(False)

        tk.Label(side, text="MÉTODO", font=("Consolas", 9, "bold"),
                 fg=TEXT2, bg=BG2, pady=12).pack()

        self.metodo_var = tk.StringVar(value="intercalacion")
        metodos = [
            ("1 · Intercalación",   "intercalacion"),
            ("2 · Mezcla Directa",  "directa"),
            ("3 · Mezcla Equilibrada", "equilibrada"),
        ]
        self.btn_metodos = {}
        for label, val in metodos:
            b = tk.Button(side, text=label, font=FONT_SM,
                          bg=BG3 if val == "intercalacion" else BG2,
                          fg=ACCENT if val == "intercalacion" else TEXT,
                          activebackground=BG3, activeforeground=ACCENT,
                          bd=0, pady=10, cursor="hand2",
                          command=lambda v=val: self._sel_metodo(v))
            b.pack(fill="x", padx=8, pady=2)
            self.btn_metodos[val] = b

        tk.Frame(side, bg=BG3, height=1).pack(fill="x", padx=8, pady=10)
        tk.Label(side, text="EJERCICIO", font=("Consolas", 9, "bold"),
                 fg=TEXT2, bg=BG2).pack()

        self.ejercicio_var = tk.IntVar(value=0)
        self.btn_ejercicios = []
        for i in range(3):
            b = tk.Button(side, text=f"Ejercicio {i+1}", font=FONT_SM,
                          bg=BG3 if i == 0 else BG2,
                          fg=YELLOW if i == 0 else TEXT,
                          activebackground=BG3, activeforeground=YELLOW,
                          bd=0, pady=9, cursor="hand2",
                          command=lambda n=i: self._sel_ejercicio(n))
            b.pack(fill="x", padx=8, pady=2)
            self.btn_ejercicios.append(b)

        tk.Frame(side, bg=BG3, height=1).pack(fill="x", padx=8, pady=10)

        # Velocidad
        tk.Label(side, text="VELOCIDAD", font=("Consolas", 9, "bold"),
                 fg=TEXT2, bg=BG2).pack()
        self.vel_var = tk.DoubleVar(value=0.35)
        tk.Scale(side, from_=0.05, to=1.0, resolution=0.05,
                 variable=self.vel_var, orient="horizontal",
                 bg=BG2, fg=TEXT, troughcolor=BG3,
                 highlightthickness=0, sliderlength=16,
                 command=lambda v: setattr(self, '_delay', float(v))
                 ).pack(fill="x", padx=8, pady=4)

        tk.Frame(side, bg=BG3, height=1).pack(fill="x", padx=8, pady=10)

        self.btn_run = tk.Button(side, text="▶  EJECUTAR",
                                 font=FONT_BTN, bg=ACCENT, fg="white",
                                 activebackground="#8B83FF", bd=0,
                                 pady=12, cursor="hand2",
                                 command=self._ejecutar)
        self.btn_run.pack(fill="x", padx=8, pady=4)

        self.btn_rand = tk.Button(side, text="⟳  ALEATORIO",
                                  font=FONT_SM, bg=BG3, fg=TEXT2,
                                  activebackground=BG2, bd=0,
                                  pady=8, cursor="hand2",
                                  command=self._aleatorio)
        self.btn_rand.pack(fill="x", padx=8, pady=2)

    def _build_main(self, parent):
        main = tk.Frame(parent, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        # Info del ejercicio
        self.lbl_titulo = tk.Label(main, text="",
                                   font=("Consolas", 13, "bold"),
                                   fg=YELLOW, bg=BG, anchor="w")
        self.lbl_titulo.pack(fill="x", pady=(0, 4))

        self.lbl_datos = tk.Label(main, text="",
                                  font=FONT_SM, fg=TEXT2, bg=BG, anchor="w",
                                  wraplength=680, justify="left")
        self.lbl_datos.pack(fill="x", pady=(0, 8))

        # Canvas de visualización
        self.canvas = tk.Canvas(main, bg=BG2, height=280,
                                highlightthickness=1,
                                highlightbackground=BG3)
        self.canvas.pack(fill="x", pady=(0, 8))

        # Log de pasos
        tk.Label(main, text="▸ PASOS DEL ALGORITMO",
                 font=("Consolas", 9, "bold"), fg=TEXT2, bg=BG,
                 anchor="w").pack(fill="x")

        log_frame = tk.Frame(main, bg=BG2,
                             highlightbackground=BG3, highlightthickness=1)
        log_frame.pack(fill="both", expand=True, pady=(4, 0))

        self.log = tk.Text(log_frame, bg=BG2, fg=TEXT,
                           font=("Consolas", 10), bd=0,
                           insertbackground=TEXT, state="disabled",
                           height=8, wrap="word")
        scroll = tk.Scrollbar(log_frame, command=self.log.yview,
                              bg=BG3, troughcolor=BG2)
        self.log.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.log.pack(fill="both", expand=True, padx=8, pady=6)

        # Tags de colores en el log
        self.log.tag_configure("acento",  foreground=ACCENT)
        self.log.tag_configure("verde",   foreground=GREEN)
        self.log.tag_configure("amarillo",foreground=YELLOW)
        self.log.tag_configure("rojo",    foreground=ACCENT2)
        self.log.tag_configure("cyan",    foreground=CYAN)

        # Barra de estado
        self.lbl_estado = tk.Label(main, text="Listo para ejecutar",
                                   font=FONT_SM, fg=TEXT2, bg=BG, anchor="w")
        self.lbl_estado.pack(fill="x", pady=(6, 0))

        self._delay = 0.35
        self._sel_metodo("intercalacion")

    # ── SELECTORES ────────────────────────────────────────

    def _sel_metodo(self, metodo):
        self.metodo_actual = metodo
        for k, b in self.btn_metodos.items():
            b.configure(bg=BG3 if k == metodo else BG2,
                        fg=ACCENT if k == metodo else TEXT)
        self._sel_ejercicio(0)

    def _sel_ejercicio(self, idx):
        self.ejercicio_actual = idx
        for i, b in enumerate(self.btn_ejercicios):
            b.configure(bg=BG3 if i == idx else BG2,
                        fg=YELLOW if i == idx else TEXT)
        self._mostrar_info()

    def _mostrar_info(self):
        m = self.metodo_actual
        ej = self.EJERCICIOS[m][self.ejercicio_actual]
        self.lbl_titulo.config(
            text=f"Ejercicio {self.ejercicio_actual+1}  ·  {ej['titulo']}")

        if m == "intercalacion":
            self.lbl_datos.config(
                text=f"Lista A: {ej['a']}    Lista B: {ej['b']}")
            datos_vis = ej['a'] + ej['b']
        else:
            self.lbl_datos.config(text=f"Datos: {ej['datos']}")
            datos_vis = ej['datos']

        self._dibujar_barras(datos_vis, [], [], "normal", m)
        self._log_clear()
        self._log("Presiona  ▶ EJECUTAR  para iniciar la animación.\n", "acento")
        self.lbl_estado.config(text="Listo para ejecutar", fg=TEXT2)

    # ── VISUALIZACIÓN CANVAS ──────────────────────────────

    def _dibujar_barras(self, valores, activos, listos, estado, metodo):
        c = self.canvas
        c.delete("all")
        if not valores:
            return

        pal = PALETAS[metodo]
        W = c.winfo_width() or 680
        H = c.winfo_height() or 280
        PAD_X, PAD_Y = 30, 30
        n = len(valores)
        ancho = max(12, (W - 2*PAD_X) // n - 4)
        espacio = (W - 2*PAD_X) // n

        # Normalizar alturas
        try:
            nums = [float(v) if not isinstance(v, str) else 0 for v in valores]
        except Exception:
            nums = list(range(1, len(valores)+1))
        minv = min(nums) if nums else 0
        maxv = max(nums) if nums else 1
        rango = maxv - minv or 1
        max_h = H - PAD_Y - 40

        for i, (val, num) in enumerate(zip(valores, nums)):
            h = max(20, int((num - minv) / rango * max_h)) if maxv != minv else max_h // 2
            x1 = PAD_X + i * espacio
            x2 = x1 + ancho
            y1 = H - PAD_Y - h
            y2 = H - PAD_Y

            if i in listos:
                color = pal["listo"]
            elif i in activos:
                color = pal["activo"]
            else:
                color = pal["normal"]

            # Barra con efecto de brillo superior
            c.create_rectangle(x1, y1, x2, y2, fill=color,
                                outline="", tags="barra")
            # Brillo
            c.create_rectangle(x1, y1, x2, y1+4,
                                fill=self._lighten(color), outline="")

            # Etiqueta valor
            label = str(val) if not isinstance(val, float) \
                    else f"{val:.1f}"
            c.create_text(x1 + ancho//2, y1 - 6,
                          text=label, fill=TEXT,
                          font=("Consolas", max(7, min(10, 120//n))),
                          anchor="s")

    @staticmethod
    def _lighten(hex_color):
        """Aclara un color hex ligeramente."""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        r = min(255, r + 60)
        g = min(255, g + 60)
        b = min(255, b + 60)
        return f"#{r:02X}{g:02X}{b:02X}"

    # ── LOG ───────────────────────────────────────────────

    def _log_clear(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _log(self, texto, tag=None):
        self.log.configure(state="normal")
        if tag:
            self.log.insert("end", texto, tag)
        else:
            self.log.insert("end", texto)
        self.log.see("end")
        self.log.configure(state="disabled")

    # ── EJECUCIÓN ─────────────────────────────────────────

    def _ejecutar(self):
        if self.animando:
            return
        self.animando = True
        self.btn_run.configure(state="disabled", text="⏳ Ejecutando...")
        m = self.metodo_actual
        ej = self.EJERCICIOS[m][self.ejercicio_actual]
        self._log_clear()

        if m == "intercalacion":
            self._animar_intercalacion(ej)
        elif m == "directa":
            self._animar_directa(ej)
        else:
            self._animar_equilibrada(ej)

    def _fin_animacion(self, resultado):
        self._log(f"\n✔  Resultado final: {resultado}\n", "verde")
        self.lbl_estado.config(text=f"✔  Ordenado: {resultado}", fg=GREEN)
        self.animando = False
        self.btn_run.configure(state="normal", text="▶  EJECUTAR")

    def _pausa(self):
        self.root.update()
        time.sleep(self._delay)

    # ── ANIMACIÓN INTERCALACIÓN ───────────────────────────

    def _animar_intercalacion(self, ej):
        a, b = list(ej['a']), list(ej['b'])
        m = "intercalacion"
        self._log(f"Lista A: {a}\n", "acento")
        self._log(f"Lista B: {b}\n", "cyan")
        self._log("─"*40 + "\n")

        resultado, pasos = intercalacion_pasos(a, b)

        for paso in pasos:
            tipo, res, i, j = paso
            activos = []
            if tipo == "cmp":
                msg = f"Comparando  A[{i}]={a[i] if i<len(a) else '—'}  vs  B[{j}]={b[j] if j<len(b) else '—'}\n"
                self._log(msg, "amarillo")
                activos = [i, len(a) + j]
            elif tipo == "add":
                self._log(f"  → Agregado {res[-1]}   parcial={res}\n")
            elif tipo == "done":
                pass

            todos = a + b
            listos = list(range(len(res)))
            self._dibujar_barras(todos, activos, [], "normal", m)
            self._pausa()

        self._dibujar_barras(resultado, [], list(range(len(resultado))), "listo", m)
        self._fin_animacion(resultado)

    # ── ANIMACIÓN MEZCLA DIRECTA ──────────────────────────

    def _animar_directa(self, ej):
        datos = list(ej['datos'])
        m = "directa"
        self._log(f"Original: {datos}\n", "acento")
        self._log("Dividiendo y mezclando (Merge Sort)...\n")
        self._log("─"*40 + "\n")

        resultado, pasos = mezcla_directa_pasos(datos)
        n = len(datos)

        for idx, estado in enumerate(pasos):
            activos = [i for i in range(min(2, n))]
            listos = list(range(len(estado))) if estado == sorted(estado) else []
            self._log(f"Paso {idx+1}: {estado}\n", "cyan")
            self._dibujar_barras(estado, activos, listos, "normal", m)
            self._pausa()

        self._dibujar_barras(resultado, [], list(range(len(resultado))), "listo", m)
        self._fin_animacion(resultado)

    # ── ANIMACIÓN MEZCLA EQUILIBRADA ──────────────────────

    def _animar_equilibrada(self, ej):
        datos = list(ej['datos'])
        k = ej.get('k', 3)
        m = "equilibrada"
        self._log(f"Original: {datos}\n", "acento")
        self._log(f"Distribuyendo en {k} sub-listas (round-robin)...\n", "cyan")
        self._log("─"*40 + "\n")

        resultado, pasos = mezcla_equilibrada_pasos(datos, k)

        for idx, (tipo, estado) in enumerate(pasos):
            if tipo == "split":
                self._log(f"Sub-listas distribuidas: {estado}\n", "amarillo")
            elif tipo == "merge":
                self._log(f"Mezclando → {estado}\n", "cyan")
            elif tipo == "done":
                self._log(f"¡Listo! → {estado}\n", "verde")
            listos = list(range(len(estado))) if estado == sorted(estado) else []
            self._dibujar_barras(estado, [], listos, "normal", m)
            self._pausa()

        self._dibujar_barras(resultado, [], list(range(len(resultado))), "listo", m)
        self._fin_animacion(resultado)

    # ── DATOS ALEATORIOS ──────────────────────────────────

    def _aleatorio(self):
        m = self.metodo_actual
        idx = self.ejercicio_actual
        ej = self.EJERCICIOS[m][idx]

        if m == "intercalacion":
            n = random.randint(4, 8)
            nuevo_a = sorted(random.sample(range(1, 50), n))
            nuevo_b = sorted(random.sample(range(1, 50), n))
            ej['a'] = nuevo_a
            ej['b'] = nuevo_b
        else:
            n = random.randint(6, 10)
            ej['datos'] = random.sample(range(1, 100), n)

        self._mostrar_info()
        self._log("⟳ Datos aleatorios generados. Presiona ▶ EJECUTAR\n",
                  "amarillo")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrdenamientoApp(root)

    # Centrar ventana
    root.update_idletasks()
    w, h = 960, 700
    x = (root.winfo_screenwidth()  - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    root.mainloop()
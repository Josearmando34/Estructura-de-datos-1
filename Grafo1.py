import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import math
import random

# ─────────────────────────────────────────────
#  CLASES DEL TDA GRAFO
# ─────────────────────────────────────────────

class Arista:
    def __init__(self, idx, u, v, obj=None, dirigida=False):
        self.idx = idx
        self.u = u          # vértice origen
        self.v = v          # vértice destino
        self.obj = obj      # elemento de información
        self.dirigida = dirigida

    def __repr__(self):
        flecha = "→" if self.dirigida else "—"
        return f"e{self.idx}({self.u}{flecha}{self.v})"


class Vertice:
    def __init__(self, idx, obj=None):
        self.idx = idx
        self.obj = obj

    def __repr__(self):
        return f"v{self.idx}({self.obj})"


class Grafo:
    """TDA Grafo con todas las operaciones de las diapositivas."""

    def __init__(self):
        self._vertices: dict[int, Vertice] = {}
        self._aristas: dict[int, Arista] = {}
        self._vid = 0   # contador vértices
        self._eid = 0   # contador aristas

    # ── Operaciones generales ──────────────────────────────────

    def numVertices(self):
        return len(self._vertices)

    def numAristas(self):
        return len(self._aristas)

    def vertices(self):
        return list(self._vertices.keys())

    def aristas(self):
        return list(self._aristas.keys())

    def grado(self, v):
        return len(self.aristasIncidentes(v))

    def verticesAdyacentes(self, v):
        adyacentes = []
        for e in self._aristas.values():
            if e.u == v:
                adyacentes.append(e.v)
            elif e.v == v and not e.dirigida:
                adyacentes.append(e.u)
        return adyacentes

    def aristasIncidentes(self, v):
        return [e.idx for e in self._aristas.values()
                if e.u == v or (e.v == v and not e.dirigida) or e.v == v]

    def verticesFinales(self, e):
        ar = self._aristas.get(e)
        if ar is None:
            return []
        return [ar.u, ar.v]

    def opuesto(self, v, e):
        ar = self._aristas.get(e)
        if ar is None:
            return None
        if ar.u == v:
            return ar.v
        if ar.v == v:
            return ar.u
        return None

    def esAdyacente(self, v, w):
        for e in self._aristas.values():
            if (e.u == v and e.v == w) or (not e.dirigida and e.u == w and e.v == v):
                return True
        return False

    # ── Operaciones con aristas dirigidas ─────────────────────

    def aristasDirigidas(self):
        return [e.idx for e in self._aristas.values() if e.dirigida]

    def aristasNodirigidas(self):
        return [e.idx for e in self._aristas.values() if not e.dirigida]

    def gradoEnt(self, v):
        return len(self.aristasIncidentesEnt(v))

    def gradoSalida(self, v):
        return len(self.aristasIncidentesSal(v))

    def aristasIncidentesEnt(self, v):
        return [e.idx for e in self._aristas.values() if e.dirigida and e.v == v]

    def aristasIncidentesSal(self, v):
        return [e.idx for e in self._aristas.values() if e.dirigida and e.u == v]

    def verticesAdyacentesEnt(self, v):
        return [e.u for e in self._aristas.values() if e.dirigida and e.v == v]

    def verticesAdyacentesSal(self, v):
        return [e.v for e in self._aristas.values() if e.dirigida and e.u == v]

    def destino(self, e):
        ar = self._aristas.get(e)
        return ar.v if ar and ar.dirigida else None

    def origen(self, e):
        ar = self._aristas.get(e)
        return ar.u if ar and ar.dirigida else None

    def esDirigida(self, e):
        ar = self._aristas.get(e)
        return ar.dirigida if ar else False

    # ── Operaciones para actualizar grafos ────────────────────

    def insertaArista(self, v, w, obj=None):
        self._eid += 1
        ar = Arista(self._eid, v, w, obj, dirigida=False)
        self._aristas[self._eid] = ar
        return self._eid

    def insertaAristaDirigida(self, v, w, obj=None):
        self._eid += 1
        ar = Arista(self._eid, v, w, obj, dirigida=True)
        self._aristas[self._eid] = ar
        return self._eid

    def insertaVertice(self, obj=None):
        self._vid += 1
        self._vertices[self._vid] = Vertice(self._vid, obj)
        return self._vid

    def eliminaVertice(self, v):
        if v not in self._vertices:
            return
        del self._vertices[v]
        to_del = [eid for eid, e in self._aristas.items() if e.u == v or e.v == v]
        for eid in to_del:
            del self._aristas[eid]

    def eliminaArista(self, e):
        if e in self._aristas:
            del self._aristas[e]

    def convierteNoDirigida(self, e):
        if e in self._aristas:
            self._aristas[e].dirigida = False

    def invierteDir(self, e):
        if e in self._aristas:
            ar = self._aristas[e]
            ar.u, ar.v = ar.v, ar.u

    def asignaDireccionDesde(self, e, v):
        if e in self._aristas:
            ar = self._aristas[e]
            if ar.v == v:
                ar.u, ar.v = ar.v, ar.u
            ar.dirigida = True

    def asignaDireccionA(self, e, v):
        if e in self._aristas:
            ar = self._aristas[e]
            if ar.u == v:
                ar.u, ar.v = ar.v, ar.u
            ar.dirigida = True

    def get_vertice(self, idx):
        return self._vertices.get(idx)

    def get_arista(self, idx):
        return self._aristas.get(idx)


# ─────────────────────────────────────────────
#  APLICACIÓN TKINTER
# ─────────────────────────────────────────────

class GrafoApp(tk.Tk):
    COLORES = {
        "bg":       "#0a0f2e",
        "panel":    "#0d1545",
        "canvas":   "#071030",
        "accent":   "#f5c518",
        "orange":   "#ff8c00",
        "btn":      "#1a2a6c",
        "btn_h":    "#253880",
        "txt":      "#e8eaf6",
        "vertice":  "#1e90ff",
        "arista":   "#00e5ff",
        "dirig":    "#ff4500",
        "sel":      "#f5c518",
    }

    FONT_TITLE = ("Segoe UI", 14, "bold")
    FONT_BODY  = ("Segoe UI", 9)
    FONT_MONO  = ("Consolas", 9)

    def __init__(self):
        super().__init__()
        self.title("TDA Grafo — Visualizador Interactivo")
        self.configure(bg=self.COLORES["bg"])
        self.geometry("1280x800")
        self.resizable(True, True)

        self.grafo = Grafo()
        self.pos: dict[int, tuple] = {}   # posición de cada vértice en canvas
        self.sel_v = None                 # vértice seleccionado
        self.sel_e = None                 # arista seleccionada
        self.modo = tk.StringVar(value="agregar_vertice")
        self.tipo_arista = tk.StringVar(value="no_dirigida")
        self.arista_origen = None         # para dibujar aristas
        self.destacados: list[int] = []   # vértices a resaltar

        self._build_ui()
        self._bind_canvas()
        self.redraw()

    # ─── Construcción de UI ───────────────────────────────────

    def _build_ui(self):
        C = self.COLORES

        # --- Top bar ---
        top = tk.Frame(self, bg=C["panel"], pady=6)
        top.pack(fill="x")
        tk.Label(top, text="⬡  TDA Grafo", font=("Segoe UI", 16, "bold"),
                 bg=C["panel"], fg=C["accent"]).pack(side="left", padx=16)

        # Modo de interacción
        modos = [
            ("➕ Vértice", "agregar_vertice"),
            ("🔗 Arista",  "agregar_arista"),
            ("🖱 Mover",   "mover"),
            ("🗑 Eliminar","eliminar"),
        ]
        for txt, val in modos:
            rb = tk.Radiobutton(top, text=txt, variable=self.modo, value=val,
                                font=self.FONT_BODY, bg=C["panel"], fg=C["txt"],
                                selectcolor=C["btn"], activebackground=C["panel"],
                                activeforeground=C["accent"], indicatoron=False,
                                relief="flat", padx=8, pady=4, cursor="hand2")
            rb.pack(side="left", padx=4)

        # Tipo de arista
        tk.Label(top, text=" | Tipo arista:", bg=C["panel"], fg=C["txt"],
                 font=self.FONT_BODY).pack(side="left", padx=(16, 4))
        for txt, val in [("No dirigida", "no_dirigida"), ("Dirigida", "dirigida")]:
            rb = tk.Radiobutton(top, text=txt, variable=self.tipo_arista, value=val,
                                font=self.FONT_BODY, bg=C["panel"], fg=C["txt"],
                                selectcolor=C["btn"], activebackground=C["panel"],
                                activeforeground=C["orange"], indicatoron=False,
                                relief="flat", padx=8, pady=4, cursor="hand2")
            rb.pack(side="left", padx=2)

        # Botón limpiar / aleatorio
        tk.Button(top, text="🔄 Aleatorio", font=self.FONT_BODY,
                  bg=C["btn"], fg=C["accent"], relief="flat", padx=8,
                  cursor="hand2", command=self._grafo_aleatorio).pack(side="right", padx=6)
        tk.Button(top, text="🗑 Limpiar", font=self.FONT_BODY,
                  bg=C["btn"], fg="#ff6b6b", relief="flat", padx=8,
                  cursor="hand2", command=self._limpiar).pack(side="right", padx=2)
        tk.Button(top, text="✏️ Crear Grafo", font=self.FONT_BODY,
                  bg="#1a5c1a", fg="#7fff7f", relief="flat", padx=8,
                  cursor="hand2", command=self._abrir_crear_grafo).pack(side="right", padx=6)

        # --- Cuerpo principal ---
        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True)

        # Panel izquierdo (operaciones)
        left = tk.Frame(body, bg=C["panel"], width=280)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="Operaciones", font=self.FONT_TITLE,
                 bg=C["panel"], fg=C["accent"]).pack(pady=(12, 4), padx=12, anchor="w")

        nb = ttk.Notebook(left)
        nb.pack(fill="both", expand=True, padx=8, pady=4)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=C["panel"], borderwidth=0)
        style.configure("TNotebook.Tab", background=C["btn"], foreground=C["txt"],
                        font=self.FONT_BODY, padding=[6, 3])
        style.map("TNotebook.Tab", background=[("selected", C["accent"])],
                  foreground=[("selected", C["bg"])])

        self._tab_general(nb)
        self._tab_dirigidas(nb)
        self._tab_actualizar(nb)

        # Canvas
        self.canvas = tk.Canvas(body, bg=C["canvas"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Panel derecho (log)
        right = tk.Frame(body, bg=C["panel"], width=300)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(right, text="Resultado", font=self.FONT_TITLE,
                 bg=C["panel"], fg=C["accent"]).pack(pady=(12, 4), padx=12, anchor="w")

        self.log = tk.Text(right, bg=C["canvas"], fg=C["txt"], font=self.FONT_MONO,
                           relief="flat", padx=8, pady=6, wrap="word",
                           insertbackground=C["accent"])
        self.log.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.log.config(state="disabled")

        tk.Button(right, text="Limpiar log", font=self.FONT_BODY,
                  bg=C["btn"], fg=C["txt"], relief="flat",
                  command=self._clear_log).pack(pady=(0, 8))

        # Status bar
        self.status = tk.StringVar(value="Modo: Agregar vértice")
        tk.Label(self, textvariable=self.status, bg=C["btn"], fg=C["txt"],
                 font=self.FONT_BODY, anchor="w", padx=8).pack(fill="x", side="bottom")

    def _btn(self, parent, texto, cmd):
        C = self.COLORES
        b = tk.Button(parent, text=texto, font=self.FONT_BODY, bg=C["btn"],
                      fg=C["txt"], activebackground=C["btn_h"], activeforeground=C["accent"],
                      relief="flat", padx=6, pady=3, cursor="hand2", command=cmd,
                      anchor="w")
        b.pack(fill="x", pady=1, padx=4)
        return b

    def _sep(self, parent):
        tk.Frame(parent, height=1, bg="#1e2d6b").pack(fill="x", padx=4, pady=4)

    def _tab_general(self, nb):
        f = tk.Frame(nb, bg=self.COLORES["panel"])
        nb.add(f, text="General")

        ops = [
            ("numVertices()",        self._op_numVertices),
            ("numAristas()",         self._op_numAristas),
            ("vertices()",           self._op_vertices),
            ("aristas()",            self._op_aristas),
            ("grado(v)",             self._op_grado),
            ("verticesAdyacentes(v)",self._op_verticesAdyacentes),
            ("aristasIncidentes(v)", self._op_aristasIncidentes),
            ("verticesFinales(e)",   self._op_verticesFinales),
            ("opuesto(v, e)",        self._op_opuesto),
            ("esAdyacente(v, w)",    self._op_esAdyacente),
        ]
        for txt, cmd in ops:
            self._btn(f, txt, cmd)

    def _tab_dirigidas(self, nb):
        f = tk.Frame(nb, bg=self.COLORES["panel"])
        nb.add(f, text="Dirigidas")

        ops = [
            ("aristasDirigidas()",          self._op_aristasDirigidas),
            ("aristasNodirigidas()",         self._op_aristasNodirigidas),
            ("gradoEnt(v)",                  self._op_gradoEnt),
            ("gradoSalida(v)",               self._op_gradoSalida),
            ("aristasIncidentesEnt(v)",      self._op_aristasIncidentesEnt),
            ("aristasIncidentesSal(v)",      self._op_aristasIncidentesSal),
            ("verticesAdyacentesEnt(v)",     self._op_verticesAdyacentesEnt),
            ("verticesAdyacentesSal(v)",     self._op_verticesAdyacentesSal),
            ("destino(e)",                   self._op_destino),
            ("origen(e)",                    self._op_origen),
            ("esDirigida(e)",                self._op_esDirigida),
        ]
        for txt, cmd in ops:
            self._btn(f, txt, cmd)

    def _tab_actualizar(self, nb):
        f = tk.Frame(nb, bg=self.COLORES["panel"])
        nb.add(f, text="Actualizar")

        ops = [
            ("insertaArista(v,w,o)",         self._op_insertaArista),
            ("insertaAristaDirigida(v,w,o)", self._op_insertaAristaDirigida),
            ("insertaVertice(o)",            self._op_insertaVertice),
            ("eliminaVertice(v)",            self._op_eliminaVertice),
            ("eliminaArista(e)",             self._op_eliminaArista),
            ("convierteNoDirigida(e)",       self._op_convierteNoDirigida),
            ("invierteDir(e)",               self._op_invierteDir),
            ("asignaDireccionDesde(e,v)",    self._op_asignaDireccionDesde),
            ("asignaDireccionA(e,v)",        self._op_asignaDireccionA),
        ]
        for txt, cmd in ops:
            self._btn(f, txt, cmd)

    # ─── Canvas binding ───────────────────────────────────────

    def _bind_canvas(self):
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self._drag_data = {"v": None, "x": 0, "y": 0}
        self._arista_tmp = None

    def _on_click(self, ev):
        modo = self.modo.get()
        v = self._vertice_en(ev.x, ev.y)
        e = self._arista_en(ev.x, ev.y) if v is None else None

        if modo == "agregar_vertice":
            obj = simpledialog.askstring("Vértice", "Nombre/valor del vértice:", parent=self)
            if obj is None:
                return
            vid = self.grafo.insertaVertice(obj or f"v{self.grafo._vid+1}")
            self.pos[vid] = (ev.x, ev.y)
            self._log(f"insertaVertice({obj!r}) → v{vid}")
            self.redraw()

        elif modo == "agregar_arista":
            if v is not None:
                if self.arista_origen is None:
                    self.arista_origen = v
                    self.sel_v = v
                    self._log(f"Origen seleccionado: v{v}. Haz clic en el destino (o en el mismo para bucle).")
                    self.redraw()
                else:
                    origen = self.arista_origen
                    self.arista_origen = None
                    self.sel_v = None
                    es_bucle = (origen == v)
                    obj = simpledialog.askstring(
                        "Arista", f"Valor de la {'arista (bucle)' if es_bucle else 'arista'} (opcional):",
                        parent=self)
                    if self.tipo_arista.get() == "dirigida":
                        eid = self.grafo.insertaAristaDirigida(origen, v, obj)
                        tipo = "bucle dirigido" if es_bucle else "arista dirigida"
                        self._log(f"insertaAristaDirigida(v{origen}, v{v}, {obj!r}) → e{eid}  [{tipo}]")
                    else:
                        eid = self.grafo.insertaArista(origen, v, obj)
                        tipo = "bucle" if es_bucle else "arista"
                        self._log(f"insertaArista(v{origen}, v{v}, {obj!r}) → e{eid}  [{tipo}]")
                    self.redraw()

        elif modo == "mover":
            if v is not None:
                self._drag_data = {"v": v, "x": ev.x, "y": ev.y}
                self.sel_v = v
                self.redraw()

        elif modo == "eliminar":
            if v is not None:
                self.grafo.eliminaVertice(v)
                del self.pos[v]
                self._log(f"eliminaVertice(v{v})")
                self.sel_v = None
                self.redraw()
            elif e is not None:
                self.grafo.eliminaArista(e)
                self._log(f"eliminaArista(e{e})")
                self.sel_e = None
                self.redraw()

    def _on_drag(self, ev):
        if self.modo.get() == "mover" and self._drag_data["v"]:
            v = self._drag_data["v"]
            self.pos[v] = (ev.x, ev.y)
            self.redraw()

    def _on_release(self, ev):
        self._drag_data["v"] = None

    def _vertice_en(self, x, y, r=18):
        for vid, (vx, vy) in self.pos.items():
            if math.hypot(x - vx, y - vy) <= r:
                return vid
        return None

    def _arista_en(self, x, y, tol=8):
        for eid, ar in self.grafo._aristas.items():
            if ar.u not in self.pos or ar.v not in self.pos:
                continue
            # bucle
            if ar.u == ar.v:
                vx, vy = self.pos[ar.u]
                ox, oy = vx + 18, vy - 18
                R_loop = 22
                dist_centro = math.hypot(x - ox, y - oy)
                if abs(dist_centro - R_loop) <= tol:
                    return eid
                continue
            x1, y1 = self.pos[ar.u]
            x2, y2 = self.pos[ar.v]
            dx, dy = x2 - x1, y2 - y1
            if dx == dy == 0:
                continue
            t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx*dx + dy*dy)))
            px, py = x1 + t*dx, y1 + t*dy
            if math.hypot(x - px, y - py) <= tol:
                return eid
        return None

    # ─── Dibujo ───────────────────────────────────────────────

    def redraw(self):
        C = self.COLORES
        self.canvas.delete("all")

        # Aristas
        for eid, ar in self.grafo._aristas.items():
            if ar.u not in self.pos or ar.v not in self.pos:
                continue
            color = C["dirig"] if ar.dirigida else C["arista"]

            # ── BUCLE (self-loop) ──────────────────────────────
            if ar.u == ar.v:
                vx, vy = self.pos[ar.u]
                R_loop = 22   # radio del óvalo del bucle
                ox, oy = vx + 18, vy - 18   # desplazamiento del centro del bucle
                self.canvas.create_oval(
                    ox - R_loop, oy - R_loop, ox + R_loop, oy + R_loop,
                    outline=color, width=2, tags=("arista", f"e{eid}")
                )
                # flecha del bucle (pequeña, en el borde del vértice)
                if ar.dirigida:
                    self.canvas.create_polygon(
                        vx + 14, vy - 6,
                        vx + 20, vy - 2,
                        vx + 10, vy - 2,
                        fill=color, outline=color
                    )
                # etiqueta del bucle
                label = f"e{eid}"
                if ar.obj:
                    label += f":{ar.obj}"
                self.canvas.create_text(ox + R_loop + 4, oy, text=label,
                                        fill=color, font=self.FONT_MONO, anchor="w")
                continue   # no dibujar como línea normal

            # ── ARISTA NORMAL ──────────────────────────────────
            x1, y1 = self.pos[ar.u]
            x2, y2 = self.pos[ar.v]
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2,
                                    tags=("arista", f"e{eid}"))
            if ar.dirigida:
                self._draw_arrow(x1, y1, x2, y2, color)
            mx, my = (x1+x2)/2, (y1+y2)/2
            label = f"e{eid}"
            if ar.obj:
                label += f":{ar.obj}"
            self.canvas.create_text(mx, my-10, text=label, fill=color,
                                    font=self.FONT_MONO)

        # Vértices
        R = 18
        for vid, (vx, vy) in self.pos.items():
            vobj = self.grafo.get_vertice(vid)
            if vobj is None:
                continue
            outline = C["sel"] if vid == self.sel_v or vid in self.destacados else C["vertice"]
            width = 3 if (vid == self.sel_v or vid in self.destacados) else 2
            fill = C["btn_h"] if vid == self.arista_origen else C["bg"]
            self.canvas.create_oval(vx-R, vy-R, vx+R, vy+R,
                                    fill=fill, outline=outline, width=width)
            label = f"v{vid}"
            if vobj.obj:
                label += f"\n{vobj.obj}"
            self.canvas.create_text(vx, vy, text=label, fill=C["txt"],
                                    font=self.FONT_MONO)

        # Actualizar status
        modo_txt = {
            "agregar_vertice": "Agregar vértice",
            "agregar_arista":  "Agregar arista",
            "mover":           "Mover vértice",
            "eliminar":        "Eliminar elemento",
        }.get(self.modo.get(), "")
        tipo_txt = "dirigida" if self.tipo_arista.get() == "dirigida" else "no dirigida"
        self.status.set(f"Modo: {modo_txt}  |  Tipo arista: {tipo_txt}  "
                        f"|  Vértices: {self.grafo.numVertices()}  "
                        f"|  Aristas: {self.grafo.numAristas()}")

    def _draw_arrow(self, x1, y1, x2, y2, color, size=12):
        dx, dy = x2-x1, y2-y1
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        ux, uy = dx/dist, dy/dist
        R = 18
        # punto en borde del vértice destino
        ex = x2 - ux*R
        ey = y2 - uy*R
        # puntas de flecha
        px = ex - ux*size + uy*(size/2)
        py = ey - uy*size - ux*(size/2)
        qx = ex - ux*size - uy*(size/2)
        qy = ey - uy*size + ux*(size/2)
        self.canvas.create_polygon(ex, ey, px, py, qx, qy,
                                   fill=color, outline=color)

    # ─── Logging ──────────────────────────────────────────────

    def _log(self, msg):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def _clear_log(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

    # ─── Helpers de input ─────────────────────────────────────

    def _ask_v(self, prompt="Índice de vértice (ej: 1):"):
        s = simpledialog.askstring("Vértice", prompt, parent=self)
        if s is None:
            return None
        try:
            return int(s.strip().lstrip("v"))
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número de vértice válido.")
            return None

    def _ask_e(self, prompt="Índice de arista (ej: 1):"):
        s = simpledialog.askstring("Arista", prompt, parent=self)
        if s is None:
            return None
        try:
            return int(s.strip().lstrip("e"))
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número de arista válido.")
            return None

    # ─── Operaciones generales ────────────────────────────────

    def _op_numVertices(self):
        r = self.grafo.numVertices()
        self._log(f"numVertices() → {r}")
        messagebox.showinfo("numVertices()", f"Número de vértices: {r}")

    def _op_numAristas(self):
        r = self.grafo.numAristas()
        self._log(f"numAristas() → {r}")
        messagebox.showinfo("numAristas()", f"Número de aristas: {r}")

    def _op_vertices(self):
        r = self.grafo.vertices()
        self._log(f"vertices() → {r}")
        messagebox.showinfo("vertices()", f"Índices de vértices:\n{r}")

    def _op_aristas(self):
        r = self.grafo.aristas()
        self._log(f"aristas() → {r}")
        messagebox.showinfo("aristas()", f"Índices de aristas:\n{r}")

    def _op_grado(self):
        v = self._ask_v()
        if v is None: return
        r = self.grafo.grado(v)
        self._log(f"grado(v{v}) → {r}")
        messagebox.showinfo("grado(v)", f"Grado de v{v}: {r}")

    def _op_verticesAdyacentes(self):
        v = self._ask_v()
        if v is None: return
        r = self.grafo.verticesAdyacentes(v)
        self.destacados = r
        self.redraw()
        self._log(f"verticesAdyacentes(v{v}) → {r}")
        messagebox.showinfo("verticesAdyacentes(v)", f"Adyacentes a v{v}:\n{r}")
        self.destacados = []
        self.redraw()

    def _op_aristasIncidentes(self):
        v = self._ask_v()
        if v is None: return
        r = self.grafo.aristasIncidentes(v)
        self._log(f"aristasIncidentes(v{v}) → {r}")
        messagebox.showinfo("aristasIncidentes(v)", f"Aristas incidentes en v{v}:\n{r}")

    def _op_verticesFinales(self):
        e = self._ask_e()
        if e is None: return
        r = self.grafo.verticesFinales(e)
        self.destacados = r
        self.redraw()
        self._log(f"verticesFinales(e{e}) → {r}")
        messagebox.showinfo("verticesFinales(e)", f"Vértices finales de e{e}:\n{r}")
        self.destacados = []
        self.redraw()

    def _op_opuesto(self):
        v = self._ask_v("Vértice v:")
        if v is None: return
        e = self._ask_e("Arista e:")
        if e is None: return
        r = self.grafo.opuesto(v, e)
        self._log(f"opuesto(v{v}, e{e}) → {r}")
        messagebox.showinfo("opuesto(v,e)", f"Opuesto de v{v} en e{e}: {r}")

    def _op_esAdyacente(self):
        v = self._ask_v("Vértice v:")
        if v is None: return
        w = self._ask_v("Vértice w:")
        if w is None: return
        r = self.grafo.esAdyacente(v, w)
        self._log(f"esAdyacente(v{v}, v{w}) → {r}")
        messagebox.showinfo("esAdyacente(v,w)", f"¿v{v} y v{w} son adyacentes? {r}")

    # ─── Operaciones dirigidas ────────────────────────────────

    def _op_aristasDirigidas(self):
        r = self.grafo.aristasDirigidas()
        self._log(f"aristasDirigidas() → {r}")
        messagebox.showinfo("aristasDirigidas()", f"Aristas dirigidas:\n{r}")

    def _op_aristasNodirigidas(self):
        r = self.grafo.aristasNodirigidas()
        self._log(f"aristasNodirigidas() → {r}")
        messagebox.showinfo("aristasNodirigidas()", f"Aristas no dirigidas:\n{r}")

    def _op_gradoEnt(self):
        v = self._ask_v()
        if v is None: return
        r = self.grafo.gradoEnt(v)
        self._log(f"gradoEnt(v{v}) → {r}")
        messagebox.showinfo("gradoEnt(v)", f"Grado de entrada de v{v}: {r}")

    def _op_gradoSalida(self):
        v = self._ask_v()
        if v is None: return
        r = self.grafo.gradoSalida(v)
        self._log(f"gradoSalida(v{v}) → {r}")
        messagebox.showinfo("gradoSalida(v)", f"Grado de salida de v{v}: {r}")

    def _op_aristasIncidentesEnt(self):
        v = self._ask_v()
        if v is None: return
        r = self.grafo.aristasIncidentesEnt(v)
        self._log(f"aristasIncidentesEnt(v{v}) → {r}")
        messagebox.showinfo("aristasIncidentesEnt(v)", f"Aristas de entrada a v{v}:\n{r}")

    def _op_aristasIncidentesSal(self):
        v = self._ask_v()
        if v is None: return
        r = self.grafo.aristasIncidentesSal(v)
        self._log(f"aristasIncidentesSal(v{v}) → {r}")
        messagebox.showinfo("aristasIncidentesSal(v)", f"Aristas de salida de v{v}:\n{r}")

    def _op_verticesAdyacentesEnt(self):
        v = self._ask_v()
        if v is None: return
        r = self.grafo.verticesAdyacentesEnt(v)
        self.destacados = r
        self.redraw()
        self._log(f"verticesAdyacentesEnt(v{v}) → {r}")
        messagebox.showinfo("verticesAdyacentesEnt(v)", f"Adyacentes de entrada a v{v}:\n{r}")
        self.destacados = []
        self.redraw()

    def _op_verticesAdyacentesSal(self):
        v = self._ask_v()
        if v is None: return
        r = self.grafo.verticesAdyacentesSal(v)
        self.destacados = r
        self.redraw()
        self._log(f"verticesAdyacentesSal(v{v}) → {r}")
        messagebox.showinfo("verticesAdyacentesSal(v)", f"Adyacentes de salida de v{v}:\n{r}")
        self.destacados = []
        self.redraw()

    def _op_destino(self):
        e = self._ask_e()
        if e is None: return
        r = self.grafo.destino(e)
        self._log(f"destino(e{e}) → {r}")
        messagebox.showinfo("destino(e)", f"Destino de e{e}: {r}")

    def _op_origen(self):
        e = self._ask_e()
        if e is None: return
        r = self.grafo.origen(e)
        self._log(f"origen(e{e}) → {r}")
        messagebox.showinfo("origen(e)", f"Origen de e{e}: {r}")

    def _op_esDirigida(self):
        e = self._ask_e()
        if e is None: return
        r = self.grafo.esDirigida(e)
        self._log(f"esDirigida(e{e}) → {r}")
        messagebox.showinfo("esDirigida(e)", f"¿e{e} es dirigida? {r}")

    # ─── Operaciones de actualización ─────────────────────────

    def _op_insertaArista(self):
        v = self._ask_v("Vértice origen v:")
        if v is None: return
        w = self._ask_v("Vértice destino w:")
        if w is None: return
        obj = simpledialog.askstring("Valor", "Valor de la arista (opcional):", parent=self)
        eid = self.grafo.insertaArista(v, w, obj)
        self._log(f"insertaArista(v{v}, v{w}, {obj!r}) → e{eid}")
        self.redraw()

    def _op_insertaAristaDirigida(self):
        v = self._ask_v("Vértice origen v:")
        if v is None: return
        w = self._ask_v("Vértice destino w:")
        if w is None: return
        obj = simpledialog.askstring("Valor", "Valor de la arista (opcional):", parent=self)
        eid = self.grafo.insertaAristaDirigida(v, w, obj)
        self._log(f"insertaAristaDirigida(v{v}, v{w}, {obj!r}) → e{eid}")
        self.redraw()

    def _op_insertaVertice(self):
        obj = simpledialog.askstring("Vértice", "Valor del vértice:", parent=self)
        if obj is None: return
        vid = self.grafo.insertaVertice(obj)
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.pos[vid] = (random.randint(60, max(60, w-60)),
                         random.randint(60, max(60, h-60)))
        self._log(f"insertaVertice({obj!r}) → v{vid}")
        self.redraw()

    def _op_eliminaVertice(self):
        v = self._ask_v()
        if v is None: return
        if v not in self.grafo._vertices:
            messagebox.showerror("Error", f"v{v} no existe.")
            return
        self.grafo.eliminaVertice(v)
        self.pos.pop(v, None)
        self._log(f"eliminaVertice(v{v})")
        self.redraw()

    def _op_eliminaArista(self):
        e = self._ask_e()
        if e is None: return
        self.grafo.eliminaArista(e)
        self._log(f"eliminaArista(e{e})")
        self.redraw()

    def _op_convierteNoDirigida(self):
        e = self._ask_e()
        if e is None: return
        self.grafo.convierteNoDirigida(e)
        self._log(f"convierteNoDirigida(e{e})")
        self.redraw()

    def _op_invierteDir(self):
        e = self._ask_e()
        if e is None: return
        self.grafo.invierteDir(e)
        self._log(f"invierteDir(e{e})")
        self.redraw()

    def _op_asignaDireccionDesde(self):
        e = self._ask_e("Arista e:")
        if e is None: return
        v = self._ask_v("Vértice v (origen):")
        if v is None: return
        self.grafo.asignaDireccionDesde(e, v)
        self._log(f"asignaDireccionDesde(e{e}, v{v})")
        self.redraw()

    def _op_asignaDireccionA(self):
        e = self._ask_e("Arista e:")
        if e is None: return
        v = self._ask_v("Vértice v (destino):")
        if v is None: return
        self.grafo.asignaDireccionA(e, v)
        self._log(f"asignaDireccionA(e{e}, v{v})")
        self.redraw()

    # ─── Utilidades ───────────────────────────────────────────

    def _abrir_crear_grafo(self):
        """Ventana para crear un grafo completo ingresando datos manualmente."""
        C = self.COLORES
        win = tk.Toplevel(self)
        win.title("✏️ Crear Grafo Manualmente")
        win.configure(bg=C["bg"])
        win.geometry("600x620")
        win.resizable(False, False)
        win.grab_set()

        # ── Título ──
        tk.Label(win, text="Crear Grafo", font=("Segoe UI", 15, "bold"),
                 bg=C["bg"], fg=C["accent"]).pack(pady=(16, 2))
        tk.Label(win, text="Define los vértices y aristas de tu grafo",
                 font=self.FONT_BODY, bg=C["bg"], fg=C["txt"]).pack()

        # ── Tipo de grafo ──
        tipo_var = tk.StringVar(value="mixto")
        frm_tipo = tk.Frame(win, bg=C["panel"], pady=8, padx=12)
        frm_tipo.pack(fill="x", padx=16, pady=(12, 4))
        tk.Label(frm_tipo, text="Tipo de grafo:", font=("Segoe UI", 10, "bold"),
                 bg=C["panel"], fg=C["accent"]).pack(side="left", padx=(0, 12))
        for txt, val in [("No dirigido", "no_dir"), ("Dirigido", "dir"), ("Mixto", "mixto")]:
            tk.Radiobutton(frm_tipo, text=txt, variable=tipo_var, value=val,
                           font=self.FONT_BODY, bg=C["panel"], fg=C["txt"],
                           selectcolor=C["btn"], activebackground=C["panel"],
                           activeforeground=C["accent"], indicatoron=False,
                           relief="flat", padx=8, pady=3, cursor="hand2").pack(side="left", padx=4)

        # ── Vértices ──
        frm_v = tk.LabelFrame(win, text="  Vértices  ", font=("Segoe UI", 10, "bold"),
                               bg=C["panel"], fg=C["accent"], padx=10, pady=8,
                               bd=1, relief="groove")
        frm_v.pack(fill="x", padx=16, pady=6)

        tk.Label(frm_v, text="Escribe los nombres separados por coma  (ej: A, B, C, 1, 2, 3)",
                 font=self.FONT_BODY, bg=C["panel"], fg=C["txt"]).pack(anchor="w")
        ent_v = tk.Entry(frm_v, font=("Consolas", 11), bg=C["canvas"], fg=C["txt"],
                         insertbackground=C["accent"], relief="flat", bd=4)
        ent_v.pack(fill="x", pady=(4, 0))
        ent_v.insert(0, "A, B, C, D")

        # ── Aristas ──
        frm_a = tk.LabelFrame(win, text="  Aristas  ", font=("Segoe UI", 10, "bold"),
                               bg=C["panel"], fg=C["accent"], padx=10, pady=8,
                               bd=1, relief="groove")
        frm_a.pack(fill="both", expand=True, padx=16, pady=6)

        instruc = (
            "Una arista por línea.  Formatos aceptados:\n"
            "  A-B          → arista no dirigida (ignora tipo global si usas → o -)\n"
            "  A→B          → arista dirigida\n"
            "  A-B:5        → no dirigida con peso 5\n"
            "  A→B:10       → dirigida con peso 10\n"
            "Si no pones flecha, se usa el Tipo de grafo seleccionado arriba."
        )
        tk.Label(frm_a, text=instruc, font=("Consolas", 8), bg=C["panel"],
                 fg="#aab4e8", justify="left").pack(anchor="w", pady=(0, 4))

        txt_a = tk.Text(frm_a, font=("Consolas", 11), bg=C["canvas"], fg=C["txt"],
                        insertbackground=C["accent"], relief="flat", bd=4,
                        height=10)
        txt_a.pack(fill="both", expand=True)
        txt_a.insert("1.0", "A-B:3\nA→C:7\nB-C:2\nB→D:5\nC-D:4")

        # ── Botones ──
        frm_btns = tk.Frame(win, bg=C["bg"])
        frm_btns.pack(pady=10)

        def _preview():
            """Muestra resumen antes de crear."""
            vs = [x.strip() for x in ent_v.get().split(",") if x.strip()]
            lineas = [l.strip() for l in txt_a.get("1.0", "end").splitlines() if l.strip()]
            msg = f"Vértices ({len(vs)}): {', '.join(vs)}\n\nAristas ({len(lineas)}):\n"
            msg += "\n".join(f"  {l}" for l in lineas)
            messagebox.showinfo("Vista previa", msg, parent=win)

        def _crear():
            vs_raw = [x.strip() for x in ent_v.get().split(",") if x.strip()]
            if not vs_raw:
                messagebox.showerror("Error", "Debes ingresar al menos un vértice.", parent=win)
                return

            lineas = [l.strip() for l in txt_a.get("1.0", "end").splitlines() if l.strip()]
            tipo_global = tipo_var.get()   # "no_dir" | "dir" | "mixto"

            # Parsear aristas antes de modificar el grafo
            aristas_parsed = []
            errores = []
            for i, linea in enumerate(lineas, 1):
                try:
                    peso = None
                    dirigida_local = None

                    # separar peso
                    if ":" in linea:
                        partes = linea.rsplit(":", 1)
                        linea_sin_peso = partes[0].strip()
                        try:
                            peso = float(partes[1].strip())
                            if peso == int(peso):
                                peso = int(peso)
                        except ValueError:
                            peso = partes[1].strip()
                    else:
                        linea_sin_peso = linea

                    # detectar dirección
                    if "→" in linea_sin_peso:
                        u_str, v_str = linea_sin_peso.split("→", 1)
                        dirigida_local = True
                    elif "->" in linea_sin_peso:
                        u_str, v_str = linea_sin_peso.split("->", 1)
                        dirigida_local = True
                    elif "-" in linea_sin_peso:
                        u_str, v_str = linea_sin_peso.split("-", 1)
                        dirigida_local = False
                    else:
                        errores.append(f"Línea {i}: '{linea}' — formato inválido (usa - o →)")
                        continue

                    u_str = u_str.strip()
                    v_str = v_str.strip()

                    if not u_str or not v_str:
                        errores.append(f"Línea {i}: vértice vacío")
                        continue

                    # si no se especificó flecha, usar tipo global
                    if dirigida_local is None:
                        dirigida_local = (tipo_global == "dir")

                    aristas_parsed.append((u_str, v_str, peso, dirigida_local))
                except Exception as ex:
                    errores.append(f"Línea {i}: {ex}")

            if errores:
                messagebox.showerror("Errores al parsear",
                                     "Corrige los siguientes errores:\n\n" + "\n".join(errores),
                                     parent=win)
                return

            # Validar que vértices de aristas existan en la lista
            nombres_set = set(vs_raw)
            for u_str, v_str, _, _ in aristas_parsed:
                for nombre in (u_str, v_str):
                    if nombre not in nombres_set:
                        errores.append(f"Vértice '{nombre}' en arista no está en la lista de vértices.")
            if errores:
                messagebox.showerror("Vértices no definidos",
                                     "\n".join(errores), parent=win)
                return

            # ── Todo OK: limpiar y construir grafo ──
            self._limpiar()
            self.update_idletasks()
            cw = max(300, self.canvas.winfo_width())
            ch = max(300, self.canvas.winfo_height())

            nombre_a_vid = {}
            n = len(vs_raw)
            for i, nombre in enumerate(vs_raw):
                vid = self.grafo.insertaVertice(nombre)
                nombre_a_vid[nombre] = vid
                # distribuir en círculo
                angle = 2 * math.pi * i / n - math.pi / 2
                r = min(cw, ch) * 0.35
                cx, cy = cw / 2, ch / 2
                self.pos[vid] = (cx + r * math.cos(angle), cy + r * math.sin(angle))

            for u_str, v_str, peso, dirigida_local in aristas_parsed:
                uid = nombre_a_vid[u_str]
                vid2 = nombre_a_vid[v_str]
                if dirigida_local:
                    eid = self.grafo.insertaAristaDirigida(uid, vid2, peso)
                else:
                    eid = self.grafo.insertaArista(uid, vid2, peso)
                tipo_txt = "→" if dirigida_local else "—"
                self._log(f"  e{eid}: {u_str}{tipo_txt}{v_str}  peso={peso}")

            self._log(f"✅ Grafo creado: {self.grafo.numVertices()} vértices, "
                      f"{self.grafo.numAristas()} aristas")
            self.redraw()
            win.destroy()

        tk.Button(frm_btns, text="👁 Vista previa", font=self.FONT_BODY,
                  bg=C["btn"], fg=C["txt"], relief="flat", padx=12, pady=4,
                  cursor="hand2", command=_preview).pack(side="left", padx=6)
        tk.Button(frm_btns, text="✅ Crear Grafo", font=("Segoe UI", 10, "bold"),
                  bg="#1a5c1a", fg="#7fff7f", relief="flat", padx=16, pady=4,
                  cursor="hand2", command=_crear).pack(side="left", padx=6)
        tk.Button(frm_btns, text="❌ Cancelar", font=self.FONT_BODY,
                  bg=C["btn"], fg="#ff6b6b", relief="flat", padx=12, pady=4,
                  cursor="hand2", command=win.destroy).pack(side="left", padx=6)

    def _limpiar(self):
        self.grafo = Grafo()
        self.pos.clear()
        self.sel_v = None
        self.sel_e = None
        self.arista_origen = None
        self.destacados = []
        self._log("── Grafo limpiado ──")
        self.redraw()

    def _grafo_aleatorio(self):
        self._limpiar()
        self.update_idletasks()
        w = max(200, self.canvas.winfo_width())
        h = max(200, self.canvas.winfo_height())

        n = random.randint(4, 7)
        for i in range(n):
            vid = self.grafo.insertaVertice(chr(65 + i))
            angle = 2 * math.pi * i / n
            cx, cy = w/2, h/2
            r = min(w, h) * 0.33
            self.pos[vid] = (cx + r*math.cos(angle), cy + r*math.sin(angle))

        vids = list(self.grafo._vertices.keys())
        m = random.randint(n-1, min(n*2, n*(n-1)//2))
        added = set()
        for _ in range(m):
            u, v = random.sample(vids, 2)
            if (u, v) not in added and (v, u) not in added:
                dirigida = random.choice([True, False])
                if dirigida:
                    self.grafo.insertaAristaDirigida(u, v)
                else:
                    self.grafo.insertaArista(u, v)
                added.add((u, v))

        self._log(f"Grafo aleatorio: {n} vértices, {self.grafo.numAristas()} aristas")
        self.redraw()


if __name__ == "__main__":
    app = GrafoApp()
    app.mainloop()
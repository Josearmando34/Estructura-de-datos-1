"""
Frontend - Sistema de Gestión de Vuelos en Aeropuerto
Interfaz gráfica con tkinter que consume backend.AeropuertoManager
"""

import tkinter as tk
from tkinter import ttk
import threading
import time

from backend import AeropuertoManager


# ─────────────────────────────────────────────
#  APLICACIÓN PRINCIPAL
# ─────────────────────────────────────────────

class VentanaAeropuerto(tk.Tk):
    COLORES = {
        "bg":           "#0D1117",
        "panel":        "#161B22",
        "borde":        "#30363D",
        "vacio":        "#21262D",
        "ocupado":      "#DA3633",
        "frente":       "#F78166",
        "listo":        "#3FB950",   # Verde: vuelo listo para despegar
        "texto":        "#E6EDF3",
        "subtexto":     "#8B949E",
        "acento":       "#388BFD",
        "verde":        "#3FB950",
        "espera":       "#D29922",
        "rechazado":    "#6E40C9",   # Morado: vuelo rechazado
        "btn_reg":      "#238636",
        "btn_dep":      "#DA3633",
        "btn_sim":      "#388BFD",
        "btn_tick":     "#D29922",   # Amarillo: botón avanzar tick
        "btn_hover":    "#2EA043",
    }

    def __init__(self):
        super().__init__()
        self.title("✈  Sistema de Gestión de Vuelos — Cola Circular")
        self.configure(bg=self.COLORES["bg"])
        self.resizable(False, False)

        # Backend
        self.manager = AeropuertoManager()
        self.simulacion_activa = False

        self._build_ui()
        self._refresh_all()

    # ── Construcción de UI ──────────────────────

    def _build_ui(self):
        # Título
        hdr = tk.Frame(self, bg=self.COLORES["bg"])
        hdr.pack(fill="x", padx=20, pady=(18, 0))

        tk.Label(
            hdr, text="✈  AEROPUERTO — GESTIÓN DE VUELOS",
            font=("Courier New", 16, "bold"),
            bg=self.COLORES["bg"], fg=self.COLORES["acento"]
        ).pack(side="left")

        tk.Label(
            hdr, text="Cola Circular · Punteros frente/final",
            font=("Courier New", 9),
            bg=self.COLORES["bg"], fg=self.COLORES["subtexto"]
        ).pack(side="left", padx=14, pady=(4, 0))

        # Tick counter en el header
        self.lbl_tick_hdr = tk.Label(
            hdr, text="Tick: 0",
            font=("Courier New", 10, "bold"),
            bg=self.COLORES["bg"], fg=self.COLORES["btn_tick"]
        )
        self.lbl_tick_hdr.pack(side="right")

        sep = tk.Frame(self, bg=self.COLORES["borde"], height=1)
        sep.pack(fill="x", padx=20, pady=10)

        # Cuerpo
        body = tk.Frame(self, bg=self.COLORES["bg"])
        body.pack(padx=20, pady=0)

        # Columna izquierda: pistas + espera
        left = tk.Frame(body, bg=self.COLORES["bg"])
        left.pack(side="left", fill="both")

        self.frames_pistas = []
        self.celdas_pistas = []
        self.lbl_info_pistas = []

        pistas = self.manager.get_pistas()
        for i, pista in enumerate(pistas):
            frame = tk.LabelFrame(
                left,
                text=f"  {pista.nombre}  ",
                font=("Courier New", 10, "bold"),
                bg=self.COLORES["panel"],
                fg=self.COLORES["acento"],
                bd=1, relief="solid",
                labelanchor="nw"
            )
            frame.pack(fill="x", padx=0, pady=(0, 10))

            celdas = []
            fila_celdas = tk.Frame(frame, bg=self.COLORES["panel"])
            fila_celdas.pack(padx=10, pady=(4, 2))

            for j in range(pista.capacidad):
                celda = tk.Label(
                    fila_celdas,
                    text="", width=7, height=3,
                    font=("Courier New", 8, "bold"),
                    bg=self.COLORES["vacio"],
                    fg=self.COLORES["texto"],
                    relief="flat", bd=0
                )
                celda.grid(row=0, column=j, padx=3, pady=3)
                celdas.append(celda)

            lbl_info = tk.Label(
                frame,
                text="",
                font=("Courier New", 8),
                bg=self.COLORES["panel"],
                fg=self.COLORES["subtexto"],
                anchor="w"
            )
            lbl_info.pack(fill="x", padx=10, pady=(0, 6))

            self.frames_pistas.append(frame)
            self.celdas_pistas.append(celdas)
            self.lbl_info_pistas.append(lbl_info)

        # Lista de espera — scrollable vertical
        espera_frame = tk.LabelFrame(
            left,
            text="  ⏳  Lista de Espera General  ",
            font=("Courier New", 10, "bold"),
            bg=self.COLORES["panel"],
            fg=self.COLORES["espera"],
            bd=1, relief="solid",
            labelanchor="nw"
        )
        espera_frame.pack(fill="x", padx=0, pady=(0, 10))

        # Canvas + Scrollbar para scroll vertical
        espera_scroll_frame = tk.Frame(espera_frame, bg=self.COLORES["panel"])
        espera_scroll_frame.pack(fill="x", padx=10, pady=(6, 2))

        self._espera_canvas = tk.Canvas(
            espera_scroll_frame,
            bg=self.COLORES["panel"],
            highlightthickness=0,
            height=120,          # altura fija; activa scroll cuando hay muchos vuelos
        )
        espera_vscroll = tk.Scrollbar(
            espera_scroll_frame,
            orient="vertical",
            command=self._espera_canvas.yview
        )
        self._espera_canvas.configure(yscrollcommand=espera_vscroll.set)

        espera_vscroll.pack(side="right", fill="y")
        self._espera_canvas.pack(side="left", fill="both", expand=True)

        # Frame interior que vive dentro del canvas
        self.espera_canvas = tk.Frame(self._espera_canvas, bg=self.COLORES["panel"])
        self._espera_window = self._espera_canvas.create_window(
            (0, 0), window=self.espera_canvas, anchor="nw"
        )

        # Ajustar región de scroll cuando cambia el tamaño del frame interior
        def _on_espera_configure(event):
            self._espera_canvas.configure(
                scrollregion=self._espera_canvas.bbox("all")
            )
        self.espera_canvas.bind("<Configure>", _on_espera_configure)

        # Ajustar ancho del frame interior al ancho del canvas
        def _on_canvas_resize(event):
            self._espera_canvas.itemconfig(self._espera_window, width=event.width)
        self._espera_canvas.bind("<Configure>", _on_canvas_resize)

        # Scroll con rueda del ratón sobre el canvas de espera
        def _on_mousewheel(event):
            self._espera_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self._espera_canvas.bind("<MouseWheel>", _on_mousewheel)

        self.lbl_espera_info = tk.Label(
            espera_frame, text="Sin vuelos en espera.",
            font=("Courier New", 8),
            bg=self.COLORES["panel"], fg=self.COLORES["subtexto"],
            anchor="w"
        )
        self.lbl_espera_info.pack(fill="x", padx=10, pady=(2, 6))

        # Columna derecha: controles + log
        right = tk.Frame(body, bg=self.COLORES["bg"])
        right.pack(side="left", fill="both", padx=(18, 0))

        # Controles
        ctrl = tk.LabelFrame(
            right,
            text="  Controles  ",
            font=("Courier New", 10, "bold"),
            bg=self.COLORES["panel"],
            fg=self.COLORES["texto"],
            bd=1, relief="solid",
            labelanchor="nw"
        )
        ctrl.pack(fill="x", pady=(0, 10))

        btn_style = dict(
            font=("Courier New", 10, "bold"),
            relief="flat", bd=0,
            cursor="hand2", pady=8
        )

        self.btn_reg = tk.Button(
            ctrl, text="✚  Registrar Vuelo",
            bg=self.COLORES["btn_reg"], fg="white",
            command=self.registrar_vuelo, **btn_style
        )
        self.btn_reg.pack(fill="x", padx=10, pady=(10, 4))

        # Selector de pista para despegar
        sel_frame = tk.Frame(ctrl, bg=self.COLORES["panel"])
        sel_frame.pack(fill="x", padx=10, pady=2)

        tk.Label(
            sel_frame, text="Pista a despegar:",
            font=("Courier New", 9),
            bg=self.COLORES["panel"], fg=self.COLORES["subtexto"]
        ).pack(side="left")

        self.pista_sel = tk.IntVar(value=0)
        opciones = ["Auto (Round-Robin)"] + [f"Pista {i+1}" for i in range(len(pistas))]
        self.combo_pista = ttk.Combobox(
            sel_frame, textvariable=self.pista_sel,
            values=opciones, state="readonly", width=18,
            font=("Courier New", 9)
        )
        self.combo_pista.current(0)
        self.combo_pista.pack(side="left", padx=6)

        self.btn_dep = tk.Button(
            ctrl, text="🛫  Despegar Vuelo (manual)",
            bg=self.COLORES["btn_dep"], fg="white",
            command=self.despegar_vuelo, **btn_style
        )
        self.btn_dep.pack(fill="x", padx=10, pady=4)

        # ── NUEVO: Botón Avanzar Tick ──────────────
        sep2 = tk.Frame(ctrl, bg=self.COLORES["borde"], height=1)
        sep2.pack(fill="x", padx=10, pady=4)

        self.btn_tick = tk.Button(
            ctrl, text="⏱  Avanzar 1 Tick",
            bg=self.COLORES["btn_tick"], fg="#0D1117",
            command=self.avanzar_tick_manual, **btn_style
        )
        self.btn_tick.pack(fill="x", padx=10, pady=4)

        self.btn_sim = tk.Button(
            ctrl, text="⚡  Simulación Automática (15 vuelos)",
            bg=self.COLORES["btn_sim"], fg="white",
            command=self.iniciar_simulacion, **btn_style
        )
        self.btn_sim.pack(fill="x", padx=10, pady=(4, 10))

        # Leyenda de colores
        leyenda_frame = tk.LabelFrame(
            right,
            text="  Leyenda  ",
            font=("Courier New", 9, "bold"),
            bg=self.COLORES["panel"],
            fg=self.COLORES["subtexto"],
            bd=1, relief="solid",
            labelanchor="nw"
        )
        leyenda_frame.pack(fill="x", pady=(0, 10))

        leyenda_items = [
            (self.COLORES["listo"],    "Listo para despegar (ticks=0)"),
            (self.COLORES["frente"],   "Frente de cola (siguiente en despegar)"),
            (self.COLORES["ocupado"],  "En preparación"),
            (self.COLORES["rechazado"],"Vuelo rechazado (espera llena)"),
        ]
        for color, desc in leyenda_items:
            row = tk.Frame(leyenda_frame, bg=self.COLORES["panel"])
            row.pack(fill="x", padx=8, pady=1)
            tk.Label(row, text="  ", bg=color, width=2).pack(side="left", padx=(0, 6))
            tk.Label(row, text=desc, font=("Courier New", 7),
                     bg=self.COLORES["panel"], fg=self.COLORES["subtexto"]).pack(side="left")

        # Punteros info
        ptr_frame = tk.LabelFrame(
            right,
            text="  Punteros de Cola  ",
            font=("Courier New", 10, "bold"),
            bg=self.COLORES["panel"],
            fg=self.COLORES["texto"],
            bd=1, relief="solid",
            labelanchor="nw"
        )
        ptr_frame.pack(fill="x", pady=(0, 10))

        self.lbl_punteros = tk.Label(
            ptr_frame, text="",
            font=("Courier New", 8),
            bg=self.COLORES["panel"],
            fg=self.COLORES["texto"],
            justify="left", anchor="w"
        )
        self.lbl_punteros.pack(fill="x", padx=10, pady=8)

        # Log
        log_frame = tk.LabelFrame(
            right,
            text="  Log de Eventos  ",
            font=("Courier New", 10, "bold"),
            bg=self.COLORES["panel"],
            fg=self.COLORES["texto"],
            bd=1, relief="solid",
            labelanchor="nw"
        )
        log_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(
            log_frame,
            font=("Courier New", 8),
            bg=self.COLORES["vacio"],
            fg=self.COLORES["texto"],
            relief="flat", bd=0,
            width=40, height=14,
            state="disabled",
            wrap="word"
        )
        self.log_text.pack(fill="both", expand=True, padx=6, pady=6)

        scroll = tk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text["yscrollcommand"] = scroll.set

        # Tags de color para el log
        self.log_text.tag_config("reg",       foreground=self.COLORES["verde"])
        self.log_text.tag_config("dep",       foreground=self.COLORES["frente"])
        self.log_text.tag_config("esp",       foreground=self.COLORES["espera"])
        self.log_text.tag_config("err",       foreground=self.COLORES["ocupado"])
        self.log_text.tag_config("sim",       foreground=self.COLORES["acento"])
        self.log_text.tag_config("info",      foreground=self.COLORES["subtexto"])
        self.log_text.tag_config("rechazado", foreground=self.COLORES["rechazado"])

    # ── Métodos de Negocio ────────────────────

    def registrar_vuelo(self):
        """Registra un nuevo vuelo a través del backend."""
        vuelo, pista_asignada, rechazado = self.manager.registrar_vuelo()

        if rechazado:
            self._log(
                f"[✗] {vuelo.nombre} RECHAZADO — lista de espera llena "
                f"({self.manager.MAX_ESPERA}/{self.manager.MAX_ESPERA})",
                "rechazado"
            )
        elif pista_asignada:
            self._log(
                f"[✚] {vuelo.nombre} → {pista_asignada.nombre} "
                f"(prep: {vuelo.ticks_restantes} ticks)",
                "reg"
            )
        else:
            self._log(
                f"[⏳] {vuelo.nombre} → Lista de Espera "
                f"({len(self.manager.lista_espera)}/{self.manager.MAX_ESPERA})",
                "esp"
            )

        self._refresh_all()

    def despegar_vuelo(self):
        """Despega manualmente un vuelo sin respetar ticks (acción forzada)."""
        sel = self.combo_pista.get()

        if sel == "Auto (Round-Robin)" or sel == "":
            pista_idx = None
        else:
            pista_idx = int(sel.split(" ")[1]) - 1

        vuelo_despegado, vuelo_de_espera = self.manager.despegar_vuelo(pista_idx)

        if vuelo_despegado is None:
            self._log("[!] No hay vuelos en la pista seleccionada.", "err")
            return

        self._log(f"[🛫] {vuelo_despegado.nombre} despegó (manual)", "dep")

        if vuelo_de_espera:
            pistas = self.manager.get_pistas()
            for p in pistas:
                if vuelo_de_espera in p.get_slots():
                    self._log(
                        f"[→] {vuelo_de_espera.nombre} pasó de Espera → {p.nombre}",
                        "esp"
                    )
                    break

        self._refresh_all()

    def avanzar_tick_manual(self):
        """Avanza un tick manualmente y actualiza la UI."""
        eventos = self.manager.avanzar_tick()
        for msg, tag in eventos:
            self._log(msg, tag)
        self._refresh_all()

    def iniciar_simulacion(self):
        """Inicia simulación automática en thread separado."""
        if self.simulacion_activa:
            return
        self.simulacion_activa = True
        self.btn_sim.config(state="disabled", text="⚡ Simulando...")
        self._log("── Simulación Automática iniciada ──", "sim")
        t = threading.Thread(target=self._run_simulacion, daemon=True)
        t.start()

    def _run_simulacion(self):
        """
        Simulación: registra 15 vuelos en los primeros ciclos,
        luego avanza ticks automáticamente hasta que todo despegue.
        En cada iteración: registra un vuelo (si quedan) y avanza un tick.
        """
        for i in range(15):
            self.after(0, self.registrar_vuelo)
            time.sleep(0.5)
            self.after(0, self.avanzar_tick_manual)
            time.sleep(0.5)

        # Seguir avanzando ticks hasta vaciar las pistas y lista de espera
        def quedan_vuelos():
            if self.manager.get_lista_espera():
                return True
            for p in self.manager.get_pistas():
                if not p.esta_vacia():
                    return True
            return False

        extra_ticks = 0
        while quedan_vuelos() and extra_ticks < 30:
            self.after(0, self.avanzar_tick_manual)
            time.sleep(0.4)
            extra_ticks += 1

        self.after(0, self._fin_simulacion)

    def _fin_simulacion(self):
        """Limpia estado de simulación."""
        self.simulacion_activa = False
        self.btn_sim.config(state="normal", text="⚡  Simulación Automática (15 vuelos)")
        self._log("── Simulación Automática finalizada ──", "sim")

    # ── Refresco de UI ─────────────────────────

    def _refresh_all(self):
        """Refresca toda la interfaz."""
        self._refresh_pistas()
        self._refresh_espera()
        self._refresh_punteros()
        self.lbl_tick_hdr.config(text=f"Tick: {self.manager.get_tick_actual()}")

    def _refresh_pistas(self):
        """
        Actualiza visualización de pistas.
        Colores:
          - Verde  → frente de cola Y listo para despegar (ticks=0)
          - Naranja → frente de cola, aún preparándose
          - Rojo   → en cola, preparándose
        """
        pistas = self.manager.get_pistas()
        for i, pista in enumerate(pistas):
            slots = pista.get_slots()
            frente_idx = pista.frente
            celdas = self.celdas_pistas[i]

            for j, celda in enumerate(celdas):
                vuelo = slots[j]
                if vuelo is None:
                    celda.config(
                        text="LIBRE",
                        bg=self.COLORES["vacio"],
                        fg=self.COLORES["subtexto"]
                    )
                else:
                    es_frente = (j == frente_idx and not pista.esta_vacia())
                    if es_frente and vuelo.listo_para_despegar():
                        color_bg = self.COLORES["listo"]   # Verde: listo
                    elif es_frente:
                        color_bg = self.COLORES["frente"]  # Naranja: frente pero no listo
                    else:
                        color_bg = self.COLORES["ocupado"] # Rojo: en cola

                    celda.config(
                        text=f"✈\n{vuelo.nombre}\n⏱{vuelo.ticks_restantes}",
                        bg=color_bg,
                        fg="white"
                    )

            sig = pista.siguiente()
            sig_str = f"{sig.nombre}(⏱{sig.ticks_restantes})" if sig else "—"
            info = (
                f"Vuelos: {pista.tamaño}/{pista.capacidad}  |  "
                f"frente={pista.frente}  final={pista.final}  |  "
                f"Siguiente: {sig_str}"
            )
            self.lbl_info_pistas[i].config(text=info)

    def _refresh_espera(self):
        """
        Actualiza visualización de lista de espera.
        Los vuelos crecen hacia abajo (una fila por vuelo) con scrollbar vertical.
        """
        for w in self.espera_canvas.winfo_children():
            w.destroy()

        lista_espera = self.manager.get_lista_espera()
        max_espera = self.manager.get_max_espera()

        if not lista_espera:
            tk.Label(
                self.espera_canvas, text="— Sin vuelos en espera —",
                font=("Courier New", 8),
                bg=self.COLORES["panel"], fg=self.COLORES["subtexto"]
            ).pack(pady=4)
            self.lbl_espera_info.config(
                text=f"Cola de espera vacía. (0/{max_espera})"
            )
        else:
            for idx, vuelo in enumerate(lista_espera):
                fila = tk.Frame(self.espera_canvas, bg=self.COLORES["panel"])
                fila.pack(fill="x", pady=2, padx=2)

                # Número de posición en cola
                tk.Label(
                    fila,
                    text=f"#{idx+1:02d}",
                    font=("Courier New", 8),
                    bg=self.COLORES["panel"],
                    fg=self.COLORES["subtexto"],
                    width=4
                ).pack(side="left", padx=(2, 4))

                # Tarjeta del vuelo
                tk.Label(
                    fila,
                    text=f"✈  {vuelo.nombre}",
                    font=("Courier New", 9, "bold"),
                    bg=self.COLORES["espera"], fg="white",
                    padx=8, pady=3, relief="flat", anchor="w"
                ).pack(side="left", fill="x", expand=True)

                # Ticks esperando
                tk.Label(
                    fila,
                    text=f"⏳ {vuelo.ticks_en_espera} ticks",
                    font=("Courier New", 8),
                    bg=self.COLORES["vacio"],
                    fg=self.COLORES["subtexto"],
                    padx=6, pady=3
                ).pack(side="left", padx=(4, 2))

            self.lbl_espera_info.config(
                text=f"Total en espera: {len(lista_espera)}/{max_espera} vuelo(s)"
            )

        # Forzar actualización del scroll region
        self.espera_canvas.update_idletasks()
        self._espera_canvas.configure(
            scrollregion=self._espera_canvas.bbox("all")
        )

    def _refresh_punteros(self):
        """Actualiza información de punteros de cola con ticks del frente."""
        pistas = self.manager.get_pistas()
        lineas = []
        for pista in pistas:
            sig = pista.siguiente()
            sig_str = f"{sig.nombre}(⏱{sig.ticks_restantes})" if sig else "—"
            lineas.append(
                f"{pista.nombre:<8}  frente={pista.frente}  "
                f"final={pista.final}  "
                f"siguiente={sig_str}"
            )
        self.lbl_punteros.config(text="\n".join(lineas))

    def _log(self, msg: str, tag: str = "info"):
        """Agrega mensaje al log con formato de color."""
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n", tag)
        self.log_text.see("end")
        self.log_text.config(state="disabled")


# ─────────────────────────────────────────────
#  ENTRADA
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = VentanaAeropuerto()
    app.mainloop()
import tkinter as tk
from tkinter import messagebox
import re

class Pila:
    """
    Implementación de una Pila (LIFO).
    Usada para evaluar expresiones posfijas y prefijas.
    """

    def __init__(self):
        self._elementos = []

    def apilar(self, elemento):
        """Agrega un elemento al tope (push)."""
        self._elementos.append(elemento)

    def desapilar(self):
        """Elimina y retorna el elemento del tope (pop)."""
        if self.esta_vacia():
            raise IndexError("Subdesbordamiento: la pila está vacía")
        return self._elementos.pop()

    def tope(self):
        """Retorna el elemento del tope sin eliminarlo (peek)."""
        if self.esta_vacia():
            return None
        return self._elementos[-1]

    def esta_vacia(self):
        """Retorna True si la pila no tiene elementos."""
        return len(self._elementos) == 0

    def tamanio(self):
        """Retorna la cantidad de elementos en la pila."""
        return len(self._elementos)

    def elementos(self):
        """Retorna una copia de los elementos (base → tope)."""
        return list(self._elementos)

    def limpiar(self):
        """Vacía la pila por completo."""
        self._elementos.clear()

    def __repr__(self):
        return f"Pila({self._elementos})"

OPERADORES = {"+", "-", "*", "/", "^", "%"}


def es_numero(token):
    """Retorna True si el token es un número (entero o decimal)."""
    try:
        float(token)
        return True
    except ValueError:
        return False


def aplicar_operacion(operador, a, b):
    """
    Aplica el operador binario a dos operandos.
    a  es el operando IZQUIERDO.
    b  es el operando DERECHO.
    Retorna el resultado como float.
    """
    if operador == "+": return a + b
    if operador == "-": return a - b
    if operador == "*": return a * b
    if operador == "/":
        if b == 0:
            raise ZeroDivisionError("División por cero")
        return a / b
    if operador == "^": return a ** b
    if operador == "%":
        if b == 0:
            raise ZeroDivisionError("Módulo por cero")
        return a % b
    raise ValueError(f"Operador desconocido: {operador}")


def evaluar_posfija(expresion: str):
    """
    Evalúa una expresión en notación POSFIJA (postfix / RPN).
    Algoritmo:
      - Recorre los tokens de IZQUIERDA a DERECHA.
      - Si es número → apilar.
      - Si es operador → desapilar b y a, operar, apilar resultado.
    Retorna (resultado, pasos) donde pasos es la traza de la pila.
    """
    tokens = expresion.strip().split()
    pila   = Pila()
    pasos  = []

    for token in tokens:
        if es_numero(token):
            pila.apilar(float(token))
            pasos.append(("push", token, list(pila.elementos())))
        elif token in OPERADORES:
            if pila.tamanio() < 2:
                raise ValueError(
                    f"Operador '{token}' sin suficientes operandos en la pila"
                )
            b = pila.desapilar()  
            a = pila.desapilar() 
            resultado = aplicar_operacion(token, a, b)
            pila.apilar(resultado)
            pasos.append(("op", f"{a} {token} {b} = {_fmt(resultado)}",
                          list(pila.elementos())))
        else:
            raise ValueError(f"Token inválido: '{token}'")

    if pila.tamanio() != 1:
        raise ValueError(
            "Expresión mal formada: quedaron múltiples valores en la pila"
        )

    return pila.desapilar(), pasos


def evaluar_prefija(expresion: str):
    """
    Evalúa una expresión en notación PREFIJA (prefix).
    Algoritmo:
      - Recorre los tokens de DERECHA a IZQUIERDA.
      - Si es número → apilar.
      - Si es operador → desapilar a y b, operar, apilar resultado.
        (orden invertido respecto a posfija porque leemos al revés)
    Retorna (resultado, pasos) donde pasos es la traza de la pila.
    """
    tokens = expresion.strip().split()[::-1] 
    pila   = Pila()
    pasos  = []

    for token in tokens:
        if es_numero(token):
            pila.apilar(float(token))
            pasos.append(("push", token, list(pila.elementos())))
        elif token in OPERADORES:
            if pila.tamanio() < 2:
                raise ValueError(
                    f"Operador '{token}' sin suficientes operandos en la pila"
                )
            a = pila.desapilar() 
            b = pila.desapilar()   
            resultado = aplicar_operacion(token, a, b)
            pila.apilar(resultado)
            pasos.append(("op", f"{a} {token} {b} = {_fmt(resultado)}",
                          list(pila.elementos())))
        else:
            raise ValueError(f"Token inválido: '{token}'")

    if pila.tamanio() != 1:
        raise ValueError(
            "Expresión mal formada: quedaron múltiples valores en la pila"
        )

    return pila.desapilar(), pasos


def _fmt(v):
    """Formatea un número: entero si no tiene decimales, si no 4 cifras."""
    return int(v) if v == int(v) else round(v, 4)

BG   = "#0d0f1a"
PAN  = "#13162a"
ACC  = "#00e5a0"
RED  = "#ff6b6b"
BLUE = "#7b8cde"
GOLD = "#f5a623"
MUTED = "#444"

EJEMPLOS_POSFIJA = [
    ("3 4 +",          "3 + 4 = 7"),
    ("5 1 2 + 4 * + 3 -", "5+((1+2)*4)-3 = 14"),
    ("2 3 ^ 1 -",      "2³ − 1 = 7"),
    ("15 7 1 1 + - / 3 * 2 1 1 + + -", "Expresión compleja = 5"),
    ("100 20 5 * -",   "100 − 20×5 = 0"),
]

EJEMPLOS_PREFIJA = [
    ("+ 3 4",          "3 + 4 = 7"),
    ("+ 5 - * 4 + 1 2 3", "5+((1+2)*4)-3 = 14"),
    ("- ^ 2 3 1",      "2³ − 1 = 7"),
    ("- * / 15 - 7 + 1 1 3 + 2 + 1 1", "Expresión compleja = 5"),
    ("- 100 * 20 5",   "100 − 20×5 = 0"),
]


class EvaluadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evaluador de Expresiones — Notación Posfija / Prefija")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        # Título
        hdr = tk.Frame(self.root, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(18, 6))
        tk.Label(hdr, text="EVALUADOR DE EXPRESIONES",
                 bg=BG, fg=ACC, font=("Courier", 18, "bold")).pack()
        tk.Label(hdr, text="Notación Posfija (RPN) y Prefija · Estructura: Clase Pila",
                 bg=BG, fg=MUTED, font=("Courier", 9)).pack()

        main = tk.Frame(self.root, bg=BG)
        main.pack(padx=20, pady=8)

        left = tk.Frame(main, bg=BG)
        left.grid(row=0, column=0, padx=(0, 20), sticky="n")

        tk.Label(left, text="ESTADO DE LA PILA",
                 bg=BG, fg=MUTED, font=("Courier", 9, "bold")).pack(pady=(0, 4))

        self.canvas = tk.Canvas(left, width=220, height=320,
                                bg=PAN, highlightthickness=1,
                                highlightbackground="#2a2d45")
        self.canvas.pack()

        self.tope_label = tk.Label(left, text="TOPE = 0",
                                   bg=PAN, fg=ACC,
                                   font=("Courier", 12, "bold"))
        self.tope_label.pack(fill="x")


        right = tk.Frame(main, bg=BG)
        right.grid(row=0, column=1, sticky="n")

        # Selector de notación
        notacion_box = self._labelframe(right, " Notación ")
        notacion_box.pack(fill="x", pady=(0, 8))

        self.var_notacion = tk.StringVar(value="Posfija")
        for txt in ["Posfija (RPN)", "Prefija"]:
            rb = tk.Radiobutton(notacion_box, text=txt,
                                variable=self.var_notacion,
                                value=txt.split()[0],
                                bg=BG, fg=ACC, selectcolor="#1e2240",
                                activebackground=BG, activeforeground=ACC,
                                font=("Courier", 10),
                                command=self._on_notacion_change)
            rb.pack(side="left", padx=10, pady=6)

        # Entrada de expresión
        entrada_box = self._labelframe(right, " Expresión ")
        entrada_box.pack(fill="x", pady=(0, 8))

        ef = tk.Frame(entrada_box, bg=BG)
        ef.pack(padx=10, pady=8, fill="x")

        self.entrada = tk.Entry(ef, width=36,
                                bg="#1e2240", fg=ACC,
                                insertbackground=ACC,
                                relief="flat", bd=4,
                                font=("Courier", 12, "bold"))
        self.entrada.pack(fill="x", pady=(0, 6))
        self.entrada.bind("<Return>", lambda e: self.evaluar())

        hint = tk.Label(ef, text="Separar tokens con espacios:  3 4 +  ó  + 3 4",
                        bg=BG, fg=MUTED, font=("Courier", 8))
        hint.pack(anchor="w")

        btn_f = tk.Frame(entrada_box, bg=BG)
        btn_f.pack(padx=10, pady=(0, 8))
        self._btn(btn_f, "▶ EVALUAR", ACC, self.evaluar).grid(row=0, column=0, padx=3)
        self._btn(btn_f, "↺ LIMPIAR", RED, self.limpiar).grid(row=0, column=1, padx=3)

        # Ejemplos
        ej_box = self._labelframe(right, " Ejemplos rápidos ")
        ej_box.pack(fill="x", pady=(0, 8))

        self.frame_ejemplos = tk.Frame(ej_box, bg=BG)
        self.frame_ejemplos.pack(padx=10, pady=6, fill="x")
        self._build_ejemplos()

        # Resultado
        res_box = self._labelframe(right, " Resultado ")
        res_box.pack(fill="x", pady=(0, 8))

        self.lbl_resultado = tk.Label(res_box, text="—",
                                      bg=BG, fg=GOLD,
                                      font=("Courier", 22, "bold"))
        self.lbl_resultado.pack(pady=8)

        # Traza de pasos
        log_box = self._labelframe(right, " Traza — Pila paso a paso ")
        log_box.pack(fill="both", expand=True)

        self.log = tk.Text(log_box, width=46, height=10,
                           bg="#0a0c14", fg="#a0a0c0",
                           font=("Courier", 9),
                           state="disabled", relief="flat",
                           insertbackground=ACC)
        sb = tk.Scrollbar(log_box, command=self.log.yview, bg=PAN)
        self.log.configure(yscrollcommand=sb.set)
        self.log.pack(side="left", padx=(8, 0), pady=8, fill="both", expand=True)
        sb.pack(side="right", fill="y", pady=8, padx=(0, 4))

        self.log.tag_config("push",  foreground=ACC)
        self.log.tag_config("op",    foreground=BLUE)
        self.log.tag_config("error", foreground=RED)
        self.log.tag_config("info",  foreground=MUTED)
        self.log.tag_config("res",   foreground=GOLD)

        self._log("info", "─" * 42)
        self._log("info", " Ingresa una expresión y presiona EVALUAR.")
        self._log("info", "─" * 42)

        # Estado inicial de la pila
        self._dibujar_pila([])

   
    def _build_ejemplos(self):
        for w in self.frame_ejemplos.winfo_children():
            w.destroy()
        ejemplos = (EJEMPLOS_POSFIJA if self.var_notacion.get() == "Posfija"
                    else EJEMPLOS_PREFIJA)
        for expr, desc in ejemplos:
            f = tk.Frame(self.frame_ejemplos, bg=BG)
            f.pack(fill="x", pady=1)
            self._btn(f, expr, BLUE,
                      lambda e=expr: self._cargar_ejemplo(e)).pack(side="left")
            tk.Label(f, text=f"  ← {desc}", bg=BG, fg=MUTED,
                     font=("Courier", 8)).pack(side="left")

    def _on_notacion_change(self):
        self._build_ejemplos()

    def _cargar_ejemplo(self, expr):
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, expr)
        self.evaluar()

    def evaluar(self):
        expr = self.entrada.get().strip()
        if not expr:
            messagebox.showwarning("Aviso", "Ingresa una expresión")
            return

        notacion = self.var_notacion.get()
        self._log_clear()
        self._log("info", f"Notación : {notacion}")
        self._log("info", f"Expresión: {expr}")
        self._log("info", "─" * 42)

        try:
            if notacion == "Posfija":
                resultado, pasos = evaluar_posfija(expr)
            else:
                resultado, pasos = evaluar_prefija(expr)

            # Mostrar traza
            for tipo, detalle, estado_pila in pasos:
                if tipo == "push":
                    self._log("push",
                              f"  PUSH {detalle:<8}  Pila: {[_fmt(x) for x in estado_pila]}")
                else:
                    self._log("op",
                              f"  OP   {detalle:<20}  Pila: {[_fmt(x) for x in estado_pila]}")

            self._log("info", "─" * 42)
            self._log("res",  f"  RESULTADO = {_fmt(resultado)}")

            # Actualizar visual
            self.lbl_resultado.config(text=str(_fmt(resultado)), fg=ACC)
            self._dibujar_pila([resultado], highlight_idx=0, highlight_color=ACC)

        except (ValueError, ZeroDivisionError, IndexError) as e:
            self._log("error", f"  ERROR: {e}")
            self.lbl_resultado.config(text="ERROR", fg=RED)
            self._dibujar_pila([])

    def limpiar(self):
        self.entrada.delete(0, tk.END)
        self.lbl_resultado.config(text="—", fg=GOLD)
        self._log_clear()
        self._log("info", "─" * 42)
        self._log("info", " Listo para una nueva expresión.")
        self._log("info", "─" * 42)
        self._dibujar_pila([])

    def _dibujar_pila(self, elementos, highlight_idx=None, highlight_color=None):
        """
        Dibuja el estado actual de la pila en el canvas.
        elementos: lista de valores (base → tope).
        """
        c = self.canvas
        c.delete("all")

        MAX_SLOTS = 8
        W, H      = 220, 320
        CELL_H    = 34
        CELL_W    = 110
        X0        = (W - CELL_W) // 2
        Y_BASE    = H - 16

        for i in range(MAX_SLOTS):
            y_top = Y_BASE - (i + 1) * CELL_H
            val   = elementos[i] if i < len(elementos) else None

            if highlight_idx == i and highlight_color:
                fill   = highlight_color + "33"
                border = highlight_color
            elif val is not None:
                fill   = "#1a2040"
                border = "#2a4a7f"
            else:
                fill   = "#0f1120"
                border = "#1e2030"

            c.create_rectangle(X0, y_top, X0 + CELL_W, y_top + CELL_H,
                               fill=fill, outline=border, width=2)
            c.create_text(X0 - 10, y_top + CELL_H // 2,
                          text=f"[{i}]", fill="#333",
                          font=("Courier", 8), anchor="e")

            txt_color = (highlight_color if highlight_idx == i and highlight_color
                         else ("#c0d0ff" if val is not None else "#1e2030"))
            display = str(_fmt(val)) if val is not None else "—"
            c.create_text(X0 + CELL_W // 2, y_top + CELL_H // 2,
                          text=display, fill=txt_color,
                          font=("Courier", 11, "bold"))

        # Flecha TOPE
        tope = len(elementos)
        if tope > 0:
            ti    = tope - 1
            y_top = Y_BASE - (ti + 1) * CELL_H
            cy    = y_top + CELL_H // 2
            c.create_text(X0 + CELL_W + 32, cy,
                          text="◄ TOPE", fill=RED,
                          font=("Courier", 9, "bold"))
        else:
            c.create_text(X0 + CELL_W + 32, Y_BASE - CELL_H // 2,
                          text="◄ TOPE=0", fill=MUTED,
                          font=("Courier", 9))

        c.create_text(W // 2, 12,
                      text=f"Elementos: {tope} / {MAX_SLOTS}",
                      fill="#888", font=("Courier", 10, "bold"))

        self.tope_label.config(text=f"TOPE = {tope}")

    def _labelframe(self, parent, text):
        return tk.LabelFrame(parent, text=text,
                             bg=BG, fg=MUTED,
                             font=("Courier", 9),
                             relief="flat", bd=1,
                             highlightbackground="#2a2d45",
                             highlightthickness=1)

    def _btn(self, parent, text, color, cmd):
        return tk.Button(parent, text=text, command=cmd,
                         bg=PAN, fg=color,
                         activebackground="#1e2240", activeforeground=color,
                         relief="flat", bd=0,
                         font=("Courier", 9, "bold"),
                         padx=8, pady=5, cursor="hand2")

    def _log(self, tag, msg):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n", tag)
        self.log.see("end")
        self.log.config(state="disabled")

    def _log_clear(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    w, h = 960, 620
    sw   = root.winfo_screenwidth()
    sh   = root.winfo_screenheight()
    root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    EvaluadorApp(root)
    root.mainloop()
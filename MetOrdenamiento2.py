"""
Sorting Visualizer — Algoritmos de Ordenamiento
================================================
Implementaciones originales adaptadas para visualización animada con tkinter.

Algoritmos:
  1. ShellSort  — Secuencia de gaps de Marcin Ciura
                  https://en.wikipedia.org/wiki/Shellsort#Pseudocode
  2. QuickSort  — 3-way partition (Dutch National Flag)
                  https://en.wikipedia.org/wiki/Quicksort
  3. HeapSort   — Max-heap puro Python
  4. RadixSort  — MSD con representación binaria
                  https://en.wikipedia.org/wiki/Radix_sort
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading


def shell_sort(collection: list, cb, delay: float) -> list:
    """
    Pure implementation of shell sort algorithm in Python.
    Uses Marcin Ciura's gap sequence: [701, 301, 132, 57, 23, 10, 4, 1]

    :param collection: Some mutable ordered collection with heterogeneous
                       comparable items inside
    :param cb:    Visual callback(arr, compare_indices, sorted_indices)
    :param delay: Pausa en segundos entre pasos
    :return: the same collection ordered by ascending

    >>> shell_sort([0, 5, 3, 2, 2], lambda *_: None, 0)
    [0, 2, 2, 3, 5]
    >>> shell_sort([], lambda *_: None, 0)
    []
    >>> shell_sort([-2, -5, -45], lambda *_: None, 0)
    [-45, -5, -2]
    """
    # Marcin Ciura's gap sequence
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]
    for gap in gaps:
        for i in range(gap, len(collection)):
            insert_value = collection[i]
            j = i
            while j >= gap and collection[j - gap] > insert_value:
                collection[j] = collection[j - gap]
                cb(collection, [j, j - gap], [])
                time.sleep(delay)
                j -= gap
            if j != i:
                collection[j] = insert_value
                cb(collection, [], [j])
                time.sleep(delay)
    return collection


def quick_sort(sorting: list, cb, delay: float) -> list:
    """
    Python implementation of quick sort with 3-way partition.
    Based on the Dutch National Flag algorithm.

    :param sorting: mutable list of comparable items
    :param cb:    Visual callback(arr, compare_indices, sorted_indices)
    :param delay: Pausa en segundos entre pasos
    :return: the same list ordered ascending

    >>> quick_sort([5, -1, -1, 5, 5, 24, 0], lambda *_: None, 0)
    [-1, -1, 0, 5, 5, 5, 24]
    >>> quick_sort([], lambda *_: None, 0)
    []
    >>> quick_sort([-2, 5, 0, -45], lambda *_: None, 0)
    [-45, -2, 0, 5]
    """
    _quick_sort_3partition(sorting, 0, len(sorting) - 1, cb, delay)
    return sorting


def _quick_sort_3partition(sorting: list, left: int, right: int,
                           cb, delay: float) -> None:
    """
    3-way partition in-place quicksort (Dutch National Flag).

    Divide en tres zonas: menor | igual al pivot | mayor
    y ordena recursivamente menor y mayor.
    """
    if right <= left:
        return

    a = i = left
    b = right
    pivot = sorting[left]

    while i <= b:
        cb(sorting, [i, b], [])
        time.sleep(delay)

        if sorting[i] < pivot:
            sorting[a], sorting[i] = sorting[i], sorting[a]
            cb(sorting, [a, i], [])
            time.sleep(delay)
            a += 1
            i += 1
        elif sorting[i] > pivot:
            sorting[b], sorting[i] = sorting[i], sorting[b]
            cb(sorting, [b, i], [])
            time.sleep(delay)
            b -= 1
        else:
            i += 1

    _quick_sort_3partition(sorting, left,  a - 1, cb, delay)
    _quick_sort_3partition(sorting, b + 1, right, cb, delay)

def heapify(unsorted: list, index: int, heap_size: int,
            cb, delay: float) -> None:
    """
    Mantiene la propiedad de max-heap para el subárbol en `index`.

    :param unsorted:   lista que contiene los enteros
    :param index:      índice raíz del subárbol
    :param heap_size:  tamaño activo del heap
    :param cb:         Visual callback
    :param delay:      Pausa en segundos

    >>> lst = [1, 4, 3, 5, 2]
    >>> heapify(lst, 0, len(lst), lambda *_: None, 0)
    >>> lst
    [4, 5, 3, 1, 2]
    """
    largest     = index
    left_index  = 2 * index + 1
    right_index = 2 * index + 2

    if left_index  < heap_size and unsorted[left_index]  > unsorted[largest]:
        largest = left_index
    if right_index < heap_size and unsorted[right_index] > unsorted[largest]:
        largest = right_index

    if largest != index:
        unsorted[largest], unsorted[index] = unsorted[index], unsorted[largest]
        cb(unsorted, [largest, index], [])
        time.sleep(delay)
        heapify(unsorted, largest, heap_size, cb, delay)


def heap_sort(unsorted: list, cb, delay: float) -> list:
    """
    A pure Python implementation of the heap sort algorithm.

    :param unsorted: a mutable ordered collection of comparable items
    :param cb:       Visual callback(arr, compare_indices, sorted_indices)
    :param delay:    Pausa en segundos entre pasos
    :return: the same collection ordered ascending

    >>> heap_sort([0, 5, 3, 2, 2], lambda *_: None, 0)
    [0, 2, 2, 3, 5]
    >>> heap_sort([], lambda *_: None, 0)
    []
    >>> heap_sort([-2, -5, -45], lambda *_: None, 0)
    [-45, -5, -2]
    >>> heap_sort([3, 7, 9, 28, 123, -5, 8, -30, -200, 0, 4], lambda *_: None, 0)
    [-200, -30, -5, 0, 3, 4, 7, 8, 9, 28, 123]
    """
    n = len(unsorted)
    # Construir max-heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(unsorted, i, n, cb, delay)
    # Extraer elementos del heap de mayor a menor
    for i in range(n - 1, 0, -1):
        unsorted[0], unsorted[i] = unsorted[i], unsorted[0]
        cb(unsorted, [0, i], [])
        time.sleep(delay)
        heapify(unsorted, 0, i, cb, delay)
    return unsorted


def radix_sort(list_of_ints: list, cb, delay: float) -> list:
    """
    MSD Radix Sort usando representación binaria de los enteros.
    Solo funciona con enteros positivos.

    :param list_of_ints: lista de enteros positivos
    :param cb:           Visual callback(arr, compare_indices, sorted_indices)
    :param delay:        Pausa en segundos entre pasos
    :return: lista ordenada
    :raises ValueError:  si algún número es negativo

    >>> radix_sort([40, 12, 1, 100, 4], lambda *_: None, 0)
    [1, 4, 12, 40, 100]
    >>> radix_sort([], lambda *_: None, 0)
    []
    >>> radix_sort([123, 345, 123, 80], lambda *_: None, 0)
    [80, 123, 123, 345]
    """
    if not list_of_ints:
        return []
    if min(list_of_ints) < 0:
        raise ValueError("RadixSort (MSD): todos los números deben ser positivos")

    most_bits = max(len(bin(x)[2:]) for x in list_of_ints)
    result    = _msd_radix_sort(list_of_ints, most_bits)

    # Copiar resultado a la lista original y animar
    for i, v in enumerate(result):
        list_of_ints[i] = v
        cb(list_of_ints, [i], list(range(i)))
        time.sleep(delay)

    return list_of_ints


def _msd_radix_sort(list_of_ints: list[int], bit_position: int) -> list[int]:
    """
    Ordena basándose en el bit en bit_position.
    Números con 0 van al inicio; con 1, al final.
    Divide recursivamente hasta bit_position == 0.

    :param list_of_ints: lista de enteros
    :param bit_position: posición del bit a comparar
    :return: lista parcialmente ordenada

    >>> _msd_radix_sort([45, 2, 32], 1)
    [2, 32, 45]
    >>> _msd_radix_sort([10, 4, 12], 2)
    [4, 12, 10]
    """
    if bit_position == 0 or len(list_of_ints) in [0, 1]:
        return list_of_ints

    zeros = []
    ones  = []

    for number in list_of_ints:
        if (number >> (bit_position - 1)) & 1:
            ones.append(number)   # bit = 1
        else:
            zeros.append(number)  # bit = 0

    # Recursivamente ordenar ambos grupos
    zeros = _msd_radix_sort(zeros, bit_position - 1)
    ones  = _msd_radix_sort(ones,  bit_position - 1)

    # Recombinar: primero los ceros, luego los unos
    res = zeros
    res.extend(ones)
    return res

ALGOS = {
    "ShellSort": shell_sort,
    "QuickSort":  quick_sort,
    "HeapSort":   heap_sort,
    "RadixSort":  radix_sort,
}

ALGO_INFO = {
    "ShellSort": ("O(n log²n)",  "Gaps Ciura:\n701→301→132→57→23→10→4→1"),
    "QuickSort":  ("O(n log n)", "3-way partition\n(Dutch National Flag)"),
    "HeapSort":   ("O(n log n)", "Max-heap puro Python.\nIn-place."),
    "RadixSort":  ("O(n·k)",     "MSD binario.\n⚠ Solo enteros positivos."),
}


C = {
    "bg":       "#0b0e1a",
    "panel":    "#111422",
    "border":   "#1e2640",
    "accent":   "#6d28d9",
    "cyan":     "#06b6d4",
    "yellow":   "#f59e0b",
    "green":    "#10b981",
    "red":      "#ef4444",
    "orange":   "#f97316",
    "text":     "#e2e8f0",
    "sub":      "#64748b",
    "input_bg": "#1e2538",
}

class InputDialog(tk.Toplevel):
    """
    Modal de dos pasos:
      Paso 1 — ¿Cuántos números?
      Paso 2 — Ingresa los valores (juntos o uno por uno)

    Restricción automática para RadixSort: solo enteros positivos.
    Resultado disponible en self.result (None si se canceló).
    """
    def __init__(self, parent, algo_name: str):
        super().__init__(parent)
        self.title("Ingresar números")
        self.configure(bg=C["bg"])
        self.resizable(False, False)
        self.grab_set()

        self.result   = None
        self._algo    = algo_name
        self._step    = 1
        self._count   = 0
        self._values: list[int] = []

        # ── Encabezado ──
        tk.Label(self, text="Ingreso de datos",
                 bg=C["bg"], fg=C["cyan"],
                 font=("Consolas", 14, "bold")).pack(pady=(18, 2))

        nota = "  ⚠  Solo enteros positivos" if algo_name == "RadixSort" else ""
        tk.Label(self, text=f"Algoritmo: {algo_name}{nota}",
                 bg=C["bg"], fg=C["sub"],
                 font=("Consolas", 9)).pack()

        self.inst_lbl = tk.Label(self,
            text="¿Cuántos números deseas ordenar?",
            bg=C["bg"], fg=C["text"],
            font=("Consolas", 10), wraplength=380)
        self.inst_lbl.pack(pady=(8, 2))

        self.prog_lbl = tk.Label(self, text="",
                                 bg=C["bg"], fg=C["sub"],
                                 font=("Consolas", 9), wraplength=380)
        self.prog_lbl.pack()

        # ── Campo de entrada ──
        ef = tk.Frame(self, bg=C["input_bg"],
                      highlightthickness=1,
                      highlightbackground=C["border"])
        ef.pack(padx=30, pady=8, fill="x")
        self.entry = tk.Entry(ef, bg=C["input_bg"], fg=C["text"],
                              insertbackground=C["cyan"],
                              font=("Consolas", 13), relief="flat",
                              justify="center")
        self.entry.pack(padx=10, pady=8, fill="x")
        self.entry.focus_set()
        self.entry.bind("<Return>", lambda _: self._next())

        self.err_lbl = tk.Label(self, text="",
                                bg=C["bg"], fg=C["red"],
                                font=("Consolas", 9))
        self.err_lbl.pack()

        # ── Botones ──
        row = tk.Frame(self, bg=C["bg"])
        row.pack(pady=(4, 18))
        for txt, cmd, col in [("Aceptar",  self._next,   C["accent"]),
                               ("Cancelar", self.destroy, C["red"])]:
            tk.Button(row, text=txt, command=cmd,
                      bg=col, fg="white", relief="flat",
                      font=("Consolas", 10, "bold"),
                      activebackground=col, activeforeground="white",
                      padx=20, pady=6, cursor="hand2").pack(side=tk.LEFT, padx=8)

        self._center(parent)

    def _center(self, parent):
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width()  // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{pw - w//2}+{ph - h//2}")

    def _next(self):
        raw = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        self.err_lbl.config(text="")

        # ── Paso 1: cantidad ──
        if self._step == 1:
            try:
                n = int(raw)
                if n < 1:
                    raise ValueError
            except ValueError:
                self.err_lbl.config(text="⚠  Ingresa un entero positivo.")
                return
            self._count = n
            self._step  = 2
            tipo = "enteros positivos" if self._algo == "RadixSort" else "enteros"
            self.inst_lbl.config(
                text=f"Ingresa {n} {tipo}.\n"
                     "Todos juntos separados por espacios o comas,\n"
                     "o uno por uno presionando Enter.")
            self._upd_prog()
            return

        # ── Paso 2: valores ──
        tokens = [t for t in raw.replace(",", " ").split() if t]
        if not tokens:
            self.err_lbl.config(text="⚠  Escribe al menos un número.")
            return

        nums: list[int] = []
        for t in tokens:
            try:
                v = int(t)
                if self._algo == "RadixSort" and v < 1:
                    raise ValueError("positivo")
            except ValueError:
                msg = (f"⚠  '{t}' no es válido. RadixSort solo acepta enteros positivos."
                       if self._algo == "RadixSort"
                       else f"⚠  '{t}' no es un entero válido.")
                self.err_lbl.config(text=msg)
                return
            nums.append(v)

        needed = self._count - len(self._values)
        if len(nums) > needed:
            self.err_lbl.config(
                text=f"⚠  Solo faltan {needed} número(s), ingresaste {len(nums)}.")
            return

        self._values.extend(nums)
        self._upd_prog()

        if len(self._values) == self._count:
            self.result = self._values[:]
            self.destroy()

    def _upd_prog(self):
        rem = self._count - len(self._values)
        if rem > 0:
            ent = ", ".join(map(str, self._values)) if self._values else "—"
            self.prog_lbl.config(
                text=f"Ingresados: {ent}\n"
                     f"Faltan: {rem}  ({len(self._values)}/{self._count})")
        else:
            self.prog_lbl.config(text="")


class SortingApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sorting Visualizer — Algoritmos de Ordenamiento")
        self.root.configure(bg=C["bg"])
        self.root.minsize(960, 640)
        self.root.resizable(True, True)

        self.arr       = []
        self.running   = False
        self.algo_var  = tk.StringVar(value="ShellSort")
        self.speed_var = tk.DoubleVar(value=0.06)

        self._build_ui()

    def _build_ui(self):
        side = tk.Frame(self.root, bg=C["panel"], width=250,
                        highlightthickness=1,
                        highlightbackground=C["border"])
        side.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=10)
        side.pack_propagate(False)

        # Logo
        tk.Label(side, text="SORT\nVISUALIZER",
                 bg=C["panel"], fg=C["cyan"],
                 font=("Courier New", 15, "bold"),
                 justify="center").pack(pady=(16, 2))
        tk.Frame(side, bg=C["accent"], height=2).pack(fill="x", padx=20, pady=(0, 8))

        self._sec(side, "⬡  ALGORITMO")
        for algo in ALGOS:
            tk.Radiobutton(
                side, text=algo,
                variable=self.algo_var, value=algo,
                bg=C["panel"], fg=C["text"],
                selectcolor=C["accent"],
                activebackground=C["panel"],
                activeforeground=C["cyan"],
                font=("Consolas", 11), bd=0, cursor="hand2",
                indicatoron=True, padx=14, pady=5,
                command=self._update_info,
            ).pack(anchor="w", fill="x", padx=8)

        # Velocidad
        self._sec(side, "⚙  VELOCIDAD")
        tk.Label(side, text="Rápido ◄──────────► Lento",
                 bg=C["panel"], fg=C["sub"],
                 font=("Consolas", 7)).pack(padx=14)
        ttk.Scale(side, from_=0.001, to=0.25,
                  variable=self.speed_var,
                  orient="horizontal").pack(fill="x", padx=14, pady=4)

        
        self._sec(side, "▶  ACCIONES")
        self._btn(side, "📋  Ingresar números", self._open_input, C["cyan"])
        self._btn(side, "▶  Ordenar",           self._start_sort, C["accent"])
        self._btn(side, "■  Detener",            self._stop_sort,  C["orange"])
        self._btn(side, "🗑  Limpiar",            self._clear,      C["sub"])
        self._btn(side, "✕  Salir",              self._exit,       C["red"])

        # Info
        self._sec(side, "ℹ  INFO")
        self.info_lbl = tk.Label(side, text="",
                                 bg=C["panel"], fg=C["sub"],
                                 font=("Consolas", 9),
                                 justify="left", wraplength=220)
        self.info_lbl.pack(anchor="w", padx=14, pady=4)
        self._update_info()

        st = ttk.Style()
        st.theme_use("clam")
        st.configure("Horizontal.TScale",
                     background=C["panel"],
                     troughcolor=C["border"],
                     sliderthickness=14)

        right = tk.Frame(self.root, bg=C["bg"])
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        top = tk.Frame(right, bg=C["bg"])
        top.pack(fill="x")

        self.title_lbl = tk.Label(top, text="— Sin datos —",
                                  bg=C["bg"], fg=C["text"],
                                  font=("Courier New", 20, "bold"))
        self.title_lbl.pack(side=tk.LEFT)

        self.status_lbl = tk.Label(top,
                                   text="Usa 'Ingresar números' para comenzar",
                                   bg=C["bg"], fg=C["sub"],
                                   font=("Consolas", 10))
        self.status_lbl.pack(side=tk.RIGHT, padx=4)

        self.arr_lbl = tk.Label(right, text="",
                                bg=C["bg"], fg=C["sub"],
                                font=("Consolas", 9),
                                wraplength=720, justify="left")
        self.arr_lbl.pack(anchor="w", pady=(2, 0))

        self.canvas = tk.Canvas(right, bg=C["bg"], bd=0,
                                highlightthickness=1,
                                highlightbackground=C["border"])
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=(4, 0))
        self.canvas.bind("<Configure>", lambda _: self._draw(self.arr, [], []))

    def _sec(self, parent, label: str):
        tk.Label(parent, text=label,
                 bg=C["panel"], fg=C["accent"],
                 font=("Consolas", 9, "bold")).pack(anchor="w", padx=14, pady=(12, 2))
        tk.Frame(parent, bg=C["border"], height=1).pack(fill="x", padx=10)

    def _btn(self, parent, text: str, cmd, col: str):
        tk.Button(parent, text=text, command=cmd,
                  bg=col, fg="white", relief="flat",
                  font=("Consolas", 10, "bold"), cursor="hand2",
                  activebackground=col, activeforeground="white",
                  padx=8, pady=7, anchor="w").pack(fill="x", padx=12, pady=3)

    def _update_info(self):
        comp, desc = ALGO_INFO.get(self.algo_var.get(), ("", ""))
        self.info_lbl.config(text=f"Complejidad: {comp}\n{desc}")

    def _open_input(self):
        if self.running:
            return
        dlg = InputDialog(self.root, self.algo_var.get())
        self.root.wait_window(dlg)
        if dlg.result:
            self.arr = dlg.result
            self._refresh("Listo para ordenar", C["cyan"])

    def _draw(self, arr: list, cmp: list, srt: list):
        self.canvas.delete("all")
        cw = self.canvas.winfo_width()  or 700
        ch = self.canvas.winfo_height() or 460

        if not arr:
            self.canvas.create_text(
                cw // 2, ch // 2,
                text="Sin datos  —  usa  'Ingresar números'",
                fill=C["sub"], font=("Consolas", 12))
            return

        pad   = 12
        n     = len(arr)
        bar_w = max(2, (cw - 2 * pad) / n)
        mx    = max(arr) or 1
        gap   = max(0.5, bar_w * 0.1)

        for i, v in enumerate(arr):
            x0 = pad + i * bar_w + gap / 2
            x1 = pad + (i + 1) * bar_w - gap / 2
            bh = (v / mx) * (ch - 2 * pad - 22)
            y0 = ch - pad - bh
            y1 = ch - pad

            if i in srt:
                col = C["green"]
            elif i in cmp:
                col = C["yellow"]
            else:
                ratio = v / mx
                r = int(0x1e + ratio * (0x6d - 0x1e))
                g = int(0x26 + ratio * (0x28 - 0x26))
                b = int(0x40 + ratio * (0xd9 - 0x40))
                col = f"#{r:02x}{g:02x}{b:02x}"

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=col, outline="")

            # Mostrar valor numérico si hay suficiente espacio
            if bar_w >= 22:
                self.canvas.create_text(
                    (x0 + x1) / 2, y0 - 7,
                    text=str(v), fill=C["sub"],
                    font=("Consolas", 7))

        self.canvas.update_idletasks()

    def _refresh(self, msg: str, col: str):
        self.title_lbl.config(text=self.algo_var.get())
        self.status_lbl.config(text=msg, fg=col)
        prev = self.arr if len(self.arr) <= 60 else self.arr[:60]
        dots = "  …" if len(self.arr) > 60 else ""
        self.arr_lbl.config(
            text=f"Arreglo ({len(self.arr)} elem): "
                 + "  ".join(map(str, prev)) + dots)
        self._draw(self.arr, [], [])

    def _start_sort(self):
        if self.running:
            return
        if not self.arr:
            messagebox.showwarning(
                "Sin datos",
                "Primero ingresa números con\n'Ingresar números'.",
                parent=self.root)
            return
        self.running = True
        self.title_lbl.config(text=self.algo_var.get())
        self.status_lbl.config(text="Ordenando…", fg=C["yellow"])
        self._update_info()
        threading.Thread(target=self._run_sort, daemon=True).start()

    def _run_sort(self):
        arr   = self.arr[:]
        algo  = self.algo_var.get()
        delay = self.speed_var.get()
        fn    = ALGOS[algo]
        try:
            fn(arr, self._draw, delay)
            self.arr = arr
            self._draw(arr, [], list(range(len(arr))))
            prev = arr if len(arr) <= 60 else arr[:60]
            dots = "  …" if len(arr) > 60 else ""
            self.arr_lbl.config(
                text=f"Ordenado ({len(arr)} elem): "
                     + "  ".join(map(str, prev)) + dots)
            self.status_lbl.config(text="¡Ordenado! ✓", fg=C["green"])
        except ValueError as e:
            messagebox.showerror("Error de datos", str(e), parent=self.root)
            self.status_lbl.config(text="Error en los datos", fg=C["red"])
        except Exception:
            pass
        finally:
            self.running = False

    def _stop_sort(self):
        self.running = False
        self.status_lbl.config(text="Detenido", fg=C["orange"])

    def _clear(self):
        if self.running:
            return
        self.arr = []
        self.arr_lbl.config(text="")
        self.title_lbl.config(text="— Sin datos —")
        self.status_lbl.config(
            text="Usa 'Ingresar números' para comenzar", fg=C["sub"])
        self._draw([], [], [])

    def _exit(self):
        if messagebox.askyesno(
                "Salir", "¿Deseas cerrar el programa?", parent=self.root):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    SortingApp(root)
    root.mainloop()

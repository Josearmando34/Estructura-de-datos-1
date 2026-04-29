import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading

# ══════════════════════════════════════════════════════
#  ALGORITMOS DE ORDENAMIENTO
# ══════════════════════════════════════════════════════

def shell_sort(arr, cb, delay):
    n = len(arr); gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]; j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                cb(arr, [j, j - gap], []); time.sleep(delay)
                j -= gap
            arr[j] = temp
            cb(arr, [], [j]); time.sleep(delay)
        gap //= 2


def quick_sort(arr, cb, delay):
    def partition(lo, hi):
        pivot = arr[hi]; i = lo - 1
        for j in range(lo, hi):
            cb(arr, [j, hi], []); time.sleep(delay)
            if arr[j] <= pivot:
                i += 1; arr[i], arr[j] = arr[j], arr[i]
                cb(arr, [i, j], []); time.sleep(delay)
        arr[i+1], arr[hi] = arr[hi], arr[i+1]
        cb(arr, [], [i+1]); time.sleep(delay)
        return i + 1
    def _q(lo, hi):
        if lo < hi:
            p = partition(lo, hi); _q(lo, p-1); _q(p+1, hi)
    _q(0, len(arr) - 1)


def heap_sort(arr, cb, delay):
    n = len(arr)
    def heapify(size, i):
        lg = i; l = 2*i+1; r = 2*i+2
        if l < size and arr[l] > arr[lg]: lg = l
        if r < size and arr[r] > arr[lg]: lg = r
        if lg != i:
            arr[i], arr[lg] = arr[lg], arr[i]
            cb(arr, [i, lg], []); time.sleep(delay)
            heapify(size, lg)
    for i in range(n//2 - 1, -1, -1): heapify(n, i)
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        cb(arr, [0, i], []); time.sleep(delay)
        heapify(i, 0)


def radix_sort(arr, cb, delay):
    def counting(exp):
        n = len(arr); out = [0]*n; cnt = [0]*10
        for x in arr: cnt[(x//exp)%10] += 1
        for i in range(1, 10): cnt[i] += cnt[i-1]
        for i in range(n-1, -1, -1):
            idx = (arr[i]//exp)%10; out[cnt[idx]-1] = arr[i]; cnt[idx] -= 1
        for i in range(n):
            arr[i] = out[i]; cb(arr, [i], []); time.sleep(delay)
    mx = max(arr); exp = 1
    while mx // exp > 0: counting(exp); exp *= 10

C = {
    "bg":"#0b0e1a","panel":"#686864","card":"#09c25ca9","border":"#465483",
    "accent":"#6d28d9","cyan":"#06b6d4","yellow":"#b1ee08","green":"#10b981",
    "red":"#44ef86","text":"#e2e8f0","sub":"#64748b","input_bg":"#15295f",
}

ALGO_INFO = {
    "ShellSort":("O(n log²n)",  "Mejora InsertionSort\ncon gaps decrecientes."),
    "QuickSort": ("O(n log n)", "Divide y conquista\ncon pivote."),
    "HeapSort":  ("O(n log n)", "Usa un montículo\n(heap) máximo."),
    "RadixSort": ("O(n·k)",     "Ordena dígito a dígito\nsin comparaciones."),
}
ALGOS = {"ShellSort":shell_sort,"QuickSort":quick_sort,"HeapSort":heap_sort,"RadixSort":radix_sort}

class InputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ingresar números")
        self.configure(bg=C["bg"])
        self.resizable(False, False)
        self.grab_set()
        self.result = None
        self._step = 1
        self._count = 0
        self._values = []

        tk.Label(self, text="Ingreso de datos", bg=C["bg"], fg=C["cyan"],
                 font=("Consolas",14,"bold")).pack(pady=(18,2))

        self.inst_lbl = tk.Label(self,
            text="¿Cuántos números deseas ordenar?",
            bg=C["bg"], fg=C["text"], font=("Consolas",10), wraplength=340)
        self.inst_lbl.pack(pady=(6,2))

        self.prog_lbl = tk.Label(self, text="", bg=C["bg"], fg=C["sub"],
                                 font=("Consolas",9), wraplength=340)
        self.prog_lbl.pack()

        ef = tk.Frame(self, bg=C["input_bg"],
                      highlightthickness=1, highlightbackground=C["border"])
        ef.pack(padx=30, pady=8, fill="x")
        self.entry = tk.Entry(ef, bg=C["input_bg"], fg=C["text"],
                              insertbackground=C["cyan"],
                              font=("Consolas",13), relief="flat", justify="center")
        self.entry.pack(padx=10, pady=8, fill="x")
        self.entry.focus_set()
        self.entry.bind("<Return>", lambda _: self._next())

        self.err_lbl = tk.Label(self, text="", bg=C["bg"], fg=C["red"],
                                font=("Consolas",9))
        self.err_lbl.pack()

        btn_row = tk.Frame(self, bg=C["bg"])
        btn_row.pack(pady=(4,18))
        for txt, cmd, col in [("Aceptar",self._next,C["accent"]),("Cancelar",self.destroy,C["red"])]:
            tk.Button(btn_row, text=txt, command=cmd, bg=col, fg="white",
                      relief="flat", font=("Consolas",10,"bold"),
                      activebackground=col, activeforeground="white",
                      padx=20, pady=6, cursor="hand2").pack(side=tk.LEFT, padx=8)

        self._center(parent)

    def _center(self, parent):
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width()//2
        ph = parent.winfo_rooty() + parent.winfo_height()//2
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{pw-w//2}+{ph-h//2}")

    def _next(self):
        raw = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        self.err_lbl.config(text="")

        if self._step == 1:
            try:
                n = int(raw)
                if n < 1: raise ValueError
            except ValueError:
                self.err_lbl.config(text="⚠  Ingresa un entero positivo."); return
            self._count = n; self._step = 2
            self.inst_lbl.config(
                text=f"Ingresa {n} número(s) enteros positivos.\n"
                     f"Puedes escribirlos todos separados\n"
                     f"por espacios o comas, o uno por uno.")
            self._upd_prog()
        else:
            tokens = [t for t in raw.replace(","," ").split() if t]
            if not tokens:
                self.err_lbl.config(text="⚠  Escribe al menos un número."); return
            nums = []
            for t in tokens:
                try:
                    v = int(t)
                    if v < 1: raise ValueError
                    nums.append(v)
                except ValueError:
                    self.err_lbl.config(text=f"⚠  '{t}' no es un entero positivo válido."); return
            needed = self._count - len(self._values)
            if len(nums) > needed:
                self.err_lbl.config(text=f"⚠  Solo faltan {needed}, ingresaste {len(nums)}."); return
            self._values.extend(nums)
            self._upd_prog()
            if len(self._values) == self._count:
                self.result = self._values[:]; self.destroy()

    def _upd_prog(self):
        rem = self._count - len(self._values)
        if rem > 0:
            ent = ", ".join(map(str,self._values)) if self._values else "—"
            self.prog_lbl.config(
                text=f"Ingresados: {ent}\nFaltan: {rem}  ({len(self._values)}/{self._count})")
        else:
            self.prog_lbl.config(text="")

class SortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer — Algoritmos de Ordenamiento")
        self.root.configure(bg=C["bg"])
        self.root.minsize(960, 640)
        self.root.resizable(True, True)
        self.arr = []; self.running = False
        self.algo_var  = tk.StringVar(value="ShellSort")
        self.speed_var = tk.DoubleVar(value=0.06)
        self._build_ui()

    def _build_ui(self):

        side = tk.Frame(self.root, bg=C["panel"], width=245,
                        highlightthickness=1, highlightbackground=C["border"])
        side.pack(side=tk.LEFT, fill=tk.Y, padx=(10,0), pady=10)
        side.pack_propagate(False)

        tk.Label(side, text="SORT\nVISUALIZER", bg=C["panel"], fg=C["cyan"],
                 font=("Courier New",15,"bold"), justify="center").pack(pady=(16,2))
        tk.Frame(side, bg=C["accent"], height=2).pack(fill="x", padx=20, pady=(0,8))

        self._sec(side, "⬡  ALGORITMO")
        for algo in ALGOS:
            tk.Radiobutton(side, text=algo, variable=self.algo_var, value=algo,
                bg=C["panel"], fg=C["text"], selectcolor=C["accent"],
                activebackground=C["panel"], activeforeground=C["cyan"],
                font=("Consolas",11), bd=0, cursor="hand2",
                indicatoron=True, padx=14, pady=5,
                command=self._update_info).pack(anchor="w", fill="x", padx=8)

        self._sec(side, "⚙  VELOCIDAD")
        tk.Label(side, text="Rápido ◄──────────► Lento",
                 bg=C["panel"], fg=C["sub"], font=("Consolas",7)).pack(padx=14)
        ttk.Scale(side, from_=0.001, to=0.25, variable=self.speed_var,
                  orient="horizontal").pack(fill="x", padx=14, pady=4)

        self._sec(side, "▶  ACCIONES")
        self._btn(side, "📋  Ingresar números", self._open_input, C["cyan"])
        self._btn(side, "▶  Ordenar",           self._start_sort, C["accent"])
        self._btn(side, "■  Detener",            self._stop_sort,  "#f97316")
        self._btn(side, "🗑  Limpiar",            self._clear,      C["sub"])
        self._btn(side, "✕  Salir",              self._exit,       C["red"])

        self._sec(side, "ℹ  INFO")
        self.info_lbl = tk.Label(side, text="", bg=C["panel"], fg=C["sub"],
                                 font=("Consolas",9), justify="left", wraplength=215)
        self.info_lbl.pack(anchor="w", padx=14, pady=4)
        self._update_info()

        st = ttk.Style(); st.theme_use("clam")
        st.configure("Horizontal.TScale", background=C["panel"],
                     troughcolor=C["border"], sliderthickness=14)

        right = tk.Frame(self.root, bg=C["bg"])
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        top = tk.Frame(right, bg=C["bg"]); top.pack(fill="x")
        self.title_lbl = tk.Label(top, text="— Sin datos —",
                                  bg=C["bg"], fg=C["text"],
                                  font=("Courier New",20,"bold"))
        self.title_lbl.pack(side=tk.LEFT)
        self.status_lbl = tk.Label(top,
                                   text="Usa 'Ingresar números' para comenzar",
                                   bg=C["bg"], fg=C["sub"], font=("Consolas",10))
        self.status_lbl.pack(side=tk.RIGHT, padx=4)

        self.arr_lbl = tk.Label(right, text="", bg=C["bg"], fg=C["sub"],
                                font=("Consolas",9), wraplength=720, justify="left")
        self.arr_lbl.pack(anchor="w", pady=(2,0))

        self.canvas = tk.Canvas(right, bg=C["bg"], bd=0,
                                highlightthickness=1, highlightbackground=C["border"])
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=(4,0))
        self.canvas.bind("<Configure>", lambda _: self._draw(self.arr,[],[]))

    def _sec(self, p, label):
        tk.Label(p, text=label, bg=C["panel"], fg=C["accent"],
                 font=("Consolas",9,"bold")).pack(anchor="w", padx=14, pady=(12,2))
        tk.Frame(p, bg=C["border"], height=1).pack(fill="x", padx=10)

    def _btn(self, p, text, cmd, col):
        tk.Button(p, text=text, command=cmd, bg=col, fg="white", relief="flat",
                  font=("Consolas",10,"bold"), cursor="hand2",
                  activebackground=col, activeforeground="white",
                  padx=8, pady=7, anchor="w").pack(fill="x", padx=12, pady=3)

    def _update_info(self):
        comp, desc = ALGO_INFO.get(self.algo_var.get(), ("",""))
        self.info_lbl.config(text=f"Complejidad: {comp}\n{desc}")

    def _open_input(self):
        if self.running: return
        dlg = InputDialog(self.root)
        self.root.wait_window(dlg)
        if dlg.result:
            self.arr = dlg.result
            self._refresh("Listo para ordenar", C["cyan"])

    def _draw(self, arr, cmp, srt):
        self.canvas.delete("all")
        cw = self.canvas.winfo_width()  or 700
        ch = self.canvas.winfo_height() or 460
        if not arr:
            self.canvas.create_text(cw//2, ch//2,
                text="Sin datos  —  usa  'Ingresar números'",
                fill=C["sub"], font=("Consolas",12)); return
        pad=12; n=len(arr); bar_w=max(2,(cw-2*pad)/n)
        mx=max(arr) or 1; gap=max(0.5, bar_w*0.1)
        for i,v in enumerate(arr):
            x0=pad+i*bar_w+gap/2; x1=pad+(i+1)*bar_w-gap/2
            bh=(v/mx)*(ch-2*pad-22); y0=ch-pad-bh; y1=ch-pad
            if i in srt: col=C["green"]
            elif i in cmp: col=C["yellow"]
            else:
                ratio=v/mx
                r=int(0x1e+ratio*(0x6d-0x1e))
                g=int(0x26+ratio*(0x28-0x26))
                b=int(0x40+ratio*(0xd9-0x40))
                col=f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_rectangle(x0,y0,x1,y1,fill=col,outline="")
            if bar_w >= 22:
                self.canvas.create_text((x0+x1)/2, y0-7, text=str(v),
                    fill=C["sub"], font=("Consolas",7))
        self.canvas.update_idletasks()

    def _refresh(self, msg, col):
        self.title_lbl.config(text=self.algo_var.get())
        self.status_lbl.config(text=msg, fg=col)
        prev = self.arr if len(self.arr)<=60 else self.arr[:60]
        dots = "  …" if len(self.arr)>60 else ""
        self.arr_lbl.config(
            text=f"Arreglo ({len(self.arr)} elem): "+"  ".join(map(str,prev))+dots)
        self._draw(self.arr,[],[])

    def _start_sort(self):
        if self.running: return
        if not self.arr:
            messagebox.showwarning("Sin datos",
                "Primero ingresa números con\n'Ingresar números'.", parent=self.root); return
        self.running = True
        self.title_lbl.config(text=self.algo_var.get())
        self.status_lbl.config(text="Ordenando…", fg=C["yellow"])
        self._update_info()
        threading.Thread(target=self._run_sort, daemon=True).start()

    def _run_sort(self):
        arr=self.arr[:]; algo=self.algo_var.get()
        delay=self.speed_var.get(); fn=ALGOS[algo]
        try:
            fn(arr, self._draw, delay)
            self.arr=arr
            self._draw(arr,[],list(range(len(arr))))
            prev=arr if len(arr)<=60 else arr[:60]
            dots="  …" if len(arr)>60 else ""
            self.arr_lbl.config(
                text=f"Ordenado ({len(arr)} elem): "+"  ".join(map(str,prev))+dots)
            self.status_lbl.config(text="¡Ordenado! ✓", fg=C["green"])
        except Exception: pass
        finally: self.running=False

    def _stop_sort(self):
        self.running=False
        self.status_lbl.config(text="Detenido", fg="#f97316")

    def _clear(self):
        if self.running: return
        self.arr=[]
        self.arr_lbl.config(text="")
        self.title_lbl.config(text="— Sin datos —")
        self.status_lbl.config(text="Usa 'Ingresar números' para comenzar", fg=C["sub"])
        self._draw([],[],[])

    def _exit(self):
        if messagebox.askyesno("Salir","¿Deseas cerrar el programa?",parent=self.root):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    SortingApp(root)
    root.mainloop()
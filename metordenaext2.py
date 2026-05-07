import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import random
import os
import pandas as pd

# --- CONFIGURACIÓN DE ESTILO ---
BG, BG2, BG3 = "#0F1117", "#1A1D2E", "#252840"
ACCENT, ACCENT2 = "#6C63FF", "#FF6584"
GREEN, YELLOW, CYAN = "#43E97B", "#FFD166", "#38BDF8"
TEXT, TEXT2 = "#E8E8F0", "#8888AA"
FONT_TIT = ("Consolas", 18, "bold")
FONT_BTN = ("Consolas", 11, "bold")
FONT_SM = ("Consolas", 9)

# ─────────────────────────────────────────────────────────
#  LÓGICA DE ALGORITMOS
# ─────────────────────────────────────────────────────────

def intercalacion_pasos(a, b):
    pasos, resultado = [], []
    i = j = 0
    a_sort, b_sort = sorted(a), sorted(b)
    while i < len(a_sort) and j < len(b_sort):
        pasos.append(("cmp", list(resultado), i, j))
        if a_sort[i] <= b_sort[j]:
            resultado.append(a_sort[i]); i += 1
        else:
            resultado.append(b_sort[j]); j += 1
        pasos.append(("add", list(resultado), i, j))
    while i < len(a_sort):
        resultado.append(a_sort[i]); i += 1
        pasos.append(("add", list(resultado), i, j))
    while j < len(b_sort):
        resultado.append(b_sort[j]); j += 1
        pasos.append(("add", list(resultado), i, j))
    return resultado, pasos

def mezcla_directa_pasos(lista):
    pasos = []
    def merge_sort(a):
        if len(a) <= 1: return a
        m = len(a) // 2
        L, R = merge_sort(a[:m]), merge_sort(a[m:])
        return merge(L, R)
    def merge(L, R):
        res, i, j = [], 0, 0
        while i < len(L) and j < len(R):
            if L[i] <= R[j]: res.append(L[i]); i += 1
            else: res.append(R[j]); j += 1
            pasos.append(list(res) + L[i:] + R[j:])
        res += L[i:] + R[j:]
        pasos.append(list(res))
        return res
    resultado = merge_sort(list(lista))
    return resultado, pasos

def mezcla_equilibrada_pasos(lista, k=3):
    pasos = []
    sublistas = [[] for _ in range(k)]
    for idx, el in enumerate(lista): sublistas[idx % k].append(el)
    sublistas = [sorted(s) for s in sublistas if s]
    pasos.append(("split", [item for s in sublistas for item in s]))
    def merge2(a, b):
        res, i, j = [], 0, 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]: res.append(a[i]); i += 1
            else: res.append(b[j]); j += 1
        return res + a[i:] + b[j:]
    while len(sublistas) > 1:
        nueva = []
        for i in range(0, len(sublistas), 2):
            if i + 1 < len(sublistas): nueva.append(merge2(sublistas[i], sublistas[i+1]))
            else: nueva.append(sublistas[i])
        sublistas = nueva
        pasos.append(("merge", sublistas[0] if len(sublistas) == 1 else [x for s in sublistas for x in s]))
    return sublistas[0], pasos

# ─────────────────────────────────────────────────────────
#  APLICACIÓN PRINCIPAL
# ─────────────────────────────────────────────────────────

class OrdenamientoApp:
    EJERCICIOS = {
        "intercalacion": [{"titulo": "Pares e Impares", "a": [1, 3, 5], "b": [2, 4, 6]}, {"titulo": "Diferente Tamaño", "a": [10, 20], "b": [5, 15, 25]}, {"titulo": "Nombres", "a": ["Ana", "Luis"], "b": ["Beto", "Zoe"]}],
        "directa": [{"titulo": "Desordenados", "datos": [38, 27, 43, 3, 9]}, {"titulo": "Calificaciones", "datos": [85, 42, 91]}, {"titulo": "Temperaturas", "datos": [36.5, 37.2, 35.8]}],
        "equilibrada": [{"titulo": "Vías k=3", "datos": [15, 3, 22, 8, 47], "k": 3}, {"titulo": "Edades k=4", "datos": [20, 35, 18, 42], "k": 4}, {"titulo": "Precios k=2", "datos": [199, 45, 320], "k": 2}],
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Ordenamiento + Excel Pro")
        self.root.configure(bg=BG)
        self.root.geometry("1000x750")
        self.animando = False
        self._delay = 0.35
        self._build_ui()
        self._sel_metodo("intercalacion")

    def _build_ui(self):
        hdr = tk.Frame(self.root, bg=BG, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="⬡ ORDENAMIENTO MULTI-ARCHIVO", font=FONT_TIT, fg=ACCENT, bg=BG).pack()
        
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=15, pady=10)

        side = tk.Frame(body, bg=BG2, width=250, highlightbackground=BG3, highlightthickness=1)
        side.pack(side="left", fill="y", padx=(0, 10))
        side.pack_propagate(False)

        tk.Label(side, text="ALGORITMO", font=FONT_SM, fg=TEXT2, bg=BG2, pady=5).pack()
        self.btn_metodos = {}
        for label, key in [("Intercalación", "intercalacion"), ("Mezcla Directa", "directa"), ("Mezcla Equilibrada", "equilibrada")]:
            btn = tk.Button(side, text=label, font=FONT_SM, bg=BG2, fg=TEXT, bd=0, pady=8, cursor="hand2", command=lambda k=key: self._sel_metodo(k))
            btn.pack(fill="x", padx=10, pady=2)
            self.btn_metodos[key] = btn

        tk.Frame(side, bg=BG3, height=1).pack(fill="x", padx=10, pady=10)
        
        tk.Label(side, text="DATOS EXTERNOS", font=FONT_SM, fg=TEXT2, bg=BG2).pack()
        self.btn_file = tk.Button(side, text="📁 CARGAR TXT/EXCEL", font=FONT_BTN, bg=BG3, fg=CYAN, bd=0, pady=12, cursor="hand2", command=self._cargar_archivo)
        self.btn_file.pack(fill="x", padx=10, pady=5)

        tk.Frame(side, bg=BG3, height=1).pack(fill="x", padx=10, pady=10)

        tk.Label(side, text="VELOCIDAD", font=FONT_SM, fg=TEXT2, bg=BG2).pack()
        self.vel_slider = tk.Scale(side, from_=0.01, to=1.0, resolution=0.05, orient="horizontal", bg=BG2, fg=TEXT, troughcolor=BG3, bd=0, highlightthickness=0)
        self.vel_slider.set(0.35)
        self.vel_slider.pack(fill="x", padx=10)

        self.btn_run = tk.Button(side, text="▶ INICIAR", font=FONT_BTN, bg=ACCENT, fg="white", bd=0, pady=15, cursor="hand2", command=self._ejecutar)
        self.btn_run.pack(fill="x", padx=10, pady=20)

        main = tk.Frame(body, bg=BG)
        main.pack(side="left", fill="both", expand=True)
        
        self.lbl_titulo = tk.Label(main, text="", font=("Consolas", 12, "bold"), fg=YELLOW, bg=BG, anchor="w")
        self.lbl_titulo.pack(fill="x")

        self.canvas = tk.Canvas(main, bg=BG2, height=320, highlightthickness=1, highlightbackground=BG3)
        self.canvas.pack(fill="x", pady=5)

        self.log = tk.Text(main, bg=BG2, fg=TEXT, font=("Consolas", 10), bd=0, padx=10, pady=10)
        self.log.pack(fill="both", expand=True)

    def _pedir_hoja(self, opciones):
        ventana_hojas = tk.Toplevel(self.root)
        ventana_hojas.title("Seleccionar Hoja")
        ventana_hojas.geometry("300x400")
        ventana_hojas.configure(bg=BG2)
        ventana_hojas.transient(self.root)
        ventana_hojas.grab_set()
        
        seleccion = tk.StringVar()
        tk.Label(ventana_hojas, text="HOJAS ENCONTRADAS", font=FONT_BTN, fg=CYAN, bg=BG2, pady=10).pack()

        frame_btns = tk.Frame(ventana_hojas, bg=BG2)
        frame_btns.pack(fill="both", expand=True, padx=20)

        def elegir(nombre):
            seleccion.set(nombre)
            ventana_hojas.destroy()

        for nombre in opciones:
            btn = tk.Button(frame_btns, text=f"📄 {nombre}", font=FONT_SM, bg=BG3, fg=TEXT, 
                            pady=8, bd=0, cursor="hand2", command=lambda n=nombre: elegir(n))
            btn.pack(fill="x", pady=3)

        self.root.wait_window(ventana_hojas)
        return seleccion.get()

    def _cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de datos", "*.txt *.xlsx *.xls")])
        if not ruta: return
        
        try:
            datos_listas = []
            ext = os.path.splitext(ruta)[1].lower()

            if ext in ['.xlsx', '.xls']:
                xls = pd.ExcelFile(ruta)
                hojas = xls.sheet_names
                
                # Si hay más de una hoja, preguntamos
                if len(hojas) > 1:
                    hoja_sel = self._pedir_hoja(hojas)
                    if not hoja_sel: return
                else:
                    hoja_sel = hojas[0]

                df = pd.read_excel(xls, sheet_name=hoja_sel, header=None)
                for _, fila in df.iterrows():
                    vals = pd.to_numeric(fila, errors='coerce').dropna().tolist()
                    if vals: datos_listas.append(vals)
            else:
                with open(ruta, 'r', encoding='utf-8') as f:
                    for linea in f:
                        numeros = [float(x) if '.' in x else int(x) for x in linea.replace(',', ' ').split() if x.replace('.','',1).isdigit()]
                        if numeros: datos_listas.append(numeros)

            if not datos_listas: raise ValueError("No se encontraron números válidos.")

            m = self.metodo_actual
            if m == "intercalacion":
                if len(datos_listas) < 2:
                    messagebox.showwarning("Aviso", "Requiere 2 filas en la hoja.")
                    return
                nuevo = {"titulo": f"Ext: {os.path.basename(ruta)}", "a": datos_listas[0], "b": datos_listas[1]}
            else:
                aplanados = [item for sub in datos_listas for item in sub]
                nuevo = {"titulo": f"Ext: {os.path.basename(ruta)}", "datos": aplanados, "k": 3}
            
            self.EJERCICIOS[m][0] = nuevo
            self._sel_ejercicio(0)
            messagebox.showinfo("Éxito", "Datos cargados correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar: {e}")

    def _sel_metodo(self, metodo):
        self.metodo_actual = metodo
        for k, b in self.btn_metodos.items():
            b.configure(bg=BG3 if k == metodo else BG2, fg=ACCENT if k == metodo else TEXT)
        self._sel_ejercicio(0)

    def _sel_ejercicio(self, idx):
        self.ejercicio_actual = idx
        ej = self.EJERCICIOS[self.metodo_actual][idx]
        self.lbl_titulo.config(text=f"MODO: {self.metodo_actual.upper()} | {ej['titulo']}")
        datos = (ej['a'] + ej['b']) if self.metodo_actual == "intercalacion" else ej['datos']
        self._dibujar(datos)

    def _dibujar(self, valores, activos=[], listos=[]):
        self.canvas.delete("all")
        if not valores: return
        W, H = 700, 320
        n = len(valores)
        ancho = (W - 60) // n
        max_val = max(valores) if valores else 1
        
        for i, v in enumerate(valores):
            h = (v / max_val) * 240 if max_val > 0 else 100
            x1, y1 = 30 + i * ancho, H - 30 - h
            x2, y2 = x1 + ancho - 4, H - 30
            color = GREEN if i in listos else (YELLOW if i in activos else ACCENT)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            self.canvas.create_text(x1 + ancho/2, y1 - 12, text=str(int(v)), fill=TEXT, font=FONT_SM)

    def _log_msg(self, msg):
        self.log.insert(tk.END, f"» {msg}\n")
        self.log.see(tk.END)

    def _ejecutar(self):
        if self.animando: return
        self.animando = True
        self._delay = self.vel_slider.get()
        m = self.metodo_actual
        ej = self.EJERCICIOS[m][self.ejercicio_actual]
        self.log.delete("1.0", tk.END)
        
        if m == "intercalacion":
            res, pasos = intercalacion_pasos(ej['a'], ej['b'])
            self._log_msg(f"Intercalando listas de tamaño {len(ej['a'])} y {len(ej['b'])}")
            for p in pasos:
                self._dibujar(ej['a'] + ej['b'], activos=[p[2], len(ej['a'])+p[3]])
                self.root.update()
                time.sleep(self._delay)
            self._dibujar(res, listos=list(range(len(res))))
        
        elif m == "directa":
            res, pasos = mezcla_directa_pasos(ej['datos'])
            self._log_msg("Iniciando Mezcla Directa (Merge Sort)...")
            for p in pasos:
                self._dibujar(p)
                self.root.update()
                time.sleep(self._delay)
            self._dibujar(res, listos=list(range(len(res))))

        elif m == "equilibrada":
            res, pasos = mezcla_equilibrada_pasos(ej['datos'], ej['k'])
            self._log_msg(f"Iniciando Mezcla Equilibrada (k={ej['k']})...")
            for p in pasos:
                self._dibujar(p[1])
                self.root.update()
                time.sleep(self._delay)
            self._dibujar(res, listos=list(range(len(res))))

        self._log_msg("¡Proceso finalizado!")
        self.animando = False

if __name__ == "__main__":
    root = tk.Tk()
    app = OrdenamientoApp(root)
    root.mainloop()
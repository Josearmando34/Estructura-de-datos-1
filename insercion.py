"""
╔══════════════════════════════════════════════╗
║   ORDENAMIENTO POR INSERCIÓN - GUI en Python ║
║   Estructura de Datos                        ║
╚══════════════════════════════════════════════╝

¿Cómo funciona el método de inserción?
- Recorre la lista de izquierda a derecha.
- En cada paso toma un elemento (la "llave").
- Lo compara con los anteriores y lo inserta en su lugar correcto.
- Es como ordenar cartas en tu mano. 🃏
"""

import tkinter as tk
from tkinter import messagebox, ttk
import time


# ─────────────────────────────────────────────
#   FUNCIÓN PRINCIPAL DE INSERCIÓN
#   (pura, sin GUI — fácil de entender)
# ─────────────────────────────────────────────

def ordenamiento_insercion(lista):
    """
    Ordena una lista usando el método de inserción.
    Retorna también todos los pasos intermedios para visualizarlos.
    """
    pasos = []                          # Guardará cada estado de la lista
    arr = lista.copy()                  # Trabajamos con una copia

    for i in range(1, len(arr)):        # Empezamos desde el segundo elemento
        llave = arr[i]                  # Tomamos el elemento actual (la "llave")
        j = i - 1

        # Movemos los elementos mayores a la derecha
        while j >= 0 and arr[j] > llave:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = llave              # Insertamos la llave en su lugar correcto

        # Guardamos el estado actual con info del paso
        pasos.append({
            "lista": arr.copy(),
            "indice_insertado": j + 1,
            "paso": i
        })

    return arr, pasos


# ─────────────────────────────────────────────
#   INTERFAZ GRÁFICA CON TKINTER
# ─────────────────────────────────────────────

class AppOrdenamiento:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Ordenamiento por Inserción")
        self.root.geometry("800x620")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        self.pasos = []
        self.paso_actual = 0

        self._construir_ui()

    def _construir_ui(self):
        """Construye todos los elementos visuales de la app."""

        # ── Título ──
        tk.Label(
            self.root,
            text="🃏 Ordenamiento por Inserción",
            font=("Helvetica", 20, "bold"),
            bg="#1e1e2e", fg="#cdd6f4"
        ).pack(pady=(20, 5))

        tk.Label(
            self.root,
            text="Ingresa números separados por comas y presiona Ordenar",
            font=("Helvetica", 10),
            bg="#1e1e2e", fg="#a6adc8"
        ).pack()

        # ── Entrada de datos ──
        frame_entrada = tk.Frame(self.root, bg="#1e1e2e")
        frame_entrada.pack(pady=15)

        tk.Label(
            frame_entrada, text="Números:", font=("Helvetica", 12),
            bg="#1e1e2e", fg="#cdd6f4"
        ).grid(row=0, column=0, padx=5)

        self.entrada = tk.Entry(
            frame_entrada, width=35, font=("Helvetica", 13),
            bg="#313244", fg="#cdd6f4", insertbackground="white",
            relief="flat", bd=5
        )
        self.entrada.insert(0, "64, 25, 12, 22, 11")
        self.entrada.grid(row=0, column=1, padx=5)

        # ── Botones ──
        frame_botones = tk.Frame(self.root, bg="#1e1e2e")
        frame_botones.pack(pady=5)

        self.btn_ordenar = tk.Button(
            frame_botones, text="▶ Ordenar", command=self.iniciar_ordenamiento,
            bg="#89b4fa", fg="#1e1e2e", font=("Helvetica", 11, "bold"),
            relief="flat", padx=15, pady=6, cursor="hand2"
        )
        self.btn_ordenar.grid(row=0, column=0, padx=8)

        self.btn_anterior = tk.Button(
            frame_botones, text="◀ Anterior", command=self.paso_anterior,
            bg="#45475a", fg="#cdd6f4", font=("Helvetica", 11),
            relief="flat", padx=15, pady=6, cursor="hand2", state="disabled"
        )
        self.btn_anterior.grid(row=0, column=1, padx=8)

        self.btn_siguiente = tk.Button(
            frame_botones, text="Siguiente ▶", command=self.paso_siguiente,
            bg="#45475a", fg="#cdd6f4", font=("Helvetica", 11),
            relief="flat", padx=15, pady=6, cursor="hand2", state="disabled"
        )
        self.btn_siguiente.grid(row=0, column=2, padx=8)

        self.btn_auto = tk.Button(
            frame_botones, text="⚡ Auto", command=self.auto_play,
            bg="#a6e3a1", fg="#1e1e2e", font=("Helvetica", 11, "bold"),
            relief="flat", padx=15, pady=6, cursor="hand2", state="disabled"
        )
        self.btn_auto.grid(row=0, column=3, padx=8)

        self.btn_limpiar = tk.Button(
            frame_botones, text="🗑 Limpiar", command=self.limpiar,
            bg="#f38ba8", fg="#1e1e2e", font=("Helvetica", 11),
            relief="flat", padx=15, pady=6, cursor="hand2"
        )
        self.btn_limpiar.grid(row=0, column=4, padx=8)

        # ── Canvas para barras ──
        self.canvas = tk.Canvas(
            self.root, width=760, height=280,
            bg="#181825", highlightthickness=0
        )
        self.canvas.pack(pady=10)

        # ── Info del paso ──
        self.lbl_paso = tk.Label(
            self.root, text="Ingresa números y presiona Ordenar",
            font=("Helvetica", 12), bg="#1e1e2e", fg="#f9e2af"
        )
        self.lbl_paso.pack()

        # ── Lista de pasos (log) ──
        tk.Label(
            self.root, text="📋 Historial de pasos:",
            font=("Helvetica", 10, "bold"), bg="#1e1e2e", fg="#a6adc8"
        ).pack(anchor="w", padx=30)

        frame_log = tk.Frame(self.root, bg="#1e1e2e")
        frame_log.pack(fill="x", padx=30, pady=(0, 15))

        self.log = tk.Text(
            frame_log, height=5, font=("Courier", 9),
            bg="#181825", fg="#a6e3a1", relief="flat", state="disabled"
        )
        self.log.pack(side="left", fill="x", expand=True)

        scroll = tk.Scrollbar(frame_log, command=self.log.yview)
        scroll.pack(side="right", fill="y")
        self.log.config(yscrollcommand=scroll.set)

    # ─── Lógica de la app ───

    def obtener_numeros(self):
        """Lee y valida la entrada del usuario."""
        texto = self.entrada.get().strip()
        try:
            numeros = [int(x.strip()) for x in texto.split(",") if x.strip()]
            if len(numeros) < 2:
                raise ValueError("Ingresa al menos 2 números.")
            if len(numeros) > 15:
                raise ValueError("Máximo 15 números para mejor visualización.")
            return numeros
        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
            return None

    def iniciar_ordenamiento(self):
        """Ejecuta el algoritmo y prepara la visualización."""
        numeros = self.obtener_numeros()
        if numeros is None:
            return

        self.lista_original = numeros.copy()
        self.lista_ordenada, self.pasos = ordenamiento_insercion(numeros)
        self.paso_actual = 0

        # Habilitar botones
        self.btn_siguiente.config(state="normal")
        self.btn_anterior.config(state="normal")
        self.btn_auto.config(state="normal")

        # Mostrar estado inicial
        self.dibujar_barras(numeros, resaltado=-1)
        self.lbl_paso.config(text=f"📌 Lista original: {numeros}  →  Presiona 'Siguiente' para ver los pasos")
        self._agregar_log(f"Lista inicial: {numeros}\n")

    def dibujar_barras(self, lista, resaltado=-1):
        """Dibuja las barras en el canvas."""
        self.canvas.delete("all")
        n = len(lista)
        if n == 0:
            return

        ancho_canvas = 760
        alto_canvas = 280
        margen = 30
        espacio = (ancho_canvas - 2 * margen) / n
        max_val = max(lista) if max(lista) != 0 else 1

        for i, val in enumerate(lista):
            x1 = margen + i * espacio + 5
            x2 = x1 + espacio - 10
            altura = (val / max_val) * (alto_canvas - 60)
            y1 = alto_canvas - altura - 20
            y2 = alto_canvas - 20

            # Color: resaltado = verde, resto = azul
            color = "#a6e3a1" if i == resaltado else "#89b4fa"
            sombra = "#40a02b" if i == resaltado else "#1d4ed8"

            # Sombra
            self.canvas.create_rectangle(x1+3, y1+3, x2+3, y2+3, fill=sombra, outline="")
            # Barra
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            # Valor encima
            self.canvas.create_text(
                (x1 + x2) / 2, y1 - 8,
                text=str(val), fill="#cdd6f4", font=("Helvetica", 9, "bold")
            )
            # Índice debajo
            self.canvas.create_text(
                (x1 + x2) / 2, y2 + 10,
                text=f"[{i}]", fill="#585b70", font=("Helvetica", 8)
            )

    def paso_siguiente(self):
        """Avanza un paso en la visualización."""
        if self.paso_actual >= len(self.pasos):
            self.lbl_paso.config(text=f"✅ ¡Listo! Lista ordenada: {self.lista_ordenada}")
            return

        info = self.pasos[self.paso_actual]
        self.dibujar_barras(info["lista"], resaltado=info["indice_insertado"])
        self.lbl_paso.config(
            text=f"Paso {info['paso']}/{len(self.pasos)}: "
                 f"Insertando en posición [{info['indice_insertado']}] → {info['lista']}"
        )
        self._agregar_log(
            f"Paso {info['paso']}: {info['lista']}  ← inserción en pos [{info['indice_insertado']}]\n"
        )
        self.paso_actual += 1

        if self.paso_actual == len(self.pasos):
            self.lbl_paso.config(text=f"✅ ¡Ordenado! Resultado final: {self.lista_ordenada}")

    def paso_anterior(self):
        """Retrocede un paso."""
        if self.paso_actual <= 0:
            return
        self.paso_actual = max(0, self.paso_actual - 2)
        self.paso_siguiente()

    def auto_play(self):
        """Reproduce todos los pasos automáticamente."""
        self.paso_actual = 0
        self._reproducir()

    def _reproducir(self):
        """Llamada recursiva con delay para el auto play."""
        if self.paso_actual < len(self.pasos):
            self.paso_siguiente()
            self.root.after(700, self._reproducir)

    def limpiar(self):
        """Limpia todo para empezar de nuevo."""
        self.canvas.delete("all")
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, "64, 25, 12, 22, 11")
        self.lbl_paso.config(text="Ingresa números y presiona Ordenar")
        self.pasos = []
        self.paso_actual = 0
        self.btn_siguiente.config(state="disabled")
        self.btn_anterior.config(state="disabled")
        self.btn_auto.config(state="disabled")
        self.log.config(state="normal")
        self.log.delete("1.0", tk.END)
        self.log.config(state="disabled")

    def _agregar_log(self, texto):
        """Agrega una línea al historial."""
        self.log.config(state="normal")
        self.log.insert(tk.END, texto)
        self.log.see(tk.END)
        self.log.config(state="disabled")


# ─────────────────────────────────────────────
#   PUNTO DE ENTRADA
# ─────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = AppOrdenamiento(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox

class PilaGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Pila (Stack)")

        self.pila = []
        self.max_pila = 8

        # variables para ejercicio
        self.variables_pop = ["Z","T","U","P"]
        self.indice_pop = 0

        # Canvas
        self.canvas = tk.Canvas(root, width=300, height=400, bg="white")
        self.canvas.pack()

        # Frame controles
        frame = tk.Frame(root)
        frame.pack(pady=10)

        self.entrada = tk.Entry(frame)
        self.entrada.grid(row=0, column=0)

        btn_push = tk.Button(frame, text="Push", command=self.push)
        btn_push.grid(row=0, column=1)

        btn_pop = tk.Button(frame, text="Pop", command=self.pop)
        btn_pop.grid(row=0, column=2)

        btn_vaciar = tk.Button(frame, text="Vaciar", command=self.vaciar_pila)
        btn_vaciar.grid(row=0, column=3)

        btn_auto = tk.Button(frame, text="Auto Llenar", command=self.auto_llenar)
        btn_auto.grid(row=0, column=4)

        # NUEVO botón eliminar ejercicio
        btn_pop_ejercicio = tk.Button(root, text="Eliminar (Ejercicio)", command=self.pop_ejercicio)
        btn_pop_ejercicio.pack(pady=3)

        # Botón ejercicio
        btn_ejercicio = tk.Button(root, text="Mostrar Ejercicio", command=self.ejecutar_ejercicio)
        btn_ejercicio.pack(pady=5)

        self.dibujar_pila()

    # ---------------- DIBUJAR PILA ----------------

    def dibujar_pila(self):
        self.canvas.delete("all")

        y = 350
        altura = 40

        for i, elemento in enumerate(reversed(self.pila)):

            self.canvas.create_rectangle(100, y-altura, 200, y, fill="lightblue")
            self.canvas.create_text(150, y-20, text=str(elemento), font=("Arial", 12))

            # posición
            self.canvas.create_text(80, y-20, text=str(len(self.pila)-i))

            # marcar tope
            if i == 0:
                self.canvas.create_text(230, y-20, text="TOPE", fill="red", font=("Arial",10,"bold"))

            y -= altura

        self.canvas.create_text(
            150, 20,
            text=f"Elementos: {len(self.pila)} / {self.max_pila}",
            font=("Arial",12,"bold")
        )

    # ---------------- PUSH ----------------

    def push(self):

        valor = self.entrada.get()

        if valor == "":
            messagebox.showwarning("Aviso", "Ingresa un valor")
            return

        if len(self.pila) >= self.max_pila:
            messagebox.showwarning("Error", "Desbordamiento: Pila llena")
            return

        self.pila.append(valor)
        self.entrada.delete(0, tk.END)
        self.dibujar_pila()

    # ---------------- POP NORMAL ----------------

    def pop(self):

        if not self.pila:
            messagebox.showwarning("Error", "Subdesbordamiento: pila vacía")
            return

        eliminado = self.pila.pop()
        messagebox.showinfo("POP", f"Elemento eliminado: {eliminado}")
        self.dibujar_pila()

    # ---------------- POP EJERCICIO ----------------

    def pop_ejercicio(self):

        if not self.pila:
            messagebox.showwarning("Error", "Subdesbordamiento: pila vacía")
            return

        if self.indice_pop >= len(self.variables_pop):
            messagebox.showinfo("Aviso", "Ya no hay más eliminaciones del ejercicio")
            return

        eliminado = self.pila.pop()
        variable = self.variables_pop[self.indice_pop]

        messagebox.showinfo("Resultado", f"{variable} = {eliminado}")

        self.indice_pop += 1
        self.dibujar_pila()

    # ---------------- VACIAR ----------------

    def vaciar_pila(self):
        self.pila.clear()
        self.indice_pop = 0
        self.dibujar_pila()

    # ---------------- AUTO LLENAR ----------------

    def auto_llenar(self):

        if len(self.pila) >= self.max_pila:
            messagebox.showwarning("Aviso", "La pila ya está llena")
            return

        self.llenar_animado()

    def llenar_animado(self):

        if len(self.pila) < self.max_pila:
            self.pila.append(len(self.pila) + 1)
            self.dibujar_pila()
            self.root.after(500, self.llenar_animado)
        else:
            messagebox.showinfo("Aviso", "La pila se llenó automáticamente")

    # ---------------- MOSTRAR EJERCICIO ----------------

    def ejecutar_ejercicio(self):

        self.vaciar_pila()

        operaciones = [
            "1) Insertar (PILA, X)",
            "2) Insertar (PILA, Y)",
            "3) Eliminar (PILA, Z)",
            "4) Eliminar (PILA, T)",
            "5) Eliminar (PILA, U)",
            "6) Insertar (PILA, V)",
            "7) Insertar (PILA, W)",
            "8) Eliminar (PILA, P)",
            "9) Insertar (PILA, R)"
        ]

        texto = "\n".join(operaciones)

        messagebox.showinfo(
            "Ejercicio",
            f"Realiza estas operaciones manualmente:\n\n{texto}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = PilaGrafica(root)
    root.mainloop()
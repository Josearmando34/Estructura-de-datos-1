import tkinter as tk
from tkinter import messagebox

class PilaGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Pila (Stack)")

        self.pila = []
        self.max_pila = 8

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

    def dibujar_pila(self):
        self.canvas.delete("all")

        y = 350
        altura = 40

        for elemento in reversed(self.pila):
            self.canvas.create_rectangle(100, y-altura, 200, y, fill="lightblue")
            self.canvas.create_text(150, y-20, text=str(elemento), font=("Arial", 12))
            y -= altura

    def push(self):
        valor = self.entrada.get()

        if valor == "":
            messagebox.showwarning("Aviso", "Ingresa un valor")
            return

        if len(self.pila) >= self.max_pila:
            messagebox.showwarning("Aviso", "Pila llena")
            return

        self.pila.append(valor)
        self.entrada.delete(0, tk.END)
        self.dibujar_pila()

    def pop(self):
        if not self.pila:
            messagebox.showwarning("Aviso", "La pila está vacía")
            return

        self.pila.pop()
        self.dibujar_pila()

    def vaciar_pila(self):
        if not self.pila:
            messagebox.showwarning("Aviso", "La pila ya está vacía")
            return

        self.pila.clear()
        self.dibujar_pila()

    def auto_llenar(self):
        if len(self.pila) >= self.max_pila:
            messagebox.showwarning("Aviso", "La pila ya está llena")
            return

        self.llenar_animado()

    def llenar_animado(self):
        if len(self.pila) < self.max_pila:
            self.pila.append(len(self.pila) + 1)
            self.dibujar_pila()
            self.root.after(500, self.llenar_animado)  # cada 500 ms agrega uno
        else:
            messagebox.showinfo("Aviso", "La pila se llenó automáticamente")


if __name__ == "__main__":
    root = tk.Tk()
    app = PilaGrafica(root)
    root.mainloop()
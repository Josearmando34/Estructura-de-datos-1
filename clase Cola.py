class Cola:
    def __init__(self):
        self.elementos = []
    
    def encolar(self, valor):
        self.elementos.append(valor)
    
    def desencolar(self):
        if not self.esta_vacia():
            return self.elementos.pop(0)
        return None
    
    def esta_vacia(self):
        return len(self.elementos) == 0
    
    def tamanio(self):
        return len(self.elementos)
    
    def __str__(self):
        return str(self.elementos)


def sumar_colas(cola_a, cola_b):
    cola_resultado = Cola()
    
    temp_a = Cola()
    temp_b = Cola()
    
    while not cola_a.esta_vacia() and not cola_b.esta_vacia():
        elemento_a = cola_a.desencolar()
        elemento_b = cola_b.desencolar()
        
        cola_resultado.encolar(elemento_a + elemento_b)
        
        temp_a.encolar(elemento_a)
        temp_b.encolar(elemento_b)
    
    # Restaurar las colas originales
    while not temp_a.esta_vacia():
        cola_a.encolar(temp_a.desencolar())
        
    while not temp_b.esta_vacia():
        cola_b.encolar(temp_b.desencolar())
    
    return cola_resultado


# Crear Cola A
cola_a = Cola()
for num in [3, 4, 2, 8, 12]:
    cola_a.encolar(num)

# Crear Cola B
cola_b = Cola()
for num in [6, 2, 9, 11, 3]:
    cola_b.encolar(num)

# Obtener cola resultado
cola_resultado = sumar_colas(cola_a, cola_b)

print(f"{'Cola A':<12} {'Cola B':<12} {'Cola Resultado'}")
print("-" * 38)

temp_a = Cola()
temp_b = Cola()
temp_r = Cola()

# Copiar datos para imprimir sin perderlos
while not cola_a.esta_vacia():
    temp_a.encolar(cola_a.desencolar())

while not cola_b.esta_vacia():
    temp_b.encolar(cola_b.desencolar())

while not cola_resultado.esta_vacia():
    temp_r.encolar(cola_resultado.desencolar())

# Mostrar resultados
while not temp_a.esta_vacia():
    a = temp_a.desencolar()
    b = temp_b.desencolar()
    r = temp_r.desencolar()
    print(f"{a:<12} {b:<12} {r}")

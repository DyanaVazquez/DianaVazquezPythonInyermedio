    
class Producto:
    moneda = "MXN"

    def __init__(self, nombre, precio, cantidad_en_inventario):
        self.nombre = nombre
        self.precio = precio
        self.cantidad_en_inventario = cantidad_en_inventario

    def valor_total(self):
        return self.precio * self.cantidad_en_inventario


# Crear tres objetos de productos: modelos de celulares
producto1 = Producto("Samsung Galaxy A55", 7500, 10)
producto2 = Producto("iPhone 15", 15000, 5)
producto3 = Producto("Xiaomi Redmi Note 14", 4500, 8)

# Guardar los productos en una lista
inventario = [producto1, producto2, producto3]

# Mostrar el valor total de cada producto
print("INVENTARIO DE CELULARES")
print("-----------------------")

for producto in inventario:
    print(f"Modelo: {producto.nombre}")
    print(f"Precio: ${producto.precio:.2f} {Producto.moneda}")
    print(f"Cantidad en inventario: {producto.cantidad_en_inventario}")
    print(f"Valor total: ${producto.valor_total():.2f} {Producto.moneda}")
    print("-----------------------")

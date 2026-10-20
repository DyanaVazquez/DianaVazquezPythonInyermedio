
class Libro:
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
        self._disponible = True

    def __str__(self):
        estado = "disponible" if self._disponible else "prestado"
        return f"{self.titulo}, de {self.autor} ({estado})"

    @property
    def disponible(self):
        return self._disponible

    def prestar(self):
        if self._disponible:
            self._disponible = False
            print(f"El libro '{self.titulo}' ha sido prestado.")
        else:
            print(f"El libro '{self.titulo}' no está disponible.")

    def devolver(self):
        if not self._disponible:
            self._disponible = True
            print(f"El libro '{self.titulo}' ha sido devuelto.")
        else:
            print(f"El libro '{self.titulo}' ya estaba disponible.")


class Biblioteca:
    def __init__(self, nombre):
        self.nombre = nombre
        self._libros = []

    def agregar(self, libro):
        self._libros.append(libro)
        print(f"Se agregó: {libro.titulo}")

    def listar(self):
        print(f"\nLibros de la biblioteca {self.nombre}:")
        if not self._libros:
            print("No hay libros registrados.")
            return

        for libro in self._libros:
            print(libro)

    def buscar(self, titulo):
        for libro in self._libros:
            if libro.titulo.lower() == titulo.lower():
                return libro

        return None


class LibroDigital(Libro):
    def __init__(self, titulo, autor, formato):
        super().__init__(titulo, autor)
        self.formato = formato

    @property
    def disponible(self):
        return True

    def prestar(self):
        print(f"El libro digital '{self.titulo}' "
              f"está disponible para lectura.")

    def devolver(self):
        print(f"El libro digital '{self.titulo}' "
              f"permanece disponible.")

    def __str__(self):
        return (
            f"{self.titulo}, de {self.autor} "
            f"(disponible, formato: {self.formato})"
        )


# Programa principal
biblioteca = Biblioteca("Biblioteca Central")

libro1 = Libro("Meditaciones", "Marco Aurelio")
libro2 = Libro("Don Quijote de la Mancha", "Miguel de Cervantes")
libro3 = Libro("Cien años de soledad", "Gabriel García Márquez")
libro4 = LibroDigital("El principito", "Antoine de Saint-Exupéry", "PDF")

biblioteca.agregar(libro1)
biblioteca.agregar(libro2)
biblioteca.agregar(libro3)
biblioteca.agregar(libro4)

print("\n--- Préstamo de un libro ---")
libro1.prestar()

print("\n--- Intento de préstamo repetido ---")
libro1.prestar()

biblioteca.listar()

print("\n--- Búsqueda de un libro ---")
resultado = biblioteca.buscar("Meditaciones")

if resultado is not None:
    print(f"Libro encontrado: {resultado}")
else:
    print("El libro no se encuentra en la biblioteca.")

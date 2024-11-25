from zeep import Client
from zeep.transports import Transport
from requests import Session
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Deshabilitar advertencias SSL durante las pruebas
warnings.simplefilter('ignore', InsecureRequestWarning)

# Configurar sesión HTTP para ignorar la verificación SSL
session = Session()
session.verify = False  # Deshabilitar la verificación de certificados SSL
transport = Transport(session=session)

# URL del WSDL del servidor local
wsdl_url = "http://localhost:56035/Service1.svc?wsdl"

# Crear cliente SOAP
client = Client(wsdl=wsdl_url, transport=transport)


# Validar entrada para campos específicos
def validate_year_input(prompt):
    while True:
        try:
            year = input(prompt).strip()
            if not year:
                raise ValueError("El año no puede estar vacío.")
            year = int(year)
            if year < 0:
                raise ValueError("El año no puede ser negativo.")
            return year
        except ValueError as e:
            print(f"Entrada inválida: {e}. Intente nuevamente.")

def validate_text_input(prompt):
    while True:
        text = input(prompt).strip()
        if text:
            return text
        else:
            print("El campo no puede estar vacío. Intente nuevamente.")

# Función para manejar excepciones SOAP de manera amigable
def handle_soap_fault(exception):
    fault_string = str(exception)
    if "no existe en la base de datos" in fault_string.lower():
        print("Error: El ID proporcionado no existe en la base de datos.")
    else:
        print(f"Error del servidor: {fault_string}")

# Funciones para las operaciones CRUD

# 1. Read: Obtener todos los libros
def get_all_books():
    try:
        libros = client.service.GetLibros()
        if not libros:
            print("\nNo hay libros en la base de datos.")
            return

        print("\nLista de libros:")
        for libro in libros:
            print(f"- ID: {libro['Id']}, Título: {libro['Titulo']}, Autor: {libro['Autor']}, Año: {libro['Año']}")
    except Exception as e:
        handle_soap_fault(e)

# 2. Read: Obtener un libro por ID
def get_book_by_id():
    try:
        book_id = validate_year_input("\nIngrese el ID del libro que desea consultar: ")
        libro = client.service.GetLibroById(book_id)
        if not libro:
            print(f"El libro con ID {book_id} no existe en la base de datos.")
            return
        
        print(f"Detalles del libro - ID: {libro['Id']}, Título: {libro['Titulo']}, Autor: {libro['Autor']}, Año: {libro['Año']}")
    except Exception as e:
        handle_soap_fault(e)

# 3. Create: Agregar un libro
def add_book():
    try:
        title = validate_text_input("\nIngrese el título del libro: ")
        author = validate_text_input("Ingrese el autor del libro: ")
        year = validate_year_input("Ingrese el año del libro: ")
        client.service.AddLibro({
            'Titulo': title,
            'Autor': author,
            'Año': year
        })
        print("Libro agregado exitosamente.")
    except Exception as e:
        handle_soap_fault(e)

# 4. Update: Actualizar un libro
def update_book():
    try:
        book_id = validate_year_input("\nIngrese el ID del libro a actualizar: ")
        libro = client.service.GetLibroById(book_id)
        if not libro:
            print(f"El libro con ID {book_id} no existe en la base de datos.")
            return
        
        print("\nSeleccione qué desea actualizar (o presione 0 para volver al menú):")
        print("1. Título")
        print("2. Autor")
        print("3. Año")
        opcion = input("Ingrese una opción: ")
        
        if opcion == "0":
            print("Volviendo al menú principal...")
            return
        
        if opcion == "1":
            new_title = validate_text_input("Ingrese el nuevo título: ")
            libro['Titulo'] = new_title
        elif opcion == "2":
            new_author = validate_text_input("Ingrese el nuevo autor: ")
            libro['Autor'] = new_author
        elif opcion == "3":
            new_year = validate_year_input("Ingrese el nuevo año: ")
            libro['Año'] = new_year
        else:
            print("Opción no válida.")
            return
        
        client.service.UpdateLibro(libro)
        print("Libro actualizado exitosamente.")
    except Exception as e:
        handle_soap_fault(e)

# 5. Delete: Eliminar un libro
def delete_book():
    try:
        book_id = validate_year_input("\nIngrese el ID del libro que desea eliminar: ")
        libro = client.service.GetLibroById(book_id)
        if not libro:
            print(f"El libro con ID {book_id} no existe en la base de datos.")
            return
        
        confirm = input(f"¿Está seguro que desea eliminar el libro '{libro['Titulo']}'? (s/n): ").strip().lower()
        if confirm != 's':
            print("Operación cancelada.")
            return
        
        client.service.DeleteLibro(book_id)
        print(f"Libro con ID {book_id} eliminado exitosamente.")
    except Exception as e:
        handle_soap_fault(e)

# Menú interactivo
def menu():
    while True:
        print("\n===== Menú de Operaciones CRUD =====")
        print("1. Obtener todos los libros")
        print("2. Obtener un libro por ID")
        print("3. Agregar un nuevo libro")
        print("4. Actualizar un libro existente")
        print("5. Eliminar un libro")
        print("6. Salir")
        
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            get_all_books()
        elif opcion == "2":
            get_book_by_id()
        elif opcion == "3":
            add_book()
        elif opcion == "4":
            update_book()
        elif opcion == "5":
            delete_book()
        elif opcion == "6":
            print("\nSaliendo del programa...")
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")

# Ejecutar el menú interactivo
if __name__ == "__main__":
    menu()

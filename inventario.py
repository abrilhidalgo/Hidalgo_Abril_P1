"""
TPI Programación 1 - Sistema de Control de Inventario
Alumna: Hidalgo Abril Antonella

Programa con menú para controlar el stock de una ferretería.
El inventario es una lista de diccionarios con las claves
'herramienta' y 'cantidad'. Se crea en main() y lo paso por
parámetro a cada función, sin variables globales.
"""


# ---------- Funciones auxiliares ----------

def convertir_entero(texto):
    """Convierto el texto a entero. Si no se puede (por ejemplo 'abc' o '3.5'),
    capturo el error de int() y lo lanzo de nuevo con un mensaje más claro."""
    try:
        return int(texto)
    except ValueError:
        raise ValueError(f"'{texto}' no es un número entero.")


def validar_nombre(nombre):
    """Le saco los espacios de los extremos al nombre y lo devuelvo.
    Si queda vacío, lanzo ValueError."""
    nombre = nombre.strip()
    if len(nombre) == 0:
        raise ValueError("El nombre no puede estar vacío.")
    return nombre


def buscar_herramienta(inventario, nombre):
    """Recorro el inventario y devuelvo la herramienta que coincide con el nombre,
    sin importar mayúsculas ni espacios. Si no la encuentro, devuelvo None."""
    for producto in inventario:
        if producto['herramienta'].strip().lower() == nombre.strip().lower():
            return producto
    return None


def validar_nombre_nuevo(inventario, nombre):
    """Valido que el nombre no esté vacío y que no esté cargado ya en el inventario."""
    nombre = validar_nombre(nombre)
    if buscar_herramienta(inventario, nombre) is not None:
        raise ValueError(f"'{nombre}' ya está cargada en el inventario.")
    return nombre


def validar_stock_inicial(texto):
    """Convierto el stock a entero y controlo que no sea negativo. El 0 vale."""
    stock = convertir_entero(texto)
    if stock < 0:
        raise ValueError("El stock no puede ser negativo.")
    return stock


# ---------- Opciones del menú ----------

def cargar_herramientas(inventario):
    """Opción 1: carga múltiple. Los errores los capturo acá adentro
    y vuelvo a pedir solo el dato que falló."""
    # pido cuántas herramientas se van a cargar hasta que sea un entero mayor que 0
    while True:
        try:
            cantidad_a_cargar = convertir_entero(input("¿Cuántas herramientas distintas vas a cargar? "))
            if cantidad_a_cargar <= 0:
                raise ValueError("La cantidad de herramientas debe ser mayor que 0.")
            break
        except ValueError as e:
            print(f"Error: {e}")

    for i in range(cantidad_a_cargar):
        print(f"\nHerramienta {i + 1} de {cantidad_a_cargar}")

        # pido el nombre hasta que no esté vacío ni repetido
        while True:
            try:
                nombre = validar_nombre_nuevo(inventario, input("Nombre: "))
                break
            except ValueError as e:
                print(f"Error: {e}")

        # pido solo el stock hasta que sea válido, el nombre ya lo tengo guardado
        while True:
            try:
                stock = validar_stock_inicial(input(f"Stock inicial de {nombre}: "))
                break
            except ValueError as e:
                print(f"Error: {e}")

        # recién acá, con los dos datos válidos, la agrego al inventario
        inventario.append({'herramienta': nombre, 'cantidad': stock})
        print(f"'{nombre}' cargada con {stock} unidades.")


def mostrar_inventario(inventario):
    """Opción 2: muestro todas las herramientas con su stock."""
    if len(inventario) == 0:
        print("Todavía no hay herramientas cargadas.")
        return
    print("\nInventario actual:")
    for producto in inventario:
        print(f"- {producto['herramienta']}: {producto['cantidad']} unidades")


def consultar_stock(inventario):
    """Opción 3: busco una herramienta por nombre y muestro su stock.
    Si el nombre está vacío, el error sale hacia main()."""
    if len(inventario) == 0:
        print("Todavía no hay herramientas cargadas.")
        return
    nombre = validar_nombre(input("Nombre de la herramienta a consultar: "))
    producto = buscar_herramienta(inventario, nombre)
    if producto is None:
        print(f"'{nombre}' no se encuentra en el catálogo.")
    else:
        print(f"Stock de {producto['herramienta']}: {producto['cantidad']} unidades.")


def reporte_agotados(inventario):
    """Opción 4: muestro solo las herramientas con stock 0."""
    if len(inventario) == 0:
        print("Todavía no hay herramientas cargadas.")
        return
    hay_agotados = False
    for producto in inventario:
        if producto['cantidad'] == 0:
            # el título lo muestro recién cuando encuentro el primer agotado
            if not hay_agotados:
                print("\nHerramientas agotadas:")
                hay_agotados = True
            print(f"- {producto['herramienta']}")
    if not hay_agotados:
        print("Ninguna herramienta tiene stock cero.")


def alta_producto(inventario):
    """Opción 5: agrego una herramienta nueva. Si algo falla, el error
    sale hacia main() y no se agrega nada."""
    # primero el nombre: si es inválido no llego a pedir el stock
    nombre = validar_nombre_nuevo(inventario, input("Nombre de la nueva herramienta: "))
    stock = validar_stock_inicial(input(f"Stock inicial de {nombre}: "))
    inventario.append({'herramienta': nombre, 'cantidad': stock})
    print(f"'{nombre}' agregada con {stock} unidades.")


def actualizar_stock(inventario):
    """Opción 6: venta o ingreso de unidades. Solo modifico el stock
    cuando todos los datos son válidos."""
    if len(inventario) == 0:
        print("Todavía no hay herramientas cargadas.")
        return

    nombre = validar_nombre(input("Nombre de la herramienta: "))
    producto = buscar_herramienta(inventario, nombre)
    if producto is None:
        print(f"'{nombre}' no se encuentra en el catálogo.")
        return

    # el tipo lo comparo como texto, así una entrada rara se resuelve con un mensaje
    print("1. Venta")
    print("2. Ingreso")
    tipo = input("Tipo de movimiento (1 o 2): ").strip()
    if tipo != "1" and tipo != "2":
        print("Tipo de movimiento inválido. Solo se acepta 1 (venta) o 2 (ingreso).")
        return

    unidades = convertir_entero(input("Unidades del movimiento: "))
    if unidades <= 0:
        raise ValueError("Las unidades deben ser mayores que 0.")

    if tipo == "1":
        if producto['cantidad'] - unidades < 0:
            raise ValueError(f"No hay stock suficiente. Disponibles: {producto['cantidad']}.")
        producto['cantidad'] = producto['cantidad'] - unidades
        print(f"Venta registrada. Stock de {producto['herramienta']}: {producto['cantidad']} unidades.")
    else:
        producto['cantidad'] = producto['cantidad'] + unidades
        print(f"Ingreso registrado. Stock de {producto['herramienta']}: {producto['cantidad']} unidades.")


# ---------- Menú principal ----------

def mostrar_menu():
    """Imprimo las siete opciones del menú."""
    print("\n===== FERRETERÍA - CONTROL DE INVENTARIO =====")
    print("1. Cargar herramientas")
    print("2. Ver inventario")
    print("3. Consultar stock")
    print("4. Reporte de agotados")
    print("5. Alta de nuevo producto")
    print("6. Actualizar stock (venta / ingreso)")
    print("7. Salir")


def main():
    """Creo el inventario y repito el menú hasta que se elija la opción 7."""
    inventario = []
    opcion = 0
    while opcion != 7:
        mostrar_menu()
        try:
            opcion = convertir_entero(input("Seleccione una opción: "))
            if opcion == 1:
                cargar_herramientas(inventario)
            elif opcion == 2:
                mostrar_inventario(inventario)
            elif opcion == 3:
                consultar_stock(inventario)
            elif opcion == 4:
                reporte_agotados(inventario)
            elif opcion == 5:
                alta_producto(inventario)
            elif opcion == 6:
                actualizar_stock(inventario)
            elif opcion != 7:
                raise ValueError("Opción fuera de rango (1 a 7).")
        except ValueError as e:
            # acá llegan los errores del menú y los que salen de las opciones 3, 5 y 6
            print(f"Error: {e}")
    print("Gracias por usar el sistema. ¡Hasta luego!")


main()
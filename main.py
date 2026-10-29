from gestion import GestionLaboratorio

#creación del menu
def mostrar_menu():
    print("\n      SISTEMA DE GESTIÓN DE LABORATORIO\n")
    print("1. Registrar equipo")
    print("2. Consultar inventario")
    print("3. Realizar préstamo")
    print("4. Registrar devolución")
    print("5. Consultar préstamos activos")
    print("6. Generar reportes")
    print("7. Salir")


def main():
    lab = GestionLaboratorio()

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-7): ").strip()

# condicionales del menu
        try:
            if opcion == "1":
                print("\n--- REGISTRAR EQUIPO ---")
                codigo = input("Código del equipo: ").strip().upper()
                nombre = input("Nombre del equipo: ").strip()
                cantidad = input("Cantidad: ").strip()
                if not codigo or not nombre or not cantidad:
                    raise ValueError("Todos los campos son obligatorios.")
                lab.registrar_equipo(codigo, nombre, int(cantidad))

            elif opcion == "2":
                lab.consultar_inventario()

            elif opcion == "3":
                print("\n--- REALIZAR PRÉSTAMO ---")
                codigo = input("Código del equipo a prestar: ").strip().upper()
                # Aquí ingresas el nombre del estudiante manualmente
                estudiante = input("Nombre del estudiante: ").strip()

                if not codigo or not estudiante:
                    raise ValueError(
                        "El código y el estudiante son obligatorios."
                    )

                # El sistema procesa tu entrada manual
                lab.realizar_prestamo(codigo, estudiante)

            elif opcion == "4":
                print("\n--- REGISTRAR DEVOLUCIÓN ---")
                codigo = input("Código del equipo: ").strip().upper()
                estudiante = input("Nombre del estudiante: ").strip()
                if not codigo or not estudiante:
                    raise ValueError(
                        "El código y el estudiante son obligatorios."
                    )
                lab.registrar_devolucion(codigo, estudiante)

            elif opcion == "5":
                lab.consultar_prestamos_activos()

            elif opcion == "6":
                lab.generar_reportes()

            elif opcion == "7":
                print("\n ¡Gracias por usar el sistema!")
                break

            else:
                print(" Opción inválida. Intente de nuevo.")

        except ValueError as e:
            print(f" Error en los datos: {e}")
        except Exception as e:
                    print(f" Ocurrió un error no identificado: {e}")


if __name__ == "__main__":
    main()

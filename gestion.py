import csv
from datetime import datetime
from pathlib import Path

# Importacion de clases
from equipo import Equipo
from prestamo import Prestamo

class GestionLaboratorio:
    def __init__(self):
        # ruta para guardar los archivos creados dentro de la carpeta de programa
        self.ruta_equipos = Path(__file__).resolve().parent / "equipos.csv"
        self.ruta_prestamos = Path(__file__).resolve().parent / "prestamos.csv"

# datos con los que se crearan los archivos txt
        self.campos_equipos = ["codigo", "nombre", "cantidad"]
        self.campos_prestamos = ["codigo", "estudiante", "fecha-prestamo"]
        #registro de equipos
    def registrar_equipo(self, codigo, nombre, cantidad):
        equipos = self._cargar_equipos()
        if codigo in equipos:
            equipos[codigo].cantidad += int(cantidad)
        else:
            equipos[codigo] = Equipo(codigo, nombre, cantidad)
        self._guardar_equipos(equipos)
        print(f"Equipo '{nombre}' registrado/actualizado correctamente.")

#para consultar el inventario actual
    def consultar_inventario(self):
        equipos = self._cargar_equipos()
        if not equipos:
            print(" El inventario está vacío.")
            return
        print("\n=== INVENTARIO DE LABORATORIO ===")
        print(f"{'Código':<10} | {'Nombre':<25} | {'Cantidad Disponible':<10}\n")

        for eq in equipos.values():
            print(f"{eq.codigo:<10} | {eq.nombre:<25} | {eq.cantidad:<10}")

    def realizar_prestamo(self, codigo, estudiante):
        equipos = self._cargar_equipos()
        if codigo not in equipos or equipos[codigo].cantidad <= 0:
            print(" No es posible realizar el préstamo. Equipo no disponible o inexistente.")
            return

        equipos[codigo].cantidad -= 1
        self._guardar_equipos(equipos)

#ingresa fecha de ofrma automatica
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nuevo_prestamo = Prestamo(codigo, estudiante, fecha_actual)
        self._guardar_prestamo(nuevo_prestamo)
        print(f" Préstamo registrado con éxito para {estudiante}.")

#sistema de devolucion
    def registrar_devolucion(self, codigo, estudiante):
        prestamos = self._cargar_prestamos()
        encontrado = False

        for p in prestamos:
            if p.codigo == codigo and p.estudiante == estudiante:
                prestamos.remove(p)
                encontrado = True
                break

        if not encontrado:
            print(" No se encontró ningún préstamo activo con esos datos.")
            return

        self._reescribir_prestamos(prestamos)
        equipos = self._cargar_equipos()
        if codigo in equipos:
            equipos[codigo].cantidad += 1
        else:
            equipos[codigo] = Equipo(codigo, "Equipo Recuperado", 1)
            
        self._guardar_equipos(equipos)
        print(f" Devolución procesada con éxito para {estudiante}.")

    def consultar_prestamos_activos(self):
        prestamos = self._cargar_prestamos()
        if not prestamos:
            print(" No hay préstamos activos registrados.")
            return
        print("\n=== HISTORIAL DE PRÉSTAMOS ACTIVOS ===")
        print(f"{'Código Equipo':<15} | {'Estudiante':<20} | {'Fecha Préstamo':<20}\n")
        
        for p in prestamos:
            print(f"{p.codigo:<15} | {p.estudiante:<20} | {p.fecha_prestamo:<20}")
#estructura para los reportes
    def generar_reportes(self):
        equipos = self._cargar_equipos()
        prestamos = self._cargar_prestamos()
        total_equipos = sum(eq.cantidad for eq in equipos.values())
        
        print("\n                 REPORTES            \n")
        print(f"• Tipos de equipos diferentes en catálogo: {len(equipos)}")
        print(f"• Unidades totales disponibles en stock:   {total_equipos}")
        print(f"• Total de equipos actualmente prestados:  {len(prestamos)}")
        print("==========================================")
    def _cargar_equipos(self):
        equipos = {}
        if not self.ruta_equipos.exists():
            return equipos
        with self.ruta_equipos.open("r", newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                equipos[fila["codigo"]] = Equipo(fila["codigo"], fila["nombre"], fila["cantidad"])
        return equipos

    def _guardar_equipos(self, equipos):
        with self.ruta_equipos.open("w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=self.campos_equipos)
            escritor.writeheader()
            for eq in equipos.values():
                escritor.writerow({"codigo": eq.codigo, "nombre": eq.nombre, "cantidad": eq.cantidad})

    def _cargar_prestamos(self):
        prestamos = []
        if not self.ruta_prestamos.exists():
            return prestamos
        with self.ruta_prestamos.open("r", newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                prestamos.append(Prestamo(fila["codigo"], fila["estudiante"], fila["fecha-prestamo"]))
        return prestamos

    def _guardar_prestamo(self, prestamo):
        necesita_encabezado = not self.ruta_prestamos.exists() or self.ruta_prestamos.stat().st_size == 0
        with self.ruta_prestamos.open("a", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=self.campos_prestamos)
            if necesita_encabezado:
                escritor.writeheader()
            escritor.writerow({
                "codigo": prestamo.codigo,
                "estudiante": prestamo.estudiante,
                "fecha-prestamo": prestamo.fecha_prestamo
            })

    def _reescribir_prestamos(self, lista_prestamos):
        with self.ruta_prestamos.open("w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=self.campos_prestamos)
            escritor.writeheader()
            for p in lista_prestamos:
                escritor.writerow({
                    "codigo": p.codigo,
                    "estudiante": p.estudiante,
                    "fecha-prestamo": p.fecha_prestamo
                })

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path


# =========================
# CONFIGURACIÓN
# =========================
RUTA_BASE = os.path.dirname(__file__)
DATA_FILE = Path(os.path.join(RUTA_BASE, "dashboard_data.json"))

UNIDADES = {
    "1": "UNIDAD 1",
    "2": "UNIDAD 2"
}

ESTADOS_TAREA = ("Pendiente", "En progreso", "Hecha")
ESTADOS_PROY = ("Activo", "Pausado", "Terminado")


# =========================
# PERSISTENCIA (JSON)
# =========================
def cargar_data():
    if not DATA_FILE.exists():
        return {"tareas": [], "proyectos": []}
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"tareas": [], "proyectos": []}


def guardar_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")


# =========================
# UTILIDADES
# =========================
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresiona Enter para continuar...")


def ahora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def mostrar_codigo(ruta_script):
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, "r", encoding="utf-8") as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {os.path.basename(ruta_script)} ---\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print("❌ El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"❌ Ocurrió un error al leer el archivo: {e}")
        return None


def ejecutar_codigo(ruta_script):
    """
    Ejecuta el script usando el mismo intérprete de Python con el que estás corriendo Dashboard.py.
    Esto evita problemas típicos de 'python' vs 'py' vs 'python3'.
    """
    try:
        python_exec = sys.executable  # ruta real del python actual

        if os.name == "nt":  # Windows: abre cmd y deja la ventana abierta
            subprocess.Popen(["cmd", "/k", python_exec, ruta_script])
        else:
            # Linux/Mac: intenta abrir terminal disponible
            # Nota: en algunos entornos puede variar, pero esto cubre casos comunes.
            terminal_cmds = [
                ["xterm", "-hold", "-e", python_exec, ruta_script],
                ["gnome-terminal", "--", python_exec, ruta_script],
                ["konsole", "-e", python_exec, ruta_script],
            ]
            for cmd in terminal_cmds:
                try:
                    subprocess.Popen(cmd)
                    return
                except FileNotFoundError:
                    continue

            # Si no hay terminal gráfica disponible, ejecútalo en la misma consola:
            print("⚠ No se encontró terminal gráfica. Ejecutando aquí mismo:\n")
            subprocess.run([python_exec, ruta_script], check=False)

    except Exception as e:
        print(f"❌ Ocurrió un error al ejecutar el código: {e}")


# =========================
# MÓDULO: GESTIÓN DE TAREAS
# =========================
def menu_tareas(data):
    while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE TAREAS (POO) ===")
        print("1) Agregar tarea")
        print("2) Listar tareas")
        print("3) Cambiar estado de una tarea")
        print("4) Eliminar tarea")
        print("0) Volver")

        op = input("Elige una opción: ").strip()

        if op == "1":
            agregar_tarea(data)
        elif op == "2":
            listar_tareas(data)
        elif op == "3":
            cambiar_estado_tarea(data)
        elif op == "4":
            eliminar_tarea(data)
        elif op == "0":
            return
        else:
            print("❌ Opción no válida.")
            pausar()


def agregar_tarea(data):
    print("\n--- Agregar tarea ---")
    titulo = input("Título: ").strip()
    descripcion = input("Descripción: ").strip()
    semana_txt = input("Semana (número): ").strip()

    if not semana_txt.isdigit():
        print("❌ Semana inválida.")
        pausar()
        return

    semana = int(semana_txt)

    tarea = {
        "titulo": titulo,
        "descripcion": descripcion,
        "semana": semana,
        "estado": "Pendiente",
        "creada_en": ahora(),
    }

    data["tareas"].append(tarea)
    guardar_data(data)
    print("✅ Tarea agregada.")
    pausar()


def listar_tareas(data):
    print("\n--- Lista de tareas ---")
    if not data["tareas"]:
        print("No hay tareas registradas.")
        pausar()
        return

    for i, t in enumerate(data["tareas"], start=1):
        print(f"{i}. [{t['estado']}] Semana {t['semana']} - {t['titulo']} (creada: {t['creada_en']})")
        print(f"   {t['descripcion']}")
    pausar()


def cambiar_estado_tarea(data):
    listar_tareas(data)
    if not data["tareas"]:
        return

    idx_txt = input("\nNúmero de tarea a cambiar: ").strip()
    if not idx_txt.isdigit():
        print("❌ Número inválido.")
        pausar()
        return

    idx = int(idx_txt)
    if idx < 1 or idx > len(data["tareas"]):
        print("❌ Índice fuera de rango.")
        pausar()
        return

    print("\nEstados disponibles:")
    for e in ESTADOS_TAREA:
        print(f"- {e}")

    nuevo = input("Nuevo estado: ").strip()
    if nuevo not in ESTADOS_TAREA:
        print("❌ Estado inválido.")
        pausar()
        return

    data["tareas"][idx - 1]["estado"] = nuevo
    guardar_data(data)
    print("✅ Estado actualizado.")
    pausar()


def eliminar_tarea(data):
    listar_tareas(data)
    if not data["tareas"]:
        return

    idx_txt = input("\nNúmero de tarea a eliminar: ").strip()
    if not idx_txt.isdigit():
        print("❌ Número inválido.")
        pausar()
        return

    idx = int(idx_txt)
    if idx < 1 or idx > len(data["tareas"]):
        print("❌ Índice fuera de rango.")
        pausar()
        return

    eliminada = data["tareas"].pop(idx - 1)
    guardar_data(data)
    print(f"✅ Tarea eliminada: {eliminada['titulo']}")
    pausar()


# =========================
# MÓDULO: GESTIÓN DE PROYECTOS
# =========================
def menu_proyectos(data):
    while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE PROYECTOS (POO) ===")
        print("1) Agregar proyecto")
        print("2) Listar proyectos")
        print("3) Cambiar estado de un proyecto")
        print("4) Eliminar proyecto")
        print("0) Volver")

        op = input("Elige una opción: ").strip()

        if op == "1":
            agregar_proyecto(data)
        elif op == "2":
            listar_proyectos(data)
        elif op == "3":
            cambiar_estado_proyecto(data)
        elif op == "4":
            eliminar_proyecto(data)
        elif op == "0":
            return
        else:
            print("❌ Opción no válida.")
            pausar()


def agregar_proyecto(data):
    print("\n--- Agregar proyecto ---")
    nombre = input("Nombre del proyecto: ").strip()
    descripcion = input("Descripción: ").strip()
    repo = input("Enlace del repo (opcional): ").strip()

    proyecto = {
        "nombre": nombre,
        "descripcion": descripcion,
        "repo_url": repo,
        "estado": "Activo",
        "creado_en": ahora(),
    }

    data["proyectos"].append(proyecto)
    guardar_data(data)
    print("✅ Proyecto agregado.")
    pausar()


def listar_proyectos(data):
    print("\n--- Lista de proyectos ---")
    if not data["proyectos"]:
        print("No hay proyectos registrados.")
        pausar()
        return

    for i, p in enumerate(data["proyectos"], start=1):
        print(f"{i}. [{p['estado']}] {p['nombre']} (creado: {p['creado_en']})")
        print(f"   {p['descripcion']}")
        if p.get("repo_url"):
            print(f"   Repo: {p['repo_url']}")
    pausar()


def cambiar_estado_proyecto(data):
    listar_proyectos(data)
    if not data["proyectos"]:
        return

    idx_txt = input("\nNúmero de proyecto a cambiar: ").strip()
    if not idx_txt.isdigit():
        print("❌ Número inválido.")
        pausar()
        return

    idx = int(idx_txt)
    if idx < 1 or idx > len(data["proyectos"]):
        print("❌ Índice fuera de rango.")
        pausar()
        return

    print("\nEstados disponibles:")
    for e in ESTADOS_PROY:
        print(f"- {e}")

    nuevo = input("Nuevo estado: ").strip()
    if nuevo not in ESTADOS_PROY:
        print("❌ Estado inválido.")
        pausar()
        return

    data["proyectos"][idx - 1]["estado"] = nuevo
    guardar_data(data)
    print("✅ Estado actualizado.")
    pausar()


def eliminar_proyecto(data):
    listar_proyectos(data)
    if not data["proyectos"]:
        return

    idx_txt = input("\nNúmero de proyecto a eliminar: ").strip()
    if not idx_txt.isdigit():
        print("❌ Número inválido.")
        pausar()
        return

    idx = int(idx_txt)
    if idx < 1 or idx > len(data["proyectos"]):
        print("❌ Índice fuera de rango.")
        pausar()
        return

    eliminado = data["proyectos"].pop(idx - 1)
    guardar_data(data)
    print(f"✅ Proyecto eliminado: {eliminado['nombre']}")
    pausar()


# =========================
# NAVEGADOR DE UNIDADES (TU CÓDIGO ORIGINAL MEJORADO)
# =========================
def mostrar_menu_principal():
    data = cargar_data()

    while True:
        limpiar_pantalla()
        print("=== Dashboard - Programación Orientada a Objetos ===\n")

        print("----- ORGANIZACIÓN -----")
        print("T) Gestionar tareas")
        print("P) Gestionar proyectos\n")

        print("----- UNIDADES -----")
        for key in UNIDADES:
            print(f"{key} - {UNIDADES[key]}")
        print("0 - Salir")

        eleccion = input("\nElige una opción: ").strip().upper()

        if eleccion == "0":
            print("Saliendo del programa.")
            break
        elif eleccion == "T":
            menu_tareas(data)
            data = cargar_data()  # recarga por seguridad
        elif eleccion == "P":
            menu_proyectos(data)
            data = cargar_data()
        elif eleccion in UNIDADES:
            ruta_unidad = os.path.join(RUTA_BASE, UNIDADES[eleccion])
            mostrar_sub_menu(ruta_unidad)
        else:
            print("❌ Opción no válida. Intenta de nuevo.")
            pausar()


def mostrar_sub_menu(ruta_unidad):
    if not os.path.exists(ruta_unidad):
        print(f"❌ No existe la carpeta: {ruta_unidad}")
        pausar()
        return

    sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]

    while True:
        limpiar_pantalla()
        print(f"=== Submenú - {os.path.basename(ruta_unidad)} ===\n")

        for i, carpeta in enumerate(sub_carpetas, start=1):
            print(f"{i} - {carpeta}")
        print("0 - Regresar")

        eleccion_carpeta = input("\nElige una subcarpeta: ").strip()

        if eleccion_carpeta == "0":
            return

        try:
            idx = int(eleccion_carpeta) - 1
            if 0 <= idx < len(sub_carpetas):
                ruta_sub = os.path.join(ruta_unidad, sub_carpetas[idx])
                mostrar_scripts(ruta_sub)
            else:
                print("❌ Opción no válida.")
                pausar()
        except ValueError:
            print("❌ Opción no válida.")
            pausar()


def mostrar_scripts(ruta_sub_carpeta):
    if not os.path.exists(ruta_sub_carpeta):
        print(f"❌ No existe la carpeta: {ruta_sub_carpeta}")
        pausar()
        return

    scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith(".py")]

    while True:
        limpiar_pantalla()
        print(f"=== Scripts en: {os.path.basename(ruta_sub_carpeta)} ===\n")

        for i, script in enumerate(scripts, start=1):
            print(f"{i} - {script}")

        print("\n0 - Regresar")
        print("9 - Menú principal")

        eleccion = input("\nElige un script: ").strip()

        if eleccion == "0":
            return
        if eleccion == "9":
            return

        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(scripts):
                ruta_script = os.path.join(ruta_sub_carpeta, scripts[idx])
                codigo = mostrar_codigo(ruta_script)
                if codigo:
                    ejecutar = input("\n¿Deseas ejecutar el script? (1: Sí, 0: No): ").strip()
                    if ejecutar == "1":
                        ejecutar_codigo(ruta_script)
                    else:
                        print("No se ejecutó el script.")
                    pausar()
            else:
                print("❌ Opción no válida.")
                pausar()
        except ValueError:
            print("❌ Opción no válida.")
            pausar()


# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    mostrar_menu_principal()

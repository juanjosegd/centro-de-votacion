import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

jurados_data = []
votantes_data = []
asistencia_data = []
resultados_data = pd.DataFrame()  # inicializado como DataFrame vacío

cedulas_jurados = set()
cedulas_votantes = set()
cedulas_asistencia = set()

def validar_entrada():
    try:
        salones = int(entry_salones.get())
        mesas = int(entry_mesas.get())
        jurados = int(entry_jurados.get())
        if salones <= 0 or mesas <= 0 or jurados <= 0:
            raise ValueError
        return salones, mesas, jurados
    except ValueError:
        messagebox.showerror("Error", "Ingrese solo números enteros positivos.")
        return None

def generar_estructura():
    global jurados_data, cedulas_jurados
    datos = validar_entrada()
    if not datos:
        return
    salones, mesas, jurados = datos
    jurados_data = [[[] for _ in range(mesas)] for _ in range(salones)]
    cedulas_jurados.clear()

    for widget in frame_structure.winfo_children():
        widget.destroy()

    for s in range(salones):
        frame_salon = tk.LabelFrame(frame_structure, text="Salón " + str(s+1))
        frame_salon.pack(padx=5, pady=5, fill="x")

        for m in range(mesas):
            frame_mesa = tk.LabelFrame(frame_salon, text="Mesa " + str(m+1))
            frame_mesa.pack(padx=5, pady=5, fill="x")

            btn_mesa = tk.Button(frame_mesa, text="Consultar Mesa " + str(m+1), command=lambda s=s, m=m: mostrar_mesa(s, m))
            btn_mesa.pack(side="left")

            for j in range(jurados):
                btn_jurado = tk.Button(frame_mesa, text="Jurado " + str(j+1), command=lambda s=s, m=m, j=j: registrar_jurado(s, m, j))
                btn_jurado.pack(side="left")

def registrar_jurado(salon, mesa, jurado):
    ventana = tk.Toplevel()
    ventana.title("Registrar Jurado")

    labels = ["Nombre", "Cédula", "Teléfono", "Dirección"]
    entradas = []

    for lbl in labels:
        tk.Label(ventana, text=lbl).pack()
        e = tk.Entry(ventana)
        e.pack()
        entradas.append(e)

    def guardar():
        datos = [e.get().strip() for e in entradas]
        if "" in datos:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if datos[1] in cedulas_jurados:
            messagebox.showerror("Error", "La cédula ya está registrada para un jurado.")
            return
        jurados_data[salon][mesa].append(datos)
        cedulas_jurados.add(datos[1])
        messagebox.showinfo("Éxito", "Jurado guardado.")
        ventana.destroy()

    tk.Button(ventana, text="Guardar", command=guardar).pack()

def mostrar_mesa(salon, mesa):
    texto = ""
    lista_jurados = jurados_data[salon][mesa]
    if lista_jurados:
        texto += "Jurados:\n"
        for j in lista_jurados:
            texto += f"Nombre: {j[0]}, Cédula: {j[1]}, Tel: {j[2]}, Dir: {j[3]}\n"
    else:
        texto += "Sin jurados registrados.\n"

    lista_votantes = [v for v in votantes_data if v[2] == f"Salón {salon+1}" and v[3] == f"Mesa {mesa+1}"]

    if lista_votantes:
        texto += "Votantes:\n"
        for v in lista_votantes:
            texto += f"Nombre: {v[0]}, Cédula: {v[1]}\n"
    else:
        texto += "Sin votantes registrados."

    messagebox.showinfo("Mesa", texto)

def guardar_datos():
    try:
        with open("estructura.txt", "w") as f:
            f.write(str(jurados_data))
        messagebox.showinfo("Guardado", "Datos guardados en estructura.txt")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")

def cargar_votantes():
    global votantes_data, cedulas_votantes
    archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not archivo:
        return
    try:
        with open(archivo, newline='') as csvfile:
            lector = csv.DictReader(csvfile)
            votantes_data.clear()
            cedulas_votantes.clear()
            for row in lector:
                if row['cedula'] in cedulas_votantes:
                    messagebox.showerror("Error", f"Cédula duplicada en votantes: {row['cedula']}")
                    return
                cedulas_votantes.add(row['cedula'])
                votantes_data.append([row['nombre'], row['cedula'], row['salon'], row['mesa']])
        messagebox.showinfo("Carga completa", "Votantes cargados.")
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando votantes: {e}")

def buscar_cedula():
    cedula = entry_buscar.get().strip()
    if not cedula:
        messagebox.showerror("Error", "Ingrese una cédula.")
        return

    for s in range(len(jurados_data)):
        for m in range(len(jurados_data[s])):
            for j in jurados_data[s][m]:
                if j[1] == cedula:
                    messagebox.showinfo("Jurado encontrado", f"Nombre: {j[0]}, Salón: {s+1}, Mesa: {m+1}")
                    return

    for v in votantes_data:
        if v[1] == cedula:
            messagebox.showinfo("Votante encontrado", f"Nombre: {v[0]}, Salón: {v[2]}, Mesa: {v[3]}")
            return

    messagebox.showinfo("No encontrado", "Cédula no encontrada.")

def registrar_asistencia():
    ventana = tk.Toplevel()
    ventana.title("Registrar Asistencia")

    labels = ["Cédula", "Salón", "Mesa", "Fecha (YYYY-MM-DD)"]
    entradas = []

    for lbl in labels:
        tk.Label(ventana, text=lbl).pack()
        e = tk.Entry(ventana)
        e.pack()
        entradas.append(e)

    def guardar():
        datos = [e.get().strip() for e in entradas]
        if "" in datos:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        cedula, salon, mesa, fecha = datos
        # Validar formato fecha
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD.")
            return
        if cedula in cedulas_asistencia:
            messagebox.showerror("Error", "Esta cédula ya registró asistencia.")
            return
        cedulas_asistencia.add(cedula)
        asistencia_data.append(datos)
        messagebox.showinfo("Éxito", "Asistencia registrada.")
        ventana.destroy()

    tk.Button(ventana, text="Guardar", command=guardar).pack()

def cargar_resultados_json():
    global resultados_data
    archivo = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not archivo:
        return
    try:
        with open(archivo, "r") as f:
            datos = json.load(f)
        # Convertimos a DataFrame para mantener compatibilidad
        resultados_data = pd.DataFrame(datos)
        # Validar que tenga columnas correctas
        if not all(c in resultados_data.columns for c in ["candidato", "votos"]):
            messagebox.showerror("Error", "JSON de resultados debe tener campos 'candidato' y 'votos'.")
            resultados_data = pd.DataFrame()  # limpiar
            return
        messagebox.showinfo("Carga completa", "Resultados JSON cargados.")
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando resultados JSON: {e}")

def mostrar_estadisticas():
    if resultados_data is None or resultados_data.empty:
        messagebox.showerror("Error", "No hay resultados cargados.")
        return

    ventana = tk.Toplevel()
    ventana.title("Estadísticas")

    # Mostrar tabla de resultados
    text = tk.Text(ventana, width=50, height=10)
    text.pack()
    text.insert(tk.END, resultados_data.to_string(index=False))

    # Mostrar gráfico de barras
    plt.figure(figsize=(6,4))
    plt.bar(resultados_data['candidato'], resultados_data['votos'], color='skyblue')
    plt.xlabel('Candidato')
    plt.ylabel('Votos')
    plt.title('Resultados Elección')
    plt.tight_layout()

    # Guardar gráfico temporal y mostrar en ventana
    plt.savefig("resultados.png")
    plt.close()

    img = tk.PhotoImage(file="resultados.png")
    label_img = tk.Label(ventana, image=img)
    label_img.image = img  # Referencia para evitar garbage collection
    label_img.pack()

# Código principal
root = tk.Tk()
root.title("Centro de Votación")

# Entradas y etiquetas
tk.Label(root, text="Número de Salones").pack()
entry_salones = tk.Entry(root)
entry_salones.pack()

tk.Label(root, text="Número de Mesas por Salón").pack()
entry_mesas = tk.Entry(root)
entry_mesas.pack()

tk.Label(root, text="Número de Jurados por Mesa").pack()
entry_jurados = tk.Entry(root)
entry_jurados.pack()

tk.Button(root, text="Generar Estructura", command=generar_estructura).pack(pady=5)
tk.Button(root, text="Guardar Datos Jurados", command=guardar_datos).pack(pady=5)
tk.Button(root, text="Cargar Votantes CSV", command=cargar_votantes).pack(pady=5)
tk.Button(root, text="Registrar Asistencia", command=registrar_asistencia).pack(pady=5)
tk.Button(root, text="Cargar Resultados JSON", command=cargar_resultados_json).pack(pady=5)
tk.Button(root, text="Mostrar Estadísticas", command=mostrar_estadisticas).pack(pady=5)

tk.Label(root, text="Buscar por Cédula").pack()
entry_buscar = tk.Entry(root)
entry_buscar.pack()
tk.Button(root, text="Buscar", command=buscar_cedula).pack(pady=5)

frame_structure = tk.Frame(root)
frame_structure.pack(fill="both", expand=True)

root.mainloop()

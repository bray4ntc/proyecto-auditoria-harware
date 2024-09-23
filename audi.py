import psutil
import csv
import os
import socket  # Importar la biblioteca socket
from tkinter import *
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Función para obtener la información del hardware
def obtener_info_hardware():
    info = {
        "CPU": {
            "Núcleos físicos": psutil.cpu_count(logical=False),
            "Núcleos lógicos": psutil.cpu_count(logical=True),
            "Frecuencia actual": f"{psutil.cpu_freq().current} MHz",
            "Uso de CPU (%)": f"{psutil.cpu_percent(interval=1)}%"
        },
        "Memoria RAM": {
            "Total": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
            "Disponible": f"{psutil.virtual_memory().available / (1024 ** 3):.2f} GB",
            "Uso (%)": f"{psutil.virtual_memory().percent}%"
        },
        "Discos": [],
        "Red": []
    }

    # Información de discos
    for part in psutil.disk_partitions():
        disco_info = psutil.disk_usage(part.mountpoint)
        info["Discos"].append({
            "Dispositivo": part.device,
            "Punto de montaje": part.mountpoint,
            "Sistema de archivos": part.fstype,
            "Espacio total": f"{disco_info.total / (1024 ** 3):.2f} GB",
            "Espacio usado": f"{disco_info.used / (1024 ** 3):.2f} GB",
            "Espacio disponible": f"{disco_info.free / (1024 ** 3):.2f} GB",
            "Uso (%)": f"{disco_info.percent}%"
        })

    # Información de red
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # Usar socket.AF_INET
                info["Red"].append({
                    "Interfaz": iface,
                    "Dirección IP": addr.address,
                    "Máscara de subred": addr.netmask
                })

    return info

# Función para guardar los resultados en CSV
def guardar_informe_csv(info, nombre_archivo="informe_hardware.csv"):
    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Categoría", "Subcategoría", "Valor"])
        
        # CPU
        for clave, valor in info["CPU"].items():
            writer.writerow(["CPU", clave, valor])
        
        # Memoria RAM
        for clave, valor in info["Memoria RAM"].items():
            writer.writerow(["Memoria RAM", clave, valor])
        
        # Discos
        for disco in info["Discos"]:
            writer.writerow(["Disco", "Dispositivo", disco["Dispositivo"]])
            writer.writerow(["", "Punto de montaje", disco["Punto de montaje"]])
            writer.writerow(["", "Sistema de archivos", disco["Sistema de archivos"]])
            writer.writerow(["", "Espacio total", disco["Espacio total"]])
            writer.writerow(["", "Espacio usado", disco["Espacio usado"]])
            writer.writerow(["", "Espacio disponible", disco["Espacio disponible"]])
            writer.writerow(["", "Uso (%)", disco["Uso (%)"]])

        # Red
        for red in info["Red"]:
            writer.writerow(["Red", "Interfaz", red["Interfaz"]])
            writer.writerow(["", "Dirección IP", red["Dirección IP"]])
            writer.writerow(["", "Máscara de subred", red["Máscara de subred"]])

# Función para generar un informe en PDF
def guardar_informe_pdf(info, nombre_archivo="informe_hardware.pdf"):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 50, "Informe de Auditoría de Hardware")
    
    y = height - 100

    # CPU
    c.drawString(100, y, "CPU:")
    y -= 20
    for clave, valor in info["CPU"].items():
        c.drawString(120, y, f"{clave}: {valor}")
        y -= 20
    
    # Memoria RAM
    c.drawString(100, y, "Memoria RAM:")
    y -= 20
    for clave, valor in info["Memoria RAM"].items():
        c.drawString(120, y, f"{clave}: {valor}")
        y -= 20

    # Discos
    for disco in info["Discos"]:
        c.drawString(100, y, f"Disco {disco['Dispositivo']}:")
        y -= 20
        c.drawString(120, y, f"Espacio total: {disco['Espacio total']}, Uso: {disco['Uso (%)']}")
        y -= 20

    # Red
    c.drawString(100, y, "Red:")
    y -= 20
    for red in info["Red"]:
        c.drawString(120, y, f"{red['Interfaz']}: {red['Dirección IP']} / {red['Máscara de subred']}")
        y -= 20
    
    c.save()

# Función para mostrar la información en la interfaz gráfica
def mostrar_info_hardware():
    info = obtener_info_hardware()
    text_info.delete(1.0, END)
    text_info.insert(END, "CPU:\n")
    for clave, valor in info["CPU"].items():
        text_info.insert(END, f"  {clave}: {valor}\n")

    text_info.insert(END, "\nMemoria RAM:\n")
    for clave, valor in info["Memoria RAM"].items():
        text_info.insert(END, f"  {clave}: {valor}\n")

    text_info.insert(END, "\nDiscos:\n")
    for disco in info["Discos"]:
        text_info.insert(END, f"  {disco['Dispositivo']}:\n")
        text_info.insert(END, f"    Espacio total: {disco['Espacio total']} - Uso: {disco['Uso (%)']}\n")
    
    text_info.insert(END, "\nRed:\n")
    for red in info["Red"]:
        text_info.insert(END, f"  {red['Interfaz']}: {red['Dirección IP']} / {red['Máscara de subred']}\n")

# Función para generar informe CSV
def generar_csv():
    info = obtener_info_hardware()
    guardar_informe_csv(info)
    messagebox.showinfo("Informe CSV", "El informe CSV se ha generado correctamente.")

# Función para generar informe PDF
def generar_pdf():
    info = obtener_info_hardware()
    guardar_informe_pdf(info)
    messagebox.showinfo("Informe PDF", "El informe PDF se ha generado correctamente.")

# Crear la interfaz gráfica
root = Tk()
root.title("Auditoría de Hardware")

frame = Frame(root)
frame.pack(pady=20)

btn_mostrar_info = Button(frame, text="Mostrar Información de Hardware", command=mostrar_info_hardware)
btn_mostrar_info.pack(side=LEFT, padx=10)

btn_generar_csv = Button(frame, text="Generar Informe CSV", command=generar_csv)
btn_generar_csv.pack(side=LEFT, padx=10)

btn_generar_pdf = Button(frame, text="Generar Informe PDF", command=generar_pdf)
btn_generar_pdf.pack(side=LEFT, padx=10)

text_info = Text(root, height=20, width=80)
text_info.pack(pady=20)

root.mainloop()

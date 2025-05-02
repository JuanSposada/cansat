import serial
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configura el puerto serie
ser = serial.Serial('COM3', 9600)  # Cambia 'COM3' por el puerto correspondiente en tu sistema 
#en linux ejecutar : ls /dev/tty* para ubicar el puerto

fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

# Conexión a SQLite
conn = sqlite3.connect(f'telemetria_serial_{fecha}.db', check_same_thread=False)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS telemetria{fecha} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        temperatura REAL,
        altitud REAL,
        co2 REAL,
        co REAL
    )
''')
conn.commit()

# Datos para graficar
tiempos, temperaturas, altitudes, co2s, cos = [], [], [], [], []

def leer_serial_guardar():
    try:
        linea = ser.readline().decode('utf-8').strip()
        if linea:
            datos = linea.split(',')
            if len(datos) == 4:
                temperatura = float(datos[0])
                altitud = float(datos[1])
                co2 = float(datos[2])
                co = float(datos[3])
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Insertar en SQLite
                cursor.execute('''
                    INSERT INTO telemetria (timestamp, temperatura, altitud, co2, co)
                    VALUES (?, ?, ?, ?, ?)
                ''', (timestamp, temperatura, altitud, co2, co))
                conn.commit()

                # Añadir a listas
                tiempos.append(timestamp)
                temperaturas.append(temperatura)
                altitudes.append(altitud)
                co2s.append(co2)
                cos.append(co)

                # Limitar longitud
                if len(tiempos) > 30:
                    tiempos.pop(0)
                    temperaturas.pop(0)
                    altitudes.pop(0)
                    co2s.pop(0)
                    cos.pop(0)
    except Exception as e:
        print("Error:", e)

# Función para animar la gráfica
def actualizar_grafica(i):
    leer_serial_guardar()
    ax1.clear()
    ax1.plot(tiempos, temperaturas, label='Temperatura (°C)', color='red')
    ax1.plot(tiempos, altitudes, label='Altitud (m)', color='blue')
    ax1.plot(tiempos, co2s, label='CO2 (ppm)', color='green')
    ax1.plot(tiempos, cos, label='CO (ppm)', color='purple')
    ax1.set_xticklabels(tiempos, rotation=45, ha='right')
    ax1.legend()
    ax1.set_title("Telemetría en tiempo real")
    ax1.set_ylabel("Valores")
    ax1.grid(True)

# Configurar gráfico
fig, ax1 = plt.subplots()
ani = animation.FuncAnimation(fig, actualizar_grafica, interval=1000)
plt.tight_layout()
plt.show()

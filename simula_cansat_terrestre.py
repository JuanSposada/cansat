import sqlite3
import random
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Conexión a SQLite
conn = sqlite3.connect('telemetria.db', check_same_thread=False)
cursor = conn.cursor()

fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
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

tiempos, temperaturas, altitudes, co2s, cos = [], [], [], [], []

def simular_datos_guardar():
    temperatura = round(random.uniform(20.0, 30.0), 1)
    altitud = round(random.uniform(1000, 3000), 1)
    co2 = random.randint(400, 1000)
    co = random.randint(1, 20)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO telemetria (timestamp, temperatura, altitud, co2, co)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, temperatura, altitud, co2, co))
    conn.commit()

    tiempos.append(timestamp)
    temperaturas.append(temperatura)
    altitudes.append(altitud)
    co2s.append(co2)
    cos.append(co)

    if len(tiempos) > 30:
        tiempos.pop(0)
        temperaturas.pop(0)
        altitudes.pop(0)
        co2s.pop(0)
        cos.pop(0)

def actualizar_grafica(i):
    simular_datos_guardar()
    ax1.clear()
    ax1.plot(tiempos, temperaturas, label='Temperatura (°C)', color='red')
    ax1.plot(tiempos, altitudes, label='Altitud (m)', color='blue')
    ax1.plot(tiempos, co2s, label='CO2 (ppm)', color='green')
    ax1.plot(tiempos, cos, label='CO (ppm)', color='purple')
    ax1.set_xticklabels(tiempos, rotation=45, ha='right')
    ax1.legend()
    ax1.set_title("Telemetría simulada en tiempo real")
    ax1.set_ylabel("Valores")
    ax1.grid(True)

fig, ax1 = plt.subplots()
ani = animation.FuncAnimation(fig, actualizar_grafica, interval=1000)
plt.tight_layout()
plt.show()

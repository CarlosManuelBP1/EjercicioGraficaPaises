import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

# Cargar datos
df = pd.read_csv("temperaturas.csv")

# Crear figura y eje
fig, ax = plt.subplots()
ax.set_xlim(0, df['dia'].max())
ax.set_ylim(df['temperatura'].min() - 2, df['temperatura'].max() + 2)
line, = ax.plot([], [], 'o-', lw=2)
text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

# Inicialización
def init():
    line.set_data([], [])
    text.set_text('')
    return line, text

# Actualización para cada frame
def update(frame):
    x = df['dia'][:frame+1]
    y = df['temperatura'][:frame+1]
    line.set_data(x, y)
    text.set_text(f'Día {df["dia"].iloc[frame]}, Temp: {df["temperatura"].iloc[frame]}°C')
    return line, text

# Crear animación
ani = FuncAnimation(fig, update, frames=len(df), init_func=init, blit=True, interval=800)

# Guardar como GIF
ani.save("temperaturas_animadas.gif", writer="pillow", fps=1)

# Mostrar (opcional)
# plt.show()
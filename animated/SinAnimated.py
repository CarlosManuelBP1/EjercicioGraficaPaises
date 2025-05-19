import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Crear figura y eje
fig, ax = plt.subplots()
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)
line, = ax.plot([], [], lw=2)

# Datos fijos del eje X
x = np.linspace(0, 2 * np.pi, 1000)

# Inicialización del gráfico
def init():
    line.set_data([], [])
    return line,

# Función de actualización para animar el seno
def update(frame):
    y = np.sin(x + 0.1 * frame)
    line.set_data(x, y)
    return line,

# Crear la animación
ani = FuncAnimation(fig, update, frames=200, init_func=init, blit=True, interval=20)

ani.save("seno_animado.gif", writer="pillow", fps=30)

# Mostrar la animación
plt.title("Animación de la función Seno")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.grid(True)
plt.show()

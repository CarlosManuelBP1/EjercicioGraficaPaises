import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

paramPais = ""
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/gifs", StaticFiles(directory="."), name="gifs")

@app.get("/")
def read_root():
    return {"message": "Hola mundo, servicio activo"}

@app.get("/graficos/{pais}")
def saludo(pais: str):
    df = pd.read_csv("01 renewable-share-energy.csv")
    # Normaliza los nombres para comparar sin importar mayúsculas/minúsculas
    paises_disponibles = df["Entity"].unique()
    paises_dict = {p.lower(): p for p in paises_disponibles}
    pais_normalizado = pais.lower()

    if pais_normalizado not in paises_dict:
        return {"error": f"País '{pais}' no encontrado. Prueba con uno de: {', '.join(paises_disponibles)}"}

    pais_real = paises_dict[pais_normalizado]
    df_pais = df[df["Entity"] == pais_real].copy()

    years = df_pais["Year"].values
    renewables = df_pais["Renewables (% equivalent primary energy)"].values

    if len(years) == 0 or len(renewables) == 0:
        return {"error": f"No hay datos para el país '{pais_real}'."}

    fig, ax = plt.subplots()
    ax.set_xlim(years.min(), years.max())
    ax.set_ylim(0, max(renewables) + 5)
    ax.set_title(f"Energía Renovable en {pais_real} (1965 en adelante)")
    ax.set_xlabel("Año")
    ax.set_ylabel("Renovables (% energía primaria)")
    ax.grid(True)
    line, = ax.plot([], [], lw=2, color='green')
    text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    def init():
        line.set_data([], [])
        text.set_text('')
        return line, text

    def update(frame):
        x = years[:frame+1]
        y = renewables[:frame+1]
        line.set_data(x, y)
        text.set_text(f"Año: {x[-1]}, Renovables: {y[-1]:.2f}%")
        return line, text

    ani = FuncAnimation(fig, update, frames=len(years), init_func=init, blit=True, interval=150)
    nameImage = pais_real + "_renewables.gif"
    ani.save(nameImage, writer="pillow", fps=5)
    return {"mensaje": f"Grafico Generado para {pais_real}"}
 
@app.get("/paises")
def paises():
    df = pd.read_csv("01 renewable-share-energy.csv")    
    paises = df["Entity"].unique()
    return paises.tolist()
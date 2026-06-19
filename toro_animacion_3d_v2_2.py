import numpy as np
import plotly.graph_objects as go

print("Generando Animación 3D v2 con Puntos Clasificados...")

# 1. Parámetros del Toro
R_major = 5
r_minor = 1.5

def mapear(x_mod, y_mod):
    v_ang = 2 * np.pi * (x_mod / 13.0)
    u_ang = 2 * np.pi * (y_mod / 20.0)
    X = (R_major + r_minor * np.cos(u_ang)) * np.cos(v_ang)
    Y = (R_major + r_minor * np.cos(u_ang)) * np.sin(v_ang)
    Z = r_minor * np.sin(u_ang)
    return X, Y, Z

# 2. Trayectoria para la animación (261 puntos para cerrar el lazo)
n_vals = np.arange(1, 262)
u_mod = n_vals % 13
v_mod = n_vals % 20
X_traj, Y_traj, Z_traj = mapear(u_mod, v_mod)

fig = go.Figure()

# --- TRAZO 0: Superficie del Toro estática ---
u_toro = np.linspace(0, 2*np.pi, 80)
v_toro = np.linspace(0, 2*np.pi, 80)
U_grid, V_grid = np.meshgrid(u_toro, v_toro)
X_surf = (R_major + r_minor * np.cos(U_grid)) * np.cos(V_grid)
Y_surf = (R_major + r_minor * np.cos(U_grid)) * np.sin(V_grid)
Z_surf = r_minor * np.sin(U_grid)

fig.add_trace(go.Surface(
    x=X_surf, y=Y_surf, z=Z_surf,
    opacity=0.2,
    colorscale='Blues',
    showscale=False,
    hoverinfo='skip',
    name='Toro'
))

# --- CLASIFICACIÓN DE LOS 260 PUNTOS ---
# Listas para cada categoría
categorías = {
    'distinguidos': {'x': [], 'y': [], 'z': [], 'text': [], 'hover': [], 'color': '#F1C40F', 'symbol': 'diamond', 'size': 11, 'name': 'Punto Distinguido (1, x)'},
    'familia_1_r': {'x': [], 'y': [], 'z': [], 'text': [], 'hover': [], 'color': '#FF7675', 'symbol': 'circle', 'size': 8, 'name': 'Elemento (1, r)'},
    'familia_q_1': {'x': [], 'y': [], 'z': [], 'text': [], 'hover': [], 'color': '#00CEC9', 'symbol': 'circle', 'size': 8, 'name': 'Elemento (q, 1)'},
    'base': {'x': [], 'y': [], 'z': [], 'text': [], 'hover': [], 'color': '#4B5563', 'symbol': 'circle', 'size': 5, 'name': 'Punto Base (q, r)'}
}

for n in range(1, 261):
    q = n % 13
    r = n % 20
    X, Y, Z = mapear(q, r)
    label = f"({q},{r})"
    hover_info = f"Día n: <b>{n}</b><br>Coordenadas: <b>({q}, {r})</b>"
    
    if q == 1 and r in [1, 13, 5, 17, 9]:
        categorías['distinguidos']['x'].append(X)
        categorías['distinguidos']['y'].append(Y)
        categorías['distinguidos']['z'].append(Z)
        categorías['distinguidos']['text'].append(label)
        categorías['distinguidos']['hover'].append(hover_info + "<br>Tipo: <b>Distinguido (1, x)</b>")
    elif q == 1:
        categorías['familia_1_r']['x'].append(X)
        categorías['familia_1_r']['y'].append(Y)
        categorías['familia_1_r']['z'].append(Z)
        categorías['familia_1_r']['text'].append(label)
        categorías['familia_1_r']['hover'].append(hover_info + "<br>Tipo: <b>Familia (1, r)</b>")
    elif r == 1:
        categorías['familia_q_1']['x'].append(X)
        categorías['familia_q_1']['y'].append(Y)
        categorías['familia_q_1']['z'].append(Z)
        categorías['familia_q_1']['text'].append(label)
        categorías['familia_q_1']['hover'].append(hover_info + "<br>Tipo: <b>Familia (q, 1)</b>")
    else:
        categorías['base']['x'].append(X)
        categorías['base']['y'].append(Y)
        categorías['base']['z'].append(Z)
        categorías['base']['text'].append(label)
        categorías['base']['hover'].append(hover_info + "<br>Tipo: <b>Base (q, r)</b>")

# Agregar los traces de los 260 puntos al gráfico
# Indices de traces:
# 1: Puntos Base
# 2: Familia (1, r)
# 3: Familia (q, 1)
# 4: Puntos Distinguidos
for cat_key in ['base', 'familia_1_r', 'familia_q_1', 'distinguidos']:
    cat = categorías[cat_key]
    line_dict = dict(color='white', width=1) if cat_key != 'base' else dict(color='black', width=0.5)
    
    fig.add_trace(go.Scatter3d(
        x=cat['x'], y=cat['y'], z=cat['z'],
        mode='markers', # Iniciamos en modo solo marcadores (limpio)
        marker=dict(
            size=cat['size'],
            color=cat['color'],
            symbol=cat['symbol'],
            line=line_dict
        ),
        text=cat['text'],
        textposition="top center",
        textfont=dict(color='#0F172A', size=9, family='Arial'),
        hovertext=cat['hover'],
        hoverinfo='text',
        name=cat['name']
    ))

# --- TRAZO 5: Rastro (Trail) animado ---
fig.add_trace(go.Scatter3d(
    x=[X_traj[0]], y=[Y_traj[0]], z=[Z_traj[0]],
    mode='lines',
    line=dict(color='yellow', width=4),
    opacity=0.8,
    name='Trayectoria',
    hoverinfo='skip'
))

# --- TRAZO 6: Generador Activo (Tracer) animado ---
fig.add_trace(go.Scatter3d(
    x=[X_traj[0]], y=[Y_traj[0]], z=[Z_traj[0]],
    mode='markers+text',
    marker=dict(
        size=10,
        color='red',
        symbol='circle',
        line=dict(color='black', width=1)
    ),
    text=["(1,1)"],
    textposition="top center",
    textfont=dict(color='red', size=12, family='Arial Black'),
    name='Generador Activo',
    hoverinfo='skip'
))

# --- CONTROL DE ANIMACIÓN Y SLIDERS ---
frames = []
for k in range(1, len(n_vals)):
    q = k % 13
    r = k % 20
    frame_data = [
        go.Scatter3d(x=X_traj[:k], y=Y_traj[:k], z=Z_traj[:k]),
        go.Scatter3d(x=[X_traj[k-1]], y=[Y_traj[k-1]], z=[Z_traj[k-1]], text=[f"({q},{r})"])
    ]
    frame = go.Frame(data=frame_data, traces=[5, 6], name=str(k))
    frames.append(frame)

fig.frames = frames

updatemenus = [
    # 1. Controles de Reproducción (Play/Pause)
    dict(
        type="buttons",
        buttons=[
            dict(label="► Play", method="animate", args=[None, dict(frame=dict(duration=300, redraw=True), fromcurrent=True, transition=dict(duration=0))]),
            dict(label="⏸ Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate", transition=dict(duration=0))])
        ],
        direction="left", pad={"r": 10, "t": 10}, showactive=False,
        x=0.15, y=1.1, xanchor="right", yanchor="top"
    ),
    # 2. Controles de Visualización de Etiquetas (Toggle Text Labels)
    dict(
        type="buttons",
        buttons=[
            dict(
                label="Ocultar Coordenadas (q,r)",
                method="restyle",
                args=[{"mode": "markers"}, [1, 2, 3, 4]]
            ),
            dict(
                label="Mostrar Solo Destacados",
                method="restyle",
                args=[
                    {"mode": ["markers", "markers+text", "markers+text", "markers+text"]},
                    [1, 2, 3, 4]
                ]
            ),
            dict(
                label="Mostrar Todas las Coordenadas",
                method="restyle",
                args=[{"mode": "markers+text"}, [1, 2, 3, 4]]
            )
        ],
        direction="down", pad={"r": 10, "t": 10}, showactive=True,
        x=0.95, y=1.1, xanchor="right", yanchor="top"
    )
]

sliders = [dict(
    active=0, yanchor="top", xanchor="left",
    currentvalue=dict(font=dict(size=14, color='#0F172A'), prefix="Día Actual (n): ", visible=True, xanchor="right"),
    transition=dict(duration=0), pad=dict(b=10, t=50), len=0.9, x=0.05, y=0,
    steps=[dict(args=[[str(k)], dict(frame=dict(duration=0, redraw=True), mode="immediate", transition=dict(duration=0))], label=str(k), method="animate") for k in range(1, len(n_vals))]
)]

# Actualizar el diseño general
fig.update_layout(
    title=dict(
        text='Toro Interactivo 3D: Modelo (q, r) en ℤ₁₃ × ℤ₂₀',
        font=dict(size=20, color='#0F172A', family='Arial'),
        x=0.5, y=0.98
    ),
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        bgcolor='white',
        aspectmode='data'
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    width=1100, height=850,
    margin=dict(l=10, r=10, b=10, t=60),
    updatemenus=updatemenus,
    sliders=sliders,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.05,
        xanchor="center",
        x=0.5,
        font=dict(color='#0F172A')
    )
)

fig.write_html("toro_animacion_3d_v2_2.html")
print("¡toro_animacion_3d_v2_2.html creado exitosamente!")

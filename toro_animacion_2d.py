import numpy as np
import plotly.graph_objects as go

print("Generando Animación 2D...")

n_vals = np.arange(1, 262)
u = n_vals % 13
v = n_vals % 20

sucesion = [13, 20, 52, 65, 260, 361, 362, 363, 364, 365, 366, 584, 18980]
colores_sucesion = {
    13: '#FF6B6B', 20: '#4ECDC4', 52: '#45B7D1', 65: '#96CEB4',
    260: '#FFD700', 361: '#FFA07A', 362: '#FA8072', 363: '#E9967A',
    364: '#DDA0DD', 365: '#FF69B4', 366: '#8A2BE2', 584: '#FF8C00', 18980: '#00FF00'
}

fig = go.Figure()

# Trazos estáticos (Hitos)
for n_destacado in sucesion:
    x_d = n_destacado % 13
    y_d = n_destacado % 20
    color = colores_sucesion.get(n_destacado, 'black')
    size = 18 if n_destacado == 260 or n_destacado == 18980 else 12
    symbol = 'star' if n_destacado == 260 or n_destacado == 18980 else 'circle'
    
    fig.add_trace(go.Scatter(
        x=[x_d], y=[y_d],
        mode='markers',
        marker=dict(size=size, color='white', symbol=symbol, line=dict(color=color, width=2)),
        hovertext=[f"Hito: {n_destacado}"],
        hoverinfo='text',
        name=f"Hito {n_destacado}",
        showlegend=False
    ))

# Trazo 1: El rastro normal (Rojo)
fig.add_trace(go.Scatter(
    x=[u[0]], y=[v[0]],
    mode='lines+markers',
    line=dict(color='red', width=2),
    marker=dict(size=4, color='red'),
    name='Trayectoria Continua',
    hoverinfo='skip'
))

# Trazo 2: Los saltos de envoltura (Gris)
fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='lines',
    line=dict(color='gray', width=1, dash='dash'),
    name='Saltos (Wrap-around)',
    hoverinfo='skip'
))

# Trazo 3: El generador activo (Tracer)
fig.add_trace(go.Scatter(
    x=[u[0]], y=[v[0]],
    mode='markers+text',
    marker=dict(size=16, color='red', line=dict(color='black', width=2), symbol='diamond'),
    text=["n=1"],
    textposition="top center",
    textfont=dict(size=14, color='black'),
    name='Generador Activo',
    hoverinfo='skip'
))

# Generar Frames
frames = []
for k in range(1, len(n_vals)):
    u_k = u[:k]
    v_k = v[:k]
    
    ur, vr = [u_k[0]], [v_k[0]]
    ug, vg = [None], [None]
    
    for i in range(1, len(u_k)):
        up, vp = u_k[i-1], v_k[i-1]
        uc, vc = u_k[i], v_k[i]
        if abs(uc - up) > 1 or abs(vc - vp) > 1:
            # Salto (Wrap-around)
            ug.extend([up, uc, None])
            vg.extend([vp, vc, None])
            ur.extend([None, uc])
            vr.extend([None, vc])
        else:
            # Continuo
            ur.append(uc)
            vr.append(vc)
            
    frame_data = [
        go.Scatter(x=ur, y=vr), # Trail Red
        go.Scatter(x=ug, y=vg), # Trail Gray
        go.Scatter(x=[u[k-1]], y=[v[k-1]], text=[f"n={k}"]) # Tracer
    ]
    frame = go.Frame(data=frame_data, traces=[len(fig.data)-3, len(fig.data)-2, len(fig.data)-1], name=str(k))
    frames.append(frame)

fig.frames = frames

# Botones y Slider
updatemenus = [dict(
    type="buttons",
    buttons=[
        dict(label="► Play", method="animate", args=[None, dict(frame=dict(duration=150, redraw=False), fromcurrent=True, transition=dict(duration=0))]),
        dict(label="⏸ Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate", transition=dict(duration=0))])
    ],
    direction="left",
    pad={"r": 10, "t": 10},
    showactive=False,
    x=0.1, y=1.1, xanchor="right", yanchor="top"
)]

sliders = [dict(
    active=0,
    yanchor="top",
    xanchor="left",
    currentvalue=dict(font=dict(size=16), prefix="Día Actual: ", visible=True, xanchor="right"),
    transition=dict(duration=0),
    pad=dict(b=10, t=50),
    len=0.9,
    x=0.1, y=0,
    steps=[dict(args=[[str(k)], dict(frame=dict(duration=0, redraw=False), mode="immediate", transition=dict(duration=0))], label=str(k), method="animate") for k in range(1, len(n_vals))]
)]

fig.update_layout(
    title='Animación Interactiva 2D: Trayectoria del Generador (Estándar)',
    xaxis=dict(title='Módulo 13 (u)', tickmode='linear', dtick=1, range=[-1, 13], showgrid=True, gridcolor='lightgray', zeroline=False),
    yaxis=dict(title='Módulo 20 (v)', tickmode='linear', dtick=1, range=[-1, 20], showgrid=True, gridcolor='lightgray', zeroline=False),
    width=1000, height=800,
    plot_bgcolor='white',
    updatemenus=updatemenus,
    sliders=sliders,
    legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5)
)

fig.add_annotation(
    x=6, y=19.5,
    text="<b>Pendiente de rectas rojas (Δv/Δu) = 1</b><br>Razón global de frecuencias = 13/20",
    showarrow=False,
    font=dict(size=14, color="black"),
    bgcolor="white", bordercolor="black", borderwidth=1,
    opacity=0.9
)

fig.write_html("toro_animacion_2d.html")
print("¡toro_animacion_2d.html creado exitosamente!")

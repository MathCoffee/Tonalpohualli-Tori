import os
import json
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

print("Generando Animación 3D v5 con estructura Z13 x Z4...")

# Mapeo fijo de imágenes de símbolos según r (1, 2, 3, 0)
simbolos_info = {
    1: {"name": "carrizo", "file": "13 - carrizo.png"},
    2: {"name": "pedernal", "file": "18 - pedernal.png"},
    3: {"name": "casa", "file": "3 - casa.png"},
    0: {"name": "conejo", "file": "8 - conejo.png"}
}

# 2. Parámetros del Toro
R_major = 5
r_minor = 1.5

def mapear(x_mod, y_mod):
    v_ang = 2 * np.pi * (x_mod / 13.0)
    u_ang = 2 * np.pi * (y_mod / 4.0)
    X = (R_major + r_minor * np.cos(u_ang)) * np.cos(v_ang)
    Y = (R_major + r_minor * np.cos(u_ang)) * np.sin(v_ang)
    Z = r_minor * np.sin(u_ang)
    return X, Y, Z

# 3. Trayectoria para la animación (53 puntos para cerrar el lazo en Z13 x Z4)
n_vals = np.arange(1, 54)
u_mod = n_vals % 13
v_mod = n_vals % 4
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
    opacity=0.20,
    colorscale='Blues',
    showscale=False,
    hoverinfo='skip',
    name='Toro'
))

# --- CLASIFICACIÓN DE LOS 52 PUNTOS Y RECOLECCIÓN DE DATOS ---
categorías = {
    'base': {
        'x': [], 'y': [], 'z': [], 'n': [],
        'text_num': [], 'text_img': [], 'hover': [],
        'color': '#4B5563', 'symbol': 'circle', 'size': 5, 'name': 'Día Regular (q, r)'
    },
    'familia_q_1': {
        'x': [], 'y': [], 'z': [], 'n': [],
        'text_num': [], 'text_img': [], 'hover': [],
        'color': '#00CEC9', 'symbol': 'circle', 'size': 8, 'name': 'Día en Círculo Principal (r=1, Carrizo)'
    },
    'tlahuiztlanpa': {
        'x': [], 'y': [], 'z': [], 'n': [],
        'text_num': [], 'text_img': [], 'hover': [],
        'color': '#F1C40F', 'symbol': 'diamond', 'size': 11, 'name': 'Inicio de Trecena (r=1, Carrizo)'
    },
    'huitztlanpa': {
        'x': [], 'y': [], 'z': [], 'n': [],
        'text_num': [], 'text_img': [], 'hover': [],
        'color': '#0984E3', 'symbol': 'diamond', 'size': 11, 'name': 'Inicio de Trecena (r=2, Pedernal)'
    },
    'cihuatlanpa': {
        'x': [], 'y': [], 'z': [], 'n': [],
        'text_num': [], 'text_img': [], 'hover': [],
        'color': '#D63031', 'symbol': 'diamond', 'size': 11, 'name': 'Inicio de Trecena (r=3, Casa)'
    },
    'mictlanpa': {
        'x': [], 'y': [], 'z': [], 'n': [],
        'text_num': [], 'text_img': [], 'hover': [],
        'color': '#7F8C8D', 'symbol': 'diamond', 'size': 11, 'name': 'Inicio de Trecena (r=0, Conejo)'
    }
}

points_data = {}

for n in range(1, 53):
    q = n % 13
    r = n % 4
    X, Y, Z = mapear(q, r)
    
    numeral = 13 if q == 0 else q
    sym_name = simbolos_info[r]["name"]
    sym_file = simbolos_info[r]["file"]
    
    label_num = f"({q},{r})"
    label_img = f"({numeral}, {sym_name.capitalize()})"
    
    hover_info = f"Día n: <b>{n}</b><br>Coordenadas: <b>({q}, {r})</b>"
    
    if q == 1:
        if r == 1:
            class_key = 'tlahuiztlanpa'
            class_name = 'Inicio de Trecena (r=1, Carrizo)'
        elif r == 2:
            class_key = 'huitztlanpa'
            class_name = 'Inicio de Trecena (r=2, Pedernal)'
        elif r == 3:
            class_key = 'cihuatlanpa'
            class_name = 'Inicio de Trecena (r=3, Casa)'
        else:
            class_key = 'mictlanpa'
            class_name = 'Inicio de Trecena (r=0, Conejo)'
    elif r == 1:
        class_key = 'familia_q_1'
        class_name = 'Día en Círculo Principal (r=1, Carrizo)'
    else:
        class_key = 'base'
        class_name = 'Día Regular'
        
    categorías[class_key]['x'].append(X)
    categorías[class_key]['y'].append(Y)
    categorías[class_key]['z'].append(Z)
    categorías[class_key]['n'].append(n)
    categorías[class_key]['text_num'].append(label_num)
    categorías[class_key]['text_img'].append(label_img)
    categorías[class_key]['hover'].append(hover_info + f"<br>Tipo: <b>{class_name}</b>")
    
    points_data[n] = {
        "q": q,
        "r": r,
        "numeral": numeral,
        "symName": sym_name,
        "symFile": sym_file,
        "className": class_name,
        "classKey": class_key
    }

# Agregar los traces al gráfico Plotly (Trazas 1 a 6)
trace_keys = ['base', 'familia_q_1', 'tlahuiztlanpa', 'huitztlanpa', 'cihuatlanpa', 'mictlanpa']
for cat_key in trace_keys:
    cat = categorías[cat_key]
    line_dict = dict(color='white', width=1) if cat_key != 'base' else dict(color='black', width=0.5)
    
    fig.add_trace(go.Scatter3d(
        x=cat['x'], y=cat['y'], z=cat['z'],
        mode='markers',
        marker=dict(
            size=cat['size'],
            color=cat['color'],
            symbol=cat['symbol'],
            line=line_dict
        ),
        text=cat['text_num'],
        textposition="top center",
        textfont=dict(color='#0F172A', size=11, family='Arial, sans-serif'),
        hovertext=cat['hover'],
        hoverinfo='text',
        customdata=cat['n'],
        name=cat['name']
    ))

# --- TRAZOS 7 a 10: 4 Tramos de trayectoria de trecenas (Multicolor) ---
colores_tramos = {
    0: '#F1C40F', # Amarillo (r=1)
    1: '#0984E3', # Azul (r=2)
    2: '#D63031', # Rojo (r=3)
    3: '#7F8C8D'  # Gris (r=0)
}

# Añadir las 4 trazas para los 4 tramos
for S in range(1, 5):
    color_seg = colores_tramos[S-1]
    fig.add_trace(go.Scatter3d(
        x=[None], y=[None], z=[None],
        mode='lines',
        line=dict(color=color_seg, width=4),
        opacity=0.8,
        name=f'Trecena {S}',
        hoverinfo='skip',
        showlegend=False
    ))

# --- TRAZO 11: Generador Activo (Tracer) animado ---
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
    r = k % 4
    
    # Preparar datos de trazas del frame (trazas 7 a 11)
    frame_data_traces = []
    
    # 4 Segmentos
    for S in range(1, 5):
        idx_start = 13 * (S - 1)
        idx_end = 13 * S
        
        if (k - 1) < idx_start:
            x_seg, y_seg, z_seg = [], [], []
        elif idx_start <= (k - 1) <= idx_end:
            x_seg = X_traj[idx_start : k]
            y_seg = Y_traj[idx_start : k]
            z_seg = Z_traj[idx_start : k]
        else:
            x_seg = X_traj[idx_start : idx_end + 1]
            y_seg = Y_traj[idx_start : idx_end + 1]
            z_seg = Z_traj[idx_start : idx_end + 1]
            
        frame_data_traces.append(go.Scatter3d(x=list(x_seg), y=list(y_seg), z=list(z_seg)))
        
    # Generador Activo
    frame_data_traces.append(go.Scatter3d(
        x=[X_traj[k-1]], y=[Y_traj[k-1]], z=[Z_traj[k-1]],
        text=[f"({q},{r})"]
    ))
    
    frame = go.Frame(data=frame_data_traces, traces=list(range(7, 12)), name=str(k))
    frames.append(frame)

fig.frames = frames

updatemenus = []

sliders = [dict(
    active=0, yanchor="top", xanchor="left",
    currentvalue=dict(font=dict(size=14, color='#0F172A'), prefix="Día Actual (n): ", visible=True, xanchor="right"),
    transition=dict(duration=0), pad=dict(b=10, t=50), len=0.9, x=0.05, y=0,
    steps=[dict(args=[[str(k)], dict(frame=dict(duration=0, redraw=True), mode="immediate", transition=dict(duration=0))], label=str(k), method="animate") for k in range(1, len(n_vals))]
)]

fig.update_layout(
    title=dict(
        text='Tonalpohualli - Modelo Toro Interactivo 3D: Z₁₃ ⊕ Z₄ (Trayectoria Multicolor)',
        font=dict(size=18, color='#0F172A', family='Arial'),
        x=0.5, y=0.95
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
    margin=dict(l=10, r=220, b=10, t=90),
    updatemenus=updatemenus,
    sliders=sliders,
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        font=dict(color='#0F172A')
    )
)

# Convertir el gráfico Plotly a un div HTML parcial
plotly_div = pio.to_html(fig, full_html=False, include_plotlyjs=False)

# 4. Formatear datos de etiquetas para inyectar en JS
text_numeros_js = [
    categorías['base']['text_num'],
    categorías['familia_q_1']['text_num'],
    categorías['tlahuiztlanpa']['text_num'],
    categorías['huitztlanpa']['text_num'],
    categorías['cihuatlanpa']['text_num'],
    categorías['mictlanpa']['text_num']
]

text_imagenes_js = [
    categorías['base']['text_img'],
    categorías['familia_q_1']['text_img'],
    categorías['tlahuiztlanpa']['text_img'],
    categorías['huitztlanpa']['text_img'],
    categorías['cihuatlanpa']['text_img'],
    categorías['mictlanpa']['text_img']
]

# 5. Generar la estructura HTML final
html_template = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Tonalpohualli - Modelo Toro Interactivo 3D: Z13 ⊕ Z4</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-3.3.1.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #F8FAFC;
            color: #1E293B;
            font-family: 'Outfit', sans-serif;
            overflow: hidden;
            display: flex;
            height: 100vh;
        }
        
        #app-container {
            display: flex;
            width: 100%;
            height: 100%;
        }
        
        #plot-area {
            width: 73%;
            height: 100%;
            position: relative;
        }
        
        #plot-area > div {
            width: 100%;
            height: 100%;
        }
        
        #plotly-div {
            width: 100%;
            height: 100%;
        }
        
        /* Sidebar container */
        #sidebar {
            width: 27%;
            height: 100%;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-left: 1px solid rgba(0, 0, 0, 0.08);
            box-shadow: -5px 0 25px rgba(0, 0, 0, 0.03);
            display: flex;
            flex-direction: column;
            padding: 30px 24px;
            box-sizing: border-box;
            z-index: 10;
            overflow-y: auto;
        }
        
        h1 {
            font-size: 22px;
            font-weight: 800;
            margin: 0 0 5px 0;
            background: linear-gradient(135deg, #0F172A 0%, #2563EB 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }
        
        .subtitle {
            font-size: 13px;
            color: #64748B;
            text-align: center;
            margin-bottom: 25px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .section-label {
            font-size: 11px;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            text-align: left;
            padding-left: 4px;
        }
        
        /* Toggle mode selector */
        .selector-container {
            background: rgba(0, 0, 0, 0.03);
            border: 1px solid rgba(0, 0, 0, 0.08);
            border-radius: 12px;
            display: flex;
            padding: 4px;
        }
        
        .selector-btn {
            flex: 1;
            background: none;
            border: none;
            color: #64748B;
            padding: 10px;
            border-radius: 8px;
            font-family: 'Outfit', sans-serif;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .selector-btn.active {
            background: #FFFFFF;
            color: #0F172A;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.08);
        }

        .control-btn {
            flex: 1;
            background: #2563EB;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 8px;
            font-family: 'Outfit', sans-serif;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
        }
        
        .control-btn:hover {
            background: #1D4ED8;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
        
        .control-btn#btn-pause {
            background: #64748B;
            box-shadow: 0 4px 12px rgba(100, 116, 139, 0.15);
        }
        
        .control-btn#btn-pause:hover {
            background: #475569;
            box-shadow: 0 4px 12px rgba(100, 116, 139, 0.3);
        }
        
        .selector-btn-vertical {
            width: 100%;
            background: rgba(0, 0, 0, 0.02);
            border: 1px solid rgba(0, 0, 0, 0.06);
            color: #64748B;
            padding: 10px;
            border-radius: 8px;
            font-family: 'Outfit', sans-serif;
            font-size: 13px;
            font-weight: 600;
            text-align: left;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .selector-btn-vertical:hover {
            background: rgba(0, 0, 0, 0.04);
            color: #0F172A;
        }
        
        .selector-btn-vertical.active {
            background: #FFFFFF;
            color: #2563EB;
            border-color: rgba(37, 99, 235, 0.2);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        
        /* Details Card */
        #details-card {
            background: rgba(0, 0, 0, 0.01);
            border: 1px solid rgba(0, 0, 0, 0.05);
            border-radius: 16px;
            padding: 24px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        
        #details-card.active {
            background: rgba(255, 255, 255, 0.75);
            border-color: rgba(37, 99, 235, 0.2);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
        }
        
        .card-bg-glow {
            position: absolute;
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(37, 99, 235, 0.04) 0%, rgba(37, 99, 235, 0) 70%);
            top: -50px;
            right: -50px;
            z-index: 1;
            pointer-events: none;
        }
        
        .placeholder-text {
            color: #64748B;
            font-size: 14px;
            line-height: 1.6;
        }
        
        .day-badge {
            font-size: 32px;
            font-weight: 800;
            color: #0F172A;
            margin-bottom: 5px;
            z-index: 2;
        }
        
        .class-badge {
            font-size: 12px;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 25px;
            z-index: 2;
        }
        
        /* Categories styling */
        #plot-area text {
            font-family: 'Arial', sans-serif !important;
        }
        .class-tlahuiztlanpa {
            background: rgba(241, 196, 15, 0.15);
            color: #B7950B;
            border: 1px solid rgba(241, 196, 15, 0.3);
        }
        .class-huitztlanpa {
            background: rgba(9, 132, 227, 0.15);
            color: #0984E3;
            border: 1px solid rgba(9, 132, 227, 0.3);
        }
        .class-cihuatlanpa {
            background: rgba(214, 48, 49, 0.15);
            color: #D63031;
            border: 1px solid rgba(214, 48, 49, 0.3);
        }
        .class-mictlanpa {
            background: rgba(127, 140, 141, 0.15);
            color: #7F8C8D;
            border: 1px solid rgba(127, 140, 141, 0.3);
        }
        .class-familia_q_1 {
            background: rgba(0, 206, 201, 0.15);
            color: #0E6251;
            border: 1px solid rgba(0, 206, 201, 0.3);
        }
        .class-base {
            background: rgba(148, 163, 184, 0.15);
            color: #475569;
            border: 1px solid rgba(148, 163, 184, 0.3);
        }
        
        /* Numerical visualization style */
        .visual-numeros {
            display: flex;
            gap: 20px;
            margin-top: 15px;
            z-index: 2;
        }
        
        .number-box {
            width: 115px;
            height: 115px;
            border-radius: 16px;
            background: rgba(0, 0, 0, 0.02);
            border: 1px solid rgba(0, 0, 0, 0.05);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.01);
        }
        
        .number-box .val {
            font-size: 28px;
            font-weight: 800;
        }
        
        .number-box .label {
            font-size: 12px;
            color: #64748B;
            text-transform: uppercase;
            margin-top: 5px;
        }
        
        /* Image visualization style */
        .visual-imagenes {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            width: 100%;
            z-index: 2;
        }
        
        .image-row {
            display: flex;
            gap: 20px;
            justify-content: center;
            align-items: center;
        }
        
        .image-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }
        
        .img-wrapper {
            width: 115px;
            height: 115px;
            border-radius: 16px;
            background: rgba(0, 0, 0, 0.02);
            border: 1px solid rgba(0, 0, 0, 0.05);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 10px;
            box-sizing: border-box;
            box-shadow: 0 4px 15px rgba(0,0,0,0.01);
            transition: transform 0.3s ease;
        }
        
        .img-wrapper:hover {
            transform: scale(1.08);
        }
        
        .img-wrapper img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }
        
        .image-card .label {
            font-size: 13px;
            color: #475569;
            font-weight: 600;
        }
        
        .traditional-name {
            font-size: 20px;
            font-weight: 800;
            color: #0F172A;
            margin-top: 15px;
            text-transform: capitalize;
            background: linear-gradient(135deg, #0F172A 0%, #2563EB 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Help footer */
        .footer-help {
            font-size: 11px;
            color: #64748B;
            text-align: center;
            margin-top: 25px;
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <div id="app-container">
        <div id="plot-area">
            {PLOTLY_DIV}
        </div>
        <div id="sidebar">
            <h1 style="margin-bottom: 2px;">Tonalpohualli</h1>
            <h1 style="margin-top: 2px; margin-bottom: 5px;">Toro Interactivo 3D</h1>
            <div class="subtitle">Modelo Z₁₃ ⊕ Z₄</div>
            
            <div class="section-label" style="margin-top: 5px;">Representación</div>
            <div class="selector-container" style="margin-bottom: 15px;">
                <button id="btn-numeros" class="selector-btn active" onclick="setRepresentation('numeros')">Números (q, r)</button>
                <button id="btn-imagenes" class="selector-btn" onclick="setRepresentation('imagenes')">(Numeral, Glifo)</button>
            </div>
 
            <div class="section-label">Modo de Seguimiento</div>
            <div class="selector-container" style="margin-bottom: 20px;">
                <button id="btn-seg-cursor" class="selector-btn active" onclick="setFollowMode('cursor')">Al Señalar</button>
                <button id="btn-seg-trayectoria" class="selector-btn" onclick="setFollowMode('trayectoria')">Al Animar</button>
            </div>

            <div class="section-label">Controles de Animación</div>
            <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                <button id="btn-play" class="control-btn" onclick="playAnimation()">► Play</button>
                <button id="btn-pause" class="control-btn" onclick="pauseAnimation()">⏸ Pause</button>
            </div>

            <div class="section-label">Velocidad de Animación</div>
            <div style="background: rgba(0, 0, 0, 0.03); border: 1px solid rgba(0, 0, 0, 0.08); border-radius: 12px; padding: 12px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 12px; color: #475569; font-weight: 600;">Intervalo:</span>
                    <span style="font-size: 12px; color: #2563EB; font-weight: 800;"><span id="speed-val">300</span> ms</span>
                </div>
                <input type="range" id="speed-slider" min="100" max="1500" step="50" value="300" oninput="updateSpeed(this.value)" style="width: 100%; cursor: pointer;">
                <div style="display: flex; justify-content: space-between; font-size: 9px; color: #94A3B8; margin-top: 4px;">
                    <span>Rápido (100ms)</span>
                    <span>Lento (1500ms)</span>
                </div>
            </div>

            <div class="section-label">Visualización de Coordenadas</div>
            <div style="display: flex; flex-direction: column; gap: 6px; margin-bottom: 20px;">
                <button id="btn-lbl-hide" class="selector-btn-vertical active" onclick="setLabelMode('hide')">Ocultar Coordenadas</button>
                <button id="btn-lbl-featured" class="selector-btn-vertical" onclick="setLabelMode('featured')">Mostrar Solo Destacados</button>
                <button id="btn-lbl-all" class="selector-btn-vertical" onclick="setLabelMode('all')">Mostrar Todas las Coordenadas</button>
            </div>
            
            <div id="details-card">
                <div class="card-bg-glow"></div>
                <div id="details-content" class="placeholder-text">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 15px;">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="16" x2="12" y2="12"></line>
                        <line x1="12" y1="8" x2="12.01" y2="8"></line>
                    </svg>
                    <br>
                    Pasa el cursor o haz clic sobre cualquier punto en el toro 3D para explorar su coordenada, día y glifo tradicional.
                </div>
            </div>
            
            <div class="footer-help">
                Gira el Toro con el mouse para explorarlo en 3D.<br>
                Usa los controles del panel lateral para reproducir la animación.
            </div>
        </div>
    </div>
    
    <script>
        const pointsData = {POINTS_DATA_JSON};
        const textNumeros = {TEXT_NUMEROS_JSON};
        const textImagenes = {TEXT_IMAGENES_JSON};
        
        let currentRepresentation = 'numeros'; // 'numeros' o 'imagenes'
        let followMode = 'cursor'; // 'cursor' o 'trayectoria'
        let hoveredDay = null;
        
        function setRepresentation(mode) {
            if (mode === currentRepresentation) return;
            currentRepresentation = mode;
            
            document.getElementById('btn-numeros').classList.toggle('active', mode === 'numeros');
            document.getElementById('btn-imagenes').classList.toggle('active', mode === 'imagenes');
            
            const plotDiv = document.querySelector('.js-plotly-plot') || document.querySelector('.plotly-graph-div');
            if (plotDiv) {
                const textArray = mode === 'numeros' ? textNumeros : textImagenes;
                const fontSize = mode === 'numeros' ? 11 : 14;
                Plotly.restyle(plotDiv, { 
                    text: textArray,
                    'textfont.family': 'Arial, sans-serif',
                    'textfont.size': fontSize
                }, [1, 2, 3, 4, 5, 6]);
            }
            
            if (hoveredDay !== null) {
                updateSidebar(hoveredDay);
            }
        }

        function setFollowMode(mode) {
            if (mode === followMode) return;
            followMode = mode;
            
            document.getElementById('btn-seg-cursor').classList.toggle('active', mode === 'cursor');
            document.getElementById('btn-seg-trayectoria').classList.toggle('active', mode === 'trayectoria');
            
            if (mode === 'trayectoria') {
                const plotDiv = document.querySelector('.js-plotly-plot') || document.querySelector('.plotly-graph-div');
                if (plotDiv && plotDiv.layout && plotDiv.layout.sliders && plotDiv.layout.sliders[0]) {
                    const activeStep = plotDiv.layout.sliders[0].active || 0;
                    const day = activeStep + 1;
                    updateSidebar(day);
                }
            }
        }

        let currentSpeed = 300;
        let isPlaying = false;

        function updateSpeed(val) {
            currentSpeed = parseInt(val);
            document.getElementById('speed-val').innerText = currentSpeed;
            if (isPlaying) {
                pauseAnimation();
                playAnimation();
            }
        }

        function playAnimation() {
            const plotDiv = document.querySelector('.js-plotly-plot') || document.querySelector('.plotly-graph-div');
            if (plotDiv) {
                isPlaying = true;
                Plotly.animate(plotDiv, null, {
                    frame: { duration: currentSpeed, redraw: true },
                    fromcurrent: true,
                    transition: { duration: 0 }
                });
            }
        }

        function pauseAnimation() {
            const plotDiv = document.querySelector('.js-plotly-plot') || document.querySelector('.plotly-graph-div');
            if (plotDiv) {
                isPlaying = false;
                Plotly.animate(plotDiv, [], {
                    frame: { duration: 0, redraw: false },
                    mode: 'immediate',
                    transition: { duration: 0 }
                });
            }
        }

        function setLabelMode(mode) {
            const plotDiv = document.querySelector('.js-plotly-plot') || document.querySelector('.plotly-graph-div');
            if (!plotDiv) return;
            
            document.getElementById('btn-lbl-hide').classList.toggle('active', mode === 'hide');
            document.getElementById('btn-lbl-featured').classList.toggle('active', mode === 'featured');
            document.getElementById('btn-lbl-all').classList.toggle('active', mode === 'all');
            
            let plotlyMode;
            if (mode === 'hide') {
                plotlyMode = 'markers';
            } else if (mode === 'featured') {
                plotlyMode = ['markers', 'markers', 'markers+text', 'markers+text', 'markers+text', 'markers+text'];
            } else if (mode === 'all') {
                plotlyMode = 'markers+text';
            }
            
            Plotly.restyle(plotDiv, { mode: plotlyMode }, [1, 2, 3, 4, 5, 6]);
        }
        
        function updateSidebar(day) {
            hoveredDay = day;
            const data = pointsData[day];
            if (!data) return;
            
            const card = document.getElementById('details-card');
            const content = document.getElementById('details-content');
            
            card.classList.add('active');
            
            let classLabel = data.className;
            let classStyle = 'class-' + data.classKey;
            
            let html = `
                <div class="day-badge">Día ${day}</div>
                <div class="class-badge ${classStyle}">${classLabel}</div>
            `;
            
            if (currentRepresentation === 'numeros') {
                html += `
                    <div class="visual-numeros">
                        <div class="number-box">
                            <span class="val" style="color: #C0392B;">${data.q}</span>
                            <span class="label">módulo 13</span>
                        </div>
                        <div class="number-box">
                            <span class="val" style="color: #0E6251;">${data.r}</span>
                            <span class="label">módulo 4</span>
                        </div>
                    </div>
                `;
            } else {
                const numImgSrc = `imagenes/numerales/${data.q}.png`;
                const symImgSrc = `imagenes/simbolos/${data.symFile}`;
                const traditionalName = `${data.numeral} - ${data.symName}`;
                
                html += `
                    <div class="visual-imagenes">
                        <div class="image-row">
                            <div class="image-card">
                                <div class="img-wrapper">
                                    <img src="${numImgSrc}" alt="Numeral ${data.q}" onerror="this.src=''; this.alt='N/A';">
                                </div>
                                <span class="label">Numeral ${data.numeral}</span>
                            </div>
                            <div class="image-card">
                                <div class="img-wrapper">
                                    <img src="${symImgSrc}" alt="Símbolo ${data.symName}" onerror="this.src=''; this.alt='N/A';">
                                </div>
                                <span class="label">Signo: ${data.symName}</span>
                            </div>
                        </div>
                        <div class="traditional-name">${traditionalName}</div>
                    </div>
                `;
            }
            
            content.innerHTML = html;
        }
        
        function initPlotlyEvents() {
            const plotDiv = document.querySelector('.js-plotly-plot') || document.querySelector('.plotly-graph-div');
            if (plotDiv) {
                plotDiv.on('plotly_hover', function(data) {
                    if (followMode === 'cursor') {
                        const pt = data.points[0];
                        if (pt && pt.customdata) {
                            updateSidebar(pt.customdata);
                        }
                    }
                });
                
                plotDiv.on('plotly_click', function(data) {
                    if (followMode === 'cursor') {
                        const pt = data.points[0];
                        if (pt && pt.customdata) {
                            updateSidebar(pt.customdata);
                        }
                    }
                });

                plotDiv.on('plotly_sliderchange', function(data) {
                    if (followMode === 'trayectoria' && data.step && data.step.label) {
                        const day = parseInt(data.step.label);
                        if (!isNaN(day)) {
                            updateSidebar(day);
                        }
                    }
                });

                plotDiv.on('plotly_animated', function() {
                    if (followMode === 'trayectoria') {
                        if (plotDiv.layout && plotDiv.layout.sliders && plotDiv.layout.sliders[0]) {
                            const activeStep = plotDiv.layout.sliders[0].active || 0;
                            const day = activeStep + 1;
                            updateSidebar(day);
                        }
                    }
                });
            } else {
                setTimeout(initPlotlyEvents, 200);
            }
        }
        
        window.addEventListener('load', initPlotlyEvents);
    </script>
</body>
</html>
"""

# Reemplazar placeholders con datos reales convertidos a JSON
html_content = html_template.replace("{PLOTLY_DIV}", plotly_div)
html_content = html_content.replace("{POINTS_DATA_JSON}", json.dumps(points_data))
html_content = html_content.replace("{TEXT_NUMEROS_JSON}", json.dumps(text_numeros_js))
html_content = html_content.replace("{TEXT_IMAGENES_JSON}", json.dumps(text_imagenes_js))

# Guardar a archivo HTML
with open("toro_animacion_3d_v5.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("¡toro_animacion_3d_v5.html creado exitosamente!")

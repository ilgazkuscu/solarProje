import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import io
import base64
from dash import Dash
app = Dash(__name__)



# Zaman dizisi
zaman = pd.date_range("2024-07-22 06:00", periods=48, freq="30min")

# İnverter verileri
inverter_output = np.clip(np.sin(np.linspace(0, np.pi, 48)) * 30 + np.random.normal(0, 1.5, 48), 0, None)
inverter_output[0:3] *= 0.3
temperature = np.clip(np.random.normal(35 + 10*np.sin(np.linspace(0, np.pi, 48)), 2), 20, 70)
voltage = np.random.normal(230, 1.5, 48)

# OSOS verisi
osos_zaman = pd.date_range("2024-07-15", periods=24, freq="h")
osos_tuketim = np.clip(np.random.normal(8000, 2000, 24), 100, 15000)

# DataFrame'ler
df_inverter = pd.DataFrame({
    "Zaman": zaman,
    "Güç (kW)": inverter_output,
    "Sıcaklık (°C)": temperature,
    "Voltaj (V)": voltage
})

df_osos = pd.DataFrame({
    "Saat": osos_zaman.strftime("%H:%M"),
    "Tüketim (kWh)": osos_tuketim
})

# Grafikler
fig_inverter = px.line(df_inverter, x="Zaman", y=["Güç (kW)", "Sıcaklık (°C)", "Voltaj (V)"],
                       title="İnverter Verileri", markers=True)

fig_osos = px.bar(df_osos, x="Saat", y="Tüketim (kWh)", color="Tüketim (kWh)",
                  title="OSOS Saatlik Elektrik Tüketimi", color_continuous_scale="RdYlGn_r")

fig_epdk = px.line(df_inverter, x="Zaman", y="Güç (kW)",
                   title="EPDK - İnverter Güç Seviyesi", markers=True)

# --- Anlık tablo verisi (matplotlib tablosu) ---
veriler = {
    "Elektrik Alışı (kWh)": round(np.random.uniform(3000, 6000), 2),
    "Elektrik Satışı (kWh)": round(np.random.uniform(1000, 4000), 2),
    "Fabrika Üretimi (kWh)": round(np.random.uniform(2000, 5000), 2),
    "Fabrika Tüketimi (kWh)": round(np.random.uniform(4000, 8000), 2)
}

df_table = pd.DataFrame({
    "": ["Elektrik Alışı", "Elektrik Satışı"],
    "Değer (kWh)": [veriler["Elektrik Alışı (kWh)"], veriler["Elektrik Satışı (kWh)"]],
    " ": ["Fabrika Üretimi", "Fabrika Tüketimi"],
    "Değer (kWh) ": [veriler["Fabrika Üretimi (kWh)"], veriler["Fabrika Tüketimi (kWh)"]],
})

def create_table_image(df):
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.axis('off')
    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     loc='center',
                     cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(1.2, 1.8)
    plt.title("Anlık Enerji Verileri", fontsize=16, weight='bold')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_bytes = buf.read()
    return "data:image/png;base64," + base64.b64encode(img_bytes).decode()

table_img_src = create_table_image(df_table)

# --- Dash App ---
app = Dash(__name__)
app.title = "Enerji İzleme Paneli"

app.layout = html.Div([
    html.H1("Enerji İzleme Web Uygulaması", style={"textAlign": "center"}),

    dcc.Tabs([
        dcc.Tab(label='İnverter Verileri', children=[
            dcc.Graph(figure=fig_inverter)
        ]),
        dcc.Tab(label='OSOS Verileri', children=[
            dcc.Graph(figure=fig_osos)
        ]),
        dcc.Tab(label='EPDK Verisi (Güç)', children=[
            dcc.Graph(figure=fig_epdk)
        ]),
        dcc.Tab(label='Anlık Tablo', children=[
            html.Img(src=table_img_src, style={"display": "block", "margin": "auto", "maxWidth": "100%"})
        ]),
    ])
])

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port, debug=False)

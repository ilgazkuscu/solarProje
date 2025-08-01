import dash
from dash import dcc, html
import pandas as pd
import numpy as np
import plotly.express as px

# Veriler
zaman = pd.date_range("2024-07-22 06:00", periods=48, freq="30min")
guc = np.clip(np.sin(np.linspace(0, np.pi, 48)) * 30 + np.random.normal(0, 1.5, 48), 0, None)
guc[0:3] *= 0.3
sicaklik = np.clip(np.random.normal(35 + 10 * np.sin(np.linspace(0, np.pi, 48)), 2), 20, 70)
voltaj = np.random.normal(230, 1.5, 48)

df_inverter = pd.DataFrame({
    "Zaman": zaman,
    "Güç (kW)": guc,
    "Sıcaklık (°C)": sicaklik,
    "Voltaj (V)": voltaj
})

fig = px.line(df_inverter, x="Zaman", y=["Güç (kW)", "Sıcaklık (°C)", "Voltaj (V)"],
              title="İnverter Verileri", markers=True)

# Dash App
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Enerji İzleme Uygulaması", style={"textAlign": "center"}),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)
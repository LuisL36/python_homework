from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = px.data.gapminder()
countries = sorted(df["country"].unique())

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    style={"maxWidth": "900px", "margin": "auto", "fontFamily": "Arial, sans-serif"},
    children=[
        html.H1("Gapminder: GDP per Capita over Time", style={"textAlign": "center"}),
        html.P("Select a country to view its GDP per capita growth over years:"),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": c, "value": c} for c in countries],
            value="Canada",
            clearable=False,
            style={"width": "100%"}
        ),
        dcc.Graph(id="gdp-growth"),
        html.Div(
            "Data source: Plotly's built-in gapminder dataset",
            style={"fontSize": "12px", "color": "#666", "marginTop": "8px"}
        )
    ]
)

@app.callback(
    Output("gdp-growth", "figure"),
    Input("country-dropdown", "value")
)
def update_graph(selected_country):
    filtered = df[df["country"] == selected_country].sort_values("year")
    fig = px.line(
        filtered,
        x="year",
        y="gdpPercap",
        title=f"GDP per Capita: {selected_country}",
        markers=True,
        labels={"gdpPercap": "GDP per Capita (USD)", "year": "Year"}
    )
    fig.update_layout(transition_duration=300)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)

"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('data\\earthquakes.csv')

#line chart
fig = px.line(df, x='date', y='mag',color='mag')

#create slider with mag values, and update line chart
#create range slider with 0.5 increments
ramge_slider = dcc.RangeSlider(
    round(df.mag.min()),round(df.mag.max()),0.5,
    id='mag-slider',
    value=[df.mag.min(), df.mag.max()],
)


# change fig with slider on mag
@app.callback(
    dash.dependencies.Output('line_chart', 'figure'),
    [dash.dependencies.Input('mag-slider', 'value')])

def update_figure(selected_mag):
    print(selected_mag)
    print(selected_mag[0],selected_mag[1])
    filtered_df = df[ selected_mag[0] <= df.mag]
    filtered_df = filtered_df[filtered_df.mag <= selected_mag[1]]
    fig = px.line(filtered_df,x='date', y='mag', color = 'mag')
    return fig

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "17rem",
    "padding": "2rem 1rem",
    "background-color": "rgb(64 191 220)",
    "color": "white",
}



# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H3("Dashboard", className="display-5"),
        html.Hr(),
        html.P(
            "A simple dashboard with Earthquick data", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact",style={"color":"#e9e9e9"}),
                dbc.NavLink("Page 1", href="/page-1", active="exact", style={"color": "#e9e9e9"}),
                dbc.NavLink("Page 2", href="/page-2", active="exact", style={"color": "#e9e9e9"}),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(children=[
            dcc.Graph(
            id='line_chart',
            figure=fig
            ),
            ramge_slider
    ])
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(threaded=True)
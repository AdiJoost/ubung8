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
line = px.line(df, x='date', y='mag',color='mag')

#bar chart with date as x-axis
scatter = px.scatter(df, x='depth', y='mag',color='depth')

#bar chart with date as x-axis with max mag as y-axis 
bar = px.histogram(df, x='mag', y='depth', hover_name='date', log_x=True, color='mag')

#create slider with mag values, and update line chart
#create range slider with 0.5 increments
ramge_slider = dcc.RangeSlider(
    round(df.mag.min()),round(df.mag.max()),0.5,
    id='mag-slider',
    value=[df.mag.min(), df.mag.max()],
)

#Create a daterange picker
date_picker = dcc.DatePickerRange(
    id='date-picker',
    min_date_allowed=df.date.min(),
    max_date_allowed=df.date.max(),
    initial_visible_month=df.date.min(),
    start_date=df.date.min(),
    end_date=df.date.max(),
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
    line = px.line(filtered_df,x='date', y='mag', color = 'mag')
    return line

# def update figure with date picker on date
@app.callback(
    dash.dependencies.Output('scatter_chart', 'figure'),
    [dash.dependencies.Input('date-picker', 'start_date'),
        dash.dependencies.Input('date-picker', 'end_date')])

def update_figure(start_date, end_date):    
    filtered_df = df[(df.date >= start_date) & (df.date <= end_date)]

    scatter = px.scatter(filtered_df, x='depth', y='mag', color='depth')
    return scatter

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
            dbc.Row(
                [
                    dbc.Col( dcc.Graph(
                            id='line_chart',
                            figure=line),
                            width = 6),
                    dbc.Col(dcc.Graph(
                        id='scatter_chart',
                        figure=scatter), width=6),
                ]),
            dbc.Row(
                [
                    dbc.Col(ramge_slider,
                    width=6),
                    dbc.Col(date_picker,
                    width=6),
                ]),
            dbc.Row(
                [
                    dbc.Col( dcc.Graph(
                            id='bar_chart',
                            figure=bar),
                            width = 12),
                ]),
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
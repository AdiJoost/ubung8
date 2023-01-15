import dash
import flask
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Input, Output, dcc, html, State
import pandas as pd
import plotly.express as px
from pseudocode import getDataMagic
from aufgabe47 import filterFrame
from aufgabe48 import getMeanMagic

server = flask.Flask(__name__)

app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.FONT_AWESOME])

df = getDataMagic()
data = getMeanMagic(df)
worlddata= df.head()
#chart for analysis
line = px.line(df, x='date', y='mag',color='mag')
scatter = px.scatter(df, x='depth', y='mag',color='depth')
barMagMean = px.bar(data, x='startDate', y='meanMag')
bardepthMean = px.bar(data, x='startDate', y='meanDepth')
world_map2 = go.Figure(go.Scattergeo(lon = worlddata['long'], lat = worlddata['lat'], mode = 'markers',marker = dict(size = 15, color = '#00d3ff', line = dict(width = 3, color = 'rgba(68, 68, 68, 0)')), text = df['mag']))
world_map2.update_geos(
    projection_type="orthographic"
)
world_map2.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})

#Create a daterange picker
date_picker = dcc.DatePickerRange(
    id='date-picker',
    min_date_allowed=df.date.min(),
    max_date_allowed=df.date.max(),
    initial_visible_month=df.date.min(),
    start_date=df.date.min(),
    end_date=df.date.max(),
)

ramge_slider = dcc.RangeSlider(
    round(data.meanMag.min()),round(data.meanMag.max()),0.2,
    id='mag-slider',
    value=[data.meanMag.min(), data.meanMag.max()],
)
depth_slider = dcc.RangeSlider(
    round(data.meanDepth.min()),round(data.meanDepth.max()),5.0,
    id='depth-slider',
    value=[data.meanDepth.min(), data.meanDepth.max()],
)
submit_buttonFirstPage = html.Button('Submit', id='submit-buttonFirstPage', n_clicks=0,className="btn btn-primary")

# Change line plot and scatter plot and bar chart for the analysis page
@app.callback(
    Output('line_chart', 'figure'),
    Output('scatter_chart', 'figure'),
    Output('bar_chart', 'figure'),
    Output('bar_chart2', 'figure'),
    Input('submit-buttonFirstPage', 'n_clicks'),
    State('date-picker', 'start_date'),
    State('date-picker', 'end_date'),
    [State('mag-slider', 'value'),
    State('depth-slider', 'value')]
    )
def update_figure(n_clicks, start_date, end_date, selected_mag, selected_depth):
    print(start_date)
    print(selected_mag)
    filtered_df = df[ selected_mag[0] <= df.mag]
    filtered_df = filtered_df[filtered_df.mag <= selected_mag[1]]

    filtered_df = filtered_df[ selected_depth[0] <= filtered_df.depth]
    filtered_df = filtered_df[filtered_df.depth <= selected_depth[1]]

    filtered_df = filtered_df[filtered_df.date >= start_date]
    filtered_df = filtered_df[filtered_df.date <= end_date]

    filteredbar = data[ selected_mag[0] <= data.meanMag]
    filteredbar = filteredbar[filteredbar.meanMag <= selected_mag[1]]

    filteredbar = filteredbar[selected_depth[0] <= data.meanDepth]
    filteredbar = filteredbar[filteredbar.meanDepth <= selected_depth[1]]


    line = px.line(filtered_df, x='date', y='mag',color='mag')
    scatter = px.scatter(filtered_df, x='depth', y='mag',color='depth')
    barMagMean = px.bar(filteredbar, x='startDate', y='meanMag')
    bardepthMean = px.bar(filteredbar, x='startDate', y='meanDepth')
    return line, scatter, barMagMean, bardepthMean

depth_input = dcc.Input(
    id='depth_input',
    type='number',
    placeholder='Enter a value...',
    value=0,
    style={"padding-bottom": "12px",},
    className="form-control"
)

#range slider for the world map
world_map_slider = dcc.RangeSlider(
    round(df.mag.min()),round(df.mag.max()),0.5,
    id='world-map-slider',
    value=[df.mag.min(), df.mag.max()],
)
dateworld_picker = dcc.DatePickerRange(
    id='date-pickerworld',
    min_date_allowed=df.date.min(),
    max_date_allowed=df.date.max(),
    initial_visible_month=df.date.min(),
    start_date=df.date.min(),
    end_date=df.date.max(),
)
dropdown = dcc.Dropdown(
    id='dropdown',
    options=[{'label': i, 'value': i} for i in range(10,df.shape[0],10)],
    value=10,
    style={"padding-bottom": "12px"}
)
submit_button = html.Button('Submit', id='submit-button', n_clicks=0,className="btn btn-primary")

@app.callback(
    dash.dependencies.Output('world_map2', 'figure'),
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('world-map-slider', 'value')],
    [dash.dependencies.State('date-pickerworld', 'start_date')],
    [dash.dependencies.State('date-pickerworld', 'end_date')],
    [dash.dependencies.State('dropdown', 'value')],
    [dash.dependencies.State('depth_input', 'value')]

    )
    
def update_figure(n_clicks, selected_mag, start_date, end_date, dropdown,input_depth):
    print(selected_mag)
    print(input_depth)
    # update map scatterpoints
    filtered_df = df[ selected_mag[0] <= df.mag]
    filtered_df = filtered_df[filtered_df.mag <= selected_mag[1]]

    filtered_df = filtered_df[filtered_df.depth >= input_depth]

    filtered_df = filtered_df[filtered_df.date >= start_date]
    filtered_df = filtered_df[filtered_df.date <= end_date]

    filtered_df = filtered_df.head(dropdown)

    world_map2 = go.Figure(go.Scattergeo(lon = filtered_df['long'], lat = filtered_df['lat'], mode = 'markers', marker = dict(size = 15, color = '#00d3ff', line = dict(width = 3, color = 'rgba(68, 68, 68, 0)')), text = filtered_df['mag']))
    world_map2.update_geos(
        projection_type="orthographic"
    )
    world_map2.update_layout(height=750, margin={"r":0,"t":0,"l":0,"b":0})

    return world_map2

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "17rem",
    "padding": "2rem 1rem",
    "color": "white",
}

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
                dbc.NavLink("Data Analysis", href="/", active="exact",style={"color":"#e9e9e9"}),
                dbc.NavLink("Worldcard Plot", href="/page-1", active="exact", style={"color": "#e9e9e9"}),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
    className="sidebarStyle",
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(children=[
            dbc.Col(html.H1("Data Analysis"), width=12, style={"color": "#3a7c92"}),
            dbc.Row(
                [
                     dbc.Col(html.H5("Filter"), width=12, style={"color": "rgb(0 120 144)"}),
                    #add icon on the right side
                    html.Label("Magnitude",style={"width": "6%"},className="designtext"),
                    dbc.Col(
                        ramge_slider,
                    width=3),
                    html.Label("Depth",style={"width": "6%"},className="designtext"),
                    dbc.Col(depth_slider,
                    width=3),
                    html.Label("Date",style={"width": "4%"},className="designtext"),
                    dbc.Col(date_picker,
                    width=3),
                    dbc.Col(submit_buttonFirstPage,
                    width=1)
                ],className="p-3 bg-light rounded-3"),
            dbc.Row(
                [
                    dbc.Col( dcc.Graph(
                            id='line_chart',
                            figure=line),
                            width = 6),
                    dbc.Col(dcc.Graph(
                        id='scatter_chart',
                        figure=scatter), width=6),

                ], style={"height": "50%"}),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(
                        id='bar_chart',
                        figure=bardepthMean), width=6),
                    dbc.Col(dcc.Graph(
                        id='bar_chart2',
                        figure=barMagMean), width=6),
                ]),
           
    ])
    elif pathname == "/page-1":
        return html.Div(children=[
            dbc.Row(
                [
                    dbc.Col(html.H1("Worldcard Plot"), width=12, style={"color": "#3a7c92"}),
                    dbc.Col(dcc.Graph(
                        id='world_map2',
                    figure=world_map2),width=9),

                    #create a filter form
                    dbc.Col(html.Div([
                        html.H3("Filter", className="display-5", style={"color": "#3a7c92"}),
                        html.Div([
                            html.P("Magnitude",className="designtext"),
                            world_map_slider,
                            html.P("Depth",className="designtext"),
                            depth_input,
                            html.P("Date", style={"padding-top": "12px"},className="designtext"),
                            dateworld_picker,
                            
                            html.Div([
                                html.P("Choose data points to display",style={"padding-top": "12px"}),
                                dropdown,
                            ]),

                            submit_button
                        ], style={'columnCount': 1}, className="p-3 bg-light rounded-3"),
                    ]), width=3),
                ]),
    ])
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
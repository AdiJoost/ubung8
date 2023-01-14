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

#chart for analysis
line = px.line(df, x='date', y='mag',color='mag')
scatter = px.scatter(df, x='depth', y='mag',color='depth')

#x-axis is start date bis end date of intervall
barMagMean =dcc.Graph(
    id='barMagMean',
    figure={
        'data': [
            {'x': data['startDate'], 'y':  data['meanMag'], 'type': 'bar', 'name': 'Mean of Magnitude'},
        ],
        'layout': {
            'title': 'Mag Data Visualization'
        }
    }
)
bardepthMean = dcc.Graph(
    id='bardepthMean',
    figure={
        'data': [
            {'x': data['startDate'], 'y':  data['meanDepth'], 'type': 'bar', 'name': 'Mean of Depth'},
        ],
        'layout': {
            'title': 'Depth Data Visualization'
        }
    }
)

world_map2 = go.Figure(go.Scattergeo(lon = df['long'], lat = df['lat'], mode = 'markers', marker = dict(size = 2, color = 'red', line = dict(width = 3, color = 'rgba(68, 68, 68, 0)')), text = df['mag']))
world_map2.update_geos(
    projection_type="orthographic"
)
world_map2.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})


world_map = px.scatter_mapbox(df, lat='lat', lon='long', zoom=1, height=600, size="mag", size_max=12,color="mag", color_continuous_scale=px.colors.cyclical.IceFire)
world_map.update_layout(mapbox_style="open-street-map")
world_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#create slider with mag values, and update line chart
#create range slider with 0.5 increments
ramge_slider = dcc.RangeSlider(
    round(df.mag.min()),round(df.mag.max()),0.5,
    id='mag-slider',
    value=[df.mag.min(), df.mag.max()],
)

# dropdown with number 10,20,30,40,50, until df length
dropdown = dcc.Dropdown(
    id='dropdown',
    options=[{'label': i, 'value': i} for i in range(10,df.shape[0],10)],
    value=10,
    style={"padding-bottom": "12px"}
)

#filter on depth

#submit form on button click
submit_button = html.Button('Submit', id='submit-button', n_clicks=0,className="btn btn-primary")

#on submit button click, update world map with mag range

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

    world_map2 = go.Figure(go.Scattergeo(lon = filtered_df['long'], lat = filtered_df['lat'], mode = 'markers', marker = dict(size = 10, color = '#0b5ed7', line = dict(width = 3, color = 'rgba(68, 68, 68, 0)')), text = filtered_df['mag']))
    world_map2.update_geos(
        projection_type="orthographic"
    )
    world_map2.update_layout(height=750, margin={"r":0,"t":0,"l":0,"b":0})

    return world_map2

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
    print("line chart")
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
                dbc.NavLink("Data Analysis", href="/", active="exact",style={"color":"#e9e9e9"}),
                dbc.NavLink("Worldcard Plot", href="/page-1", active="exact", style={"color": "#e9e9e9"}),
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
                    #add icon on the right side
                    dbc.Col(html.H1("Data Analysis"), width=12, style={"color": "#3a7c92"}),
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
                    dbc.Col(
                        barMagMean, 
                        width=6),
                    dbc.Col(
                        bardepthMean, 
                        width=6),
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
                        html.H3("Filter", className="display-5"),
                        html.Div([
                            html.P("Magnitude"),
                            world_map_slider,
                            html.P("Depth"),
                            depth_input,
                            html.P("Date", style={"padding-top": "12px"}),
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
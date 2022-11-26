# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import Dash, html, dcc
from inflection import dasherize
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


app = Dash(__name__
           , external_stylesheets=[dbc.themes.BOOTSTRAP]) 

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
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


app.layout = html.Div(children=[
    html.H1(children='Earthquake Dashboard'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    

    dcc.Graph(
        id='line_chart',
        figure=fig
    ),

    ramge_slider
])

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
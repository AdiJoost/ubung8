# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import Dash, html, dcc
from inflection import dasherize
import plotly.express as px
import pandas as pd

app = Dash(__name__) 

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('data\\earthquakes.csv')

#line chart
fig = px.line(df, x='date', y='mag',color='mag')

#create slider with mag values, and update line chart
slider = dcc.Slider(
    id='mag-slider',
    min=df.mag.min(),
    max=df.mag.max(),
    value=df.mag.min(),
    marks={str(mag): str(mag) for mag in df.mag.unique()},
    step=None
)


# change fig with slider on mag
@app.callback(
    dash.dependencies.Output('line_chart', 'figure'),
    [dash.dependencies.Input('mag-slider', 'value')])

def update_figure(selected_mag):
    filtered_df = df[df.mag  <= selected_mag]    
    fig = px.line(filtered_df,x='date', y='mag', color = 'mag')
    print(fig)
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

    slider
])

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
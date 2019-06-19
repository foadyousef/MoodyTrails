import dash
import dash_core_components as dcc
import dash_html_components as html
import trail_stat as ts
from datetime import datetime as dt
from datetime import date, timedelta
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'text': '#7FDBFF'
}

markdown_text = "**A web application to make Real-time prediction of Trail Conditions.**"

app.layout = html.Div(children=[
    html.H1(children='MoodyTrails', style={'textAlign': 'center',
        'color': colors['text']}),

    dcc.Markdown(children=markdown_text),


    html.Div(children='''
        Step 1: Pick a Date
    ''', style={'textAlign': 'left','fontSize': 14}),


    dcc.DatePickerSingle(id='date-picker-single', date= dt.today().date()),

    html.Div(children='''
        Step 2. Pick a trail
    ''', style={'textAlign': 'left','fontSize': 14}),


    dcc.Dropdown(id='my-id',
    options=[
        {'label': 'Adams', 'value': 'ADM'},
        {'label': 'Washington', 'value': 'WSH'}
    ],
    value='ADM'),

    html.Div(id='my-div')

    #dcc.Input(id='my-id', value='initial value', type='text'),
    #html.Div(id='my-div')





])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value'),
    Input(component_id='date-picker-single', component_property='date')])

def update_output_div(trailname, userdate):
    s = ts.trail_stat(trailname, userdate)
    return s

if __name__ == '__main__':
    app.run_server(debug=True)
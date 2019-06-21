import dash
import dash_core_components as dcc
import dash_html_components as html
import trail_stat as ts
from datetime import datetime as dt
from datetime import date, timedelta
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import base64

# Layout CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#mapbox token
mapbox_access_token = 'pk.eyJ1IjoiZnlvdXNlZiIsImEiOiJ0TzQ3N093In0.fObm0vzOitrMaZTtpfA6xg'

# Style CSS or bootstrap
# The image
image_filename = 'trail1.jpg'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Without this line, the app does not work on Heroku
server = app.server

colors = {'text': '#7FDBFF'}

markdown_text = "**Real-time Trail Condition**"


app.layout = html.Div(
	html.Div([
		html.Div([
			html.Div([
				html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'height' : '15%','width' : '15%'}),
				dcc.Markdown(markdown_text),
			], className="row"),
			html.Div([
				html.Div([
					html.Div('''
					Step 1: Pick a Date
					''', style={'textAlign': 'left','fontSize': 14}),
					dcc.DatePickerSingle(id='date-picker-single', 
						date= dt.today().date(),
						day_size= 50),
					], className= 'five columns'
					),
				html.Div([
					html.Div('''
						Step 2. Pick a trail
						''', style={'textAlign': 'left','fontSize': 14}),
					dcc.Dropdown(id='my-id',
						options=[
						{'label': 'Adams', 'value': 'ADM'},
						{'label': 'Jefferson', 'value': 'JEF'},
						{'label': 'Madison', 'value': 'MAD'},
						{'label': 'Monroe', 'value': 'MNO'},
						{'label': 'Washington', 'value': 'WSH'}
						],
						value='ADM')
					], className= 'five columns'
					), 
					#dcc.Input(id='my-id', value='initial value', type='text'),
					#html.Div(id='my-div')
				], className="row"
				),
			html.Div([
				dcc.Graph(id="my-div"),
				html.Div('''
					Green indicates good condition, while Red indicates bad condition
					''', style={'textAlign': 'left','fontSize': 14})
				],className="row"
				)
			]
			)
		], className='eight columns offset-by-one'
		)
	)

@app.callback(
    Output(component_id='my-div', component_property='figure'),
    [Input(component_id='my-id', component_property='value'),
    Input(component_id='date-picker-single', component_property='date')])

def update_output_div(trailname, userdate):
    s = ts.trail_stat(trailname, userdate)
    print(s)
    #return s
    if s == 0:
    	plot_col = "rgb(255, 0, 0)"
    else:
    	plot_col = "rgb(0, 255, 0)"

    trace = []

    trace.append(go.Scattermapbox(lat=[44.2706], lon=[-71.3033], mode='markers', marker=go.scattermapbox.Marker(size=12,color=plot_col)))

    data = trace
    layout = go.Layout(autosize=True,
   		hovermode='closest',
   		showlegend=False,
   		height=500,
   		mapbox={'accesstoken': mapbox_access_token,
   		'bearing': 0,
   		'center': {'lat': 44.27, 'lon': -71.30},
   		'pitch': 0,
   		'zoom': 8,
   		"style": 'mapbox://styles/mapbox/light-v9'})

    figure = go.Figure(data=data, layout=layout)
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
import dash
import dash_core_components as dcc
import dash_html_components as html
import trail_stat as ts
from datetime import datetime as dt
from datetime import date, timedelta
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import base64
import pandas as pd
import numpy as np

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
					Step 1: Pick a date
					''', style={'textAlign': 'left','fontSize': 14}),
					dcc.DatePickerSingle(id='date-picker-single', 
						date= dt.today().date(),
						max_date_allowed= dt.today().date() + timedelta(days=3),
						day_size= 50),
					], className= 'five columns'
					),
				html.Div([
					html.Div('''
						Step 2: Pick a trail
						''', style={'textAlign': 'left','fontSize': 14}),
					dcc.Dropdown(id='my-id',
						options=[
						{'label': 'Adams', 'value': 'ADM'},
						{'label': 'Washington', 'value': 'WSH'},
						{'label': 'Jefferson', 'value': 'JEF'},
						{'label': 'Madison', 'value': 'MAD'},
						{'label': 'Eisenhower', 'value': 'EIS'},
						{'label': 'Lafayette', 'value': 'LAF'},
						{'label': 'Dome Carter', 'value': 'CAR'},
						{'label': 'Moosilauke', 'value': 'MOS'},
						{'label': 'WildCat', 'value': 'WIL'},
						{'label': 'Moriah', 'value': 'MOR'},
						{'label': 'Monroe', 'value': 'MNO'},
						{'label': 'Cabot', 'value': 'CAB'}
						],
						value='ADM')
					], className= 'five columns'
					), 
					#dcc.Input(id='my-id', value='initial value', type='text'),
				], className="row"
				),
			html.Div([
				html.Div('''
					Trail condition prediction: 
					''', style={'color':'grey','marginTop': 25,'textAlign': 'left','fontSize': 20}),
				html.H1(id='print_test', children='', style={'textAlign': 'left','fontSize': 18})
				],className="row"
				),
			html.Div([
				dcc.Graph(id="my-div"),
				html.Div([
					html.P([
						html.Span('Green', style={'color': 'green'}), ' = dry condition']),
					html.P([
						html.Span('Brown', style={'color': 'brown'}), ' = wet/muddy condition']),
					html.P([
						html.Span('Cyan', style={'color': 'Cyan'}), ' = snow/icy condition'])
					],),
				html.Div(
					html.Label(["Please visit my ", html.A('slides', href='https://drive.google.com/open?id=1DnIding39Z1_dXZjjxpH-KZFAM7eU0xrv_HevdMTCoU'), " here"], style={'marginBottom': 50})
					)
				],className="row"
				)
			]
			)
		], className='eight columns offset-by-one'
		)
	)

@app.callback([
    Output(component_id='my-div', component_property='figure'),
    Output('print_test', 'children')],
    [Input(component_id='my-id', component_property='value'),
    Input(component_id='date-picker-single', component_property='date')])

def update_output_div(trailname, userdate):
    s = ts.trail_stat(trailname, userdate)
    #print("You reached here", s)

    try:
    	from sklearn.preprocessing import LabelBinarizer
    	lb = LabelBinarizer()
    	lb.fit_transform([0,1,2])
    	s = lb.inverse_transform(s)
    	#print("Hey Hey ############################",s)

    	if s == 0:
    		plot_col = "rgb(0,255,255)"
    		con = "Hikers should expect snow/ice on trail. Crampons and proper clothing is  advised."
    	elif s == 1:
    		plot_col = "rgb(165,42,42)"
    		con = "Hikers should expect a wet/muddy trail. Waterproof boots will guarantee a pleasent hike."
    	elif s == 2:
    		plot_col = "rgb(0, 255, 0)"
    		con = "Trail is most likely in excellent conidtion."
    except:
    	print('dont want to be here')
    	plot_col = "rgb(0, 0, 0)"
    	con = ""

    lst = pd.read_csv("trail_cor.csv")
    lat = lst[lst['abv']==trailname].values.tolist()[0][1]
    lon = lst[lst['abv']==trailname].values.tolist()[0][2]

    # the figure layout
    trace = []
    trace.append(go.Scattermapbox(
    	lat=[lat], 
    	lon=[lon], 
    	#text=con,
    	hoverinfo='text',
    	mode='markers', 
    	marker=go.scattermapbox.Marker(
    		size=12,
    		color=plot_col)))

    data = trace
    layout = go.Layout(autosize=True,hovermode='closest',showlegend=False,height=400, margin = dict(l = 0, r = 0, t = 0, b = 0),mapbox={'accesstoken': mapbox_access_token,'bearing': 0,'center': {'lat': lat, 'lon': lon},'pitch': 0,'zoom': 8,"style": 'mapbox://styles/mapbox/light-v9'})

    figure = go.Figure(data=data, layout=layout)

    print(con)
    return figure, con

if __name__ == '__main__':
    app.run_server(debug=True)
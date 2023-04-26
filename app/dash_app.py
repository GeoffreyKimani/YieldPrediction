import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import requests

from YieldPrediction.consts.constants import Country, Crop, Location, API_ENDPOINT

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Label("Country"),
            dcc.Dropdown(
                id='country',
                options=[{'label': c, 'value': c} for c in Country],
                placeholder='Select country',
                searchable=True
            )
        ], md=3),
        dbc.Col([
            html.Label("Location"),
            dcc.Dropdown(
                id='location',
                options=[{'label': c, 'value': c} for c in Location],
                placeholder='Select location',
                searchable=True
            )
        ], md=3),
        dbc.Col([
            html.Label("Crop"),
            dcc.Dropdown(
                id='crop',
                options=[{'label': c, 'value': c} for c in Crop],
                placeholder='Select crop',
                searchable=True
            )
        ], md=3),
        dbc.Col([
            html.Label("Land Area (in hectares)"),
            dcc.Input(id='land-area', type='number', placeholder='Enter land area')
        ], md=3),
    ], className='mb-3'),
    dbc.Row([
        dbc.Col([
            html.Button('Submit', id='submit-btn', n_clicks=0, className='btn btn-primary')
        ], md=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Div(id='output')
        ])
    ])
], className='mt-3')
Crop = ['Rainfed maize', 'Rainfed millet', 'Rainfed pigeonpea',
        'Rainfed sorghum', 'Rainfed wheat', 'Rainfed chickpea',
        'Rainfed common bean', 'Rainfed rice', 'Rainfed cowpea',
        'Rainfed groundnut']


# Define the layout

# Define the callback function to handle form submission
@app.callback(
    dash.dependencies.Output('output', 'children'),
    [dash.dependencies.Input('submit-btn', 'n_clicks')],
    [dash.dependencies.State('country', 'value'),
     dash.dependencies.State('location', 'value'),
     dash.dependencies.State('crop', 'value'),
     dash.dependencies.State('land-area', 'value')])
def submit_form(n_clicks, country, location, crop, land_area):
    # Here you can send the data to the server and receive a response
    # For now, we'll just return a simple message with the entered values
    if n_clicks > 0:
        message = f"You entered the following:\nCountry: {country}\nLocation: {location}\nCrop: {crop}\nLand Area: {land_area} hectares"

        # make api call
        url = API_ENDPOINT
        data = {'station': location, 'country': country, 'crop': crop, 'area': land_area}

        response = requests.post(url, data=data)

        if response.status_code == 200:
            print('Success!')
            print(response.text, type(response.text))
        else:
            print(f'Request failed with status code {response.status_code}')

        message = response.text

        return dbc.Alert(message, color='success')


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=4000, debug=True)

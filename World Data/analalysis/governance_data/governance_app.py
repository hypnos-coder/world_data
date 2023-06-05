# Import packages
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc

# Incorporate data
df = pd.read_csv('to_app.csv')

# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS['indigo'][4]]
app = Dash(__name__, external_stylesheets=external_stylesheets)
value = 'Weighted Governance'

# App layout
app.layout = dmc.Container(
    [
        dmc.Title('Insight App', color="blue", size="h3", align="center"),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dcc.Dropdown(
                            options=[{'label': country, 'value': country} for country in df['Country Name'].unique()],
                            value='Canada',
                            id='country-selection'
                        ),
                    ],
                    span=6
                ),
                dmc.Col(
                    [
                        dcc.Dropdown(
                            options=[{'label': col, 'value': col} for col in df.columns[4:]],
                            value='Control of Corruption Score',
                            id='column-selection'
                        )
                    ],
                    span=6
                ),
            ],
            align="center"
        ),
        dmc.Center(
            [
                dmc.Grid(
                    [
                        dmc.Col(
                            [
                                dcc.Graph(figure={}, id='graph-content')
                            ],
                            span=6
                        ),
                        dmc.Col(
                            [
                                dcc.Graph(id='map-content')
                            ],
                            span=6
                        )
                    ],
                    align="center"
                )
            ]
        )
    ],
    fluid=True
)

# Add controls to build the interaction
@app.callback(
    Output(component_id='graph-content', component_property='figure'),
    Output(component_id='map-content', component_property='figure'),
    Input(component_id='country-selection', component_property='value'),
    Input(component_id='column-selection', component_property='value')
)
def update_graph(country_selected, column_selected):
    dff = df[df['Country Name'] == country_selected]
    line_figure = px.line(dff, x='Year', y=column_selected)

    map_figure = px.choropleth(
        data_frame=df,
        locations='Country Name',
        locationmode='country names',
        color=value,
        animation_frame='Year',
        color_continuous_scale='YlOrRd_r',
        range_color=(df[value].min(), df[value].max()),
        title='Time Series on World Map',
        labels={'Value': value},
        projection='natural earth'  # Set the projection to natural earth
    )
    
    map_figure.update_geos(showframe=False, showcoastlines=False, projection_type='orthographic', showocean=True, oceancolor="LightBlue")
    map_figure.update_layout(
        width=800,  # Set the width of the figure
        height=600,  # Set the height of the figure
        transition_duration=2000
    )

    return line_figure, map_figure

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)

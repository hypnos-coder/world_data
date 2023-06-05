# Import packages
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc

# Incorporate data
df1 = pd.read_csv('governance_data/to_app.csv')
df2 = pd.read_csv('world_death/to_app.csv')
df3 = pd.read_csv('world_Education/to_app.csv')
# df4 = pd.read_csv('world_gdp/to_app.csv')

dataset_dic = [
    {'label': 'Governance Data', 'value': 'dataset1'},
    {'label': 'World Death', 'value': 'dataset2'},
    {'label': 'World Education', 'value': 'dataset3'},
    # {'label': 'World GDP', 'value': 'dataset4'}
]


# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dmc.Container(
    [
        dmc.Title('Insight App', color="blue", size="h3", align="center"),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dcc.Dropdown(
                            options=dataset_dic,
                            value='dataset1',
                            id='dataset-selection'
                        )
                    ],
                    span=4
                ),
                dmc.Col(
                    [
                        dcc.Dropdown(
                            options=[],
                            value='',
                            id='country-selection'
                        ),
                    ],
                    span=4
                ),
                dmc.Col(
                    [
                        dcc.Dropdown(
                            options=[],
                            value='',
                            id='column-selection'
                        )
                    ],
                    span=4
                )
                
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

# Update the options for the column-selection dropdown based on the selected dataset
@app.callback(
    Output(component_id='column-selection', component_property='options'),
    Output(component_id='column-selection', component_property='value'),
    Input(component_id='dataset-selection', component_property='value'),
)
def update_column_options(dataset_selected):
    if dataset_selected == 'dataset1':
        column_options = [{'label': col, 'value': col} for col in df1.columns[4:]]
    elif dataset_selected == 'dataset2':
        column_options = [{'label': col, 'value': col} for col in df2.columns[4:]]
    elif dataset_selected == 'dataset3':
        column_options = [{'label': col, 'value': col} for col in df3.columns[4:]]
    # elif dataset_selected == 'dataset4':
    #     column_options = [{'label': col, 'value': col} for col in df4.columns[4:]]
    else:
        column_options = []
    default_value = column_options[-1]['value'] if column_options else ''
    return column_options, default_value

# Update the options for the country-selection dropdown based on the selected dataset and column
@app.callback(
    Output(component_id='country-selection', component_property='options'),
    Output(component_id='country-selection', component_property='value'),
    Input(component_id='dataset-selection', component_property='value'),
    Input(component_id='column-selection', component_property='value'),
)
def update_country_options(dataset_selected, column_selected):
    if dataset_selected == 'dataset1':
        df = df1
    elif dataset_selected == 'dataset2':
        df = df2
    elif dataset_selected == 'dataset3':
        df = df3
    # elif dataset_selected == 'dataset4':
    #     df = df4
    else:
        df = pd.DataFrame()  # Empty DataFrame if no dataset is selected

    if column_selected:
        available_countries = df[df[column_selected].notnull()]['Country Name'].unique()
    else:
        available_countries = []

    country_options = [{'label': country, 'value': country} for country in available_countries]
    default_value = country_options[-1]['value'] if country_options else ''
    return country_options, default_value

# Update the graph and map based on the selected dataset, country, and column
@app.callback(
    Output(component_id='graph-content', component_property='figure'),
    Output(component_id='map-content', component_property='figure'),
    Input(component_id='dataset-selection', component_property='value'),
    Input(component_id='country-selection', component_property='value'),
    Input(component_id='column-selection', component_property='value'),
)
def update_graph(dataset_selected, country_selected, column_selected):
    if dataset_selected == 'dataset1':
        df = df1
    elif dataset_selected == 'dataset2':
        df = df2
    elif dataset_selected == 'dataset3':
        df = df3
    # elif dataset_selected == 'dataset4':
    #     df = df4
    else:
        df = pd.DataFrame()  # Empty DataFrame if no dataset is selected

    dff = df[df['Country Name'] == country_selected]
    line_figure = px.line(dff, x='Year', y=column_selected)

    value = dff.columns.to_list()[-1]

    map_figure = px.choropleth(
        data_frame=df,
        locations='Country Name',
        locationmode='country names',
        color=column_selected,
        animation_frame='Year',
        color_continuous_scale='YlOrRd_r',
        range_color=(dff[column_selected].min(), dff[column_selected].max()),
        title='Time Series on World Map',
        labels={'Value': column_selected},
       
    )

    map_figure.update_geos(showframe=False, showcoastlines=False, projection_type='orthographic', showocean=True, oceancolor="LightBlue")
    map_figure.update_layout(
        width=800,
        height=600,
        transition_duration=2000
    )

    return line_figure, map_figure

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)

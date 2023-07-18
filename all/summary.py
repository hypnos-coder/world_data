# Import packages
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc


# Incorporate data
dataframe = pd.read_csv('main.csv')
dataframe.insert(0,'Ranking', dataframe.index+1)

df1 = pd.read_csv('governance_final_version.csv')
df2 = pd.read_csv('world_Death_final_version.csv')
df3 = pd.read_csv('edu.csv')
df4 = pd.read_csv('gdp_final_version.csv')

dataset_dic = [
    {'label': 'Gouvernance', 'value': 'dataset1'},
    {'label': 'Death', 'value': 'dataset2'},
    {'label': 'Education', 'value': 'dataset3'},
    {'label': 'GDP', 'value': 'dataset4'}
]


# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

table_style = {
    'border':'thin lightgrey solid',
    'fontFamily':'Arial, sans-serif',
    'fontSize':'12px'
}

cell_style = {
    'padding':'8px',
    'textAlign':'left'
}

header_style = {
    'backgroundColor':'lightgrey',
    'fontWeight':'bold'
}
# App layout
app.layout = dmc.Container(
    [
        dmc.Title('Insight App', color="blue", size="h3", align="center"),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Text("Dataset", weight=500),
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
                        dmc.Text("Countries", weight=500),
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
                        dmc.Text("Factors", weight=500),
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
        dmc.Space(h=30),
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
        ),
        dmc.Space(h=30),
        dmc.Center(
            dmc.Table(
                dash_table.DataTable(
                    id='table',
                    columns=[{'name':col, 'id':col} for col in dataframe.columns],
                    data=dataframe.to_dict('records'),
                    page_size=10,
                    style_table=table_style,
                    style_cell=cell_style,
                    style_header=header_style
                )
            )
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
        column_options = [{'label': col, 'value': col} for col in df1.columns[3:]]
    elif dataset_selected == 'dataset2':
        column_options = [{'label': col, 'value': col} for col in df2.columns[3:]]
    elif dataset_selected == 'dataset3':
        column_options = [{'label': col, 'value': col} for col in df3.columns[3:]]
    elif dataset_selected == 'dataset4':
        column_options = [{'label': col, 'value': col} for col in df4.columns[3:]]
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
    elif dataset_selected == 'dataset4':
        df = df4
    else:
        df = pd.DataFrame()  # Empty DataFrame if no dataset is selected

    if column_selected:
        available_countries = df[df[column_selected].notnull()]['Country_Name'].unique()
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
    elif dataset_selected == 'dataset4':
        df = df4
    else:
        df = pd.DataFrame()  # Empty DataFrame if no dataset is selected

    dff = df[df['Country_Name'] == country_selected]
    line_figure = px.line(dff, x='Year', y=column_selected)

    value = dff.columns.to_list()[-1]
    # print(value)
    map_figure = px.choropleth(
        data_frame=df,
        locations='Country_Name',
        locationmode='country names',
        color=value,
        animation_frame='Year',
        color_continuous_scale='YlOrRd_r',
        range_color=(df[value].min(), df[value].max()),
        title='World Map',
        labels={'Value': value},
       
    )

    map_figure.update_geos(showframe=False, showcoastlines=False, projection_type='orthographic', showocean=True, oceancolor="LightBlue")
    map_figure.update_layout(
        width=600,
        height=600,
        transition_duration=2000
    )

    return line_figure, map_figure

# Run the App
if __name__ == '__main__':
   app.run_server(debug=True)
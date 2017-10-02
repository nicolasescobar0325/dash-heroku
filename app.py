import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly
import os

app = dash.Dash(__name__)
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

#app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv("https://raw.githubusercontent.com/nicolasescobar0325/csv-tables/master/dataset.csv", delimiter = ';', encoding = 'latin-1')
options_reg = df['REGIONAL'].unique()
options_dpto = df['DEPARTAMENTO'].unique()
options_ciud = df['CIUDAD'].unique()
options_ofic = df['NOMBRE_OFICINA'].unique()

app.layout = html.Div([
    dcc.Graph(id='graph-with-drop', animate=True),
    dcc.Dropdown(
        id='reg-drop',
        options = [{'label': i, 'value': i} for i in options_reg]
    ),
    dcc.Dropdown(
        id='dpto-drop',
        options = [{'label': i, 'value': i} for i in options_dpto]
    ),
    dcc.Dropdown(
        id='ciud-drop',
        options = [{'label': i, 'value': i} for i in options_ciud]
    ),
    dcc.Dropdown(
        id='oficina-drop',
        options = [{'label': i, 'value': i} for i in options_ofic]
    )    
    
])

@app.callback(
    dash.dependencies.Output('graph-with-drop', 'figure'),
    [dash.dependencies.Input('oficina-drop', 'value')])
def update_figure(selected_ofic):
    sub_df = df[['FECHA_APERTURA', 'NOMBRE_OFICINA', 'DAVIDA', 'VAL_DAVIDA']].groupby(['FECHA_APERTURA', 'NOMBRE_OFICINA'], as_index = False).sum()
    filtered_df = sub_df[sub_df.NOMBRE_OFICINA == selected_ofic]
    traces = []
    for i in filtered_df.NOMBRE_OFICINA.unique():
        df_by_oficina = filtered_df[filtered_df['NOMBRE_OFICINA'] == i]

        trace1 = Scatter(
        x=df_by_oficina['FECHA_APERTURA'],
        y=df_by_oficina['DAVIDA'],
        text='Pólizas emitidas',
        name='',
        opacity=0.7,
        marker={'symbol': 'circle', 'size': "6" },
        mode="markers+lines",
        yaxis = 'y2',
        fill="tonexty"
        )

        trace2 = Scatter(
        x=df_by_oficina['FECHA_APERTURA'],
        y=df_by_oficina['VAL_DAVIDA'],
        text='Valor Primas ($)',
        name='',
        opacity=0.7,
        marker={'symbol': 'star', 'size': "8" },
        mode="markers+lines"
        )

        layout = Layout(
        x=df_by_oficina['FECHA_APERTURA'],
        y=df_by_oficina['DAVIDA'],
        text='Pólizas emitidas',
        name='',
        opacity=0.7,
        marker={'symbol': 'circle', 'size': "6" },
        mode="markers+lines",
        yaxis = 'y2',
        fill="tonexty"
        )

    layout = Layout(
        xaxis={'title': 'Mes'},
        yaxis= dict(autorange = True, title='Valor Primas', showgrid=False, zeroline=False, showline=False, showticklabels=True),
        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        legend={'x': 0, 'y': 1},
        hovermode='closest'
        )

    return Figure(data=[trace1, trace2], layout=layout)

if __name__ == '__main__':
    app.run_server(debug=False)

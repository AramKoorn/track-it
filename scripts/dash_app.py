import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
import plotly.graph_objs as go
from scripts import coolblue

# Print options
pd.set_option('expand_frame_repr', False)

# Init search key
SEARCH_KEY = 'consoles/nintendo-switch'

df = coolblue.CoolBLue().evaluate(search_key=SEARCH_KEY)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Coolblue product tracker'),
    html.H2(children=f'Tracking information for: {SEARCH_KEY}'),
    dash_table.DataTable(
        id='id_table',
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
            'whiteSpace': 'normal'
        },
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        editable=True,
        sort_action='native',
        filter_action="native",
        style_data_conditional=[
        {
            'if': {
                'filter_query': '{state} = "temporary-out-of-stock"',
                'column_id': 'state'
            },
            'backgroundColor': '#FF4136',
            'color': 'white'
        }

            ,
    ]
    )
])

# @app.callback(
#     dash.dependencies.Output('graph-with-dropdowm', 'figure'),
#     [dash.dependencies.Input('store-dropdown', 'value')])
# def update_figure(selected_store):
#     df_tmp = df_test[selected_store]
#     return{
#             'data': [
#                 {
#                     'x': df_tmp,
#                     'name': 'test',
#                     'type': 'histogram'
#                 }
#             ],
#             'layout': {}
#         }
#


def update_output(value):
    return f'You have selected {value}'


if __name__ == '__main__':
    app.run_server(debug=True)
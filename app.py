import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import psycopg2
from dash.dependencies import Input, Output

import pandas as pd

conn = psycopg2.connect(database='airflow', user='airflow',password='airflow')
sql1 = 'SELECT * FROM cyptoexchangerate_cleaned'
data_cleaned = pd.read_sql_query(sql1, conn)
sql2 = 'SELECT * FROM cyptoexchangerate_agg_daily'
data_daily = pd.read_sql_query(sql2, conn)


def figure_hourminute(data,crypto_code='BTC'):
    df = data[data['crypto_code']==crypto_code].copy()
    fig = px.line(df,x='ddate',y='exchange_rate',text='exchange_rate')
    fig.update_traces(mode='markers+lines+text',line_color='blue',marker_color='red')
    fig.update_traces(texttemplate='%{text:.4s}', textposition='top center')
    fig.update_layout(title_text='Exchange_Rate',showlegend=True,paper_bgcolor='white',plot_bgcolor='white')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False,visible=False)

    return fig

def figure_daily(data,crypto_code='BTC'):
    df = data[data['crypto_code']==crypto_code].copy()
    fig = px.line(df,x='ddate',y='avg_exchange_rate',text='avg_exchange_rate')
    fig.update_traces(mode='markers+lines+text',line_color='green',marker_color='blue')
    fig.update_traces(texttemplate='%{text:.4s}', textposition='top center')
    fig.update_layout(title_text='Exchange_Rate Daily',showlegend=True,paper_bgcolor='white',plot_bgcolor='white')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False,visible=False)

    return fig

def get_dropdown(data):
    option = []
    for val in data[['crypto_name','crypto_code',]].drop_duplicates().values.tolist():
        option.append({'label':val[0],'value':val[1]})
    return option

app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Welcome to Project Crypto'),
    dcc.Dropdown(id='crypto_selector',
                           options=get_dropdown(data_cleaned),
                           multi=False,
                           value="BTC",
                           className='stockselector'),
    dcc.Graph(
        id='graph1',
        figure=figure_hourminute(data_cleaned,crypto_code='BTC')
    ),
    dcc.Graph(
        id='graph2',
        figure=figure_daily(data_daily,crypto_code='BTC')
    ),


])

@app.callback(
    Output('graph1', 'figure'),
    Input('crypto_selector', 'value')
)
def update_output(value):
    return figure_hourminute(data_cleaned,crypto_code=value)

@app.callback(
    Output('graph2', 'figure'),
    Input('crypto_selector', 'value')
)
def update_output(value):
    return figure_daily(data_daily,crypto_code=value)


if __name__ == '__main__':
    app.run_server(debug=True)

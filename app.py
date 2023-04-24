# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 12:50:31 2023

@author: morid
"""

from dash import Dash, html, dcc, callback, Output, Input, dash_table
from dash.dependencies import State
import pandas as pd
import ProjectCache
# import dash_bootstrap_components as dbc

# Some default set of tweets (could be 1) - the relevant part is the column headers
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

database = "mongodb://localhost:27017"

PC = ProjectCache(database)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Tweet Search', style={'textAlign':'center'}),
    dcc.RadioItems(['Text', 'Hashtag'], 'Text', id='search_selection', inline=True),
    dcc.Input(id="search_query", type="text", placeholder="search query"),
    html.Button('Search', id='search_submit'),
    html.H2(children='Output'),
    dash_table.DataTable(data=pd.DataFrame().to_dict('records'),
    columns=[{"name": i, "id": i} for i in ['user_name', 'create_at', 'text', 'reply_count', 'retweet_count']], id='search_output'),
    html.H2(children='Similar'),
    dash_table.DataTable(data=pd.DataFrame().to_dict('records'),
    columns=[{"name": i, "id": i} for i in pd.DataFrame().columns], id='similar_df')
])

@callback(
    Output('search_output', 'data'),
    Output('similar_df', 'data'),
    State('search_selection', 'stype'),
    State('search_query', 'value'),
    Input('search_submit', 'n_clicks')
) # This function should be updated to refer to and call tweets as appropriate
def update_table(stype, value, n):
    # dff = df[df.country==value] if len(value)>0 else pd.DataFrame()
    # c2 = [i for i in df.country.unique().tolist() if i<value]
    # v2 = max(c2) if len(value)>0 and len(c2)>0 else ""
    # dff2 = df[df.country==v2] if len(value)>0  else pd.DataFrame()
    dff, dff2 = PC.keyword(value, stype)
    
    return dff, dff2

if __name__ == '__main__':
    app.run_server(debug=False)


# -*- coding: utf-8 -*-
"""
Créée le 15 mai 2021

@author: Cécile Guillot

Script permettant de nettoyer les données de l'étude Coviprev
et de générer un tableau de bord contenant les résultats de cette enquête
"""

# Importation des librairies nécessaires au préprocessing
import pandas as pd

# Chargement des données
filepath = 'coviprev-age.csv'
df = pd.read_csv(filepath, sep=';')

# Préprocessing des données
df.drop(["Unnamed: 29", "Unnamed: 30", "Unnamed: 31"], axis=1, inplace=True)
df['semaine'] = df['semaine'].apply(lambda x:str(x))
df['vague'] = df["semaine"].apply(lambda x: x.split(':')[0])
data = df[["age","vague", "semaine", "anxiete", "depression","pbsommeil"]]
data.columns = ["Age", "Vague", "Semaine", "Anxiété", "Dépression", "Troubles du sommeil"]
del df
for col in data.columns:
    if data[col].dtype == object:
        data[col] = pd.to_numeric(data[col].str.replace(',', '.'), errors='ignore')
data.dropna(inplace=True)

# Création du dashboard

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

age = data.Age.unique()
indice = ['Anxiété', 'Dépression', 'Troubles du sommeil']

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    dcc.Checklist(
        id="checklist",
        options=[{"label": x, "value": x} 
                 for x in age],
        value=age[1:],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Dropdown(
        id='dropdown',
        options=[{"label": i, "value": i} 
                 for i in indice],
        value=indice[0:]
            ),
    dcc.Graph(id="line-chart"),
])

@app.callback(
    dash.dependencies.Output("line-chart", "figure"), 
    [dash.dependencies.Input("checklist", "value"),
     dash.dependencies.Input("dropdown", "value")])

def update_graph(age, indice):
    mask = data.age.isin(age)
    fig = px.line(data[mask], x="vague", y=indice, color="age", 
                  title="Evolution des différents indices mesurées par l'enquête Coviprev au cours du temps en fonction de l'âge")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

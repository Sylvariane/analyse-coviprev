# -*- coding: utf-8 -*-
"""
Créée le 15 mai 2021

@author: Cécile Guillot

Script permettant de nettoyer les données de l'étude Coviprev (données sur l'âge)
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
import plotly.io as pio

pio.templates.default = "seaborn"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

age = data.Age.unique()
indice = ['Anxiété', 'Dépression', 'Troubles du sommeil']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    dcc.Markdown('''# Tableau de bord des données de l'étude Coviprev
Cette appli sert à montrer les résultats obtenus dans l'étude Coviprev réalisée par Santé Publique France. Les données présentées ci-dessous montrent le pourcentage de personnes dépressives, anxieuses et ayant des troubles du sommeil au moment des mesures. Les mesures ont été effectuées par la passation de questionnaire. Une note limite était définie pour savoir si la personne était ou non dépressive, anxieuse ou avait des troubles du sommeil.

Le test utilisé pour déterminer si les individus étaient dépressifs et/ou anxieux était la HAD (Hospitality Anxiety and Depression scale ).


Source : *[Données Coviprev](https://www.data.gouv.fr/fr/datasets/donnees-denquete-relatives-a-levolution-des-comportements-et-de-la-sante-mentale-pendant-lepidemie-de-covid-19-coviprev/)*'''),
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
        placeholder="Choississez un indice",
            ),
    dcc.Graph(id="line-chart"),
])

@app.callback(
    dash.dependencies.Output("line-chart", "figure"), 
    [dash.dependencies.Input("checklist", "value"),
     dash.dependencies.Input("dropdown", "value")])

def update_graph(age, indice):
    mask = data.Age.isin(age)
    fig = px.line(data[mask], x="Semaine", y=indice, color="Age")
    fig.update_layout(title="Evolution des différents indices mesurés par l'enquête Coviprev en 2020",
                   yaxis_title="% de personnes",
                   xaxis_title="Date de la mesure")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

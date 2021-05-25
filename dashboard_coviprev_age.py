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
df_age = pd.read_csv(filepath, sep=';')

# Préprocessing des données
df_age.drop(["Unnamed: 29", "Unnamed: 30", "Unnamed: 31"], axis=1, inplace=True)
df_age['semaine'] = df_age['semaine'].apply(lambda x:str(x))
df_age['vague'] = df_age["semaine"].apply(lambda x: x.split(':')[0])
data_age = df_age[["age","vague", "semaine", "anxiete", "depression","pbsommeil"]]
data_age.columns = ["Age", "Vague", "Semaine", "Anxiété", "Dépression", "Troubles du sommeil"]
del df_age
for col in data_age.columns:
    if data_age[col].dtype == object:
        data_age[col] = pd.to_numeric(data_age[col].str.replace(',', '.'), errors='ignore')
data_age.dropna(inplace=True)

filepath_sexe = 'coviprev-sexe.csv'
df_sexe = pd.read_csv(filepath_sexe, sep=';')

# Préprocessing des données
df_sexe.drop(["Unnamed: 29", "Unnamed: 30", "Unnamed: 31"], axis=1, inplace=True)
df_sexe['semaine'] = df_sexe['semaine'].apply(lambda x:str(x))
df_sexe['vague'] = df_sexe["semaine"].apply(lambda x: x.split(':')[0])
data_sexe = df_sexe[["sexe","vague", "semaine", "anxiete", "depression","pbsommeil"]]
data_sexe.columns = ["Sexe", "Vague", "Semaine", "Anxiété", "Dépression", "Troubles du sommeil"]
del df_sexe
for col in data_sexe.columns:
    if data_sexe[col].dtype == object:
        data_sexe[col] = pd.to_numeric(data_sexe[col].str.replace(',', '.'), errors='ignore')
data_sexe.dropna(inplace=True)

# Création du dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.io as pio

pio.templates.default = "seaborn"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

age = data_age.Age.unique()
sexe = data_sexe.Sexe.unique()
indice = ['Anxiété', 'Dépression', 'Troubles du sommeil']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.Div([ dcc.Markdown('''# Tableau de bord des données de l'étude Coviprev
Cette appli sert à montrer les résultats obtenus dans l'étude Coviprev réalisée par Santé Publique France. Les données présentées ci-dessous montrent le pourcentage de personnes dépressives, anxieuses et ayant des troubles du sommeil au moment des mesures. Les mesures ont été effectuées par la passation de questionnaire. Une note limite était définie pour savoir si la personne était ou non dépressive, anxieuse ou avait des troubles du sommeil.

Le test utilisé pour déterminer si les individus étaient dépressifs et/ou anxieux était la HAD (Hospitality Anxiety and Depression scale ).


Source : *[Données Coviprev](https://www.data.gouv.fr/fr/datasets/donnees-denquete-relatives-a-levolution-des-comportements-et-de-la-sante-mentale-pendant-lepidemie-de-covid-19-coviprev/)*''')]),
   html.Div([        
           dcc.Dropdown(
            id='dropdown',
            options=[{"label": i, "value": i} 
                 for i in indice],
            placeholder="Choississez un indice",
            ),]),
     html.Div([
        dcc.Checklist(
            id="checklist",
            options=[{"label": x, "value": x} 
                 for x in age],
            value=age[1:],
            labelStyle={'display': 'inline-block'}
            ),
        dcc.Graph(id="line-chart-age"),
        ], 
        style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        dcc.Checklist(
            id="checklist-sexe",
            options=[{"label": x, "value": x} 
                     for x in sexe],
            value=sexe[1:],
            labelStyle={'display': 'inline-block'}
            ),
        dcc.Graph(id='line-chart-sexe')], 
        style={'width': '49%', 'display': 'inline-block'}),])

@app.callback(
    dash.dependencies.Output("line-chart-age", "figure"), 
    [dash.dependencies.Input("checklist", "value"),
     dash.dependencies.Input("dropdown", "value")])

def update_graph(age, indice):
    mask = data_age.Age.isin(age)
    fig = px.line(data_age[mask], x="Semaine", y=indice, color="Age")
    fig.update_layout(yaxis_title="% de personnes",
                      xaxis_title="Date de la mesure")
    return fig


@app.callback(
    dash.dependencies.Output("line-chart-sexe", "figure"), 
    [dash.dependencies.Input("checklist-sexe", "value"),
     dash.dependencies.Input("dropdown", "value")])

def graph_sexe(sexe, indice):
    mask_sex = data_sexe.Sexe.isin(sexe)
    fig=px.line(data_sexe[mask_sex], x="Semaine", y=indice, color="Sexe")
    fig.update_layout(yaxis_title="% de personnes",
                      xaxis_title="Date de la mesure")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

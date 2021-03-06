# Analyses des données de l'enquête coviprev

L'enquête Coviprev réalisé par *Santé Publique France* et *BVA Access Panel* s'intéresse à la santé mentale et à l'acceptation des mesures sanitaires par les français. Elle a été réalisé sur un échantillon de *2000 personnes* et a permis d'obtenir ces renseignements.
Dans un premier temps, on s'intéresse uniquement aux données sur la *santé mentale* et plus particulièrement aux scores d'anxiété, de dépression et les troubles du sommeil. On va étudier les différences entre hommes et femmes puis les différences entre les tranches d'âge.
Dans un second temps, on s'intéressera aux données sur l'*acceptation des mesures sanitaires* (port du masque, distanciation sociale, lavage des mains, etc.) dans notre échantillon. Là aussi, on s'intéressera aux différences entre hommes et femmes puis aux différences entre les tranches d'âge. 

## Etudes sur les effets du Covid sur la santé mentale des français

### Analyses des différences entre Hommes et Femmes 

*Projet visible ici :* [Deepnote](https://deepnote.com/project/CoviprevAnalysis-UUVMmZkdQ52wjEKPgVUK9A/%2Fcoviprev_gender_analysis.ipynb) & [GitHub](https://github.com/Sylvariane/analyse-coviprev/blob/main/coviprev_gender_analysis.ipynb)

Les variables en lien avec l'anxiété, la dépression et les troubles du sommeil ont été analysés. On retrouve des résultats présents dans la littérature avec notamment des scores d'anxiété plus importants chez les femmes que chez les hommes. On observe aussi une forte augmentation des scores de dépression et des troubles du sommeil à l'annonce du second confinement et ces scores ne diminuent pas après la fin de ce second confinement. 

![newplot(2)](https://user-images.githubusercontent.com/64648386/115441010-a963d280-a210-11eb-8c76-7383af6cbc35.png)

![newplot(1)](https://user-images.githubusercontent.com/64648386/115441021-af59b380-a210-11eb-8422-773628d268b2.png)

**Il semble donc que le second confinement a eu des effets néfastes sur la santé mentale des français par rapport au premier confinement. Il serait intéressant d'avoir les données qui ont suivi ainsi que celle du troisième confinement pour suivre cette évolution.**

### Analyses des différences en fonction de l'âge

*Projet visible ici :* [Script Dashboard](https://github.com/Sylvariane/analyse-coviprev/blob/main/dashboard_coviprev_age.py), [App Web avec Heroku](https://coviprev-app.herokuapp.com/) & [Notebook](https://github.com/Sylvariane/analyse-coviprev/blob/main/coviprev_age_analysis.ipynb)

Cette fois-ci l'idée était d'analyser les résultats entre les différents groupes d'âge et de créer un dashboard interactif. On observe que ce sont les tranches d'âge les plus jeunes qui sont sensibles à l'anxiété et à la dépression et qui présentent une forte augmentation des troubles du sommeil. 

![newplot](https://user-images.githubusercontent.com/64648386/118511248-011f2c00-b732-11eb-8aa4-46b8cfb6bada.png)

Les résultats des 65 ans et plus restent stables au cours du temps.



---
title: Analyse et Modélisation de données en Python avec Pandas
status: published
date: 2019-07-06
tags: [python, science, informatique, programmation]
---


Dans  cet article,  nous  allons explorer  comment faire  de
l'analyse de  données en  Python, en utilisant  la librairie
[Pandas](https://pandas.pydata.org/).   L'article est  assez
long,  car j'ai  essayé d'explorer  toutes les  possibilités
offertes par Pandas.

Avant de commencer,  il est important de noter  que Pandas a
pour objectif d'effectuer de l'analyse et de la modélisation
de données. Par contre, il  n'implémente pas un grand nombre
de  fonctionnalités   de  modélisation   en  dehors   de  la
régression linéaire.  Pour ce  type d'analyses  avancées, il
faut                     plutôt                     regarder
[statsmodel](http://statsmodels.sf.net/)                  et
[scikit-learn](http://scikit-learn.org/).

Les exemples  de codes  Python que  vous trouverez  dans cet
article sont pensés  pour être utilisés dans  une session de
l'interpréteur    Python.     Je    recommande    d'utiliser
[ipython](https://ipython.readthedocs.io/en/stable/)      ou
mieux,                      un                     [notebook
Jupyter](https://jupyter.readthedocs.io/en/latest/content-quickstart.html).

Commençons!

## Les structures de données Pandas

* Les [Series](http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html#pandas.Series)
  pour les données 1D  labélisées et homogènement typées (ce
  sont des conteneurs pour des données scalaires). La taille
  des séries est immutable.

* Les [DataFrame](http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)
  pour  les  données  2D   labélisées,  de  taille  mutable,
  tabulaires  et potentiellement  de  types hétérogènes  (ce
  sont des conteneurs de Séries)

Bon à savoir: la grande majorité des méthodes des structures
Pandas produisent de nouveaux objets et ne modifient pas les
objets d'entrée.

## Créer une structure de données Pandas

Pandas    est    souvent    utilisé    de    concert    avec
[Numpy](http://www.numpy.org/)                            et
[matplotlib](https://matplotlib.org/). Nous  commençons donc
par importer ces 3 librairies:


```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

Quand on crée une série en passant une liste de scalaires au
constructeur,  Pandas  crée  un index  automatiquement  (des
entiers, comme pour les index des listes):


```python
s = pd.Series([1, 3, 5, np.nan, 6, 8])
s
```




    0    1.0
    1    3.0
    2    5.0
    3    NaN
    4    6.0
    5    8.0
    dtype: float64



On peut créer un index de dates avec pandas, en précisant la
date de  début et le nombre  de dates qu'on veut  avoir dans
l'index, sous  la forme d'un  nombre de jours  consécutifs à
partir du jour précisé dans la date de début.

Dans le code qui suit, on  crée un index de dates commençant
le 30 mars 2019, et s'étendant sur 6 jours:

```python
dates = pd.date_range('20190330', periods=6)
dates
```




    DatetimeIndex(['2019-03-30', '2019-03-31', '2019-04-01', '2019-04-02',
                   '2019-04-03', '2019-04-04'],
                  dtype='datetime64[ns]', freq='D')



On peut construire un DataFrame à partir d'un array numpy de
dimension 2, en précisant les colonnes et les index.


```python
df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
df
```




<div>
<style scoped>

    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>-2.759782</td>
      <td>-0.754355</td>
      <td>0.636811</td>
      <td>-0.412057</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>-0.276277</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>0.694458</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>1.054788</td>
      <td>-0.461713</td>
      <td>0.801541</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
      <td>0.642595</td>
      <td>-0.136862</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>0.437396</td>
      <td>0.310099</td>
      <td>-0.169594</td>
      <td>0.391921</td>
    </tr>
  </tbody>
</table>
</div>



On   peut   construire   un    DataFrame   à   partir   d'un
dictionnaire.  Les   clés  deviennent  alors   les  colonnes
(dimensions du  dataframe) et  les valeurs sont  répétées si
nécessaire (si ce sont des  scalaires), dans le cas où l'une
des colonnes contient une Série  ou un array numpy de taille
supérieure à 1.


```python
df2 = pd.DataFrame({
    'A': 1.,
    'B': pd.Timestamp('20190221'),
    'C': pd.Series(1, index=list(range(4))),
    'D': np.array([3] * 4, dtype='int32'),
    'E': pd.Categorical(['test', 'train', 'test', 'train']),
    'F': 'foo'
})
df2
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>E</th>
      <th>F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.0</td>
      <td>2019-02-21</td>
      <td>1</td>
      <td>3</td>
      <td>test</td>
      <td>foo</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.0</td>
      <td>2019-02-21</td>
      <td>1</td>
      <td>3</td>
      <td>train</td>
      <td>foo</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1.0</td>
      <td>2019-02-21</td>
      <td>1</td>
      <td>3</td>
      <td>test</td>
      <td>foo</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1.0</td>
      <td>2019-02-21</td>
      <td>1</td>
      <td>3</td>
      <td>train</td>
      <td>foo</td>
    </tr>
  </tbody>
</table>
</div>



La preuve  que les  dataframe peuvent  avoir des  données de
types hétérogènes:


```python
df2.dtypes
```




    A           float64
    B    datetime64[ns]
    C             int64
    D             int32
    E          category
    F            object
    dtype: object



## Voir les données

On peut voir les premières  lignes, et les dernières lignes,
l'index, les  colonnes, la représentation Numpy  des données
sous-jacentes,  des statistiques  de base  des données.  On
peut également  accéder à la  transposée des données  et les
ordonner soit  par index, soit  par valeurs en  précisant la
colonne à partir de laquelle les données seront ordonnées.


```python
df.head(3)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>-2.759782</td>
      <td>-0.754355</td>
      <td>0.636811</td>
      <td>-0.412057</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>-0.276277</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>0.694458</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.tail(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>-0.276277</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>0.694458</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>1.054788</td>
      <td>-0.461713</td>
      <td>0.801541</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
      <td>0.642595</td>
      <td>-0.136862</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>0.437396</td>
      <td>0.310099</td>
      <td>-0.169594</td>
      <td>0.391921</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.index
```




    DatetimeIndex(['2019-03-30', '2019-03-31', '2019-04-01', '2019-04-02',
                   '2019-04-03', '2019-04-04'],
                  dtype='datetime64[ns]', freq='D')




```python
df.columns
```




    Index(['A', 'B', 'C', 'D'], dtype='object')




```python
df2.to_numpy()    # Méthode non disponible dans la version 0.23 de Pandas
```




    array([[1.0, Timestamp('2019-02-21 00:00:00'), 1, 3, 'test', 'foo'],
           [1.0, Timestamp('2019-02-21 00:00:00'), 1, 3, 'train', 'foo'],
           [1.0, Timestamp('2019-02-21 00:00:00'), 1, 3, 'test', 'foo'],
           [1.0, Timestamp('2019-02-21 00:00:00'), 1, 3, 'train', 'foo']],
          dtype=object)




```python
df.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>6.000000</td>
      <td>6.000000</td>
      <td>6.000000</td>
      <td>6.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>-0.525894</td>
      <td>0.536102</td>
      <td>0.449196</td>
      <td>0.177121</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.176395</td>
      <td>0.796318</td>
      <td>0.658857</td>
      <td>0.520569</td>
    </tr>
    <tr>
      <th>min</th>
      <td>-2.759782</td>
      <td>-0.754355</td>
      <td>-0.461713</td>
      <td>-0.412057</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>-0.611590</td>
      <td>0.262663</td>
      <td>0.032008</td>
      <td>-0.241423</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>-0.252036</td>
      <td>0.560012</td>
      <td>0.639703</td>
      <td>0.127529</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>0.238895</td>
      <td>0.993572</td>
      <td>0.676485</td>
      <td>0.618823</td>
    </tr>
    <tr>
      <th>max</th>
      <td>0.437396</td>
      <td>1.549302</td>
      <td>1.359295</td>
      <td>0.801541</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.T
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>2019-03-30 00:00:00</th>
      <th>2019-03-31 00:00:00</th>
      <th>2019-04-01 00:00:00</th>
      <th>2019-04-02 00:00:00</th>
      <th>2019-04-03 00:00:00</th>
      <th>2019-04-04 00:00:00</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A</th>
      <td>-2.759782</td>
      <td>-0.153566</td>
      <td>-0.698618</td>
      <td>-0.350507</td>
      <td>0.369715</td>
      <td>0.437396</td>
    </tr>
    <tr>
      <th>B</th>
      <td>-0.754355</td>
      <td>0.246851</td>
      <td>0.809926</td>
      <td>1.054788</td>
      <td>1.549302</td>
      <td>0.310099</td>
    </tr>
    <tr>
      <th>C</th>
      <td>0.636811</td>
      <td>1.359295</td>
      <td>0.687781</td>
      <td>-0.461713</td>
      <td>0.642595</td>
      <td>-0.169594</td>
    </tr>
    <tr>
      <th>D</th>
      <td>-0.412057</td>
      <td>-0.276277</td>
      <td>0.694458</td>
      <td>0.801541</td>
      <td>-0.136862</td>
      <td>0.391921</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.sort_index(axis=0, ascending=False)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-04-04</th>
      <td>0.437396</td>
      <td>0.310099</td>
      <td>-0.169594</td>
      <td>0.391921</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
      <td>0.642595</td>
      <td>-0.136862</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>1.054788</td>
      <td>-0.461713</td>
      <td>0.801541</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>0.694458</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>-0.276277</td>
    </tr>
    <tr>
      <th>2019-03-30</th>
      <td>-2.759782</td>
      <td>-0.754355</td>
      <td>0.636811</td>
      <td>-0.412057</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.sort_values(by='B')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>-2.759782</td>
      <td>-0.754355</td>
      <td>0.636811</td>
      <td>-0.412057</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>-0.276277</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>0.437396</td>
      <td>0.310099</td>
      <td>-0.169594</td>
      <td>0.391921</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>0.694458</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>1.054788</td>
      <td>-0.461713</td>
      <td>0.801541</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
      <td>0.642595</td>
      <td>-0.136862</td>
    </tr>
  </tbody>
</table>
</div>



## Sélectionner les données

Il est recommandé d'utiliser les méthodes optimisées d'accès
aux données spécifiques de  Pandas telles que `.at`, `.iat`,
`.loc` et `.iloc` pour les  codes déployés en production, et
de se  contenter des  expressions de sélection  standards de
Python et Numpy pour les analyses simples de données.

### Récupérer les données

Les dataframes sont comme des dictionnaires:


```python
df['A']
```




    2019-03-30   -2.759782
    2019-03-31   -0.153566
    2019-04-01   -0.698618
    2019-04-02   -0.350507
    2019-04-03    0.369715
    2019-04-04    0.437396
    Freq: D, Name: A, dtype: float64



La  structure  renvoyée est  une  `Series`  (une colonne  de
dataframe)


```python
type(df['A'])
```




    pandas.core.series.Series



On  peut  sélectionner  un  sous-ensemble  du  dataframe  en
appliquant                                                un
[slice](http://sametmax.com/connaissez-vous-lobjet-slice-en-python/):


```python
df[0:3]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>-2.759782</td>
      <td>-0.754355</td>
      <td>0.636811</td>
      <td>-0.412057</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>-0.276277</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>0.694458</td>
    </tr>
  </tbody>
</table>
</div>



Le type retourné est un `DataFrame`


```python
type(df[0:3])
```




    pandas.core.frame.DataFrame



### Sélection par Label

On  peut récupérer  une série  indexée par  les colonnes  du
`DataFrame` (une ligne):


```python
df.loc[dates[0]]
```




    A   -2.759782
    B   -0.754355
    C    0.636811
    D   -0.412057
    Name: 2019-03-30 00:00:00, dtype: float64



Ou un `DataFrame` en récupérant plusieurs lignes


```python
df.loc[:, ['A', 'B']]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>-2.759782</td>
      <td>-0.754355</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>1.054788</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>0.437396</td>
      <td>0.310099</td>
    </tr>
  </tbody>
</table>
</div>



Pour  le slicing  par Label  des  lignes, les  2 labels  des
extrémités  sont  inclus (à  la  différence  du slicing  des
listes Python)


```python
df.loc['20190330':'20190331', ['A', 'B']]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>-2.759782</td>
      <td>-0.754355</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
    </tr>
  </tbody>
</table>
</div>



Pour récupérer  un scalaire,  il faut sélectionner  le Label
(la ligne) et la colonne:


```python
df.loc[dates[0], 'A']
```




    -2.759782433495169



L'accès est  beaucoup plus rapide  si on utilise  la méthode
`.at`


```python
df.at[dates[0], 'A']
```




    -2.759782433495169



### Sélection par position

La sélection par  position se fait en  utilisant les méthode
préfixées `.i`


```python
df.iloc[3]
```




    A   -0.350507
    B    1.054788
    C   -0.461713
    D    0.801541
    Name: 2019-04-02 00:00:00, dtype: float64




```python
df.iloc[3:5, 0:2]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>1.054788</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
    </tr>
  </tbody>
</table>
</div>



Remarquez  que  dans  le   cas  précédent,  on  retrouve  le
comportement  du slicing  des  listes  en Python  (l'extrême
droite n'est pas inclu).

On peut passer une liste des indices qu'on veut sélectionner
pour les lignes ou pour les colonnes (cherry-pick):


```python
df.iloc[[1, 2, 4], [0, 2]]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>1.359295</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.687781</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>0.642595</td>
    </tr>
  </tbody>
</table>
</div>



Pour obtenir un slice uniquement sur les lignes:


```python
df.iloc[1:3, :]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>-0.276277</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>0.694458</td>
    </tr>
  </tbody>
</table>
</div>



Pour obtenir un slice uniquement sur les colonnes:


```python
df.iloc[:, 1:3]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>B</th>
      <th>C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>-0.754355</td>
      <td>0.636811</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>0.246851</td>
      <td>1.359295</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>0.809926</td>
      <td>0.687781</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>1.054788</td>
      <td>-0.461713</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>1.549302</td>
      <td>0.642595</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>0.310099</td>
      <td>-0.169594</td>
    </tr>
  </tbody>
</table>
</div>



Pour récupérer une valeur scalaire explicitement:


```python
df.iloc[1, 1]
```




    0.24685134417220603



Ou encore plus rapide:


```python
df.iat[1, 1]
```




    0.24685134417220603



### Indexation booléenne

On peut  récupérer les  lignes pour lesquelles  une certaine
condition est vérifiée sur une colonne:


```python
df[df.A > 0]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
      <td>0.642595</td>
      <td>-0.136862</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>0.437396</td>
      <td>0.310099</td>
      <td>-0.169594</td>
      <td>0.391921</td>
    </tr>
  </tbody>
</table>
</div>



Ou alors récupérer les  lignes pour lesquelles une condition
est vérifiée pour au moins une colonne dans la ligne:


```python
df[df > 0]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.636811</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>NaN</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>NaN</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>0.694458</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>NaN</td>
      <td>1.054788</td>
      <td>NaN</td>
      <td>0.801541</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
      <td>0.642595</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>0.437396</td>
      <td>0.310099</td>
      <td>NaN</td>
      <td>0.391921</td>
    </tr>
  </tbody>
</table>
</div>



On peut sélectionner les  lignes pour lesquelles les valeurs
d'une certaine colonne sont  contenue dans une collection de
valeurs:


```python
df2 = df.copy()
df2['E'] = ['one', 'one', 'two', 'three', 'four', 'three']
df2
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>E</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>-2.759782</td>
      <td>-0.754355</td>
      <td>0.636811</td>
      <td>-0.412057</td>
      <td>one</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>-0.276277</td>
      <td>one</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>0.694458</td>
      <td>two</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>1.054788</td>
      <td>-0.461713</td>
      <td>0.801541</td>
      <td>three</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
      <td>0.642595</td>
      <td>-0.136862</td>
      <td>four</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>0.437396</td>
      <td>0.310099</td>
      <td>-0.169594</td>
      <td>0.391921</td>
      <td>three</td>
    </tr>
  </tbody>
</table>
</div>




```python
df2[df2['E'].isin(['two', 'four'])]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>E</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>0.694458</td>
      <td>two</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
      <td>0.642595</td>
      <td>-0.136862</td>
      <td>four</td>
    </tr>
  </tbody>
</table>
</div>



### Assignation de valeurs

Quand  on  crée  une  nouvelle  colonne,  les  données  sont
automatiquement  alignées sur  l'index  déjà  en place  (les
valeurs associées  à l'index déjà en  place sont conservées,
celles en trop dans l'ordre lexicographique sont ignorées et
celles manquantes sont mises à NAN)


```python
s1 = pd.Series([1, 2, 3, 4, 5, 6], index=pd.date_range('20190331', periods=6))
s1
```




    2019-03-31    1
    2019-04-01    2
    2019-04-02    3
    2019-04-03    4
    2019-04-04    5
    2019-04-05    6
    Freq: D, dtype: int64




```python
df['F'] = s1
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>-2.759782</td>
      <td>-0.754355</td>
      <td>0.636811</td>
      <td>-0.412057</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>-0.276277</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>0.694458</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>1.054788</td>
      <td>-0.461713</td>
      <td>0.801541</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
      <td>0.642595</td>
      <td>-0.136862</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>0.437396</td>
      <td>0.310099</td>
      <td>-0.169594</td>
      <td>0.391921</td>
      <td>5.0</td>
    </tr>
  </tbody>
</table>
</div>



On peut  assigner des valeurs  en indexant le  dataframe par
des labels ou par des entiers:


```python
df.at[dates[0], 'A'] = 0
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>0.000000</td>
      <td>-0.754355</td>
      <td>0.636811</td>
      <td>-0.412057</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>-0.276277</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>0.694458</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>1.054788</td>
      <td>-0.461713</td>
      <td>0.801541</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
      <td>0.642595</td>
      <td>-0.136862</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>0.437396</td>
      <td>0.310099</td>
      <td>-0.169594</td>
      <td>0.391921</td>
      <td>5.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.iat[0, 1] = 0
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.636811</td>
      <td>-0.412057</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>-0.276277</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>0.694458</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>1.054788</td>
      <td>-0.461713</td>
      <td>0.801541</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
      <td>0.642595</td>
      <td>-0.136862</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>0.437396</td>
      <td>0.310099</td>
      <td>-0.169594</td>
      <td>0.391921</td>
      <td>5.0</td>
    </tr>
  </tbody>
</table>
</div>



On peut aussi assigner une  nouvelle colonne en utilisant un
ndarray Numpy. Il  faut par contre que la  taille du ndarray
soit la même que celle du dataframe (son nombre de lignes)


```python
df.loc[:, 'D'] = np.array([5] * len(df))
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.636811</td>
      <td>5</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>5</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>5</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>1.054788</td>
      <td>-0.461713</td>
      <td>5</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>0.369715</td>
      <td>1.549302</td>
      <td>0.642595</td>
      <td>5</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>0.437396</td>
      <td>0.310099</td>
      <td>-0.169594</td>
      <td>5</td>
      <td>5.0</td>
    </tr>
  </tbody>
</table>
</div>



On peut modifier des valeurs  dans le dataframe aux endroits
vérifiant un condition (une clause `WHERE`):


```python
df2 = df.copy()
df2[df2 > 0] = -df2
df2
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>-0.636811</td>
      <td>-5</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>-0.246851</td>
      <td>-1.359295</td>
      <td>-5</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>-0.809926</td>
      <td>-0.687781</td>
      <td>-5</td>
      <td>-2.0</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>-1.054788</td>
      <td>-0.461713</td>
      <td>-5</td>
      <td>-3.0</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>-0.369715</td>
      <td>-1.549302</td>
      <td>-0.642595</td>
      <td>-5</td>
      <td>-4.0</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>-0.437396</td>
      <td>-0.310099</td>
      <td>-0.169594</td>
      <td>-5</td>
      <td>-5.0</td>
    </tr>
  </tbody>
</table>
</div>



## Données manquantes

Les  données manquantes  dans Pandas  sont représentées  par
`np.nan`. Ces  données manquantes ne sont  pas incluses dans
les calculs par défaut.

Pour  changer, ajouter  ou effacer  des index  sur des  axes
spécifiques, on applique l'opération `.reindex` en précisant
le nouvel index (pour les lignes) et les nouvelles colonnes:


```python
df1 = df.reindex(index=dates[0:4], columns=list(df.columns) + ['E'])
df1.loc[dates[0]:dates[1], 'E'] = 1
df1
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>F</th>
      <th>E</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.636811</td>
      <td>5</td>
      <td>NaN</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>5</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>5</td>
      <td>2.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>1.054788</td>
      <td>-0.461713</td>
      <td>5</td>
      <td>3.0</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



Pour supprimer les lignes qui ont des données manquantes, il
faut utiliser `.dropna`


```python
df1.dropna(how='any')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>F</th>
      <th>E</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>5</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
</div>



Pour  remplacer les  valeurs manquantes  par une  valeur par
défaut, il faut utiliser `.fillna`


```python
df1.fillna(value=5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>F</th>
      <th>E</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.636811</td>
      <td>5</td>
      <td>5.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.359295</td>
      <td>5</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.698618</td>
      <td>0.809926</td>
      <td>0.687781</td>
      <td>5</td>
      <td>2.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-0.350507</td>
      <td>1.054788</td>
      <td>-0.461713</td>
      <td>5</td>
      <td>3.0</td>
      <td>5.0</td>
    </tr>
  </tbody>
</table>
</div>



On  peut obtenir  un  masque de  booléens,  qui indique  les
endroits où il manque des données avec `pd.isna`


```python
pd.isna(df1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>F</th>
      <th>E</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
</div>



## Opérations

En général, les opérations exclues les données manquantes.

### Statistiques

Pour obtenir une moyenne colonne par colonne:


```python
df.mean()
```




    A   -0.065930
    B    0.661828
    C    0.449196
    D    5.000000
    F    3.000000
    dtype: float64



Pour obtenir une moyenne ligne par ligne:


```python
df.mean(1)
```




    2019-03-30    1.409203
    2019-03-31    1.490516
    2019-04-01    1.559818
    2019-04-02    1.648513
    2019-04-03    2.312322
    2019-04-04    2.115580
    Freq: D, dtype: float64



Le `1`  dans le code  précédent indique suivant quel  axe on
veut faire la  moyenne, sachant que `0`  (ou pas d'argument)
correspond à l'axe des lignes et `1` à l'axe des colonnes.

On peut faire  des opérations entre 2  structures de données
de dimensions différentes (dataframe et series):


```python
s = pd.Series([1, 3, 5, np.nan, 6, 8], index=dates).shift(2)
s
```




    2019-03-30    NaN
    2019-03-31    NaN
    2019-04-01    1.0
    2019-04-02    3.0
    2019-04-03    5.0
    2019-04-04    NaN
    Freq: D, dtype: float64




```python
df.sub(s, axis='index')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-1.698618</td>
      <td>-0.190074</td>
      <td>-0.312219</td>
      <td>4.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-3.350507</td>
      <td>-1.945212</td>
      <td>-3.461713</td>
      <td>2.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>-4.630285</td>
      <td>-3.450698</td>
      <td>-4.357405</td>
      <td>0.0</td>
      <td>-1.0</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



### Application

On  peut appliquer  des  fonctions aux  données colonne  par
colonne (le paramètre de la fonction est une colonne)


```python
df.apply(np.cumsum)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-03-30</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.636811</td>
      <td>5</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2019-03-31</th>
      <td>-0.153566</td>
      <td>0.246851</td>
      <td>1.996106</td>
      <td>10</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2019-04-01</th>
      <td>-0.852184</td>
      <td>1.056777</td>
      <td>2.683887</td>
      <td>15</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>2019-04-02</th>
      <td>-1.202691</td>
      <td>2.111565</td>
      <td>2.222174</td>
      <td>20</td>
      <td>6.0</td>
    </tr>
    <tr>
      <th>2019-04-03</th>
      <td>-0.832976</td>
      <td>3.660867</td>
      <td>2.864769</td>
      <td>25</td>
      <td>10.0</td>
    </tr>
    <tr>
      <th>2019-04-04</th>
      <td>-0.395580</td>
      <td>3.970966</td>
      <td>2.695176</td>
      <td>30</td>
      <td>15.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.apply(lambda x: x.max() - x.min())
```




    A    1.136014
    B    1.549302
    C    1.821009
    D    0.000000
    F    4.000000
    dtype: float64



### Histogrammes

Pour obtenir  un histogramme (le compte  valeur par valeur),
on dispose de la méthode `.value_counts`


```python
s = pd.Series(np.random.randint(0, 7, size=10))
s
```




    0    0
    1    2
    2    0
    3    5
    4    5
    5    4
    6    2
    7    0
    8    0
    9    1
    dtype: int64




```python
s.value_counts()
```




    0    4
    5    2
    2    2
    4    1
    1    1
    dtype: int64



### Méthodes sur les chaînes de caractères

Ces  méthodes sont  rassemblées  dans  l'attribut `str`  des
structures de données Pandas,  et permettent d'effectuer des
opérations  sur les  valeurs de  la structure  qui sont  des
chaînes de caractères.


```python
s = pd.Series(['A', 'B', 'C', 'Aaba', 'Baca', np.nan, 'CABA', 'dog', 'cat'])
s.str.lower()
```




    0       a
    1       b
    2       c
    3    aaba
    4    baca
    5     NaN
    6    caba
    7     dog
    8     cat
    dtype: object



## Combinaisons

Pandas fournit  différentes façons de combiner  aisément les
`Series` et les  `DataFrame`. On peut le  faire en utilisant
différents types  de logiques d'ensembles pour  les index et
d'algèbre relationnelle pour les opérations de type jointure
/ fusion.

### Concaténer

La  concaténation de  2 objets  Pandas  se fait  grâce à  la
fonction `pd.concat`


```python
df = pd.DataFrame(np.random.randn(10, 4))
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1.729973</td>
      <td>0.058934</td>
      <td>-0.434967</td>
      <td>1.108158</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-0.933198</td>
      <td>-1.116243</td>
      <td>0.398964</td>
      <td>-1.573282</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.023501</td>
      <td>0.625520</td>
      <td>-0.154714</td>
      <td>-0.654235</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.344503</td>
      <td>-0.249123</td>
      <td>-1.504876</td>
      <td>-1.203312</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-0.244597</td>
      <td>0.115774</td>
      <td>-0.830470</td>
      <td>2.052748</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-1.340891</td>
      <td>0.584198</td>
      <td>0.238852</td>
      <td>-0.596003</td>
    </tr>
    <tr>
      <th>6</th>
      <td>3.031119</td>
      <td>-1.437290</td>
      <td>-0.581537</td>
      <td>-1.749066</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.224386</td>
      <td>0.097499</td>
      <td>0.577294</td>
      <td>-0.069991</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0.292925</td>
      <td>-0.606479</td>
      <td>1.050523</td>
      <td>-1.607612</td>
    </tr>
    <tr>
      <th>9</th>
      <td>-0.878079</td>
      <td>-1.290651</td>
      <td>-0.628939</td>
      <td>-0.334491</td>
    </tr>
  </tbody>
</table>
</div>




```python
pieces = [df[:3], df[3:7], df[7:]]
pd.concat(pieces)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>-1.729973</td>
      <td>0.058934</td>
      <td>-0.434967</td>
      <td>1.108158</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-0.933198</td>
      <td>-1.116243</td>
      <td>0.398964</td>
      <td>-1.573282</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.023501</td>
      <td>0.625520</td>
      <td>-0.154714</td>
      <td>-0.654235</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.344503</td>
      <td>-0.249123</td>
      <td>-1.504876</td>
      <td>-1.203312</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-0.244597</td>
      <td>0.115774</td>
      <td>-0.830470</td>
      <td>2.052748</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-1.340891</td>
      <td>0.584198</td>
      <td>0.238852</td>
      <td>-0.596003</td>
    </tr>
    <tr>
      <th>6</th>
      <td>3.031119</td>
      <td>-1.437290</td>
      <td>-0.581537</td>
      <td>-1.749066</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.224386</td>
      <td>0.097499</td>
      <td>0.577294</td>
      <td>-0.069991</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0.292925</td>
      <td>-0.606479</td>
      <td>1.050523</td>
      <td>-1.607612</td>
    </tr>
    <tr>
      <th>9</th>
      <td>-0.878079</td>
      <td>-1.290651</td>
      <td>-0.628939</td>
      <td>-0.334491</td>
    </tr>
  </tbody>
</table>
</div>



### Joindre

Il s'agit de l'opération analogue  en SQL. Pour ce faire, il
faut utilser la fonction `pd.merge`


```python
left = pd.DataFrame({'key': ['foo', 'foo'], 'lval': [1, 2]})
right = pd.DataFrame({'key': ['foo', 'foo'], 'rval': [4, 5]})
left
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>lval</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>foo</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>foo</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>




```python
right
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>rval</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>foo</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>foo</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.merge(left, right, on='key')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>lval</th>
      <th>rval</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>foo</td>
      <td>1</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>foo</td>
      <td>1</td>
      <td>5</td>
    </tr>
    <tr>
      <th>2</th>
      <td>foo</td>
      <td>2</td>
      <td>4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>foo</td>
      <td>2</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>



Le  `pd.merge`   effectue  une  union  des   données  des  2
structures en se basant sur la clé passée en paramètre.


```python
left = pd.DataFrame({'key': ['foo', 'bar'], 'lval': [1, 2]})
right = pd.DataFrame({'key': ['foo', 'bar'], 'rval': [4, 5]})
left
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>lval</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>foo</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>bar</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>




```python
right
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>rval</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>foo</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>bar</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.merge(left, right, on='key')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>key</th>
      <th>lval</th>
      <th>rval</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>foo</td>
      <td>1</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>bar</td>
      <td>2</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>



### Annexer

On peut rajouter des lignes à un `DataFrame`


```python
df = pd.DataFrame(np.random.randn(8, 4), columns=['A', 'B', 'C', 'D'])
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.620042</td>
      <td>0.222848</td>
      <td>-1.542318</td>
      <td>0.265275</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-0.035750</td>
      <td>-0.484962</td>
      <td>1.657518</td>
      <td>0.920229</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1.610796</td>
      <td>-0.123767</td>
      <td>3.037619</td>
      <td>-1.396509</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.047643</td>
      <td>-0.687491</td>
      <td>-0.944381</td>
      <td>3.190332</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-0.780613</td>
      <td>0.409961</td>
      <td>-0.673624</td>
      <td>0.905534</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-1.532464</td>
      <td>-0.396571</td>
      <td>-0.105000</td>
      <td>-0.054862</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1.699681</td>
      <td>-0.072909</td>
      <td>-0.830766</td>
      <td>-0.770954</td>
    </tr>
    <tr>
      <th>7</th>
      <td>-1.513352</td>
      <td>0.328086</td>
      <td>0.934592</td>
      <td>-0.124238</td>
    </tr>
  </tbody>
</table>
</div>




```python
s = df.iloc[3]
df.append(s, ignore_index=True)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.620042</td>
      <td>0.222848</td>
      <td>-1.542318</td>
      <td>0.265275</td>
    </tr>
    <tr>
      <th>1</th>
      <td>-0.035750</td>
      <td>-0.484962</td>
      <td>1.657518</td>
      <td>0.920229</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1.610796</td>
      <td>-0.123767</td>
      <td>3.037619</td>
      <td>-1.396509</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.047643</td>
      <td>-0.687491</td>
      <td>-0.944381</td>
      <td>3.190332</td>
    </tr>
    <tr>
      <th>4</th>
      <td>-0.780613</td>
      <td>0.409961</td>
      <td>-0.673624</td>
      <td>0.905534</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-1.532464</td>
      <td>-0.396571</td>
      <td>-0.105000</td>
      <td>-0.054862</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1.699681</td>
      <td>-0.072909</td>
      <td>-0.830766</td>
      <td>-0.770954</td>
    </tr>
    <tr>
      <th>7</th>
      <td>-1.513352</td>
      <td>0.328086</td>
      <td>0.934592</td>
      <td>-0.124238</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0.047643</td>
      <td>-0.687491</td>
      <td>-0.944381</td>
      <td>3.190332</td>
    </tr>
  </tbody>
</table>
</div>



## Grouper

L'opération `.grouby`  est une  procédure impliquant  une ou
plusieurs des actions suivantes:

* Séparer les données en groupes suivant un certain critère

* Appliquer une fonction à chaque groupe indépendamment

* Combiner le résultat dans une structure de donnée


```python
df = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar',
                         'foo', 'bar', 'foo', 'foo'],
                   'B': ['one', 'one', 'two', 'three',
                         'two', 'two', 'one', 'three'],
                   'C': np.random.randn(8),
                   'D': np.random.randn(8)})
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>foo</td>
      <td>one</td>
      <td>0.647957</td>
      <td>-0.725883</td>
    </tr>
    <tr>
      <th>1</th>
      <td>bar</td>
      <td>one</td>
      <td>0.376489</td>
      <td>-0.385296</td>
    </tr>
    <tr>
      <th>2</th>
      <td>foo</td>
      <td>two</td>
      <td>-0.399363</td>
      <td>-1.342656</td>
    </tr>
    <tr>
      <th>3</th>
      <td>bar</td>
      <td>three</td>
      <td>0.458775</td>
      <td>1.688988</td>
    </tr>
    <tr>
      <th>4</th>
      <td>foo</td>
      <td>two</td>
      <td>1.076639</td>
      <td>0.131735</td>
    </tr>
    <tr>
      <th>5</th>
      <td>bar</td>
      <td>two</td>
      <td>-1.100755</td>
      <td>-0.753938</td>
    </tr>
    <tr>
      <th>6</th>
      <td>foo</td>
      <td>one</td>
      <td>0.084555</td>
      <td>1.546450</td>
    </tr>
    <tr>
      <th>7</th>
      <td>foo</td>
      <td>three</td>
      <td>1.105213</td>
      <td>-1.946767</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.groupby('A').sum() 
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>C</th>
      <th>D</th>
    </tr>
    <tr>
      <th>A</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>bar</th>
      <td>-0.265491</td>
      <td>0.549754</td>
    </tr>
    <tr>
      <th>foo</th>
      <td>2.515001</td>
      <td>-2.337120</td>
    </tr>
  </tbody>
</table>
</div>



Grouper par plusieurs colonnes forme un index hiérarchique


```python
df.groupby(['A', 'B']).sum()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>C</th>
      <th>D</th>
    </tr>
    <tr>
      <th>A</th>
      <th>B</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="3" valign="top">bar</th>
      <th>one</th>
      <td>0.376489</td>
      <td>-0.385296</td>
    </tr>
    <tr>
      <th>three</th>
      <td>0.458775</td>
      <td>1.688988</td>
    </tr>
    <tr>
      <th>two</th>
      <td>-1.100755</td>
      <td>-0.753938</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">foo</th>
      <th>one</th>
      <td>0.732512</td>
      <td>0.820567</td>
    </tr>
    <tr>
      <th>three</th>
      <td>1.105213</td>
      <td>-1.946767</td>
    </tr>
    <tr>
      <th>two</th>
      <td>0.677276</td>
      <td>-1.210921</td>
    </tr>
  </tbody>
</table>
</div>



## Modification de la forme des structures de données

### Empilement

La méthode  `.stack` "comprime" un niveau  dans les colonnes
du  DataFrame   (i.e  les  colonnes  deviennent   un  niveau
supplémentaire d'indexation à la ligne des données)


```python
tuples = list(zip(*[['bar', 'bar', 'baz', 'baz',
                     'foo', 'foo', 'qux', 'qux'],
                    ['one', 'two', 'one', 'two',
                     'one', 'two', 'one', 'two']]))
index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second'])
df = pd.DataFrame(np.random.randn(8, 2), index=index, columns=['A', 'B'])
df2 = df[:4]
df2
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>A</th>
      <th>B</th>
    </tr>
    <tr>
      <th>first</th>
      <th>second</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">bar</th>
      <th>one</th>
      <td>-0.030511</td>
      <td>0.412391</td>
    </tr>
    <tr>
      <th>two</th>
      <td>-0.790359</td>
      <td>-1.050496</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">baz</th>
      <th>one</th>
      <td>-0.641583</td>
      <td>0.139852</td>
    </tr>
    <tr>
      <th>two</th>
      <td>-0.621345</td>
      <td>0.009085</td>
    </tr>
  </tbody>
</table>
</div>




```python
stacked = df2.stack()
stacked
```




    first  second   
    bar    one     A   -0.030511
                   B    0.412391
           two     A   -0.790359
                   B   -1.050496
    baz    one     A   -0.641583
                   B    0.139852
           two     A   -0.621345
                   B    0.009085
    dtype: float64



L'opération  inverse   de  `.stack`  c'est   `.unstack`.  La
structure d'entrée doit contenir un `MultiIndex` comme index
pour que ça marche:


```python
stacked.unstack()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>A</th>
      <th>B</th>
    </tr>
    <tr>
      <th>first</th>
      <th>second</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">bar</th>
      <th>one</th>
      <td>-0.030511</td>
      <td>0.412391</td>
    </tr>
    <tr>
      <th>two</th>
      <td>-0.790359</td>
      <td>-1.050496</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">baz</th>
      <th>one</th>
      <td>-0.641583</td>
      <td>0.139852</td>
    </tr>
    <tr>
      <th>two</th>
      <td>-0.621345</td>
      <td>0.009085</td>
    </tr>
  </tbody>
</table>
</div>


Si  une  valeur  numérique  est passée  en  paramètre,  elle
indique suivant quel niveau d'indexation il faut déplier les
données:

```python
stacked.unstack(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>second</th>
      <th>one</th>
      <th>two</th>
    </tr>
    <tr>
      <th>first</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">bar</th>
      <th>A</th>
      <td>-0.030511</td>
      <td>-0.790359</td>
    </tr>
    <tr>
      <th>B</th>
      <td>0.412391</td>
      <td>-1.050496</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">baz</th>
      <th>A</th>
      <td>-0.641583</td>
      <td>-0.621345</td>
    </tr>
    <tr>
      <th>B</th>
      <td>0.139852</td>
      <td>0.009085</td>
    </tr>
  </tbody>
</table>
</div>




```python
stacked.unstack(0)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>first</th>
      <th>bar</th>
      <th>baz</th>
    </tr>
    <tr>
      <th>second</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">one</th>
      <th>A</th>
      <td>-0.030511</td>
      <td>-0.641583</td>
    </tr>
    <tr>
      <th>B</th>
      <td>0.412391</td>
      <td>0.139852</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">two</th>
      <th>A</th>
      <td>-0.790359</td>
      <td>-0.621345</td>
    </tr>
    <tr>
      <th>B</th>
      <td>-1.050496</td>
      <td>0.009085</td>
    </tr>
  </tbody>
</table>
</div>


### Tableaux croisés dynamiques (Pivot tables)

D'après       Wikipédia,       un      [tableau       croisé
dynamique](https://fr.wikipedia.org/wiki/Tableau_crois%C3%A9_dynamique)
est une synthèse d'une table de données brutes. Dans Pandas,
une  telle   table  s'obtient   à  l'aide  de   la  fonction
`pd.pivot_table`


```python
df = pd.DataFrame({'A': ['one', 'one', 'two', 'three'] * 3,
                   'B': ['A', 'B', 'C'] * 4,
                   'C': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'] * 2,
                   'D': np.random.randn(12),
                   'E': np.random.randn(12)})
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>E</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>one</td>
      <td>A</td>
      <td>foo</td>
      <td>-1.637443</td>
      <td>-0.198674</td>
    </tr>
    <tr>
      <th>1</th>
      <td>one</td>
      <td>B</td>
      <td>foo</td>
      <td>0.538599</td>
      <td>0.902056</td>
    </tr>
    <tr>
      <th>2</th>
      <td>two</td>
      <td>C</td>
      <td>foo</td>
      <td>-2.065462</td>
      <td>-0.817254</td>
    </tr>
    <tr>
      <th>3</th>
      <td>three</td>
      <td>A</td>
      <td>bar</td>
      <td>0.298942</td>
      <td>0.411964</td>
    </tr>
    <tr>
      <th>4</th>
      <td>one</td>
      <td>B</td>
      <td>bar</td>
      <td>1.100118</td>
      <td>2.218368</td>
    </tr>
    <tr>
      <th>5</th>
      <td>one</td>
      <td>C</td>
      <td>bar</td>
      <td>0.198245</td>
      <td>-0.056927</td>
    </tr>
    <tr>
      <th>6</th>
      <td>two</td>
      <td>A</td>
      <td>foo</td>
      <td>0.917070</td>
      <td>-0.406791</td>
    </tr>
    <tr>
      <th>7</th>
      <td>three</td>
      <td>B</td>
      <td>foo</td>
      <td>-1.003526</td>
      <td>-2.001790</td>
    </tr>
    <tr>
      <th>8</th>
      <td>one</td>
      <td>C</td>
      <td>foo</td>
      <td>-0.379830</td>
      <td>-0.396019</td>
    </tr>
    <tr>
      <th>9</th>
      <td>one</td>
      <td>A</td>
      <td>bar</td>
      <td>0.406914</td>
      <td>1.897216</td>
    </tr>
    <tr>
      <th>10</th>
      <td>two</td>
      <td>B</td>
      <td>bar</td>
      <td>1.009347</td>
      <td>-0.139946</td>
    </tr>
    <tr>
      <th>11</th>
      <td>three</td>
      <td>C</td>
      <td>bar</td>
      <td>-0.182149</td>
      <td>-1.637063</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.pivot_table(df, values='D', index=['A', 'B'], columns=['C'])
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>C</th>
      <th>bar</th>
      <th>foo</th>
    </tr>
    <tr>
      <th>A</th>
      <th>B</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="3" valign="top">one</th>
      <th>A</th>
      <td>0.406914</td>
      <td>-1.637443</td>
    </tr>
    <tr>
      <th>B</th>
      <td>1.100118</td>
      <td>0.538599</td>
    </tr>
    <tr>
      <th>C</th>
      <td>0.198245</td>
      <td>-0.379830</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">three</th>
      <th>A</th>
      <td>0.298942</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>B</th>
      <td>NaN</td>
      <td>-1.003526</td>
    </tr>
    <tr>
      <th>C</th>
      <td>-0.182149</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">two</th>
      <th>A</th>
      <td>NaN</td>
      <td>0.917070</td>
    </tr>
    <tr>
      <th>B</th>
      <td>1.009347</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>C</th>
      <td>NaN</td>
      <td>-2.065462</td>
    </tr>
  </tbody>
</table>
</div>



## Séries temporelles

Pandas  fournit  un  moyen  simple,  puissant  et  efficient
d'effectuer  du re-échantillonage  (par  exemple, passer  de
données variant  toutes les  secondes à des  données variant
toutes les 5 minutes)


```python
rng = pd.date_range('1/1/2012', periods=100, freq='S')
ts = pd.Series(np.random.randint(0, 500, len(rng)), index=rng)
ts.resample('5Min').sum()
```




    2012-01-01    29667
    Freq: 5T, dtype: int64



Pandas   permet  de   représenter   les  zones   temporelles
(TimeZones)


```python
rng = pd.date_range('3/6/2012 00:00', periods=5, freq='D')
ts = pd.Series(np.random.randn(len(rng)), rng)
ts
```




    2012-03-06   -1.802124
    2012-03-07    1.500321
    2012-03-08   -0.263506
    2012-03-09   -1.027141
    2012-03-10   -2.014588
    Freq: D, dtype: float64


Le résultat ci-dessus n'est  pas "localisé" (i.e ne contient
pas les "vraie"  date et heure associée à un  pays). Pour ce
faire, il suffit d'appeler la méthode `tz_localize`:

```python
ts_utc = ts.tz_localize('UTC')
ts_utc
```




    2012-03-06 00:00:00+00:00   -1.802124
    2012-03-07 00:00:00+00:00    1.500321
    2012-03-08 00:00:00+00:00   -0.263506
    2012-03-09 00:00:00+00:00   -1.027141
    2012-03-10 00:00:00+00:00   -2.014588
    Freq: D, dtype: float64



On peut ainsi convertir d'une timezone à l'autre


```python
ts_utc.tz_convert('US/Eastern')
```




    2012-03-05 19:00:00-05:00   -1.802124
    2012-03-06 19:00:00-05:00    1.500321
    2012-03-07 19:00:00-05:00   -0.263506
    2012-03-08 19:00:00-05:00   -1.027141
    2012-03-09 19:00:00-05:00   -2.014588
    Freq: D, dtype: float64



On    peut    convertir     entre    différentes    étendues
temporelles. Créons  une série  temporelle s'étendant  sur 5
mois (`freq="M"` ci-dessous):


```python
rng = pd.date_range('1/1/2012', periods=5, freq='M')
ts = pd.Series(np.random.randn(len(rng)), index=rng)
ts
```




    2012-01-31    0.441643
    2012-02-29   -0.711276
    2012-03-31    0.784683
    2012-04-30   -0.984221
    2012-05-31    0.061811
    Freq: M, dtype: float64

Ci-dessus,   on   a   débuté   l'index   temporel   au   1er
Janvier 2012. Comme on a précisé qu'on voulait une fréquence
mensuelle,  Pandas  a  automatiquement converti  l'index  en
prenant les fins de mois de la période.

Avec la méthode `to_period`, on  peut ne retenir que le mois
(dans le cadre d'une fréquence mensuelle):


```python
ps = ts.to_period()
ps
```




    2012-01    0.441643
    2012-02   -0.711276
    2012-03    0.784683
    2012-04   -0.984221
    2012-05    0.061811
    Freq: M, dtype: float64


Avec la  méthode `to_timestamp`, Pandas respecte  la date de
début de la  période. C'est donc le 1er jour  de chaque mois
de la période qui est choisi:


```python
ps.to_timestamp()
```




    2012-01-01    0.441643
    2012-02-01   -0.711276
    2012-03-01    0.784683
    2012-04-01   -0.984221
    2012-05-01    0.061811
    Freq: MS, dtype: float64



Convertir  entre  période  et timestamp  permet  d'appliquer
certaines fonctions arithmétiques  utiles. Par exemple, pour
convertir d'une  fréquence de  1/4 d'années avec  l'année se
terminant  en  Novembre en  une  fréquence  de 1/4  d'années
chaque quart  se terminant à 9h  du matin de la  fin du mois
suivant la fin du 1/4, on fait ceci:


```python
prng = pd.period_range('1990Q1', '2000Q4', freq='Q-NOV')
ts = pd.Series(np.random.randn(len(prng)), prng)
ts.index = (prng.asfreq('M', 'e') + 1).asfreq('H', 's')
ts.head()
```




    1990-03-01 00:00   -0.182267
    1990-06-01 00:00    0.342509
    1990-09-01 00:00   -0.179646
    1990-12-01 00:00    0.147279
    1991-03-01 00:00    0.938427
    Freq: H, dtype: float64



## Catégories

Pandas peut inclure des données de catégories dans un `DataFrame`


```python
df = pd.DataFrame({'id': [1, 2, 3, 4, 5, 6],
                   'raw_grade': ['a', 'b', 'b', 'a', 'a', 'e']})
```

Convertir les moyennes brûtes en données de type catégories:


```python
df['grade'] = df['raw_grade'].astype('category')
df['grade']
```




    0    a
    1    b
    2    b
    3    a
    4    a
    5    e
    Name: grade, dtype: category
    Categories (3, object): [a, b, e]



Renommer les catégories en des noms plus significatifs:


```python
df['grade'].cat.categories = ['very good', 'good', 'very bad']
```

Réordonner  les  catégories  et  ajouter  simultanément  les
catégories manquantes:


```python
df['grade'] = df['grade'].cat.set_categories(['very bad', 'bad', 'medium', 'good', 'very good'])
df['grade']
```

    0    very good
    1         good
    2         good
    3    very good
    4    very good
    5     very bad
    Name: grade, dtype: category
    Categories (5, object): [very bad, bad, medium, good, very good]



## Affichages graphiques

La méthode `.plot`  est une méthode utile  pour afficher sur
un graphique toutes les colonnes avec les labels:


```python
ts = pd.Series(np.random.randn(1000),
               index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
ts.plot()
```

    <matplotlib.axes._subplots.AxesSubplot at 0x7fc3a2db3748>

<img src="/images/an_mod_donnees_python_pandas/output_165_1.png" alt="output_165_1" style="background-color: white;" />



```python
df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, 
                  columns=['A', 'B', 'C', 'D'])
df = df.cumsum()
plt.figure()
df.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fc3a2a7d470>

<img src="/images/an_mod_donnees_python_pandas/output_169_1.png" alt="output_169_1" style="background-color: white;" />


## Gestion des entrées / sorties des données

### CSV

utiliser `.to_csv` pour écrire dans un CSV, `.read_csv` pour
lire un CSV.

### HDF5

Utiliser  `.to_hdf`   pour  écrire   dans  un   HDFStore  et
`.read_hdf` pour en lire un.

### Excel

Utiliser `.to_excel`  pour écrire  et `.read_excel`  pour la
lecture.

Pour conclure,  comme vous pouvez  le voir, Pandas  offre un
panel bien  large de possibilité pour  l'analyse des données
avec Python.

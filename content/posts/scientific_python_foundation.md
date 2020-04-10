---
title: Le socle du calcul scientifique en Python
date: 2019-05-15
status: published
tags: [python, science, informatique, programmation]
---


Tout calcul scientifique efficient qui utilise le langage de
programmation  Python  est  construit   sur  la  base  d'une
structure de  donnée efficiente: le tableau  à N dimensions,
dont   l'implémentation  est   fournie   par  la   librairie
scientifique [Numpy](https://www.numpy.org/). Cette dernière
apporte non seulement cette  structure de donnée importante,
mais également toute  une batterie d'implémentation d'outils
mathématiques manipulant  cette structure, et  permettant de
réaliser   tout   genre  d'opérations,   depuis   l'[algèbre
linéaire](https://fr.wikipedia.org/wiki/Alg%C3%A8bre_lin%C3%A9aire)
jusqu'aux                  [transformées                  de
Fourier](https://fr.wikipedia.org/wiki/Transformation_de_Fourier),
etc. Les prochaines lignes sont  dédiées à la découverte des
possibilités offertes par cette librairie.

## L'élément fondamental

L'objet de  base de  Numpy est un  tableau multidimensionnel
homogène  (tous les  éléments du  tableau, généralement  des
nombres,    sont   du    même    type)    indexé   par    un
[tuple](https://docs.python.org/3.5/library/functions.html#func-tuple)
d'entiers. Une  dimension du  tableau est appelé  `axis` (au
pluriel `axes`).

Cette classe est appelée  `ndarray` (avec un alias `array`),
et ses éléments les plus importants sont:

- `ndarray.ndim`: Le nombre de dimensions du tableau
-  `ndarray.shape`:  Un  tuple d'entiers  correspondant  aux
  dimensions du tableau. Une dimension est représentée, dans
  ce   tuple,  par   la  taille   du  tableau   dans  chaque
  dimension.  Par  conséquent,  la   longueur  de  ce  tuple
  correspond exactement à la valeur de l'attribut `.ndim`
- `ndarray.size`: Le nombre total  d'éléments du tableau à N
  dimensions. Il s'agit  du produit de tous  les éléments de
  la valeur de l'attribut `.shape`
-  `ndarray.dtype`:  Le type  des  éléments  du tableau.  En
  principe  cela peut  être  tout type  de  base du  langage
  Python ou  des types spécifiques définis  par la librairie
  Numpy elle-même
- `ndarray.itemsize`:  La taille  occupée par un  élément du
  tableau     dans      la     mémoire      (exprimée     en
  [bytes](https://en.wikipedia.org/wiki/Byte)).   Elle   est
  définie  par  l'implémentation  du type  des  éléments  du
  tableau.
-   `ndarray.data`:  Le   tampon   contenant  les   éléments
  proprement  dits du  tableau. Cet  attribut n'est  que peu
  utilisé  directement  normalement,   car  l'obtention  des
  éléments se fait par des méthodes d'indexation du tableau.

## Création d'un array

Il  existe plusieurs  façons différentes  de créer  un objet
`ndarray`.

- Une liste (ou un tuple)  Python permet de créer un tableau
  à  une  dimension.  Si  le  paramètre  `dtype`  n'est  pas
  précisé,   un  type   est   automatiquement  assigné   aux
  éléments. Ce type  est le plus proche type  commun dans la
  [hiérarchie
  d'héritage](https://www.python.org/download/releases/2.3/mro/)
  de tous les éléments de  la liste. Si le paramètre `dtype`
  est précisé, tous les éléments de la liste doivent pouvoir
  être convertis en ce type.


```python
import numpy as np

a = np.array([1, 2, 3])
repr(a)
#array([1, 2, 3])
repr(a.dtype)
#dtype('int64')


class UneClasse:
    pass

# Tous les objets Python descendent de object. C'est donc lui le plus petit ancêtre
# commun à une Chaîne et une instance de classe définie par l'utilisateur
np.array(["chaîne", UneClasse()])
#array(['chaîne', <__main__.UneClasse object at 0x11002d990>], dtype=object)

# Type précisé, mais un élément de la liste n'est pas convertible ==> BOUM !
np.array([1, "non-convertible", 42], dtype=np.float64)
#    ---------------------------------------------------------------------------
#
#    ValueError                                Traceback (most recent call last)
#
#    <ipython-input-5-6cd39bcf21ee> in <module>
#          1 # Tpe précisé, mais un élément de la liste n'est pas convertible ==> BOUM !
#    ----> 2 np.array([1, "non-convertible", 42], dtype=np.float64)
#    
#
#    ValueError: could not convert string to float: 'non-convertible'
```

- Une séquence de séquences de même taille donne naissance à
  un tableau contenant  autant de dimensions qu'il  n'y a de
  séquences dans la séquence:


```python
np.array([[1, 2, 3], [4, 5, 6], (7, 8, 9)])
# array([[1, 2, 3],
#       [4, 5, 6],
#       [7, 8, 9]])

# L'opération échoue (obtention d'un tableau à N dimensions) si une seule séquence diffère par sa taille
a = np.array([(1, 2), [3, 4, 5], [6, 7, 8]])
repr(a)
#array([(1, 2), list([3, 4, 5]), list([6, 7, 8])], dtype=object)

# A la place, on obtient un tableau à une dimension, la classe la plus proche dans la hiérarchie des classes
# de chaque élément de la séquence
print("Number of Dimensions: ", a.ndim)
print("Shape: ", a.shape)
#Number of Dimensions:  1
#Shape:  (3,)
```

- On peut créer un tableau en connaissant seulement sa forme
  (`shape`). Pour cela il existe des fonctions spéciales qui
  remplissent le tableau de valeurs prédéfinies ou issues de
  la mémoire:


```python
# Remplit le tableau avec la valeur 1
np.ones((3, 5))
#array([[1., 1., 1., 1., 1.],
#       [1., 1., 1., 1., 1.],
#       [1., 1., 1., 1., 1.]])

# Remplit le tableau de 0s
np.zeros((3, 5))
#    array([[0., 0., 0., 0., 0.],
#           [0., 0., 0., 0., 0.],
#           [0., 0., 0., 0., 0.]])

# Remplit le teableau avec des valeurs aléatoires de la mémoire
np.empty((3, 5))
# Dans ce cas ca a donné:
#    array([[0., 0., 0., 0., 0.],
#           [0., 0., 0., 0., 0.],
#           [0., 0., 0., 0., 0.]])
```


- On peut générer une plage de nombres sous forme de tableau
  avec l'analogue Numpy de `range`:


```python
np.arange(10, 30, 5)
#    array([10, 15, 20, 25])
```



Avec la particularité que `arange` prend aussi des nombres à
virgule flottante comme paramètre:


```python
np.arange(0, 2, 0.3)
#    array([0. , 0.3, 0.6, 0.9, 1.2, 1.5, 1.8])
```


- Parfois, en  utilisant `arange`, il n'est  pas possible de
  savoir  combien d'éléments  vont être  générés à  cause du
  manque de  précision dans  l'implémentation des  nombres à
  virgule  flottante.  Il  est  donc  préférable  d'utiliser
  `linspace`, où on  peut préciser les limites  et le nombre
  d'éléments à générer:


```python
from numpy import pi

# Générer 9 nombres réels entre 0 et 2
np.linspace(0, 2, 9)
#    array([0.  , 0.25, 0.5 , 0.75, 1.  , 1.25, 1.5 , 1.75, 2.  ])

# Générer 100 nombres réels entre 0 et 2*pi
x = np.linspace(0, 2*pi, 100)
x
#    array([0.        , 0.06346652, 0.12693304, 0.19039955, 0.25386607,
#           0.31733259, 0.38079911, 0.44426563, 0.50773215, 0.57119866,
#           0.63466518, 0.6981317 , 0.76159822, 0.82506474, 0.88853126,
#           0.95199777, 1.01546429, 1.07893081, 1.14239733, 1.20586385,
#           1.26933037, 1.33279688, 1.3962634 , 1.45972992, 1.52319644,
#           1.58666296, 1.65012947, 1.71359599, 1.77706251, 1.84052903,
#           1.90399555, 1.96746207, 2.03092858, 2.0943951 , 2.15786162,
#           2.22132814, 2.28479466, 2.34826118, 2.41172769, 2.47519421,
#           2.53866073, 2.60212725, 2.66559377, 2.72906028, 2.7925268 ,
#           2.85599332, 2.91945984, 2.98292636, 3.04639288, 3.10985939,
#           3.17332591, 3.23679243, 3.30025895, 3.36372547, 3.42719199,
#           3.4906585 , 3.55412502, 3.61759154, 3.68105806, 3.74452458,
#           3.8079911 , 3.87145761, 3.93492413, 3.99839065, 4.06185717,
#           4.12532369, 4.1887902 , 4.25225672, 4.31572324, 4.37918976,
#           4.44265628, 4.5061228 , 4.56958931, 4.63305583, 4.69652235,
#           4.75998887, 4.82345539, 4.88692191, 4.95038842, 5.01385494,
#           5.07732146, 5.14078798, 5.2042545 , 5.26772102, 5.33118753,
#           5.39465405, 5.45812057, 5.52158709, 5.58505361, 5.64852012,
#           5.71198664, 5.77545316, 5.83891968, 5.9023862 , 5.96585272,
#           6.02931923, 6.09278575, 6.15625227, 6.21971879, 6.28318531])
```


On voit donc qu'on peut utiliser `linspace` pour évaluer une
fonction mathématique sur un intervalle donné:


```python
y = np.sin(x)
y
#    array([ 0.00000000e+00,  6.34239197e-02,  1.26592454e-01,  1.89251244e-01,
#            2.51147987e-01,  3.12033446e-01,  3.71662456e-01,  4.29794912e-01,
#            4.86196736e-01,  5.40640817e-01,  5.92907929e-01,  6.42787610e-01,
#            6.90079011e-01,  7.34591709e-01,  7.76146464e-01,  8.14575952e-01,
#            8.49725430e-01,  8.81453363e-01,  9.09631995e-01,  9.34147860e-01,
#            9.54902241e-01,  9.71811568e-01,  9.84807753e-01,  9.93838464e-01,
#            9.98867339e-01,  9.99874128e-01,  9.96854776e-01,  9.89821442e-01,
#            9.78802446e-01,  9.63842159e-01,  9.45000819e-01,  9.22354294e-01,
#            8.95993774e-01,  8.66025404e-01,  8.32569855e-01,  7.95761841e-01,
#            7.55749574e-01,  7.12694171e-01,  6.66769001e-01,  6.18158986e-01,
#            5.67059864e-01,  5.13677392e-01,  4.58226522e-01,  4.00930535e-01,
#            3.42020143e-01,  2.81732557e-01,  2.20310533e-01,  1.58001396e-01,
#            9.50560433e-02,  3.17279335e-02, -3.17279335e-02, -9.50560433e-02,
#           -1.58001396e-01, -2.20310533e-01, -2.81732557e-01, -3.42020143e-01,
#           -4.00930535e-01, -4.58226522e-01, -5.13677392e-01, -5.67059864e-01,
#           -6.18158986e-01, -6.66769001e-01, -7.12694171e-01, -7.55749574e-01,
#           -7.95761841e-01, -8.32569855e-01, -8.66025404e-01, -8.95993774e-01,
#           -9.22354294e-01, -9.45000819e-01, -9.63842159e-01, -9.78802446e-01,
#           -9.89821442e-01, -9.96854776e-01, -9.99874128e-01, -9.98867339e-01,
#           -9.93838464e-01, -9.84807753e-01, -9.71811568e-01, -9.54902241e-01,
#           -9.34147860e-01, -9.09631995e-01, -8.81453363e-01, -8.49725430e-01,
#           -8.14575952e-01, -7.76146464e-01, -7.34591709e-01, -6.90079011e-01,
#           -6.42787610e-01, -5.92907929e-01, -5.40640817e-01, -4.86196736e-01,
#           -4.29794912e-01, -3.71662456e-01, -3.12033446e-01, -2.51147987e-01,
#           -1.89251244e-01, -1.26592454e-01, -6.34239197e-02, -2.44929360e-16])
```



## Affichage d'un array

Un tableau est  affiché comme le sont  les listes imbriquées
en Python,  avec les  règles suivantes  pour la  lecture des
dimensions:

- La  dernière dimension est  affichée de la gauche  vers la
  droite (c'est la dimension des colones)
- L'avant  dernière dimension est  affichée du haut  vers le
  bas (c'est la dimension des lignes)
- Les autres dimensions sont  affichées du haut vers le bas,
  les éléments de chaque dimension étant séparés de ceux des
  autres par des lignes vides
-  Si   un  tableau  est   trop  large  pour   être  affiché
  correctement, seules  les extrémités sont  affichées, avec
  des points  de suspension  entre les  2. Pour  afficher la
  totalité des éléments  du tableau, il faut  faire appel à:
  `numpy.set_printoptions(threshold=numpy.nan)`


```python
a = np.arange(6) # Vecteur (ou matrice à une dimension)
print(a)
#    [0 1 2 3 4 5]

b = np.arange(12).reshape(4, 3) # Matrice à 2D 4x3
print(b)
#    [[ 0  1  2]
#     [ 3  4  5]
#     [ 6  7  8]
#     [ 9 10 11]]

c = np.arange(24).reshape(2, 3, 4) # Matrice 3D 2x3x4
# Affiche une liste de 2 matrices 2D 3x4 séparées par une ligne blanche vide.
print(c)
#    [[[ 0  1  2  3]
#      [ 4  5  6  7]
#      [ 8  9 10 11]]
#    
#     [[12 13 14 15]
#      [16 17 18 19]
#      [20 21 22 23]]]

c = np.arange(72).reshape(3, 2, 4, 3) # Matrice 4D 3x2x4x3
print(c)
#    [[[[ 0  1  2]
#       [ 3  4  5]
#       [ 6  7  8]
#       [ 9 10 11]]
#    
#      [[12 13 14]
#       [15 16 17]
#       [18 19 20]
#       [21 22 23]]]
#    
#    
#     [[[24 25 26]
#       [27 28 29]
#       [30 31 32]
#       [33 34 35]]
#    
#      [[36 37 38]
#       [39 40 41]
#       [42 43 44]
#       [45 46 47]]]
#    
#    
#     [[[48 49 50]
#       [51 52 53]
#       [54 55 56]
#       [57 58 59]]
#    
#      [[60 61 62]
#       [63 64 65]
#       [66 67 68]
#       [69 70 71]]]]
```

## Opérations basiques sur les array

-  Les  opérations  arithmétiques agissent  sur  le  tableau
  élément par  élément, et créent un  nouveau tableau auquel
  sont affectés les résultats de l'opération.


```python
a = np.arange(5)
b = np.array([5, 6, 7, 8, 9])
c = a + b
print(c)
#    [ 5  7  9 11 13]

d = b ** 2
print(d)
assert id(d) != id(b) # d est un objet différent de b
#    [25 36 49 64 81]
```


- L'opérateur  `*` agit également élément  par élément. Pour
  avoir le  produit matriciel,  il faut  utilisé l'opérateur
  `@` (pour  les versions  de Python >=  3.5) ou  la méthode
  `dot` (valide pour toutes les versions de Python):


```python
A = np.array([[1, 1],
              [0, 1]])

B = np.array([[1, 0],
              [0, 1]])

A * B
#    array([[1, 0],
#           [0, 1]])

A @ B
#    array([[1, 1],
#           [0, 1]])

A.dot(B)
#    array([[1, 1],
#           [0, 1]])
```


-  Les opérateurs  tels que  `+=` et  consorts modifient  le
  tableau correspondant, sans créer de nouveau tableau:


```python
a = np.ones((2, 3), dtype=int)
b = np.random.random((2, 3))
a *= 3
a
#    array([[3, 3, 3],
#           [3, 3, 3]])

b += 3
b
#    array([[3.31138499, 3.94754759, 3.93125152],
#           [3.97691206, 3.74311961, 3.26751699]])

# L'opérateur ne convertit pas automatiquement l'opérande
a += b
#    ---------------------------------------------------------------------------
#
#    UFuncTypeError                            Traceback (most recent call last)
#
#    <ipython-input-27-3833203f37e2> in <module>
#          1 # L'opérateur ne convertit pas automatiquement l'opérande
#    ----> 2 a += b
#    
#
#    UFuncTypeError: Cannot cast ufunc 'add' output from dtype('float64') to dtype('int64') with casting rule 'same_kind'
```

-  Dans une  opération  impliquant 2  tableaux,  le type  du
  tableau résultant correspond au type le plus général des 2
  entrées (upcasting)


```python
# La conversion est faite ici car un nouveau tableau est créé
e = a + b
e
#    array([[6.31138499, 6.94754759, 6.93125152],
#           [6.97691206, 6.74311961, 6.26751699]])

e.dtype
#    dtype('float64')

f = np.exp(e * 1j)
f
#    array([[0.99960242+0.02819595j, 0.78731013+0.61655718j,
#            0.79725261+0.60364582j],
#           [0.76886845+0.639407j  , 0.89608166+0.44388924j,
#            0.99987725-0.01566767j]])

f.dtype
#    dtype('complex128')
```


- Plusieurs  opérations unaires sont implémentées  comme des
  méthodes de la  classe `ndarray` et agissent  sur tous les
  éléments  scalaires  du  tableau. Il  faut  préciser  dans
  quelle dimension  l'effectuer si on ne  veut en considérer
  qu'une avec le paramètre `axis` de l'opération


```python
a = np.random.random((2, 3))
a
#    array([[0.59337358, 0.29323615, 0.68107569],
#           [0.11571329, 0.77500957, 0.28323479]])

a.sum()
#    2.7416430676478827

a.min()
#    0.11571329244066308

a.max()
#    0.7750095662572198

b = np.arange(12).reshape((3, 4))
b
#    array([[ 0,  1,  2,  3],
#           [ 4,  5,  6,  7],
#           [ 8,  9, 10, 11]])

b.sum(axis=1) # Somme des éléments de chaque ligne
#    array([ 6, 22, 38])

b.sum(axis=0) # Somme des éléments de chaque colonne (PS: les colonnes sont toujours sur axis=0)
#    array([12, 15, 18, 21])

b.cumsum(axis=1) # Somme cumulative sur chaque ligne
#    array([[ 0,  1,  3,  6],
#           [ 4,  9, 15, 22],
#           [ 8, 17, 27, 38]])
```


## Fonctions universelles

Numpy fournit des  fonctions mathématiques familières telles
que `sin`, `cos`, `exp`. Ces fonctions sont appelées `ufunc`
(*universal functions*)  et agissent  sur chaque  élément du
tableau, produisant un tableau en sortie:


```python
a = np.arange(5)
a
#    array([0, 1, 2, 3, 4])

np.exp(a)
#    array([ 1.        ,  2.71828183,  7.3890561 , 20.08553692, 54.59815003])

np.sqrt(a)
#    array([0.        , 1.        , 1.41421356, 1.73205081, 2.        ])

b = np.array([-1, -3, -5.6, 7, 0])
b
#    array([-1. , -3. , -5.6,  7. ,  0. ])

np.add(a, b)
#    array([-1. , -2. , -3.6, 10. ,  4. ])
```


## Indexation

-  Les tableaux  Numpy 1D  peuvent être  indexés, itérés  et
  "slicés" comme des listes


```python
a = np.arange(10) ** 3
a
#    array([  0,   1,   8,  27,  64, 125, 216, 343, 512, 729])

a[2]
#    8

a[2:5]
#    array([ 8, 27, 64])

a[:6:2] == a[0:6:2]
#    array([ True,  True,  True])

a[:6:2] = -1    # Du 1er au 6ème élément, changer chaque 2ème élément à -1
a
#    array([ -1,   1,  -1,  27,  -1, 125, 216, 343, 512, 729])

# Inversion d'un array
a[::-1]
#    array([729, 512, 343, 216, 125,  -1,  27,  -1,   1,  -1])

for i in a:
    print(i ** (1/3))
#    nan
#    1.0
#    nan
#    3.0
#    nan
#    4.999999999999999
#    5.999999999999999
#    6.999999999999999
#    7.999999999999999
#    8.999999999999998
#
#
#    /Users/morningdew/.virtualenvs/monrdv/lib/python3.7/site-packages/ipykernel_launcher.py:2: RuntimeWarning: invalid value encountered in power
```      


- Les  Tableaux multidimensionnels  peuvent avoir  un indice
  par "direction"  (ou dimension),  spécifiés sous  forme de
  tuples


```python
b = np.fromfunction(lambda x,y: 10 * x + y, (5, 4), dtype=int)
b
#    array([[ 0,  1,  2,  3],
#           [10, 11, 12, 13],
#           [20, 21, 22, 23],
#           [30, 31, 32, 33],
#           [40, 41, 42, 43]])
```

Je vais m'arreter la pour  ce billet. Cette librairie permet
de  faire beaucoup  de choses  interrestantes, mais  il faut
dire  qu'elle  reste  plutot  bas  niveau.   Il  existe  des
librairies  qui sont  construites  au-dessus  de numpy  pour
fournir  une  interface  plus  intuitive  selon  le  domaine
d'application.

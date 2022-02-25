# Rapport TME 5

### Étudiants :
- ### Etienne PENAULT
- ### Luka LAVAL
- ### Ruizheng XU

-----

## ETUDE
### Objectif de l’expérience
Dans cette expérience, on s’intéresse au traitement pré-attentif de la **courbure** (concave/convexe), la **taille** (petit/gros) et leurs combinaisons (**taille** + **courbure**).

### Question de recherche / Hypothèses
On se demande quel est le rôle de ces deux variables et de leurs combinaisons lors d'un traitement pré-attentif sur des cercles.
Nous partons de l'hypothèse selon laquelle la difficulté va croitre linéairement avec le nombre d'entités. De plus nous pensons qu'il sera plus facile de traiter des entités selon la variable de la **taille** puis selon la **courbure** et enfin la combinaison des deux sera vraisemblablement le plus difficile pour les participants.

![](https://codimd.s3.shivering-isles.com/demo/uploads/4dc90b3ff2d712976a85fc572.png)

### Participants
L'expérience est réalisée sur 3 participants agés entre 21 et 23 ans de profil sociaux culturels similaires en master d'informatique. 

### Appareil
Le participant réalise le test sur son ordinateur (écran + clavier + souris). Nous n'avons pas d'influence sur son environnement lors du test. Un logiciel a été développé pour l'expérience. Il fait appel à la vision du participant pour reconnaitre des formes et des nuances de gris mais aussi son touché (clavier + souris) pour la validation et la selection.

### Plan expérimental
Chaque participant est associé à un identifiant unique auquel est associé une batterie de 37 exerices. Les exerices sont distribués par blocs dont l'ordre diffère selon l'identifiant. Le participant doit finir tous les exercices pour que les informations soient prises en compte. Un participant ne peut participer qu'une fois à l'expérience. Chaque exercice commence quand le participant le décide, il peut donc attendre le temps qu'il veut entre chacun des exercices. Il y a trois familles d'exerices qui se basent respectivement sur : la **taille** uniquement, la **courbure** uniquement, la **taille** et la **courbure** de cercles disposés de manière ordonée (comme une matrice carré). Enfin dans une même famille d'exerice, le nombre d'entités affichées à l'écran diffère parmis 16, 25 et 36 cercles.

### Tâche et stimulus
Un exercice affiche des cercles (de tailles et/ou courbures différentes) de manière ordonnée. Le participant doit repérer l'intru parmis ces cercles. Une fois l'intru repéré, il appuie sur la touche **espace**, les cercles disparaissent, il doit ensuite utiliser la **souris** pour sélectionner la zone du cercle en question. La notion d'intru se base sur l'unicité du cercle parmis ceux affichés. Il n'y a qu'un seul intru par exercice. Le participant a terminé l'expérience uniquement une fois tous les exerices terminés.

### Design
L'expérimentation se base sur un design within groups. Chaque participant se voit associé des exercices par blocs dont l'ordre diffère selon l'identifiant. On défini un bloc par un ensemble d'exerices similaires dépendant de la même variable ou des mêmes variables et d'un même nombre de cercles. Un bloc ne revient jamais deux fois pour un même participant. Les seules répétitions aux niveau types d'exercices (variable et nombre d'entités) se font dans un même bloc.

### Mesures
Dans cette expérience, nous mesurons le temps que met un participant à trouver l'intru (c'est-à-dire le temps entre le début de l'exercice et le moment où il appuie sur la touche **espace**). De plus nous gardons une trace de l'identifiant du cercle sélectionné et du cercle intru pour savoir si il a effectivement trouvé l'intru de l'exercice. Ceci permet de ne prendre en compte que les temps pour lesquels le participant à réussi à sélectionner le bon cercle.

## RESULTATS

Dans la partie d'analyse des résultats, nous avons tracé des courbes en regroupant les temps en fonction de la taille de la matrice (le nombre de cercles correspond au nombre **taille*taille**) et de la courbure des cercles.

Figure 1             |  Figure 2
:-------------------------:|:-------------------------:
![](https://codimd.s3.shivering-isles.com/demo/uploads/ef9a60607f07fe6906cb44a40.png) | ![](https://codimd.s3.shivering-isles.com/demo/uploads/ef9a60607f07fe6906cb44a41.png)

Dans ces deux premières figures, nous pouvons observer l'évolution et la répartion des temps (en secondes) passés pour un test en fonction de la taille de la matrice et de la condition du test (courbure). 
Nous remarquons que pour les tests sur 16 et 25 cercles, la différence est légère. Tandis que sur une grille de 36 cercles (6x6), l'utilisateur peut avoir du mal à trouver l'intru, car on a des points de données avec un temps assez grand.

Par contre, sur la figure 1, on voit directement que les différentes instances de la *condition* joue un rôle beaucoup plus important que la variable *size*. En effet, nous observons un effet d'échelle sur nos trois courbes, et que le fait de modifier la courbure et la taille du cercle en même temps augmente considérablement la difficulté.

Figure 3             |  Figure 4
:-------------------------:|:-------------------------:
![](https://codimd.s3.shivering-isles.com/demo/uploads/ef9a60607f07fe6906cb44a3f.png) | ![](https://codimd.s3.shivering-isles.com/demo/uploads/ef9a60607f07fe6906cb44a3e.png)

Et l'impact de la variable *condition* est encore plus visible sur la figure 4. Cette figure représente le temps utilisé pour trouver l'intrus sur les matrices de tailles différentes, sous les différentes types de cercles. On remarque que peu importe la taille de la matrice, lorsqu'on ne modifie **que la taille ou la courbure** du cercle, le résultat reste quasi-constant et rapide (< 2s).
Alors que pour les cercles avec modification sur **la taille et la courbure**, le temps est supérieur à 4 secondes sur une matrice de plus petite taille, et ce dernier augmente encore avec la taille de grille (proche de 6 secondes sur une matrice de taille 6x6).

Figure 5             |  Figure 6
:-------------------------:|:-------------------------:
![](https://codimd.s3.shivering-isles.com/demo/uploads/ef9a60607f07fe6906cb44a3c.png) | ![](https://codimd.s3.shivering-isles.com/demo/uploads/ef9a60607f07fe6906cb44a3d.png)

À travers ces deux dernières figures, on apprend que l'impact de la variable *size* ne s'exprime que sur les cercles avec des modifications sur la taille et la courbure, le temps augmente en échelle lorsque *condition* est instanciée avec "CourbureTaille" sur la figure 5, alors que pour les deux autres instances de *condition*, le temps reste constant.
Et on remarque aussi que la variance de l'instance "CourbureTaille" est beaucoup plus grand que les deux autres instances.

---

Ci-dessous, les moyennes de temps en fonction de la condition et de la taille de grille :

| condition      |mean (s) | std  (s)|
|:---------------|--------:|---------:|
| Taille         | 1.13683 | 0.144202 |
| Courbure       | 1.58356 | 0.609111 |
| CourbureTaille | 4.83127 | 1.79937  |

|   size |    mean (s) |   std (s) |
|-------:|--------:|--------:|
|     16 | 2.43558 | 1.61962 |
|     25 | 2.35519 | 1.69051 |
|     36 | 2.76088 | 2.52408 |

La moyenne de l'instance CourbureTaille de la variables *condition*  est presque égale à 5, et sa variance est aussi très grande par rapport aux autres instances.
Pour la variable *size*, les moyennes restent proches, mais on remarque que la variance de l'instance 36 est relativement grand face aux autres. Donc la variable impact pas beaucoup sur le temps, mais plus sur la variance. Nous pensons que ceci est dû à la taille de grille qui agrandi, donc l'utilisateur met plus de temps à parcourir l'écran malgré qu'il trouve rapidement l'intru.

Donc, l'impact de la condition est beaucoup plus important que la taille de grille, et la taille de grille n'aura un impact remarquable que si son instance devient très grand.

Pour finir l'analyse des données, nous avons effectué un test ANOVA grâce à la librairie *pingouin*.
Cette ligne de code `pg.rm_anova(data=df, dv="time", within=["size", "condition"], subject="participant_id")` nous renvoie le tableau ci-dessous:

|    | Source           |        SS |   ddof1 |   ddof2 |        MS |         F |       p-unc |   p-GG-corr |      np2 |      eps |
|---:|:-----------------|----------:|--------:|--------:|----------:|----------:|------------:|------------:|---------:|---------:|
|  0 | size             |  0.528283 |       2 |       6 |  0.264142 |  0.788758 | 0.496447    |  0.451722   | 0.208184 | 0.578272 |
|  1 | condition        | 98.0873   |       2 |       6 | 49.0437   | 67.4663   | 7.71649e-05 |  0.00221352 | 0.957426 | 0.567541 |
|  2 | size * condition |  3.55477  |       4 |      12 |  0.888692 |  2.61971  | 0.087879    |  0.226921   | 0.466164 | 0.198313 |

Depuis ce tableau, on peut observer que la valeur **SS** (Sum of Squares) est très bas pour *size* et très haute pour *condition*. Donc on en déduit que les temps obtenus par rapport à la variable *size* sont très proches de la moyenne de temps de cette variable, et c'est le contraire pour la variable *condition* avec une **SS** proche de 98 (cette différence est attendu avec la variance que nous avons analysé au-dessus).

Ensuite, concentrons sur la valeur **F**. Cette valeur est aussi très grande chez la variable *condition*, cela a la même signification que les valeurs **SS** et **MS** (Mean Squares), car ces trois valeurs sont fortements liées (**MS** calculée à partir de **SS** et **F** à partir de **MS**).
Ainsi, de là on peut conclure qu'avec la variable *condition*, on a une différence de performance plus significative entre les sujets, c'est-à-dire les participant. Bien que les performances ne changent pas énormément en fonction de la variable *size*.

## DISCUSSION

Pour compléter notre analyse, à la fin de cette expérience nous avons appris que la principale difficulté pour les participants provient surtout pas le nombre de variables indépendantes que l'on instancie.

En effet le nombre de cercles uniques différents augmente exponentiellement avec le nombre de variables indépendantes instanciées ==> nombre de combinaison possibles avec les différentes instnaces (dans notre cas 2*2 = 4 cercles uniques différents). 
Donc plus on instancie de variables indépendantes pour nos cercles, plus la complexité augmente.

De plus, l'impact de nombre de cercles est aussi très lié au nombre de variables indépendantes instanciées. Car avec une seule variable instanciée, on aura que 2 types de cercles différents, donc il est très facile d'obtenir un bon temps.
Ainsi, notre hypothèse de début est à moitié vérifiée. Nous avions eu raison de penser que l'instance "CourbureTaille" de la variable *condition* aura le plus gros impact, mais nous avions pas prévu que les deux autres instances ("taille" du cercle seulement et "condition" du cercle seulement) ont une influence quasiment nulle sur le temps des participants.

---

Le nombre réduit de participants pour cette expérience a un impact négatif évident sur la représentativité et la qualité des résultats. Tout comme leurs origines sociaux culturelles similaires. Le déploiement de ce test à large échelle est relativement facile grâce au logiciel développé.

---

Pour affiner les résultats, il peut être intéressant de prendre en compte l'ordre des exerices lors de l'étude statistique ainsi que l'âge des participants et leur acquité visuelle (lunettes...). De plus nous pourrions étaler l'expérimentation à plusieurs examens par participants à des intervalles de temps différents. Enfin favoriser un environnement calme et neutre autour du participant lors de l'expérience (par exemple dans une salle de laboratoire) peut être bénéfique pour l'expérimentation.
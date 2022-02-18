# TP Qt 2

Implémentation d'un outil de Dessin en Qt.

Pour lancer le programme :
```
python MainWindow.py
```

Les fonctionnalités implémentées :
- Dessiner avec différentes formes:
  - Libre, ligne, rectangle, cercle, ellipse
- Changer la largeur du crayon
- Changer la couleur des éléments dessinés
- Remplir l'intérieur des figures avec de différentes couleurs
- Effacer la dernière figure, ou tout effacer
- Sélectionner un ou plusieurs formes géométriques, et changer leurs attributs
- Messages de log pour ouvrir un fichir et sauvegarder un fichiers, les erreurs de fichiers, etc...
- Sauvegarder, ouvrir un desssin

Les fonctionnalités implémentées mais ne fonctionnent pas de façon optimisées:
- Déplacer les figures (déplacement trop rapide et non linéaire)

Les fonctionnalités en cours d'implémentation :
- Zommer et dé-zoomer

Fonctionnalités non implémentées :
- Scriboli

-------

Pour re-compiler le fichier resources.qrc en resources.py :
```
pyrcc5 -o resources.py resources.qrc
```

Auteur : XU Ruizheng (21111473)
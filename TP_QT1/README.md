# TP Qt 1

Implémentation d'un éditeur de texte avec PyQT5.

Pour re-compiler le fichier resources.qrc en resources.py :
```
pyrcc5 -o resources.py resources.qrc
```

Les fonctionnalités implémentées :
- Ouvrir un fichier .txt ou .html
- Sauvegarder le contenu de l'éditeur dans un fichier .txt ou .html
- Couper, copier, coller à travers des icons dans la barre d'outil
- Changer la taille, la famille, la couleur du texte
- Gras, italique, souligné, surligner les textes

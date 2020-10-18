# Magic Maze

## Exécuter le programme

Clonez ce dépôt, puis ouvrez un terminal dans le dossier contenant le code source, et faites la commande appropriée pour exécuter le programme :

- Linux :
```bash
python3 main.py
```

- Windows :
```batch
python main.py
```

Vous devez bien entendu avoir [Python](https://www.python.org/downloads/) d'installé pour pouvoir exécuter le programme.

## Phase 1

### Implémentations

Ont été implémentés :
- une fonction gérant l'affichage à partir de l'état de la partie (sortie activée, temps écoulé depuis le début), du plateau de jeu et des coordonnées des joueurs.
- 4 fonctions gérant le déplacement dans une direction (haut, bas, gauche, droite), gérant également les collisions entre les différents pions ainsi qu'entre ceux ci et les bords du plateau
- un timer de 3 minutes arrêtant la partie s'il arrive à 0
- un mode debug bougeant automatiquement un pion aléatoirement choisi dans une direction aléatoire

### Choix techniques

- Pour représenter le plateau de jeu, une matrice a été choisie. Elle permet de représenter de façon intuitive et claire le plateau.
- Pour représenter les pions, nous avons choisi des listes de deux éléments représentant leurs coordonnées sur le plateau. Nous avions dans un premier temps voulu utiliser des tuples pour représenter les coordonnées des pions, mais nous avons finalement changé d'avis et choisit d'utiliser des listes pour pouvoir modifier un des deux champs des coordonnées du pion en place au moment de le déplacer sur le plateau. 
- Nous avons choisi, pour regrouper les pions, d'utiliser un dictionnaire dont les clés sont les couleurs des pions et les valeurs leurs coordonnées. Cela permet, en stockant la couleur du pion actuellement sélectionné dans une variable, d'effectuer des actions sur n'importe quel pion de la même façon. Si nous avions utilisé des listes à la place, nous aurions du choisir de représenter chacun des pions de couleur par un des indices de 0 à 3. Cela aurait été beaucoup moins clair et potentiellement source de confusions.

## Crédits
Cyprien Molinet et Baptiste Mlynarz
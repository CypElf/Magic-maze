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

Fonctionnalités implémentées :
- un module display s'occupant de passer de la partie logique à l'affichage à l'écran de l'utilisateur : affichage de splash screen, du jeu en lui même, des messages de victoire ou de défaite, etc.
- un module move s'occupant de la partie logique du déplacement des pions et de son impact sur l'état du jeu : déplacement d'un pion dans le plateau de jeu, prise en compte des collisions, gestion de l'activation de la sortie, etc.
- un système de timer de 3 minutes qui, s'il arrive à 0, indique que la partie est perdue.
- un mode debug bougeant automatiquement un pion aléatoirement choisi dans une direction aléatoire.

### Organisation du programme

Un splash screen est affiché au démarrage, affichant les commandes du jeu. Puis, après un clic de l'utilisateur, le jeu démarre. Il enregistre le temps actuel et lance ainsi le compte à rebours de 3 minutes. Ensuite, il rentre dans une boucle infinie, dans laquelle il attend que le joueur appuie sur une des touches utilisables pour se déplacer, changer de pion, entrer en mode debug ou encore arrêter le programme. Lorsque le joueur a gagné ou que le temps est écoulé, le programme s'arrête en affichant un message approprié selon la cause de sa fin.

### Choix techniques

- Pour représenter le plateau de jeu, une matrice a été choisie. Elle permet de représenter de façon intuitive et claire le plateau. Pour représenter les éléments de ce plateau, nous avons choisi certaines valeurs à placer comme éléments dans la matrice représentant le plateau de jeu.
- Pour représenter un pion, nous avons choisi d'utiliser une liste de deux éléments représentant ses coordonnées sur le plateau. Nous avions dans un premier temps, intuitivement, voulu utiliser des tuples pour représenter les coordonnées des pions, mais nous avons finalement changé d'avis et choisi d'utiliser des listes pour pouvoir modifier un des deux champs des coordonnées du pion en place au moment de le déplacer sur le plateau (les tuples sont iummutables et auraient donc rendu la modification d'un de ses deux éléments plus lourde à écrire). 
- Nous avons choisi, pour regrouper les pions, d'utiliser un dictionnaire dont les clés sont les couleurs des pions et les valeurs la liste de leurs coordonnées. Cela permet, en stockant la couleur du pion actuellement sélectionné dans une variable, d'effectuer des actions sur n'importe quel pion de la même faç, en utilisant la couleur du pion actuellement sélectionné comme clé du dictionnaire des pions. Pour comparer, si nous avions utilisé des listes à la place, nous aurions du choisir un ordre par convention pour représenter chacun des pions de couleur, par des indices de 0 à 3. Cela aurait été beaucoup moins clair au moment d'accéder à un élément et aurait rendu les choses plus compliquées et bien moins claires au moment de les manipuler.
- De manière plus générale, pour structurer le programme, vous avons suivi la démarche suivante : chaque partie du programme est séparée des autres et fonctionne indépendamment. Chaque partie demande certaines données dont elle ne se préoccupe pas de l'origine, et effectue son travail dessus sans se soucier de quoi que ce soir d'autre. C'est enfin en combinant toutes ces fonctionnalités (affichage, déplacement...) dans le coeur du programme que le programme se déroule.

### Problèmes rencontrés

Un problème qui a été assez problématique est que le jeu ralentissait avec le temps, c'est à dire que déplacer les pions avait une latence de plus en plus élevée. Finalement, cela s'est révélé être du à l'oubli d'appeler la fonction `efface_tout()` de upemtk pour effacer le contenu de la fenêtre avant de ré afficher le plateau de jeu. A cause de cet oubli, chaque affichage était "superposé" aux anciens et c'est ce qui causait ce ralentissement, augmentant avec le temps, un peu plus à chaque affichage supplémentaire effectué par dessus les anciens. Il s'agit d'un problème finalement simple à fixer, mais qui a été très compliqué à identifier et donc source de beaucoup de recherches sur son origine. A part ça, nous n'avons pas rencontré de problème en particulier.

## Crédits
Cyprien Molinet et Baptiste Mlynarz.
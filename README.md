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

## Phase 2

### Implémentations

Fonctionnalités implémentées :
- des murs entre certaines cases
- un système d'escalators
- un système de vortex
- un système de renversement de sablier
- un menu de sélection du nombre de joueurs et une distribution aléatoire des actions possibles aux touches des joueurs
- un menu de pause par lequel le jeu peut être sauvegardé pour être plus tard relancé dans le même état

### Choix techniques

- Pour sauvegarder l'état du jeu, il nous fallait pouvoir sauvegarder des types de données complexes tels que des listes ou des dictionnaires. Nous avons par conséquent choisi de sauvegarder l'état du jeu en JSON (JavaScript Object Notation), qui répond bien à ce critère. Grâce au module standard json de Python, il a été très facile de mettre en place les sauvegardes et restaurations du jeu.
- L'organisation du code a bien évolué. Le module move a été renommé de façon plus large en `logic` et contient toutes les fonctions s'occupant de la partie logique du jeu. Le module `menu` contient des fonctions qui s'occupent de gérer l'appui sur certaines zones d'un menu donné. Un module `timer` contient tout ce qui est lié à la gestion du timer du jeu. Et enfin, tout ce qui est lié aux touches et leur appui est géré par le module `keys`.
- Ces modules ont été placés dans un sous dossier `src` pour rendre l'arborescence du projet plus claire.
- Dans les tuiles qui devront être implémentées pour la phase 3, on peut constater qu'il n'y a que 3 cas types d'escalators : un allant à 1 case en haut et 1 à droite, une allant de 2 en haut et 1 à droite, et enfin une allant de 2 à droite et 1 en haut. Par conséquent, comme faire une image d'escalator qui s'adapterait aux cases entre lesquelles elle serait aurait été très compliqué à réaliser et qu'il n'y aura que 3 cas possibles, nous avons choisi de faire 3 images différentes pour chacun de ces cas, choisies automatiquement lors de l'affichage d'un escalator en fonction du cas.

### Problèmes rencontrés

- La sélection du vortex a été plutôt embêtante. En effet, lorsque le programme arrivait à la partie de sélection du vortex, l'affichage de la partie n'était logiquement plus effectué et le timer se retrouvait donc figé dans l'affichage (mais continuait de tourner en fond quand même, bien sur). De plus, le cercle noir de sélection de vortex ne pouvait pas être effacé tout seul pour en afficher un autre sur un autre vortex lorsque le joueur veut en sélectionner un autre. Il était nécessaire d'effacer la fenêtre. Par conséquent, un affichage de la fenêtre similaire à celui de la boucle principale du programme a du être mis en place pendant la sélection du vortex.
- Un autre problème souvent rencontré est que les fonctions ont souvent besoin de bien trop d'arguments. Cela devient rapidement compliqué de s'y retrouver. En effet, les fonctions peuvent être classées en 2 rangs : les fonctions plus globales, effectuant une tâche large (par exemple, `display_game()` qui affiche le plateau de jeu) et les fonctions plus spécialisées, appelées par les fonctions plus globales, pour faire certaines tâches précises (par exemple, `display_cell()` ou encore `display_players()`, qui affichent respectivement une cellule donnée et les pions, sont appelées par `display_game()`). Cependant, souvent, il y a de nombreuses sous fonctions demandant de nombreux arguments différents, et les fonctions globales ont donc besoin de ces arguments également afin de pouvoir les transmettre. Le résultat est que les fonctions les plus globales comme `display_game()` ou `key_triggered()` prennent de très nombreux arguments et cela n'est pas forcément idéal. Nous n'avons pas trouvé de solution à ce problème.

## Phase 3

### Choix techniques

Un problème rencontré à la phase 2 (celui des fonctions avec beaucoup trop de paramètres) a été résolu. Une première solution à laquelle nous avons pensé aurait été de faire du jeu un objet et de lui définir comme attributs les différentes variables correspondant à son état, permettant ainsi d'y accéder depuis les différentes fonctions qui seraient alors pour certaines devenues des méthodes.
La programmation orienté objet n'étant pas autorisée pour ce projet, et les variables globales n'existant pas en Python, il fallait donc trouver une autre solution.
Après quelques recherches sur internet, nous sommes tombés sur une [FAQ de Python](https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules), où ils expliquent qu'on peut partager une information à travers plusieurs modules en en faisant un module séparé qu'on importe dans ces différents modules. Cela a demandé de grosses modifications partout dans le code, mais grâce à cela, la quantité de paramètres passés aux fonctions a été considérablement réduite, les variables de l'état du jeu étant devenues accessibles partout grâce à leur import.

## Crédits
Cyprien Molinet et Baptiste Mlynarz.
# Projet IA de jeux — Othello & Morpion

Projet **Data Science et Intelligence Artificielle** — ESILV.

Ce dépôt regroupe deux jeux dotés d'une intelligence artificielle fondée sur
l'algorithme **MinMax avec élagage Alpha-Bêta** :

- le **Morpion** (Tic-Tac-Toe), réalisé comme exercice d'entraînement pour mettre en
  place l'algorithme sur un jeu simple ;
- l'**Othello**, le projet principal, qui applique la même approche à un jeu plus riche
  (plateau 8×8, règles de capture, heuristique multi-critères).

Ce document sert à la fois de mode d'emploi et de compte-rendu : il présente les deux
jeux, leur architecture, le fonctionnement de leurs IA et les choix de conception.

---

## Organisation du dépôt

Le Morpion a servi de terrain d'essai : y implémenter MinMax + Alpha-Bêta a permis de
valider l'approche avant de la transposer, en plus ambitieux, à Othello. Les deux jeux
partagent donc la même logique d'IA, adaptée à chaque plateau.

Un menu principal permet de choisir le jeu à lancer.

---

# Morpion (Tic-Tac-Toe) — exercice d'entraînement

## Présentation

Le morpion se joue sur une grille 3×3 : chaque joueur pose à tour de rôle son symbole
(`X` ou `O`), le but étant d'aligner trois symboles identiques (ligne, colonne ou
diagonale). Sa petite taille en fait un cas idéal pour mettre au point l'algorithme
MinMax.

## Fichiers

| Fichier | Rôle |
|---------|------|
| `iaMorpion.py` | La classe `Noeud_Morpion` : un état de la partie (grille + joueur), génération des coups possibles, évaluation. |
| `JeuMorpion.py` | L'algorithme `minimax` (avec élagage alpha-bêta), le choix du coup de l'IA, la saisie et la boucle de jeu. |

## Lancement et déroulement

Le joueur humain joue les `X`, l'IA les `O`. Au lancement, le jeu demande **qui commence**.
Le coup se saisit en une fois, au format lettre + chiffre (par exemple `B2`), la saisie
tolérant minuscules et espaces.

## L'intelligence artificielle

L'IA explore l'arbre des coups avec **MinMax et élagage Alpha-Bêta**. Elle alterne entre
nœuds Max (le joueur qui maximise) et nœuds Min (celui qui minimise), et évalue chaque
position avec une heuristique : victoire ou défaite valent le score extrême, et chaque
alignement de deux symboles identiques complété par une case vide (une menace) est
récompensé ou pénalisé. Grâce à cette recherche, l'IA du morpion joue de façon optimale :
elle ne perd jamais et sanctionne la moindre erreur de l'adversaire.

---

# Othello — projet principal

## Présentation

Othello se joue sur un plateau 8×8. Chaque joueur pose à tour de rôle un pion de sa
couleur (Noir ou Blanc) sur une case vide, de façon à encadrer un ou plusieurs pions
adverses entre le pion posé et un pion de sa couleur déjà présent ; les pions encadrés
sont alors retournés. Le but est d'avoir le plus de pions de sa couleur à la fin de la
partie. C'est un jeu de stratégie combinatoire à information parfaite (sans hasard),
idéal pour un algorithme de type MinMax.

## Architecture

Le code est découpé en **6 modules**, chacun ayant une seule responsabilité. C'est un
choix de conception central : plutôt qu'un gros fichier mélangeant tout, chaque
préoccupation (données, règles, joueurs, orchestration) vit à un seul endroit, ce qui
rend le code lisible et testable morceau par morceau.

Les dépendances entre modules vont toujours dans le même sens (des couches hautes vers
les couches basses), sans jamais remonter :

```
jeuOthello  →  { joueur, ia }  →  regles  →  plateau
   │                              │
   └──────────   constantes   ────┘     (socle, importé par tous)
```

| Fichier | Responsabilité |
|---------|----------------|
| `constantes.py` | Valeurs partagées : `VIDE`/`NOIR`/`BLANC`, les 8 `DIRECTIONS`, `couleur_nom()`. |
| `plateau.py` | Affichage texte du plateau, comptage des pions, annonce du vainqueur. |
| `regles.py` | Cœur des règles : `coups_valides()`, `peut_jouer()`, `jouer()` (pose + retournement). |
| `joueur.py` | Joueur humain : saisie d'un coup (format `A1`) et validation via les règles. |
| `ia.py` | Joueur IA : la classe `Noeud` (arbre de recherche), l'algorithme `minmax`, la façade `JoueurIA`. |
| `jeuOthello.py` | Orchestration : boucle de jeu, alternance, passage de tour, fin de partie, point d'entrée `lancer_othello()`. |

Un principe fort a guidé ce découpage : **une seule source de vérité pour les règles.**
Toute la logique « ce coup est-il légal et quels pions retourne-t-il ? » est concentrée
dans `regles.py`. Le joueur humain comme l'IA s'appuient dessus, au lieu de recoder
chacun sa propre vérification.

## Convention de coordonnées

Une convention unique est utilisée dans tout le code : le plateau est
`tab[ligne][colonne]`, avec des indices de 0 à 7, et les cases valent `0` (vide),
`1` (Noir) ou `2` (Blanc). La traduction vers la notation lisible `A1` (la lettre A–H
désigne la colonne, le chiffre 1–8 la ligne) n'intervient qu'à l'affichage et à la
saisie. Fixer cette convention dès le départ évite toute ambiguïté entre lignes et
colonnes à travers les modules.

## Règles implémentées

Les Noirs commencent toujours. À son tour, un joueur pose un pion sur une case vide qui
encadre au moins un pion adverse, dans au moins une des huit directions ; les pions
encadrés sont retournés. Si un joueur n'a aucun coup légal, il **passe** son tour. La
partie se termine lorsque **aucun** des deux joueurs ne peut jouer ; le gagnant est celui
qui possède le plus de pions.

## Lancement et déroulement d'une partie

Prérequis : **Python 3** et **NumPy** (`pip install numpy`).

Depuis le menu principal, choisir Othello ; ou directement :

```python
from jeuOthello import lancer_othello
lancer_othello()
```

Au lancement, le jeu demande **qui commence** (le joueur ou l'IA prend les Noirs, donc
joue en premier) puis la **profondeur** d'exploration de l'IA (2 à 4 : plus la profondeur
est élevée, plus l'IA joue fort mais lentement). Le joueur humain saisit son coup au
format lettre + chiffre (par exemple `D3`), et les coups possibles sont affichés à chaque
tour pour le guider.

## L'intelligence artificielle

### MinMax avec élagage Alpha-Bêta

L'IA explore l'arbre des coups possibles jusqu'à une profondeur fixée. Chaque nœud
représente un état du plateau ; ses enfants sont les états atteignables par un coup légal
(avec le joueur adverse au trait). L'algorithme alterne entre nœuds **Max** (au tour du
Noir, qui maximise l'évaluation) et nœuds **Min** (au tour du Blanc, qui la minimise).
Les feuilles de l'exploration — fin de partie ou profondeur maximale atteinte — sont
évaluées par la fonction heuristique.

L'**élagage Alpha-Bêta** accélère la recherche en maintenant deux bornes, `alpha` (le
meilleur score garanti au joueur Max) et `beta` (celui garanti au joueur Min). Dès qu'une
branche ne peut plus influencer la décision finale, elle est abandonnée sans être
explorée. Le coup obtenu est identique à celui d'un MinMax complet, mais en visitant
beaucoup moins de nœuds — essentiel puisque le temps de décision est un critère du projet.

### La fonction d'évaluation

L'heuristique évalue une position du point de vue du Noir (une valeur positive est
favorable au Noir) en combinant deux critères :

- la **force des positions**, via une table de poids : les coins valent très cher car ils
  sont imprenables, tandis que les cases qui les jouxtent sont pénalisées car elles
  offrent souvent le coin à l'adversaire ;
- la **mobilité**, la différence entre le nombre de coups possibles des deux joueurs :
  conserver un maximum d'options tout en réduisant celles de l'adversaire est un avantage
  reconnu à Othello.

### L'interface uniforme des joueurs

Choix de conception important : le joueur humain (`Joueur`) et le joueur IA (`JoueurIA`)
exposent **la même méthode** `choisir_coup(regles)`. La boucle de jeu traite donc les deux
de façon identique, sans jamais distinguer un humain d'une IA. Cela permet aussi, sans
aucune modification, de faire jouer humain contre humain, humain contre IA, ou IA contre
IA. Toute la logique de recherche (l'arbre de `Noeud` et le minmax) reste un détail
interne à `ia.py`.

---

## Synthèse des choix d'implémentation

- Une **même approche d'IA** (MinMax + Alpha-Bêta) validée sur le Morpion avant d'être
  transposée à Othello.
- Un **découpage en modules à responsabilité unique**, avec des dépendances orientées.
- Des **règles centralisées** dans un seul module, utilisées par l'humain et l'IA.
- Une **convention de coordonnées unique**, la notation lisible n'apparaissant qu'aux
  entrées/sorties.
- Une **interface commune aux joueurs**, rendant humain et IA interchangeables.
- Une **profondeur réglable**, pour gérer le compromis entre qualité de jeu et rapidité.

## Améliorations possibles (Othello)

- Ajouter le **nombre de pions** comme troisième critère d'évaluation, pondéré surtout en
  fin de partie.
- Rendre la **profondeur adaptative** : explorer plus loin quand le nombre de coups
  diminue.
- Brancher une **interface graphique** en remplacement de l'affichage console.

---

*Projet réalisé en groupe dans le cadre du cours de Data Science et Intelligence
Artificielle (ESILV).*

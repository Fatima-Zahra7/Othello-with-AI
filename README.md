# Othello — IA MinMax avec élagage Alpha-Bêta

Module Othello du projet **IA de jeux** (ESILV — Data Science et Intelligence Artificielle).

Le jeu se joue en console : un joueur humain affronte une IA (ou humain vs humain,
ou IA vs IA). L'IA repose sur l'algorithme **MinMax avec élagage Alpha-Bêta** et une
fonction d'évaluation combinant la force des positions et la mobilité.

---

## Architecture

Le code est découpé en 6 modules, chacun avec une seule responsabilité. Les
dépendances vont toujours du haut vers le bas (aucune ne remonte) :

```
partie  →  { joueur, ia }  →  regles  →  plateau
   │                            │
   └──────────  constantes  ────┘   (socle, importé par tous)
```

| Fichier | Responsabilité |
|---------|----------------|
| `constantes.py` | Valeurs partagées : `VIDE`/`NOIR`/`BLANC`, les 8 `DIRECTIONS`, `couleur_nom()`. |
| `plateau.py` | Affichage texte du plateau, comptage des pions, annonce du vainqueur. |
| `regles.py` | **Cœur des règles** : `coups_valides()`, `peut_jouer()`, `jouer()` (pose + retournement). Source de vérité unique sur ce qui est légal. |
| `joueur.py` | Joueur humain : saisie d'un coup (format `A1`) et validation via `regles`. |
| `ia.py` | Joueur IA : classe `Noeud` (arbre de recherche), `minmax` alpha-bêta, façade `JoueurIA`. |
| `partie.py` | Orchestration : boucle de jeu, alternance, passage de tour, fin de partie. |

Le point d'entrée du jeu est la fonction `lancer_othello()` dans `partie.py`,
appelée depuis le menu principal.

---

## Lancer et jouer

Prérequis : **Python 3** et **NumPy** (`pip install numpy`).

Depuis le menu principal, choisir Othello ; ou directement :

```python
from partie import lancer_othello
lancer_othello()
```

**Règles du jeu.** Les Noirs (`N`) commencent toujours. À son tour, un joueur pose
un pion sur une case vide qui encadre au moins un pion adverse entre le pion posé et
un pion de sa couleur ; les pions encadrés sont retournés. Si un joueur n'a aucun coup
légal, il passe. La partie se termine quand aucun des deux joueurs ne peut jouer ; le
gagnant est celui qui a le plus de pions.

**Saisie d'un coup.** Le joueur humain entre son coup en une fois, au format lettre +
chiffre : la **lettre** (A–H) désigne la colonne, le **chiffre** (1–8) la ligne — par
exemple `D3`. La saisie tolère les minuscules et les espaces. Les coups possibles sont
affichés à chaque tour.

---

## L'intelligence artificielle

L'IA (`ia.py`) explore l'arbre du jeu avec **MinMax + élagage Alpha-Bêta**.

- **`Noeud`** représente un état du jeu. `successeurs()` engendre un enfant par coup
  légal (en s'appuyant sur `regles`), avec le plateau résultant et l'adversaire au trait.
- **`est_feuille()`** détecte la fin de partie (aucun des deux joueurs ne peut jouer).
- **Heuristique** (du point de vue du Noir, positif = favorable au Noir) :
  - *force des positions* via une table de poids (coins = +120, cases pièges près des
    coins = négatives) ;
  - *mobilité* : différence du nombre de coups possibles entre les deux joueurs.
- **`JoueurIA`** est la façade manipulée par `partie`. Elle expose la **même interface**
  que le joueur humain (`choisir_coup(regles)` → `(lig, col, pions)`), ce qui rend les
  deux types de joueurs interchangeables dans la boucle de jeu.
- La **profondeur** d'exploration est réglable (2 à 4).

---

## Convention de coordonnées

Une seule convention dans tout le code : le plateau est `tab[ligne][colonne]`, indices
0 à 7. Les cases valent `0` (vide), `1` (Noir), `2` (Blanc). La traduction vers la
notation `A1` (colonne = lettre, ligne = chiffre) ne se fait qu'à l'affichage et à la
saisie.

---

## État d'avancement

Le moteur (plateau, règles, saisie, boucle de jeu) est complet et testé ; humain vs
humain et IA vs IA jouent des parties entières. La dernière brique en cours de
finalisation est le **`minmax` récursif avec élagage** (une version provisoire à
évaluation directe est en place le temps de valider la façade). L'**interface
graphique** (bonus) est une couche de présentation séparée, à brancher une fois le jeu
console finalisé.
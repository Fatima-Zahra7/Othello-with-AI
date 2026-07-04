# Morpion (Tic-Tac-Toe) — IA MinMax avec élagage Alpha-Bêta

Branche `morpion` du projet **Othello / IA** (ESILV — Data Science et Intelligence Artificielle).

Ce module implémente le jeu du morpion joué contre une IA. Il sert d'**exercice
d'entraînement** demandé dans le sujet : traduire le pseudo-code MinMax + Alpha-Bêta
sur un jeu simple avant de l'adapter à Othello.

---

## Contenu de la branche

| Fichier | Rôle |
|---------|------|
| `NoeudMorpion.py` | La classe `NoeudMorpion` : un état de la partie (grille 3×3 + joueur à jouer). Génère les coups possibles (`successeurs`) et évalue une position (`heuristique`). |
| `JeuMorpion.py` | La logique de jeu : algorithme `minimax` (avec élagage alpha-bêta), choix du coup de l'IA, saisie du joueur, détection de fin de partie et boucle de jeu. |
| `Menu_principale.py` | Point d'entrée. Menu de sélection du jeu (Othello / Morpion / Quitter). |

---

## Lancer le jeu

Prérequis : **Python 3** (aucune bibliothèque externe).

```bash
python Menu_principale.py
```

Puis choisir `2` pour lancer le morpion.

---

## Comment jouer

- Au lancement, le jeu demande **qui commence** : le joueur (`1`) ou l'IA (`2`).
- Le joueur **humain joue les `X`**, l'**IA joue les `O`**.
- À chaque tour, saisir son coup **en une seule fois** : une lettre pour la colonne
  (`A`, `B`, `C`) suivie d'un chiffre pour la ligne (`1`, `2`, `3`).

Exemple :

```
X coup (ex: A1) : B2
```

La saisie tolère les minuscules et les espaces (`b 2` fonctionne). Une case déjà
occupée ou un format incorrect sont rejetés et redemandés.

Grille (colonnes A–C, lignes 1–3) :

```
     A   B   C
 1 :   |   |   |
     -----------
 2 :   |   |   |
     -----------
 3 :   |   |   |
```

---

## L'intelligence artificielle

L'IA utilise l'algorithme **MinMax avec élagage Alpha-Bêta**.

- **Convention** : `X` est le joueur **Max**, `O` le joueur **Min**.
- **Profondeur d'exploration** : 6 (paramètre passé à `prochain_coup_morpion`).
- **Fonction d'évaluation** (`heuristique`) :
  - `+100` / `-100` : victoire de Max / de Min ;
  - `±10` par alignement (ligne, colonne, diagonale) contenant 2 symboles
    identiques et 1 case vide (menace).
- L'exploration s'**arrête dès qu'une victoire est détectée** (`abs(évaluation) == 100`),
  ce qui évite d'explorer des positions déjà gagnées et réduit le nombre de nœuds visités.

### Fonctions clés

- `minimax(noeud, profondeur, alpha, beta)` — évaluation récursive avec élagage.
- `prochain_coup_morpion(noeud, profondeur)` — choisit et renvoie les coordonnées du meilleur coup pour l'IA.
- `etat_partie(grille)` — renvoie le symbole gagnant, `'-'` (nul) ou `None` (partie en cours).

---

## Remarques

- L'IA en `O` joue de façon défensive/optimale : dans les cas testés elle prend les
  victoires et bloque les menaces.
- Ce module est volontairement simple. Les principes (nœuds, successeurs, minimax
  alpha-bêta, heuristique) seront **réutilisés et adaptés** pour l'IA d'Othello,
  avec un plateau 8×8 et une heuristique à plusieurs critères (nombre de pions,
  force des positions, mobilité).
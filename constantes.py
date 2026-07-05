"""Constantes partagées par tout le jeu d'Othello."""

# Contenu d'une case du plateau
VIDE = 0
NOIR = 1
BLANC = 2

# Les 8 directions autour d'une case : (delta_ligne, delta_colonne)
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]


def couleur_nom(joueur):
    """Nom lisible d'un joueur : 1 -> 'Noir', 2 -> 'Blanc'."""
    return 'Noir' if joueur == NOIR else 'Blanc'

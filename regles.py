"""
Règles du jeu d'Othello : détection des coups légaux et retournement des pions.
Convention unique : tab[ligne][colonne], vide=0, Noir=1, Blanc=2.
"""
from constantes import VIDE, DIRECTIONS


class Regles:

    def __init__(self, tab, joueur, ennemi=None):
        self.tab = tab
        self.joueur = joueur    # 1 (Noir) ou 2 (Blanc)
        self.ennemi = ennemi    # l'autre couleur

    def set_joueur(self, joueur):
        self.joueur = joueur

    def set_ennemi(self, ennemi):
        self.ennemi = ennemi

    def _pions_retournes(self, lig, col):
        """Liste des pions adverses capturés si le joueur pose en (lig, col)."""
        a_retourner = []
        for d_lig, d_col in DIRECTIONS:
            ligne_capturee = []
            l, c = lig + d_lig, col + d_col
            # On avance tant qu'on longe des pions adverses
            while 0 <= l < 8 and 0 <= c < 8 and self.tab[l][c] == self.ennemi:
                ligne_capturee.append((l, c))
                l += d_lig
                c += d_col
            # La file d'adverses doit être refermée par un pion à nous
            if ligne_capturee and 0 <= l < 8 and 0 <= c < 8 and self.tab[l][c] == self.joueur:
                a_retourner.extend(ligne_capturee)
        return a_retourner

    def coups_valides(self):
        """Dictionnaire { (lig, col) : [pions à retourner] } de tous les coups légaux."""
        coups = {}
        for lig in range(8):
            for col in range(8):
                if self.tab[lig][col] == VIDE:
                    pions = self._pions_retournes(lig, col)
                    if pions:
                        coups[(lig, col)] = pions
        return coups

    def peut_jouer(self):
        """True si le joueur courant a au moins un coup légal."""
        return len(self.coups_valides()) > 0

    def jouer(self, lig, col, pions_a_retourner):
        """Pose le pion en (lig, col) et retourne les pions capturés."""
        self.tab[lig][col] = self.joueur
        for l, c in pions_a_retourner:
            self.tab[l][c] = self.joueur

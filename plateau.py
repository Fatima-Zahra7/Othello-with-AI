"""Affichage texte du plateau d'Othello et comptage des scores."""
import numpy as np
from constantes import VIDE, NOIR, BLANC

SYMBOLES = {VIDE: '.', NOIR: 'N', BLANC: 'B'}
COLONNES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


class Plateau:

    def __init__(self, tab):
        self.tab = tab

    def compter(self):
        """Renvoie (nb_noirs, nb_blancs)."""
        noirs = int(np.count_nonzero(self.tab == NOIR))
        blancs = int(np.count_nonzero(self.tab == BLANC))
        return noirs, blancs

    def afficher(self):
        noirs, blancs = self.compter()
        print(f"   Noir (N) : {noirs}    Blanc (B) : {blancs}")
        print("     " + "  ".join(COLONNES))
        for lig in range(8):
            cases = "  ".join(SYMBOLES[int(self.tab[lig][col])] for col in range(8))
            print(f"  {lig + 1}  {cases}")
        print()

    def annoncer_vainqueur(self):
        noirs, blancs = self.compter()
        if noirs > blancs:
            print(f"Le joueur Noir a gagné : {noirs} à {blancs}")
        elif blancs > noirs:
            print(f"Le joueur Blanc a gagné : {blancs} à {noirs}")
        else:
            print(f"Match nul : {noirs} partout")

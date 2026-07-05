# -*- coding: utf-8 -*-
"""
IA d'Othello, du plus bas niveau au plus haut :
  - Noeud      : un état de l'arbre de recherche (successeurs, heuristique)
  - minmax     : l'algorithme d'exploration avec élagage alpha-bêta
  - JoueurIA   : la façade manipulée par la partie (même interface que Joueur)
"""
import numpy as np
from constantes import NOIR, BLANC, couleur_nom
from regles import Regles

# Poids positionnels : les coins valent cher, les cases qui les jouxtent sont pièges.
POIDS = [[120, -20,  20,   5,   5,  20, -20, 120],
         [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
         [ 20,  -5,  15,   3,   3,  15,  -5,  20],
         [  5,  -5,   3,   3,   3,   3,  -5,   5],
         [  5,  -5,   3,   3,   3,   3,  -5,   5],
         [ 20,  -5,  15,   3,   3,  15,  -5,  20],
         [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
         [120, -20,  20,   5,   5,  20, -20, 120]]


# ===========================================================================
# Noeud : un état du jeu dans l'arbre de recherche
# ===========================================================================
class Noeud:

    def __init__(self, tab, joueur, ennemi):
        self.tab = tab            # plateau numpy 8x8
        self.joueur = joueur      # à qui de jouer dans cet état : 1 ou 2
        self.ennemi = ennemi

    def get_joueur(self):
        return self.joueur

    def get_couleur(self):
        return couleur_nom(self.joueur)

    def est_noeud_max(self):
        return self.joueur == NOIR    # Noir maximise, Blanc minimise

    def coups_valides(self):
        return Regles(self.tab, self.joueur, self.ennemi).coups_valides()

    def successeurs(self):
        """Un noeud enfant par coup légal : plateau résultant, à l'adversaire de jouer."""
        enfants = {}
        for (lig, col), pions in self.coups_valides().items():
            nouveau_tab = self.tab.copy()
            nouveau_tab[lig][col] = self.joueur
            for l, c in pions:
                nouveau_tab[l][c] = self.joueur
            enfants[(lig, col)] = Noeud(nouveau_tab, self.ennemi, self.joueur)
        return enfants

    def est_feuille(self):
        """Feuille = fin de partie : aucun des deux joueurs ne peut jouer."""
        moi = Regles(self.tab, self.joueur, self.ennemi).peut_jouer()
        lui = Regles(self.tab, self.ennemi, self.joueur).peut_jouer()
        return not moi and not lui

    def heuristique(self):
        """Évalue l'état du point de vue du Noir (positif = bon pour le Noir)."""
        score_position = 0
        for lig in range(8):
            for col in range(8):
                if self.tab[lig][col] == NOIR:
                    score_position += POIDS[lig][col]
                elif self.tab[lig][col] == BLANC:
                    score_position -= POIDS[lig][col]

        coups_noir = len(Regles(self.tab, NOIR, BLANC).coups_valides())
        coups_blanc = len(Regles(self.tab, BLANC, NOIR).coups_valides())
        mobilite = coups_noir - coups_blanc

        return score_position + 5 * mobilite


# ===========================================================================
# minmax : PLACEHOLDER provisoire
# À REMPLACER à l'étape suivante par le vrai alpha-bêta récursif.
# Pour l'instant : évaluation directe, sans exploration en profondeur.
# ===========================================================================
def minmax(noeud, profondeur, alpha, beta):
    if profondeur == 0:
        return noeud.heuristique()

    # Nœud MAX (c'est au Noir de jouer dans ce nœud)
    if noeud.est_noeud_max():
        valeur = float('-inf')
        for enfant in noeud.successeurs().values():
            valeur = max(valeur, minmax(enfant, profondeur-1, alpha, beta))
            if valeur >= beta:
                return valeur   # coupure beta : Min n'ira jamais ici
            alpha = max(alpha, valeur)  # on relève notre borne
        return valeur

    else: # Nœud MIN (c'est au Blanc de jouer dans ce nœud)
        valeur = float('inf')
        for enfant in noeud.successeurs().values():
            valeur = min(valeur, minmax(enfant, profondeur-1, alpha, beta))
            if valeur <= alpha:
                return valeur   # coupure alpha : Max n'ira jamais ici
            beta = min(beta, valeur)    # on abaisse notre borne
        return valeur


# ===========================================================================
# JoueurIA : la façade (même interface que le Joueur humain)
# ===========================================================================
class JoueurIA:

    def __init__(self, joueur, profondeur):
        self.joueur = joueur
        self.profondeur = profondeur

    def get_joueur(self):
        return self.joueur

    def get_couleur(self):
        return couleur_nom(self.joueur)

    def get_profondeur(self):
        return self.profondeur

    def choisir_coup(self, regles):
        """Choisit le meilleur coup via minmax et renvoie (lig, col, pions)."""
        coups = regles.coups_valides()
        racine = Noeud(regles.tab, regles.joueur, regles.ennemi)
        enfants = racine.successeurs()   # { (lig, col) : Noeud enfant }

        meilleur_coup = None
        meilleure_valeur = None
        for coup, enfant in enfants.items():
            valeur = minmax(enfant, self.profondeur - 1, float('-inf'), float('inf'))
            # racine maximise si Noir, minimise si Blanc
            if (meilleure_valeur is None
                    or (racine.est_noeud_max() and valeur > meilleure_valeur)
                    or (not racine.est_noeud_max() and valeur < meilleure_valeur)):
                meilleure_valeur = valeur
                meilleur_coup = coup

        lig, col = meilleur_coup
        return lig, col, coups[(lig, col)]
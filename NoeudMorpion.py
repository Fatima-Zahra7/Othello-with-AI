"""
Created on Fri May  5 17:51:57 2023
"""


class NoeudMorpion:
    """Un noeud représente un état quelconque de la partie."""

    def __init__(self, grille, joueur, enfants=None):
        self.grille = grille          # La grille du jeu : matrice 3x3
        self.joueur = joueur          # Le joueur qui va jouer ce tour : 'X' ou 'O'
        self.enfants = enfants if enfants is not None else []  # Noeuds des tours suivants

    def est_noeud_max(self):
        return self.joueur == 'X'

    def est_noeud_min(self):
        return self.joueur == 'O'

    def successeurs(self):
        # Génère les noeuds enfants correspondant à tous les coups possibles
        # et les stocke dans self.enfants
        liste_enfants = []
        prochain_joueur = 'X' if self.joueur == 'O' else 'O'
        for i in range(len(self.grille)):
            for j in range(len(self.grille[i])):
                if self.grille[i][j] == ' ':
                    nouvelle_grille = [ligne.copy() for ligne in self.grille]
                    nouvelle_grille[i][j] = self.joueur
                    nouveau_noeud = NoeudMorpion(nouvelle_grille, prochain_joueur)
                    liste_enfants.append(nouveau_noeud)

        self.enfants = liste_enfants
        return self.enfants

    def est_feuille(self):
        # Un noeud est une feuille si la grille est pleine (aucune case vide).
        pleine = True
        i, j = 0, 0
        while pleine and i < len(self.grille):
            while pleine and j < len(self.grille[i]):
                if self.grille[i][j] == ' ':
                    pleine = False
                j += 1
            i += 1
            j = 0
        return pleine

    def afficher_grille(self):
        grille = self.grille
        abscisse = ['A', 'B', 'C']

        for x in abscisse:
            print('\t', x, end=' ')
        print('\n')

        for y, ligne in enumerate(grille):
            print("{:2d} :".format(y + 1), end="")
            for elem in ligne:
                print(elem, end=" | ")
            print('\n', "\t-----------")

    def heuristique(self):
        # Compte les alignements de 2 symboles + 1 case vide, et détecte les victoires.
        joueur = self.joueur
        grille = self.grille
        # Convention : 'X' = joueur Max, 'O' = joueur Min
        if joueur == 'X':
            symbole_max = joueur
            symbole_min = 'O'
        else:
            symbole_max = 'X'
            symbole_min = joueur

        score = 0

        # Lignes
        for i in range(3):
            if grille[i].count(symbole_max) == 3:
                return 100
            if grille[i].count(symbole_min) == 3:
                return -100
            if grille[i].count(symbole_max) == 2 and grille[i].count(' ') == 1:
                score += 10
            if grille[i].count(symbole_min) == 2 and grille[i].count(' ') == 1:
                score -= 10

        # Colonnes
        for j in range(3):
            colonne = [ligne[j] for ligne in grille]
            if colonne.count(symbole_max) == 3:
                return 100
            if colonne.count(symbole_min) == 3:
                return -100
            if colonne.count(symbole_max) == 2 and colonne.count(' ') == 1:
                score += 10
            if colonne.count(symbole_min) == 2 and colonne.count(' ') == 1:
                score -= 10

        # Diagonales
        diag1 = [grille[i][i] for i in range(3)]
        diag2 = [grille[i][2 - i] for i in range(3)]
        for diag in [diag1, diag2]:
            if diag.count(symbole_max) == 3:
                return 100
            if diag.count(symbole_min) == 3:
                return -100
            if diag.count(symbole_max) == 2 and diag.count(' ') == 1:
                score += 10
            if diag.count(symbole_min) == 2 and diag.count(' ') == 1:
                score -= 10

        return score

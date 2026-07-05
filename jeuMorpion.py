"""
Created on Fri May  5 17:53:00 2023

@author: ing
"""
from iaMorpion import *


# %% Minimax
def minimax(noeud, profondeur, alpha, beta):
    evaluation = noeud.heuristique()
    if noeud.est_feuille() or profondeur == 0 or abs(evaluation) == 100:
        return evaluation

    if noeud.est_noeud_max():  # Noeud Max
        valeur = None
        noeud.successeurs()
        for enfant in noeud.enfants:
            valeur_enfant = minimax(enfant, profondeur - 1, alpha, beta)
            if valeur is None or valeur < valeur_enfant:
                valeur = valeur_enfant
            if valeur >= beta:
                return valeur
            alpha = max(alpha, valeur)

    else:  # Noeud Min
        valeur = None
        noeud.successeurs()
        for enfant in noeud.enfants:
            valeur_enfant = minimax(enfant, profondeur - 1, alpha, beta)
            if valeur is None or valeur > valeur_enfant:
                valeur = valeur_enfant
            if valeur <= alpha:
                return valeur
            beta = min(beta, valeur)

    return valeur


# %% Choix du prochain coup via minimax
def prochain_coup_morpion(noeud, profondeur):
    enfants = noeud.successeurs()
    valeurs = []
    for enfant in enfants:
        valeurs.append(minimax(enfant, profondeur, float('-inf'), float('inf')))

    if noeud.est_noeud_max():
        meilleur_index = valeurs.index(max(valeurs))
    else:
        meilleur_index = valeurs.index(min(valeurs))

    meilleur_enfant = enfants[meilleur_index]

    # Extraction des coordonnées du coup joué : la case qui a changé
    grille_actuelle = noeud.grille
    grille_suivante = meilleur_enfant.grille
    for i in range(len(grille_actuelle)):
        for j in range(len(grille_actuelle[i])):
            if grille_actuelle[j][i] != grille_suivante[j][i] and grille_actuelle[j][i] == ' ':
                return i, j


# %%
def lettre_vers_indice(lettre):
    return ord(lettre) - ord('A')


def saisir_coordonnees(grille, joueur):
    while True:
        saisie = input(joueur + " coup (ex: A1) : ").strip().upper().replace(" ", "")

        if len(saisie) < 2:
            print("Format invalide : entrez une lettre puis un chiffre (ex: A1).")
            continue

        x = lettre_vers_indice(saisie[0])   # colonne : A, B ou C
        reste = saisie[1:]                  # ligne : 1, 2 ou 3

        if x < 0 or x > 2:
            print("Colonne invalide (A, B ou C).")
            continue
        if not reste.isdigit() or int(reste) < 1 or int(reste) > 3:
            print("Ligne invalide (1, 2 ou 3).")
            continue

        y = int(reste) - 1  # Ajustement de l'indexation de y

        if grille[y][x] != ' ':
            print("La case est déjà occupée, veuillez choisir une autre case.")
            continue

        return grille, x, y


# %%
def etat_partie(grille):
    # Renvoie le symbole gagnant, '-' si nul, ou None si la partie continue.
    # Lignes
    for ligne in grille:
        if ligne[0] == ligne[1] == ligne[2] and ligne[0] != ' ':
            return ligne[0]

    # Colonnes
    for col in range(3):
        if grille[0][col] == grille[1][col] == grille[2][col] and grille[0][col] != ' ':
            return grille[0][col]

    # Diagonales
    if grille[0][0] == grille[1][1] == grille[2][2] and grille[0][0] != ' ':
        return grille[0][0]
    if grille[0][2] == grille[1][1] == grille[2][0] and grille[0][2] != ' ':
        return grille[0][2]

    # Cases vides restantes ?
    for i in range(3):
        for j in range(3):
            if grille[j][i] == ' ':
                return None

    # Grille pleine sans gagnant : match nul
    return '-'


def alterne_joueur(joueur):
    return 'X' if joueur == 'O' else 'O'


def afficher_grille(grille):
    abscisse = ['A', 'B', 'C']

    for x in abscisse:
        print('\t', x, end=' ')
    print('\n')

    for y, ligne in enumerate(grille):
        print("{:2d} :".format(y + 1), end="")
        for elem in ligne:
            print(elem, end=" | ")
        print('\n', "\t-----------")


def choisir_premier_joueur():
    # Renvoie 'X' si le joueur humain commence, 'O' si c'est l'IA.
    while True:
        choix = input("Qui commence ? (1: Vous, 2: l'IA) : ").strip()
        if choix == '1':
            return 'X'
        if choix == '2':
            return 'O'
        print("Choix invalide, tapez 1 ou 2.")


def morpion():
    joueur_courant = choisir_premier_joueur()  # 'X' = humain, 'O' = IA
    grille = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']]

    noeud = Noeud(grille, 'O')

    while True:
        afficher_grille(grille)

        if joueur_courant == 'X':
            grille, x, y = saisir_coordonnees(grille, joueur_courant)
            if grille[y][x] == ' ':
                grille[y][x] = 'X'
        else:
            (x, y) = prochain_coup_morpion(noeud, 6)
            grille[y][x] = 'O'

        joueur_courant = alterne_joueur(joueur_courant)

        resultat = etat_partie(grille)
        if resultat is not None:  # La partie est terminée
            afficher_grille(grille)
            if resultat == '-':
                print("Match nul!")
            else:
                print(f"Le joueur {resultat} a gagné!")
            break

"""Orchestration d'une partie d'Othello : la boucle de jeu."""
import numpy as np
from constantes import NOIR, BLANC
from plateau import Plateau
from regles import Regles
from joueur import Joueur, coup_vers_notation
from ia import JoueurIA


class Partie:

    def __init__(self, joueur_noir, joueur_blanc):
        # Plateau de départ : 4 pions au centre
        self.tab = np.zeros((8, 8))
        self.tab[3][3] = BLANC
        self.tab[3][4] = NOIR
        self.tab[4][3] = NOIR
        self.tab[4][4] = BLANC

        self.joueur_noir = joueur_noir  # joueur 1
        self.joueur_blanc = joueur_blanc  # joueur 2
        self.plateau = Plateau(self.tab)


    def _adversaire(self, joueur):
        return self.joueur_blanc if joueur is self.joueur_noir else self.joueur_noir

    def _regles_de(self, joueur):
        """Construit l'objet Regles pour le joueur donné."""
        adversaire = self._adversaire(joueur)
        return Regles(self.tab, joueur.get_joueur(), adversaire.get_joueur())

    def partie_terminee(self):
        """La partie est finie quand AUCUN des deux joueurs ne peut jouer."""
        return (not self._regles_de(self.joueur_noir).peut_jouer()
                and not self._regles_de(self.joueur_blanc).peut_jouer())

    def _tour(self, joueur):
        regles = self._regles_de(joueur)

        if not regles.peut_jouer():
            print(f"{joueur.get_couleur()} ne peut pas jouer : il passe son tour.\n")
            return

        lig, col, pions = joueur.choisir_coup(regles)
        regles.jouer(lig, col, pions)
        print(f"{joueur.get_couleur()} joue en {coup_vers_notation(lig, col)}.\n")

    def jouer(self):
        joueur_courant = self.joueur_noir  # les Noirs commencent toujours
        self.plateau.afficher()

        while not self.partie_terminee():
            self._tour(joueur_courant)
            self.plateau.afficher()
            joueur_courant = self._adversaire(joueur_courant)

        print("=== Partie terminée ===")
        self.plateau.annoncer_vainqueur()


def choix_profondeur():
    """Demande la profondeur d'exploration de l'IA (entre 2 et 4) et la renvoie."""
    while True:
        print("A quelle profondeur souhaitez-vous que l'IA joue ?")
        print("  2 : rapide, jeu plus faible")
        print("  3 : équilibré")
        print("  4 : plus fort, mais plus lent")
        saisie = input("Votre choix (2, 3 ou 4) : ").strip()

        if saisie in ("2", "3", "4"):
            return int(saisie)

        print("Choix invalide, tapez 2, 3 ou 4.\n")


def lancer_othello():
    """Point d'entrée appelé par le menu (pour l'instant : humain contre humain)."""
    print("=== Othello ===")
    choix = choix_profondeur()

    noir = Joueur(NOIR)
    blanc = JoueurIA(BLANC, choix)

    Partie(noir, blanc).jouer()

"""Joueur humain : saisie d'un coup et validation via les règles."""
from constantes import couleur_nom


def coup_vers_notation(lig, col):
    """(0, 0) -> 'A1', (2, 3) -> 'D3'  (colonne = lettre, ligne = chiffre)."""
    return f"{chr(ord('A') + col)}{lig + 1}"


class Joueur:

    def __init__(self, joueur):
        self.joueur = joueur    # 1 (Noir) ou 2 (Blanc)

    def get_joueur(self):
        return self.joueur

    def get_couleur(self):
        return couleur_nom(self.joueur)

    def _saisir(self):
        """Lit un coup au format A1 et le traduit en (lig, col). Ne juge pas la légalité."""
        while True:
            saisie = input(f"{self.get_couleur()} - votre coup (ex: A1) : ").strip().upper().replace(" ", "")

            if len(saisie) < 2:
                print("Format invalide : une lettre puis un chiffre (ex: A1).")
                continue

            col = ord(saisie[0]) - ord('A')   # colonne : A..H -> 0..7
            reste = saisie[1:]                # ligne   : 1..8 -> 0..7

            if col < 0 or col > 7:
                print("Colonne invalide (A à H).")
                continue
            if not reste.isdigit() or int(reste) < 1 or int(reste) > 8:
                print("Ligne invalide (1 à 8).")
                continue

            lig = int(reste) - 1
            return lig, col

    def choisir_coup(self, regles):
        """Demande un coup LÉGAL au joueur et renvoie (lig, col, pions_a_retourner)."""
        coups = regles.coups_valides()
        options = ", ".join(coup_vers_notation(l, c) for (l, c) in sorted(coups))
        print(f"Coups possibles : {options}")

        while True:
            lig, col = self._saisir()
            if (lig, col) in coups:
                return lig, col, coups[(lig, col)]
            print("Coup illégal : cette case ne retourne aucun pion. Réessayez.")

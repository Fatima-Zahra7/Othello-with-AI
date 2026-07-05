"""
Created on Mon May  8 02:18:30 2023
"""
from jeuMorpion import morpion


def main():
    while True:
        print("A quel jeu voulez-vous jouer ?")
        print("1: Othello")
        print("2: Morpion")
        print("3. Exit")
        try:
            choice = int(input("Enter your choice (1, 2, or 3): "))
            if choice == 1:
                print("Othello n'est pas encore disponible !")
            elif choice == 2:
                morpion()
            elif choice == 3:
                print("Thank you for playing. Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()

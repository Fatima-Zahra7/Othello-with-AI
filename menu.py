"""
Created on Mon May  8 02:18:30 2023
"""
from jeuOthello import lancer_othello


def main():
    while True:
        print("A quel jeu voulez-vous jouer ?")
        print("1: Othello")
        print("2: Morpion")
        print("3. Exit")
        try:
            choice = int(input("Enter your choice (1, 2, or 3): "))
            if choice == 1:
                lancer_othello()
            elif choice == 2:
                print("Morpion !")
            elif choice == 3:
                print("Thank you for playing. Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()

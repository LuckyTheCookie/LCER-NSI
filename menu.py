import admin
import client
from utils import clear_console

def menu_principal():
    while True:
        print("""
------------------------------------------
Bienvenue chez LCER
Entrez un entier :
  0 : Sortir du menu et du programme
  1 : Menu dirigeant
  2 : Menu utilisateur
------------------------------------------
""")
        choix = input('Entrez votre choix : ')
        if choix == '0':
            return
        elif choix == '1':
            clear_console()
            admin.admin_menu()
        elif choix == '2':
            clear_console()
            client.client_menu()
        else:
            print('Choix non disponible')

if __name__ == '__main__':
    menu_principal()


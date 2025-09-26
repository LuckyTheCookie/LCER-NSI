from utils import conn, cur, close_module, clear_console

def achat():
    print("Bienvenue dans le menu d'achat LCER")
    print("Commençons par vous identifier")
    identifiant = input("Entrez votre identifiant : ")
    cur.execute("SELECT nom FROM CLIENT WHERE idc = ?", (identifiant,))
    nom = cur.fetchone()
    if nom:
        print(f"Identifiant reconnu : {identifiant}. Bienvenue {nom[0]} !")
        print("Voici la liste des produits disponibles :")
        cur.execute("SELECT idp, nom, prix FROM PRODUIT")
        produits = cur.fetchall()
        for idp, nom, prix in produits:
            print(f"{idp} : {nom} - {prix} euros")
        choix = input("Entrez l'identifiant du produit que vous souhaitez acheter : ")
        cur.execute("SELECT nom, prix FROM PRODUIT WHERE idp = ?", (choix,))
        produit = cur.fetchone()
        if produit:
            print(f"Vous avez choisi d'acheter {produit[0]} au prix de {produit[1]} euros.")
            cur.execute("INSERT INTO ACHAT (idc, idp, expedie) VALUES (?, ?, ?)", (identifiant, choix, 'non'))
            cur.execute("UPDATE CLIENT SET debit = debit + ? WHERE idc = ?", (produit[1], identifiant))
            conn.commit()
            print("Achat enregistré avec succès, merci pour votre achat !")
            close_module()
        else:
            print("Produit inconnu.")
    else:
        print("Identifiant inconnu.")
        close_module()
        return

def paiement():
    print("Bienvenue dans le module de paiement LCER")
    identifiant = input("Commençons par vous identifier. Entrez votre identifiant : ")
    cur.execute("SELECT nom, debit FROM CLIENT WHERE idc = ?", (identifiant,))
    client = cur.fetchone()
    if client:
        print(f"Identifiant reconnu : {identifiant}. Bienvenue {client[0]} !")
        print(f"Votre débit actuel est de {client[1]} euros.")
        if client[1] > 0:
            montant = float(input("Entrez le montant que vous souhaitez payer : "))
            if montant <= 0:
                print("Le montant doit être positif.")
            elif montant > client[1]:
                print("Le montant dépasse votre débit actuel.")
            else:
                cur.execute("UPDATE CLIENT SET debit = debit - ? WHERE idc = ?", (montant, identifiant))
                conn.commit()
                print(f"Paiement de {montant} euros effectué avec succès. Nouveau débit : {client[1] - montant} euros.")
        else:
            print("Vous n'avez pas de débit à régler. Merci !")
    else:
        print("Identifiant inconnu.")
    close_module()

def client_menu():
    while True:
        print("\n--- Menu Utilisateur ---")
        print("1 : Achat d'un produit")
        print("2 : Paiement du débit")
        print("0 : Revenir au menu principal")
        choix = input('Entrez votre choix : ')
        if choix == '0':
            clear_console()
            return
        elif choix == '1':
            achat()
        elif choix == '2':
            paiement()
        else:
            print('Choix non disponible')

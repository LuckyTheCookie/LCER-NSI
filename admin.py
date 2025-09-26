from utils import conn, cur, close_module, clear_console

def relance():
    client = input("Entrez le nom du client à relancer : ")
    cur.execute('SELECT * FROM CLIENT WHERE nom=?', (client,))
    client = cur.fetchone()
    if client is None:
        print("Client non trouvé.")
        return
    # Vérification du débit
    if client[4] == 0:
        print("Le client n'a pas de débit à régler.")
        return
    # Envoi de la relance
    print(f"Relance envoyée au client {client[1]} pour un montant de {client[4]} euros.")
    close_module()

def analyse():
    cur.execute('''
                SELECT SUM(PRODUIT.prix) AS total_ventes
                FROM PRODUIT
                JOIN ACHAT ON PRODUIT.idp = ACHAT.idp
                ''')
    total_ventes = cur.fetchone()[0]
    print(f"Total des ventes : {total_ventes} euros")
    client = input("Entrez le nom du client pour voir ses achats : ")
    cur.execute('''SELECT PRODUIT.nom, PRODUIT.prix
                FROM ACHAT
                JOIN PRODUIT ON ACHAT.idp = PRODUIT.idp
                JOIN CLIENT ON ACHAT.idc = CLIENT.idc
                WHERE CLIENT.nom = ?
                ''', (client,))
    achats = cur.fetchall()
    if achats:
        print(f"Achats de {client} : ({str(len(achats))} articles)")
        for nom, prix in achats:
            print(f"- {nom} : {prix} euros")
    close_module()

def expedition():
    print("Bienvenue dans le menu d'expédition LCER")
    cur.execute('''
        SELECT A.ida, P.nom, C.nom
        FROM ACHAT A 
        JOIN CLIENT C ON A.idc = C.idc 
        JOIN PRODUIT P ON A.idp = P.idp 
        WHERE A.expedie = 'non'
    ''')
    achats = cur.fetchall()
    if achats:
        print("Voici la liste des achats en attente d'expédition :")
        for ida, nom_produit, nom_client in achats:
            print(f"{ida} : {nom_produit} (Client : {nom_client})")
        choix = input("Entrez l'identifiant de l'achat que vous souhaitez expédier : ")
        cur.execute("SELECT ida FROM ACHAT WHERE ida = ? AND expedie = 'non'", (choix,))
        achat = cur.fetchone()
        if achat:
            # Marquer l'achat comme expédié
            cur.execute("UPDATE ACHAT SET expedie = 'oui' WHERE ida = ?", (choix,))
            # Mettre à jour le stock du produit
            cur.execute('''
                UPDATE PRODUIT 
                SET stock = stock - 1 
                WHERE idp = (SELECT idp FROM ACHAT WHERE ida = ?)
            ''', (choix,))
            conn.commit()
            print("Achat expédié avec succès.")
        else:
            print("Achat inconnu ou déjà expédié.")
    else:
        print("Vous êtes au top ! Aucun achat en attente d'expédition.")
    close_module()

def admin_menu():
    while True:
        print("\n--- Menu Dirigeant ---")
        print("1 : Relance pour le paiement d'un débit")
        print("2 : Analyse des ventes")
        print("3 : Expédition d'un achat")
        print("0 : Revenir au menu principal")
        choix = input('Entrez votre choix : ')
        if choix == '0':
            clear_console()
            return
        elif choix == '1':
            relance()
        elif choix == '2':
            analyse()
        elif choix == '3':
            expedition()
        else:
            print('Choix non disponible')

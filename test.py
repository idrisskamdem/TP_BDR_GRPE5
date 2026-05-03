from cassandra.cluster import Cluster
import pandas as pd

# Connexion à Cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('etudiants')

# Préparer la requête d'insertion
insert_query = session.prepare("""
INSERT INTO etudiant (matricule, nom, dateNaiss, regionOrigine)
VALUES (?, ?, ?, ?)
""")

# ----------- FONCTIONS -----------

def inserer_donnees():
    try:
        file_path = "etudiants_5000.xlsx"
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            date_naiss = pd.to_datetime(row['DateNaiss']).date()

            session.execute(insert_query, (
                row['Matricule'],
                row['Nom'],
                date_naiss,
                row['RegionOrigine']
            ))

        print(" Données insérées avec succès !")

    except Exception as e:
        print(" Erreur lors de l'insertion :", e)


def lire_donnees():
    try:
        region = input("👉 Entrez la région (Nord/Sud/Est/Ouest) : ")

        rows = session.execute("""
        SELECT * FROM etudiant WHERE regionOrigine=%s
        """, (region,))

        print(f"\n Étudiants de la région {region} :\n")

        count = 0
        for row in rows:
            print(row)
            count += 1
            if count >= 10:
                break

        if count == 0:
            print(" Aucune donnée trouvée.")

    except Exception as e:
        print(" Erreur lors de la lecture :", e)


# ----------- MENU -----------

def menu():
    while True:
        print("\n===== MENU =====")
        print("1 - Insérer les données depuis Excel")
        print("2 - Lire les données par région")
        print("0 - Quitter")

        choix = input(" Votre choix : ")

        if choix == "1":
            inserer_donnees()

        elif choix == "2":
            lire_donnees()

        elif choix == "0":
            print(" Fin du programme")
            break

        else:
            print(" Choix invalide, réessayez.")


# Lancer le menu
menu()

# Fermer connexion
cluster.shutdown()

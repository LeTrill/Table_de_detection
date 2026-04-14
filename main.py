import os
from app.detection import TableDetector

def main():
    # 1. Configuration
    image_a_traiter = "data/inputs/facture3.png"
    dossier_sortie = "data/outputs"
    
    # 2. Initialisation (Charge le processeur et le modèle une seule fois)
    detector = TableDetector(threshold=0.7)

    print(f"\n--- Lancement de l'analyse ---")

    try:
        # 3. Prédiction (Détection des tableaux)
        resultats = detector.predict(image_a_traiter)

        # Affichage des résultats récupérés via _format_detections
        if not resultats:
            print("Aucun tableau détecté sur ce document.")
        else:
            print(f"Succès : {len(resultats)} tableau(x) identifié(s).\n")
            for i, tab in enumerate(resultats):
                print(f"  Tableau {i+1} :")
                print(f"     Type       : {tab['type']}")
                print(f"     Confiance  : {tab['confiance']}")
                print(f"     Coordonnées :")
                print(f"       • X min   : {tab['coords']['xmin']}")
                print(f"       • Y min   : {tab['coords']['ymin']}")
                print(f"       • X max   : {tab['coords']['xmax']}")
                print(f"       • Y max   : {tab['coords']['ymax']}")
                print()

            # 4. Appel de EXTRACT_TABLES
            # Utilise les coordonnées déjà calculées pour découper et sauvegarder
            print(f"\n--- Extraction physique vers {dossier_sortie} ---")
            fichiers_crees = detector.extract_tables(image_a_traiter, output_folder=dossier_sortie)
            
            for f in fichiers_crees:
                print(f"  [FICHIER CRÉÉ] : {f}")

    except FileNotFoundError as e:
        print(f"Erreur de chemin : {e}")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    main()
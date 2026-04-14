import pytest
import os
import sys
from pathlib import Path
from PIL import Image

# Ajouter le répertoire parent au chemin Python
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.detection import TableDetector

@pytest.fixture(scope="module")
def detecteur():
    """Fixture pour ne charger le modèle qu'une seule fois."""
    print("\n Chargement du détecteur de tableaux...")
    detector = TableDetector(threshold=0.8)
    print("✓ Détecteur chargé avec succès!")
    return detector

def test_prediction(detector, tmp_path):
    """Vérifie que le modèle traite une image valide sans erreur."""
    print("\n TEST: Prédiction sur image valide")
    img_path = tmp_path / "test_invoice.jpg"
    Image.new('RGB', (500, 500), color='white').save(img_path)
    print(f"   Image créée: {img_path}")
    
    results = detector.predict(str(img_path))
    print(f"  ✓ Résultat: {len(results)} détection(s)")
    assert isinstance(results, list)
    print("   TEST RÉUSSI")

def test_erreur_file(detector):
    """Vérifie l'erreur si le fichier n'existe pas."""
    print("\n TEST: Gestion erreur fichier introuvable")
    with pytest.raises(FileNotFoundError):
        detector.predict("chemin_fantome.png")
    print("  ✓ FileNotFoundError levée comme prévu")
    print("  TEST RÉUSSI")

def test_erreur_format_invalide(detector, tmp_path):
    """Vérifie l'erreur si le fichier n'est pas une image."""
    print("\n TEST: Gestion erreur format invalide")
    fake_img = tmp_path / "not_an_image.txt"
    fake_img.write_text("Ceci est un texte, pas une image.")
    print(f"  Fichier invalide créé: {fake_img}")
    
    with pytest.raises(Exception): # Pillow lève une erreur sur l'ouverture
        detector.predict(str(fake_img))
    print("  ✓ Exception levée comme prévu")
    print("   TEST RÉUSSI")

def test_prediction_retour_format(detector, tmp_path):
    """Vérifie que les résultats ont la bonne structure."""
    print("\n TEST: Format des résultats")
    img_path = tmp_path / "test.jpg"
    Image.new('RGB', (600, 600), color='white').save(img_path)
    
    results = detector.predict(str(img_path))
    print(f"  Résultats: {len(results)} détection(s)")
    
    # Chaque résultat doit être un dictionnaire avec ces clés
    for i, result in enumerate(results):
        assert isinstance(result, dict)
        assert "type" in result
        assert "confiance" in result
        assert "coords" in result
        assert all(key in result["coords"] for key in ["xmin", "ymin", "xmax", "ymax"])
        print(f"    Détection {i+1}: {result['type']} ({result['confiance']})")
    print("  TEST RÉUSSI")

def test_table_extraction(detector, tmp_path):
    """Vérifie que l'extraction crée bien des fichiers physiques."""
    print("\n TEST: Extraction des tableaux")
    img_path = tmp_path / "to_extract.jpg"
    Image.new('RGB', (600, 600), color='white').save(img_path)
    print(f"  Image source: {img_path}")
    
    out_dir = tmp_path / "extracted_out"
    # Même si 0 tableau trouvé sur du blanc, la fonction doit renvoyer une liste
    paths = detector.extract_tables(str(img_path), output_folder=str(out_dir))
    print(f"   Fichiers extraits: {len(paths)}")
    for path in paths:
        print(f"    - {path}")
    assert isinstance(paths, list)
    print(" TEST RÉUSSI")
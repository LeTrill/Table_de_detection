# 🔍 Table Detection - Automatic Table Detection System

An automatic table detection project in documents (invoices, receipts, PDFs) using the **DETR** (Detection Transformer) model from Hugging Face.

## 📋 Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Configuration](#configuration)
- [Tests](#tests)
- [Examples](#examples)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)

---

## 📝 Description

This project automates **table detection** in document images. It uses the pre-trained model `TahaDouaji/detr-doc-table-detection` from Hugging Face, based on the DETR (Detection Transformer) architecture.

**Use Cases:**
- 📄 Data extraction from invoices
- 📊 Analysis of receipts and administrative documents
- 🔲 Detection of table structures in PDF scans
- 📈 Automatic document preprocessing

---

## ✨ Features

✅ **Table Detection** - Identifies all tables present in an image  
✅ **Physical Extraction** - Crops and saves tables as separate files  
✅ **GPU/CPU Support** - Automatic detection and hardware adaptation  
✅ **Configurable Confidence Threshold** - Adjust detection sensitivity  
✅ **Structured Results** - JSON output with type, confidence, and coordinates  
✅ **Complete Unit Tests** - Test suite for validation  
✅ **Robust Error Handling** - Comprehensive error case handling

---

## 🚀 Installation

### Requirements

- Python 3.10+
- pip or conda
- 4GB RAM minimum (8GB recommended)
- NVIDIA GPU (optional, but recommended for speed)

### Step 1: Clone the Project

```bash
git clone https://github.com/LeTrill/Table-detection2.git
cd Table-detection2
```

### Step 2: Create a Virtual Environment

**With Python venv:**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

**With Conda:**
```bash
conda create -n table-detection python=3.11
conda activate table-detection
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Or directly:**
```bash
pip install torch torchvision transformers pillow numpy huggingface-hub timm pytest
```

### Step 4: Verify Installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'GPU available: {torch.cuda.is_available()}')"
```

---

## 📁 Project Structure

```
Table-detection2/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── detection.py          # TableDetector class (project core)
│   └── detection.ipynb       # Development notebook
├── tests/
│   ├── test_detector.py      # Unit test suite
│   └── test_detector.ipynb   # Test notebook
├── data/
│   ├── inputs/               # Input images
│   └── outputs/              # Extracted tables
├── main.py                   # Main execution script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .gitignore               # Git ignore file
```

---

## 💻 Usage

### Method 1: Main Script (Recommended)

```bash
python main.py
```

The script:
1. Initializes the detector
2. Analyzes the image `data/inputs/facture3.png`
3. Displays the results
4. Extracts tables to `data/outputs/`

### Method 2: Use as a Module

```python
from app.detection import TableDetector

# Create a detector instance
detector = TableDetector(threshold=0.5)

# Analyze an image
results = detector.predict("path/to/image.jpg")

# Display results
for detection in results:
    print(f"Type: {detection['type']}")
    print(f"Confidence: {detection['confiance']}")
    print(f"Coordinates: {detection['coords']}")

# Extract tables
files = detector.extract_tables("path/to/image.jpg", output_folder="output/")
print(f"Files created: {files}")
```

### Method 3: Use the Helper Function

```python
from app import create_detector

detector = create_detector(threshold=0.6)
results = detector.predict("my_image.jpg")
```

---

## ⚙️ Configuration

### Detector Parameters

```python
TableDetector(
    model_name="TahaDouaji/detr-doc-table-detection",  # Model to use
    threshold=0.5                                        # Confidence threshold (0.0-1.0)
)
```

#### Confidence Threshold (threshold)

| Value | Description | Use Case |
|-------|-------------|----------|
| 0.9+ | Very strict | Highly reliable detections |
| 0.7-0.8 | Moderate | Balanced confidence/sensitivity |
| 0.5-0.6 | **Recommended** | Most cases |
| 0.3-0.4 | Permissive | More detections |
| <0.3 | Very permissive | Risk of false positives |

### Environment Variables

```bash
# Enable GPU (optional)
export CUDA_VISIBLE_DEVICES=0  # Linux/Mac
set CUDA_VISIBLE_DEVICES=0     # Windows
```

---

## 🧪 Tests

### Run All Tests

```bash
pytest tests/test_detector.py -v -s
```

### Test Options

```bash
# Verbose + print display
pytest tests/test_detector.py -v -s

# With code coverage
pytest tests/test_detector.py --cov=app

# Specific test
pytest tests/test_detector.py::test_prediction_on_valid_image -v
```

### Available Tests

1. **test_prediction_on_valid_image** - Prediction on valid image
2. **test_error_file_not_found** - Handle missing file error
3. **test_error_invalid_format** - Handle invalid format error
4. **test_prediction_returns_correct_format** - Validate result format
5. **test_table_extraction** - Physical table extraction

---

## 📊 Examples

### Example 1: Simple Detection

```python
from app.detection import TableDetector

detector = TableDetector(threshold=0.5)
results = detector.predict("invoice.jpg")

if results:
    print(f"✅ {len(results)} table(s) found")
else:
    print("⚠️ No tables detected")
```

### Example 2: Extraction with Detailed Output

```python
from app.detection import TableDetector
import json

detector = TableDetector()
results = detector.predict("document.jpg")

# Save to JSON
with open("results.json", "w") as f:
    json.dump(results, f, indent=2)

# Extract tables
files = detector.extract_tables("document.jpg", output_folder="tables/")
print(f"Extracted: {', '.join(files)}")
```

### Example 3: Loop Over Multiple Images

```python
from app.detection import TableDetector
import os

detector = TableDetector()
folder = "data/inputs/"

for file in os.listdir(folder):
    if file.lower().endswith(('.jpg', '.png')):
        path = os.path.join(folder, file)
        print(f"\n🔍 Processing: {file}")
        
        results = detector.predict(path)
        print(f"   → {len(results)} table(s)")
```

---

## 📦 Dependencies

### Main Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| torch | ≥2.0.0 | Deep learning framework |
| torchvision | ≥0.15.0 | Computer vision |
| transformers | ≥4.30.0 | Pre-trained models |
| timm | ≥0.9.0 | Backbone architectures |
| Pillow | ≥9.0.0 | Image processing |
| huggingface-hub | ≥0.16.0 | Model downloads |
| numpy | 1.22.4-2.3.0 | Numerical computing |

### Test Dependencies

```
pytest ≥7.0.0
pytest-cov ≥4.0.0
```

---

## 🔧 Troubleshooting

### Problem 1: ModuleNotFoundError: No module named 'torch'

**Solution:**
```bash
pip install torch torchvision
```

### Problem 2: CUDA out of memory

**Solutions:**
- Reduce input resolution
- Use CPU instead of GPU
- Close resource-intensive applications

```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Force CPU
```

### Problem 3: No tables detected

**Possible causes:**
- Threshold too high → Reduce to 0.5 or less
- Poor image quality → Check the image
- Unsupported format → Convert to JPG/PNG

**Solution:**
```python
detector = TableDetector(threshold=0.3)  # More permissive
```

### Problem 4: NumPy/SciPy Warning

```
UserWarning: A NumPy version >=1.22.4 and <2.3.0 is required
```

**Solution:**
```bash
pip install "numpy>=1.22.4,<2.3.0"
```

### Problem 5: Slow performance

**Optimizations:**
- Use GPU if available
- Reduce input resolution
- Process by batch if possible

```python
detector = TableDetector()
print(f"Using: {detector.device}")  # Check GPU/CPU
```

---

## 📈 Performance

### Benchmarks (Intel i7 CPU)

| Resolution | Time | Tables |
|-----------|------|--------|
| 500×500 | ~2s | 0-1 |
| 1000×1000 | ~3s | 1-2 |
| 2000×2000 | ~5s | 2-3 |

**With NVIDIA RTX 3060 GPU:** ~50% faster

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🔗 Resources

- [DETR Paper](https://arxiv.org/abs/2005.12677)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Model Used](https://huggingface.co/TahaDouaji/detr-doc-table-detection)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)

---

## 📞 Support

For questions or issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Open an issue on GitHub
3. Consult Hugging Face documentation

---

**Last Update:** April 15, 2026  
**Version:** 1.0.0  
**Status:** ✅ Production Ready

---

##  Description

Ce projet automatise la **détection de tableaux** dans des images de documents. Il utilise le modèle pré-entraîné `TahaDouaji/detr-doc-table-detection` de Hugging Face, basé sur l'architecture DETR (Detection Transformer).

**Cas d'usage :**
- 📄 Extraction de données depuis des factures
- 📊 Analyse de reçus et documents administratifs
- 🔲 Détection de structures de tableaux dans des scans PDF
- 📈 Pré-traitement automatique de documents

---

##  Fonctionnalités

✅ **Détection de tableaux** - Identifie tous les tableaux présents dans une image  
✅ **Extraction physique** - Découpe et sauvegarde les tableaux en fichiers séparés  
✅ **Support GPU/CPU** - Détection automatique et adaptation au matériel disponible  
✅ **Seuil de confiance configurable** - Ajustez la sensibilité de détection  
✅ **Résultats structurés** - Sortie JSON avec type, confiance et coordonnées  
✅ **Tests unitaires complets** - Suite de tests pour validation  
✅ **Gestion d'erreurs robuste** - Gestion complète des cas d'erreur

---

##  Installation

### Prérequis

- Python 3.10+
- pip ou conda
- 4GB RAM minimum (8GB recommandé)
- GPU NVIDIA (optionnel, mais recommandé pour la vitesse)

### Étape 1 : Cloner le projet

```bash
git clone <https://github.com/LeTrill/Table_de_detection.git>
cd Table-detection2
```

### Étape 2 : Créer un environnement virtuel

**Avec Python venv :**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

**Avec Conda :**
```bash
conda create -n table-detection python=3.11
conda activate table-detection
```

### Étape 3 : Installer les dépendances

```bash
pip install -r requirements.txt
```

**Ou directement :**
```bash
pip install torch torchvision transformers pillow numpy huggingface-hub timm pytest
```

### Étape 4 : Vérifier l'installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'GPU disponible: {torch.cuda.is_available()}')"
```

---

## Structure du projet

```
Table-detection2/
├── app/
│   ├── detection.py          # Classe TableDetector (cœur du projet)
│  
├── tests/
│   ├── test_detector.py      # Suite de tests unitaires
│   
├── data/
│   ├── inputs/               # Images d'entrée
│   └── outputs/              # Tableaux extraits
├── main.py                   # Script principal d'exécution
├── requirements.txt          # Dépendances Python
├── README.md                 # Ce fichier
└── .gitignore               # Fichiers Git ignorés
```

---

##  Utilisation

### Méthode 1 : Script principal (recommandé)

```bash
python main.py
```

Le script :
1. Initialise le détecteur
2. Analyse l'image 
3. Affiche les résultats
4. Extrait les tableaux vers 

### Méthode 2 : Utilisation en tant que module

```python
from app.detection import TableDetector

# Créer une instance du détecteur
detector = TableDetector(threshold=0.5)

# Analyser une image
resultats = detector.predict("chemin/vers/image.jpg")

# Afficher les résultats
for detection in resultats:
    print(f"Type: {detection['type']}")
    print(f"Confiance: {detection['confiance']}")
    print(f"Coordonnées: {detection['coords']}")

# Extraire les tableaux
fichiers = detector.extract_tables("chemin/vers/image.jpg", output_folder="output/")
print(f"Fichiers créés: {fichiers}")
```

### Méthode 3 : Utiliser la fonction helper

```python
from app import create_detector

detector = create_detector(threshold=0.6)
resultats = detector.predict("mon_image.jpg")
```

---

## Configuration

### Paramètres du détecteur

```python
TableDetector(
    model_name="TahaDouaji/detr-doc-table-detection",  # Modèle à utiliser
    threshold=0.5                                        # Seuil de confiance (0.0-1.0)
)
```

#### Seuil de confiance (threshold)

| Valeur | Description | Cas d'usage |
|--------|-------------|-----------|
| 0.9+ | Très stricte | Détections très fiables |
| 0.7-0.8 | Modéré | Équilibre confiance/sensibilité |
| 0.5-0.6 | **Recommandé** | Plupart des cas |
| 0.3-0.4 | Permissif | Captures plus de détections |
| <0.3 | Très permissif | Risque de faux positifs |

### Variables d'environnement

```bash
# Activer le GPU (optionnel)
export CUDA_VISIBLE_DEVICES=0  # Linux/Mac
set CUDA_VISIBLE_DEVICES=0     # Windows
```

---

## Tests

### Lancer tous les tests

```bash
pytest tests/test_detector.py -v -s
```

### Options de test

```bash
# Verbose + affichage des prints
pytest tests/test_detector.py -v -s

# Avec couverture de code
pytest tests/test_detector.py --cov=app

# Test spécifique
pytest tests/test_detector.py::test_prediction_on_valid_image -v
```

### Tests disponibles

1. **test_prediction_on_valid_image** - Prédiction sur image valide
2. **test_error_file_not_found** - Gestion erreur fichier inexistant
3. **test_error_invalid_format** - Gestion erreur format invalide
4. **test_prediction_returns_correct_format** - Validation du format des résultats
5. **test_table_extraction** - Extraction physique des tableaux


---

##  Dépendances

### Dépendances principales

| Paquet | Version | Utilité |
|--------|---------|---------|
| torch | ≥2.0.0 | Framework deep learning |
| torchvision | ≥0.15.0 | Vision par ordinateur |
| transformers | ≥4.30.0 | Modèles pré-entraînés |
| timm | ≥0.9.0 | Architectures backbone |
| Pillow | ≥9.0.0 | Traitement d'images |
| huggingface-hub | ≥0.16.0 | Téléchargement modèles |
| numpy | 1.22.4-2.3.0 | Calculs numériques |

### Dépendances de test

```
pytest ≥7.0.0
pytest-cov ≥4.0.0
```

---

## Troubleshooting

### Problème 1 : ModuleNotFoundError: No module named 'torch'

**Solution :**
```bash
pip install torch torchvision
```

### Problème 2 : CUDA out of memory

**Solutions :**
- Réduire la résolution d'entrée
- Utiliser CPU au lieu de GPU
- Fermer les applications gourmandes en VRAM

```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Force CPU
```

### Problème 3 : Aucun tableau détecté

**Causes possibles :**
- Seuil trop élevé → Réduisez à 0.5 ou moins
- Image de mauvaise qualité → Vérifiez l'image
- Format non supporté → Convertissez en JPG/PNG

**Solution :**
```python
detector = TableDetector(threshold=0.3)  # Plus permissif
```

### Problème 4 : Avertissement NumPy/SciPy

```
UserWarning: A NumPy version >=1.22.4 and <2.3.0 is required
```

**Solution :**
```bash
pip install "numpy>=1.22.4,<2.3.0"
```

### Problème 5 : Performance lente

**Optimisations :**
- Utilisez GPU si disponible
- Réduisez la résolution d'entrée
- Traitez par batch si possible

```python
detector = TableDetector()
print(f"Utilisant: {detector.device}")  # Vérifier GPU/CPU
```

---

## 📈 Performance

### Benchmarks (sur CPU Intel i7)

| Résolution | Temps | Tableaux |
|-----------|------|---------|
| 500×500 | ~2s | 0-1 |
| 1000×1000 | ~3s | 1-2 |
| 2000×2000 | ~5s | 2-3 |

**Avec GPU NVIDIA RTX 3060 :** ~50% plus rapide


---

##  Ressources

- [DETR Paper](https://arxiv.org/abs/2005.12677)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Modèle utilisé](https://huggingface.co/TahaDouaji/detr-doc-table-detection)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)

---

## Support

Pour toute question ou problème :
1. Vérifiez le [Troubleshooting](#troubleshooting)
2. Ouvrez une issue sur GitHub
3. Consultez la documentation de Hugging Face

---

**Dernière mise à jour :** 14 avril 2026  
**Version :** 1.0.0  


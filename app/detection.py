import torch
from PIL import Image
from transformers import DetrImageProcessor, DetrForObjectDetection
import os

class TableDetector:

    def __init__(self, model_name="TahaDouaji/detr-doc-table-detection", threshold=0.9):

        # Détection du matériel : utilise la carte graphique (GPU) si disponible, sinon le processeur (CPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Chargement du modèle sur : {self.device}")
        self.processor = DetrImageProcessor.from_pretrained(model_name)
        self.model = DetrForObjectDetection.from_pretrained(model_name).to(self.device)
        self.threshold = threshold

    def predict(self, image_path):
      
        # 1. Vérifier si le fichier existe
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"L'image {image_path} est introuvable.")
        # 2. Ouvrir l'image et s'assurer qu'elle est en mode RGB (3 canaux couleurs)
        image = Image.open(image_path).convert("RGB")

        # 3. Pré-traitement (Preprocessing)
        # Transforme l'image en tenseurs (objets mathématiques) compréhensibles par PyTorch
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)

        # 4. Inférence (Prédiction)
        with torch.no_grad():
            outputs = self.model(**inputs)

        # 5. Post-traitement (Post-processing)
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.processor.post_process_object_detection(
            outputs,
            target_sizes=target_sizes,
            threshold=self.threshold
        )[0]

        # 6. Formatage des résultats pour une utilisation facile
        return self._format_detections(results)

    def _format_detections(self, results):
        """
        Méthode interne pour transformer les tenseurs bruts en liste lisible.
        """
        final_results = []

        # on boucle sur chaque détection trouvée au-dessus du seuil (threshold)
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            # Extraction des coordonnées de la boîte : [x_min, y_min, x_max, y_max]
            box_values = [round(i, 2) for i in box.tolist()]

            
            label_name = self.model.config.id2label[label.item()]

            final_results.append({
                "type": label_name,
                "confiance": f"{round(score.item() * 100, 2)}%",
                "coords": {
                    "xmin": box_values[0],
                    "ymin": box_values[1],
                    "xmax": box_values[2],
                    "ymax": box_values[3]
                }
            })

        return final_results

    def extract_tables(self, image_path, output_folder="data/outputs"):
        """Découpe les tableaux détectés et les enregistre séparément."""
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        predictions = self.predict(image_path)
        image_originale = Image.open(image_path).convert("RGB")
        
        extracted_paths = []
        base_name = os.path.basename(image_path).split('.')[0]

        for i, det in enumerate(predictions):
            box = det['coords']
            # Crop : (left, top, right, bottom)
            table_img = image_originale.crop((box['xmin'], box['ymin'], box['xmax'], box['ymax']))
            
            save_path = os.path.join(output_folder, f"{base_name}_table_{i}.jpg")
            table_img.save(save_path)
            extracted_paths.append(save_path)
            
        return extracted_paths

import cv2
import numpy as np
from PIL import Image

FABRIC_CATEGORIES = [
    "silk-like",
    "cotton-like",
    "velvet-like",
    "net",
    "georgette-like",
    "satin-like",
    "brocade-like"
]

def classify_fabric_and_style(image_path: str):
    """
    Analyze image texture features (specular highlights, edge variance, color standard deviation)
    to categorize fabric type and embroidery visual style.
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            pil_img = Image.open(image_path).convert('RGB')
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Calculate texture features
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()  # Edge richness / embroidery density
        std_dev = np.std(gray)  # Contrast / sheen
        mean_val = np.mean(gray)

        # High sheen + high contrast = silk or satin
        if std_dev > 65 and laplacian_var > 400:
            fabric = "silk-like"
            confidence = 0.88
        elif std_dev > 75 and laplacian_var > 800:
            fabric = "brocade-like"
            confidence = 0.84
        elif laplacian_var < 150:
            fabric = "georgette-like"
            confidence = 0.81
        elif std_dev < 40 and mean_val < 100:
            fabric = "velvet-like"
            confidence = 0.79
        elif std_dev < 45:
            fabric = "cotton-like"
            confidence = 0.82
        else:
            fabric = "silk-like"
            confidence = 0.85

        # Infer style
        if laplacian_var > 600:
            style = "Heavy Zari"
        elif laplacian_var > 350:
            style = "Floral"
        elif laplacian_var > 200:
            style = "Peacock"
        else:
            style = "Minimalistic"

        return {
            "fabric": fabric,
            "confidence": confidence,
            "style": style
        }

    except Exception as e:
        print(f"Fabric classification fallback: {e}")
        return {
            "fabric": "silk-like",
            "confidence": 0.80,
            "style": "Floral"
        }


def calculate_fabric_compatibility(garment_fabric: str, suitable_fabrics: list):
    """Calculate fabric suitability match score (0.0 to 100.0)."""
    if not suitable_fabrics:
        return 80.0

    garment_fab = garment_fabric.lower().strip()
    suitable_list = [f.lower().strip() for f in suitable_fabrics]

    if garment_fab in suitable_list:
        return 100.0

    # Cross-compatibility rules
    silk_family = ["silk-like", "satin-like", "brocade-like"]
    sheer_family = ["georgette-like", "net", "chiffon"]

    if garment_fab in silk_family and any(sf in suitable_list for sf in silk_family):
        return 90.0

    if garment_fab in sheer_family and any(sf in suitable_list for sf in sheer_family):
        return 85.0

    return 70.0


def calculate_style_compatibility(garment_style: str, design_style: str, category: str = None):
    """Calculate style compatibility match score (0.0 to 100.0)."""
    if not garment_style or not design_style:
        return 85.0

    g_style = garment_style.lower()
    d_style = design_style.lower()

    if g_style == d_style:
        return 100.0

    # Harmonious style pairings
    if "zari" in d_style and g_style in ["traditional", "heavy zari", "bridal"]:
        return 95.0

    if "floral" in d_style or "peacock" in d_style or "paisley" in d_style:
        return 90.0

    return 80.0

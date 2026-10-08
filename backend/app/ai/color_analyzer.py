import numpy as np
import cv2
from PIL import Image
from sklearn.cluster import KMeans
import math

COLOR_PALETTE_MAP = [
    {"name": "Maroon", "hex": "#800000", "rgb": (128, 0, 32)},
    {"name": "Dark Wine / Maroon", "hex": "#58111A", "rgb": (88, 17, 26)},
    {"name": "Crimson Red", "hex": "#DC143C", "rgb": (210, 25, 45)},
    {"name": "Coral / Orange-Red", "hex": "#FF7F50", "rgb": (240, 95, 50)},
    {"name": "Rust / Copper", "hex": "#B87333", "rgb": (165, 75, 45)},
    {"name": "Magenta / Rani Pink", "hex": "#FF007F", "rgb": (215, 15, 120)},
    {"name": "Deep Rose Pink", "hex": "#E05286", "rgb": (220, 85, 135)},
    {"name": "Baby Pink", "hex": "#FFC0CB", "rgb": (250, 185, 195)},
    {"name": "Peach", "hex": "#FFDAB9", "rgb": (255, 190, 160)},
    {"name": "Gold Zari", "hex": "#D4AF37", "rgb": (212, 175, 55)},
    {"name": "Mustard Yellow", "hex": "#E1AD01", "rgb": (225, 173, 1)},
    {"name": "Lemon Yellow", "hex": "#FFF44F", "rgb": (245, 230, 80)},
    {"name": "Emerald Green", "hex": "#50C878", "rgb": (35, 160, 85)},
    {"name": "Bottle Green", "hex": "#006A4E", "rgb": (10, 80, 50)},
    {"name": "Olive Green", "hex": "#808000", "rgb": (105, 125, 40)},
    {"name": "Mint Green", "hex": "#98FF98", "rgb": (150, 220, 170)},
    {"name": "Royal Blue", "hex": "#4169E1", "rgb": (30, 70, 200)},
    {"name": "Navy Blue", "hex": "#000080", "rgb": (10, 25, 80)},
    {"name": "Sky Blue", "hex": "#87CEEB", "rgb": (135, 206, 235)},
    {"name": "Teal / Peacock Blue", "hex": "#008080", "rgb": (0, 128, 128)},
    {"name": "Purple / Violet", "hex": "#800080", "rgb": (120, 30, 140)},
    {"name": "Lavender", "hex": "#E6E6FA", "rgb": (180, 140, 210)},
    {"name": "Brown / Chocolate", "hex": "#7B3F00", "rgb": (90, 45, 25)},
    {"name": "Cream / Ivory", "hex": "#FFFDD0", "rgb": (245, 235, 205)},
    {"name": "Pure White", "hex": "#FFFFFF", "rgb": (255, 255, 255)},
    {"name": "Silver Zari", "hex": "#C0C0C0", "rgb": (192, 192, 192)},
    {"name": "Charcoal Grey", "hex": "#36454F", "rgb": (70, 70, 70)},
    {"name": "Black", "hex": "#1A1A1A", "rgb": (20, 20, 20)},
]

def rgb_to_lab(rgb):
    """Convert RGB tuple (0-255) to CIE LAB color space."""
    r, g, b = [x / 255.0 for x in rgb]
    
    def pivot(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = pivot(r), pivot(g), pivot(b)

    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    x /= 0.95047
    y /= 1.00000
    z /= 1.08883

    def f(t):
        return t ** (1/3) if t > 0.008856 else (7.787 * t) + (16 / 116)

    fx, fy, fz = f(x), f(y), f(z)

    L = (116 * fy) - 16
    a = 500 * (fx - fy)
    b_val = 200 * (fy - fz)
    return L, a, b_val


def color_distance_lab(lab1, lab2):
    """Euclidean distance in CIE LAB space (perceptual Delta E)."""
    return math.sqrt((lab1[0] - lab2[0])**2 + (lab1[1] - lab2[1])**2 + (lab1[2] - lab2[2])**2)


def get_closest_color_info(rgb):
    """Find closest standard color name, hex, and RGB tuple."""
    lab = rgb_to_lab(rgb)
    min_dist = float('inf')
    best_match = COLOR_PALETTE_MAP[0]

    for item in COLOR_PALETTE_MAP:
        item_lab = rgb_to_lab(item["rgb"])
        dist = color_distance_lab(lab, item_lab)
        if dist < min_dist:
            min_dist = dist
            best_match = item

    return best_match["name"], best_match["hex"], best_match["rgb"]


def extract_dominant_colors(image_path: str, k: int = 4):
    """
    Dynamically extract dominant colors from a garment or embroidery image using K-Means clustering.
    Deduplicates identical color names automatically into merged percentage chips.
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            pil_img = Image.open(image_path).convert('RGB')
            image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        h, w, _ = image.shape
        cy, cx = h // 2, w // 2
        rh, rw = int(h * 0.4), int(w * 0.4)
        roi = image[max(0, cy - rh):min(h, cy + rh), max(0, cx - rw):min(w, cx + rw)]
        
        resized = cv2.resize(roi, (150, 150), interpolation=cv2.INTER_AREA)
        pixels = resized.reshape(-1, 3)

        # Filter out plain black background (<20) if image has non-black motif colors
        non_bg_pixels = [p for p in pixels if not (p[0] < 22 and p[1] < 22 and p[2] < 22)]
        if len(non_bg_pixels) > 100:
            pixels = np.array(non_bg_pixels)

        kmeans = KMeans(n_clusters=min(k, len(pixels)), random_state=42, n_init=5)
        kmeans.fit(pixels)

        counts = np.bincount(kmeans.labels_)
        total = sum(counts)

        raw_results = []
        for i in range(len(counts)):
            center = kmeans.cluster_centers_[i]
            rgb = tuple(int(c) for c in center)
            name, hex_code, std_rgb = get_closest_color_info(rgb)
            percentage = round((counts[i] / total) * 100, 1)

            raw_results.append({
                "name": name,
                "hex": hex_code,
                "rgb": rgb,
                "percentage": percentage
            })

        # DEDUPLICATE CLUSTERS BY NAME
        merged_map = {}
        for r in raw_results:
            name = r["name"]
            if name in merged_map:
                merged_map[name]["percentage"] = round(merged_map[name]["percentage"] + r["percentage"], 1)
            else:
                merged_map[name] = r

        results = list(merged_map.values())
        results.sort(key=lambda x: x["percentage"], reverse=True)
        return results

    except Exception as e:
        print(f"Error in extract_dominant_colors: {e}")
        return [
            {"name": "Maroon", "hex": "#800000", "rgb": (128, 0, 0), "percentage": 75.0},
            {"name": "Gold Zari", "hex": "#D4AF37", "rgb": (212, 175, 55), "percentage": 25.0}
        ]


def calculate_deep_palette_harmony(garment_colors: list, design_colors: list):
    """
    DEEP DYNAMIC COLOR MATCHING ENGINE:
    Evaluates pairwise CIE LAB perceptual distance between garment colors and design motif colors.
    Returns dynamic color harmony score (30.0 - 98.0) reflecting true garment color contrast.
    """
    if not garment_colors or not design_colors:
        return 70.0, {"blouse_primary": "garment", "design_accent": "embroidery", "delta_e": 35.0, "delta_l": 25.0}

    # Extract garment LAB colors
    garment_labs = []
    garment_names = []
    for gc in garment_colors[:3]:
        rgb = gc.get("rgb", (128, 0, 0)) if isinstance(gc, dict) else (128, 0, 0)
        name = gc.get("name", "Blouse Base") if isinstance(gc, dict) else str(gc)
        garment_labs.append((rgb_to_lab(rgb), name, gc.get("percentage", 50.0) if isinstance(gc, dict) else 50.0))
        garment_names.append(name.lower())

    blouse_primary_lab, blouse_primary_name, _ = garment_labs[0]

    # Extract design motif LAB colors (ignore pure black framing if other colors exist)
    design_labs = []
    design_names = []
    for dc in design_colors:
        name = dc.get("name", "") if isinstance(dc, dict) else str(dc)
        rgb = dc.get("rgb", (212, 175, 55)) if isinstance(dc, dict) else (212, 175, 55)
        if name.lower() != "black" or len(design_colors) == 1:
            design_labs.append((rgb_to_lab(rgb), name))
            design_names.append(name.lower())

    if not design_labs:
        design_labs = [(rgb_to_lab(design_colors[0].get("rgb", (212, 175, 55))), design_colors[0].get("name", "Gold Zari"))]
        design_names = [design_colors[0].get("name", "Gold Zari").lower()]

    # Calculate LAB perceptual distances
    delta_es = []
    delta_ls = []
    for d_lab, d_name in design_labs:
        de = color_distance_lab(blouse_primary_lab, d_lab)
        dl = abs(blouse_primary_lab[0] - d_lab[0])
        delta_es.append(de)
        delta_ls.append(dl)

    avg_delta_e = float(np.mean(delta_es)) if delta_es else 40.0
    max_delta_l = float(np.max(delta_ls)) if delta_ls else 30.0

    # BASE DYNAMIC SCORE CALCULATION
    # Range 45 to 80 based on CIE LAB perceptual contrast
    if 35 <= avg_delta_e <= 80:
        base_score = 62.0 + (avg_delta_e - 35) * 0.35
    elif avg_delta_e > 80:
        base_score = 78.0 + min(10.0, (avg_delta_e - 80) * 0.2)
    else:  # avg_delta_e < 35 (low contrast penalty)
        base_score = 40.0 + (avg_delta_e * 0.6)

    score = base_score

    # Metallic Accent Bonus (Gold Zari / Silver Zari)
    has_zari = any("zari" in n or "gold" in n or "silver" in n for n in design_names)
    if has_zari:
        score += 10.0

    is_dark_blouse = blouse_primary_lab[0] < 42
    is_pastel_blouse = blouse_primary_lab[0] > 68
    primary_b_name = blouse_primary_name.lower()

    # GARMENT SPECIFIC HARMONY MATRIX
    if is_dark_blouse:
        # Dark Blouse (Black, Navy, Dark Green, Dark Maroon) needs high lightness motif pop
        if any(dl > 35 for dl in delta_ls) or has_zari:
            score += 12.0
        else:
            score -= 22.0  # Dark motif on dark blouse penalty

    elif "pink" in primary_b_name or "magenta" in primary_b_name:
        if any(x in ["emerald green", "bottle green", "gold zari", "royal blue", "mint green"] for x in design_names):
            score += 16.0
        elif any(x in ["charcoal grey", "black"] for x in design_names) and not has_zari:
            score -= 18.0

    elif "maroon" in primary_b_name or "red" in primary_b_name or "wine" in primary_b_name:
        if any(x in ["gold zari", "emerald green", "mustard yellow", "royal blue", "silver zari"] for x in design_names):
            score += 16.0
        elif any(x in ["black"] for x in design_names) and not has_zari:
            score -= 20.0

    elif "yellow" in primary_b_name or "gold" in primary_b_name:
        if any(x in ["crimson red", "magenta / rani pink", "bottle green", "maroon", "royal blue"] for x in design_names):
            score += 16.0
        elif any(x in ["cream / ivory", "lemon yellow"] for x in design_names):
            score -= 15.0

    elif "green" in primary_b_name:
        if any(x in ["magenta / rani pink", "crimson red", "gold zari", "mustard yellow", "coral / orange-red"] for x in design_names):
            score += 16.0

    elif "blue" in primary_b_name:
        if any(x in ["magenta / rani pink", "coral / orange-red", "gold zari", "silver zari", "crimson red"] for x in design_names):
            score += 16.0

    final_score = round(min(98.0, max(30.0, score)), 1)

    analysis_details = {
        "blouse_primary": blouse_primary_name,
        "design_accent": ", ".join([d[1] for d in design_labs[:2]]),
        "delta_e": round(avg_delta_e, 1),
        "delta_l": round(max_delta_l, 1),
        "has_zari": has_zari,
        "is_dark_blouse": is_dark_blouse,
        "is_pastel_blouse": is_pastel_blouse
    }

    return final_score, analysis_details


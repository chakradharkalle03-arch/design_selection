"""
Pre-download and verify script for local CLIP AI Model.
Run this script to download model weights before starting the application,
or run_app launchers will execute it automatically.
"""
import sys
import os
from pathlib import Path

# Fix Windows console encoding for all code pages (cp950, cp1252, etc.)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure backend directory is in path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.config import MODEL_NAME, STORAGE_DIR

def download_and_verify_model():
    print("=" * 65)
    print("  ZariVision AI - Local CLIP Model Downloader & Verification")
    print("=" * 65)
    print(f"[1/3] Target Model: '{MODEL_NAME}'")
    print(f"[2/3] Downloading model weights directly from HuggingFace to local cache...")
    print("      (Approx ~600MB. Required only once, works 100% offline afterwards).")
    
    try:
        import torch
        from transformers import CLIPProcessor, CLIPModel
        from PIL import Image

        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"      Detected hardware device: '{device.upper()}'")

        # Load & cache model and processor
        processor = CLIPProcessor.from_pretrained(MODEL_NAME)
        model = CLIPModel.from_pretrained(MODEL_NAME)
        model.to(device)
        model.eval()

        print("[3/3] Running verification test with dummy tensor...")
        # Verify vision features
        dummy_img = Image.new("RGB", (224, 224), color=(200, 50, 100))
        img_inputs = processor(images=dummy_img, return_tensors="pt")
        if device != "cpu":
            img_inputs = {k: v.to(device) for k, v in img_inputs.items()}

        with torch.no_grad():
            img_out = model.get_image_features(**img_inputs)
            feats = img_out.pooler_output if getattr(img_out, "pooler_output", None) is not None else (img_out[0] if isinstance(img_out, (tuple, list)) else img_out)
            feats = feats / feats.norm(p=2, dim=-1, keepdim=True)

        # Verify text features
        txt_inputs = processor(text=["traditional Indian silk embroidery blouse"], return_tensors="pt", padding=True)
        if device != "cpu":
            txt_inputs = {k: v.to(device) for k, v in txt_inputs.items()}

        with torch.no_grad():
            txt_out = model.get_text_features(**txt_inputs)
            txt_feats = txt_out.pooler_output if getattr(txt_out, "pooler_output", None) is not None else (txt_out[0] if isinstance(txt_out, (tuple, list)) else txt_out)
            txt_feats = txt_feats / txt_feats.norm(p=2, dim=-1, keepdim=True)

        similarity = (feats @ txt_feats.T).item()

        print("-" * 65)
        print(f"[SUCCESS] Model '{MODEL_NAME}' is ready!")
        print(f"          Visual Embedding Shape: {list(feats.shape)}")
        print(f"          Text Embedding Shape:   {list(txt_feats.shape)}")
        print(f"          Test Cosine Similarity: {similarity:.4f}")
        print("          All embeddings will run 100% locally and offline.")
        print("=" * 65)
        return True

    except Exception as e:
        print(f"[ERROR] Model download or verification failed: {e}")
        print("Please check your internet connection for the initial download.")
        return False

if __name__ == "__main__":
    success = download_and_verify_model()
    sys.exit(0 if success else 1)

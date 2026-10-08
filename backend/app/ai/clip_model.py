import os
import numpy as np
from PIL import Image
from app.config import MODEL_NAME, HF_TOKEN, LOW_MEMORY_MODE

class CLIPEmbeddingEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CLIPEmbeddingEngine, cls).__new__(cls)
            cls._instance._model = None
            cls._instance._processor = None
            cls._instance._torch = None
            cls._instance._is_loaded = False
        return cls._instance

    def load_model(self):
        """Lazy loader for CLIP vision & text model."""
        if self._is_loaded:
            return

        if LOW_MEMORY_MODE:
            print("Low Memory Mode enabled (512MB RAM Optimization). Using fast visual feature embedding engine.")
            self._is_loaded = False
            return

        try:
            print(f"Loading HuggingFace CLIP model: {MODEL_NAME}...")
            import torch
            from transformers import CLIPProcessor, CLIPModel

            self._torch = torch
            token = HF_TOKEN if HF_TOKEN and not HF_TOKEN.startswith("your_") else None
            
            self._processor = CLIPProcessor.from_pretrained(MODEL_NAME, token=token)
            self._model = CLIPModel.from_pretrained(MODEL_NAME, token=token)
            self._model.eval()
            self._is_loaded = True
            print("CLIP model loaded successfully for vision & text matching.")
        except Exception as e:
            print(f"Warning: Could not load HuggingFace CLIP model ({e}). Using feature embedding fallback.")
            self._is_loaded = False

    def generate_image_embedding(self, image_path: str) -> list:
        """Generate normalized 512-dim embedding for an image."""
        try:
            self.load_model()
            if self._is_loaded and self._model is not None and self._processor is not None and self._torch is not None:
                image = Image.open(image_path).convert("RGB")
                inputs = self._processor(images=image, return_tensors="pt")
                with self._torch.no_grad():
                    output = self._model.get_image_features(**inputs)
                    
                    if hasattr(output, "image_embeds"):
                        feats = output.image_embeds
                    elif hasattr(output, "pooler_output"):
                        feats = output.pooler_output
                    elif isinstance(output, self._torch.Tensor):
                        feats = output
                    else:
                        feats = output[0]

                    feats = feats / feats.norm(p=2, dim=-1, keepdim=True)
                    embedding = feats.squeeze().cpu().numpy().tolist()
                    return [float(x) for x in embedding]
        except Exception as e:
            print(f"Error during CLIP image inference: {e}. Falling back.")

        return self._generate_fallback_embedding(image_path)

    def generate_text_embedding(self, text_prompt: str) -> list:
        """Generate normalized 512-dim text embedding for custom customer requirements."""
        if not text_prompt or not text_prompt.strip():
            return []

        try:
            self.load_model()
            if self._is_loaded and self._model is not None and self._processor is not None and self._torch is not None:
                inputs = self._processor(text=[text_prompt], return_tensors="pt", padding=True)
                with self._torch.no_grad():
                    output = self._model.get_text_features(**inputs)
                    
                    if hasattr(output, "text_embeds"):
                        feats = output.text_embeds
                    elif hasattr(output, "pooler_output"):
                        feats = output.pooler_output
                    elif isinstance(output, self._torch.Tensor):
                        feats = output
                    else:
                        feats = output[0]

                    feats = feats / feats.norm(p=2, dim=-1, keepdim=True)
                    embedding = feats.squeeze().cpu().numpy().tolist()
                    return [float(x) for x in embedding]
        except Exception as e:
            print(f"Error generating text embedding: {e}")

        # Basic keyword fallback vector
        vec = np.zeros(512, dtype=np.float32)
        vec[0] = 1.0
        return vec.tolist()

    def _generate_fallback_embedding(self, image_path: str) -> list:
        """Create normalized 512-element visual feature vector using PIL + NumPy."""
        try:
            img = Image.open(image_path).convert("RGB").resize((64, 64))
            arr = np.array(img, dtype=np.float32) / 255.0
            
            r_hist, _ = np.histogram(arr[:, :, 0], bins=64, range=(0, 1))
            g_hist, _ = np.histogram(arr[:, :, 1], bins=64, range=(0, 1))
            b_hist, _ = np.histogram(arr[:, :, 2], bins=64, range=(0, 1))
            
            spatial = arr[::4, ::4, :].flatten()[:256]

            features = np.concatenate([r_hist, g_hist, b_hist, spatial])
            if len(features) < 512:
                features = np.pad(features, (0, 512 - len(features)))
            else:
                features = features[:512]

            norm = np.linalg.norm(features)
            if norm > 0:
                features = features / norm

            return [float(x) for x in features]
        except Exception as e:
            print(f"Fallback embedding generation error: {e}")
            vec = np.zeros(512, dtype=np.float32)
            vec[0] = 1.0
            return vec.tolist()

clip_engine = CLIPEmbeddingEngine()

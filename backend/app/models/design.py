import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from app.database.database import Base

class Design(Base):
    __tablename__ = "designs"

    id = Column(Integer, primary_key=True, index=True)
    design_code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    image_url = Column(String(255), nullable=False)
    category = Column(String(50), default="Traditional", index=True)
    style = Column(String(50), default="Floral", index=True)
    colors_json = Column(Text, default="[]")  # JSON list of color dicts or strings
    fabric_suitable_json = Column(Text, default="[]")  # JSON list of suitable fabrics
    placement = Column(String(50), default="Full Blouse")
    description = Column(Text, nullable=True)
    embedding_json = Column(Text, nullable=True)  # Pre-computed float embedding array
    created_at = Column(DateTime, default=datetime.utcnow)

    @property
    def colors(self):
        try:
            return json.loads(self.colors_json or "[]")
        except Exception:
            return []

    @colors.setter
    def colors(self, val):
        self.colors_json = json.dumps(val)

    @property
    def fabric_suitable(self):
        try:
            return json.loads(self.fabric_suitable_json or "[]")
        except Exception:
            return []

    @fabric_suitable.setter
    def fabric_suitable(self, val):
        self.fabric_suitable_json = json.dumps(val)

    @property
    def embedding(self):
        try:
            return json.loads(self.embedding_json or "[]") if self.embedding_json else []
        except Exception:
            return []

    @embedding.setter
    def embedding(self, val):
        self.embedding_json = json.dumps(val)


class GarmentUpload(Base):
    __tablename__ = "garment_uploads"

    id = Column(String(100), primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    image_url = Column(String(255), nullable=False)
    garment_type = Column(String(50), default="blouse")
    colors_json = Column(Text, default="[]")
    fabric = Column(String(50), default="silk-like")
    style = Column(String(50), default="traditional")
    embedding_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    @property
    def colors(self):
        try:
            return json.loads(self.colors_json or "[]")
        except Exception:
            return []

    @colors.setter
    def colors(self, val):
        self.colors_json = json.dumps(val)

    @property
    def embedding(self):
        try:
            return json.loads(self.embedding_json or "[]") if self.embedding_json else []
        except Exception:
            return []

    @embedding.setter
    def embedding(self, val):
        self.embedding_json = json.dumps(val)


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    design_code = Column(String(50), index=True)
    rating = Column(String(20))  # "like" or "dislike"
    reason = Column(String(100), nullable=True)  # e.g., "Color mismatch", "Too heavy"
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

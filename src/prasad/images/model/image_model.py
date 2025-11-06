# models.py
from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional
from enum import Enum


class ImageReason(str, Enum):
    PROFILE = "profile"



class ImageModel(Document):
    image_url: str
    reason: ImageReason
    original_filename: str
    stored_filename: str
    file_path: str
    content_type: str
    size: int
    uploaded_at: datetime = Field(default_factory=datetime.now)
    metadata: dict = Field(default_factory=dict)

    class Settings:
        name = "images"
        use_state_management = True

    class Config:
        schema_extra = {
            "example": {
                "image_url": "/uploads/product/product_12345.jpg",
                "reason": "product",
                "original_filename": "product.jpg",
                "stored_filename": "product_12345.jpg",
                "file_path": "uploads/product/product_12345.jpg",
                "content_type": "image/jpeg",
                "size": 1024000,
                "metadata": {"user_id": "123", "product_id": "456"}
            }
        }
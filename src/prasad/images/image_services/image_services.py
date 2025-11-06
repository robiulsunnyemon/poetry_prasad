# app/images/image_services/image_services.py
import os
import shutil
from datetime import datetime
from typing import Any, Coroutine

from fastapi import HTTPException, UploadFile
from prasad.images.model.image_model import ImageModel, ImageReason
import uuid


class ImageService:
    def __init__(self):
        self.base_upload_dir = "uploads"
        self.setup_directories()

    def setup_directories(self):
        """Create necessary directories"""
        directories = [
            self.base_upload_dir,
            os.path.join(self.base_upload_dir, "profile"),
            os.path.join(self.base_upload_dir, "product"),
            os.path.join(self.base_upload_dir, "category")
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    async def validate_image(self, file: UploadFile, max_size_mb: int = 5):
        """Validate uploaded image"""
        if not file.content_type.startswith('image/'):
            raise HTTPException(400, "Only image files are allowed")

        allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
        if file.content_type not in allowed_types:
            raise HTTPException(400, f"Allowed formats: {', '.join(allowed_types)}")

        # Check file size
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > max_size_mb * 1024 * 1024:
            raise HTTPException(400, f"File size exceeds {max_size_mb}MB")

        return file_size

    def generate_filename(self, original_filename: str, reason: ImageReason) -> str:
        """Generate unique filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        file_extension = os.path.splitext(original_filename)[1]

        return f"{reason.value}_{timestamp}_{unique_id}{file_extension}"

    async def save_image(self, file: UploadFile, reason: ImageReason, metadata: dict = None) -> ImageModel:
        """Save image and return Image document"""
        try:
            # Validate image
            file_size = await self.validate_image(file)

            # Generate unique filename
            stored_filename = self.generate_filename(file.filename, reason)

            # Determine upload directory based on reason
            upload_dir = os.path.join(self.base_upload_dir, reason.value)
            file_path = os.path.join(upload_dir, stored_filename)
            image_url = f"/uploads/{reason.value}/{stored_filename}"

            # Save file to appropriate folder
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Create Image document
            image_data = {
                "image_url": image_url,
                "reason": reason,
                "original_filename": file.filename,
                "stored_filename": stored_filename,
                "file_path": file_path,
                "content_type": file.content_type,
                "size": file_size,
                "metadata": metadata or {}
            }

            image = ImageModel(**image_data)
            await image.insert()

            return image

        except Exception as e:
            # Clean up file if database operation fails
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(500, f"Image upload failed: {str(e)}")

    async def get_images_by_reason(self, reason: ImageReason, skip: int = 0, limit: int = 50):
        """Get images by reason"""
        return await ImageModel.find(ImageModel.reason == reason).skip(skip).limit(limit).to_list()

    async def get_image_by_id(self, image_id: str):
        """Get image by ID"""
        return await ImageModel.get(image_id)

    async def delete_image(self, image_id: str):
        """Delete image and file"""
        image = await ImageModel.get(image_id)
        if not image:
            raise HTTPException(404, "Image not found")

        # Delete physical file
        if os.path.exists(image.file_path):
            os.remove(image.file_path)

        # Delete from database
        await image.delete()

        return {"message": "Image deleted successfully"}




    async def save_image_from_api(self, file: UploadFile, reason: ImageReason, metadata: dict = None) -> str:
        """Save image and return Image document"""
        try:
            # Validate image
            file_size = await self.validate_image(file)

            # Generate unique filename
            stored_filename = self.generate_filename(file.filename, reason)

            # Determine upload directory based on reason
            upload_dir = os.path.join(self.base_upload_dir, reason.value)
            file_path = os.path.join(upload_dir, stored_filename)
            image_url = f"/uploads/{reason.value}/{stored_filename}"

            # Save file to appropriate folder
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Create Image document
            image_data = {
                "image_url": image_url,
                "reason": reason,
                "original_filename": file.filename,
                "stored_filename": stored_filename,
                "file_path": file_path,
                "content_type": file.content_type,
                "size": file_size,
                "metadata": metadata or {}
            }

            image = ImageModel(**image_data)
            await image.insert()

            return image.image_url

        except Exception as e:
            # Clean up file if database operation fails
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(500, f"Image upload failed: {str(e)}")


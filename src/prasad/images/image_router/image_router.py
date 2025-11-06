# app/images/image_router/image_router.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Query
from typing import Optional, List
import os

from prasad.images.model.image_model import ImageModel, ImageReason
from prasad.images.image_services.image_services import ImageService

router = APIRouter(prefix="/api/v1/images", tags=["Images"])
image_service = ImageService()


@router.post("/upload/")
async def upload_image(
        reason: ImageReason = Form(...),
        file: UploadFile = File(...),
        user_id: Optional[str] = Form(None),
        product_id: Optional[str] = Form(None),
        category_id: Optional[str] = Form(None)
):
    """Upload image with specific reason"""
    try:
        # Prepare metadata
        metadata = {}
        if user_id:
            metadata["user_id"] = user_id
        if product_id:
            metadata["product_id"] = product_id
        if category_id:
            metadata["category_id"] = category_id

        # Save image
        image = await image_service.save_image(file, reason, metadata)

        return {
            "message": "Image uploaded successfully",
            "image_id": str(image.id),
            "image_url": image.image_url,
            "reason": image.reason,
            "filename": image.stored_filename,
            "size": image.size
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Upload failed: {str(e)}")


@router.post("/upload-multiple/")
async def upload_multiple_images(
        files: List[UploadFile] = File(...),
        reason: ImageReason = Form(...),
        user_id: Optional[str] = Form(None)
):
    """Upload multiple images with same reason"""
    results = []

    for file in files:
        try:
            metadata = {"user_id": user_id} if user_id else {}
            image = await image_service.save_image(file, reason, metadata)

            results.append({
                "filename": file.filename,
                "status": "success",
                "image_id": str(image.id),
                "image_url": image.image_url
            })

        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "failed",
                "error": str(e)
            })

    return {
        "message": "Multiple upload completed",
        "results": results
    }


@router.get("/")
async def get_images(
        reason: Optional[ImageReason] = Query(None),
        skip: int = Query(0, ge=0),
        limit: int = Query(50, ge=1, le=100)
):
    """Get all images with optional filtering by reason"""
    try:
        if reason:
            images = await image_service.get_images_by_reason(reason, skip, limit)
            total = await ImageModel.find(ImageModel.reason == reason).count()
        else:
            images = await ImageModel.find().skip(skip).limit(limit).to_list()
            total = await ImageModel.find().count()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "images": [
                {
                    "id": str(img.id),
                    "image_url": img.image_url,
                    "reason": img.reason,
                    "original_filename": img.original_filename,
                    "size": img.size,
                    "uploaded_at": img.uploaded_at.isoformat(),
                    "metadata": img.metadata
                }
                for img in images
            ]
        }

    except Exception as e:
        raise HTTPException(500, f"Error fetching images: {str(e)}")


@router.get("/{image_id}")
async def get_image(image_id: str):
    """Get specific image details"""
    try:
        image = await image_service.get_image_by_id(image_id)
        if not image:
            raise HTTPException(404, "Image not found")

        return {
            "id": str(image.id),
            "image_url": image.image_url,
            "reason": image.reason,
            "original_filename": image.original_filename,
            "stored_filename": image.stored_filename,
            "file_path": image.file_path,
            "content_type": image.content_type,
            "size": image.size,
            "uploaded_at": image.uploaded_at.isoformat(),
            "metadata": image.metadata
        }

    except Exception as e:
        raise HTTPException(500, f"Error fetching image: {str(e)}")


@router.get("/{image_id}/file")
async def get_image_file(image_id: str):
    """Serve image file"""
    try:
        image = await image_service.get_image_by_id(image_id)
        if not image:
            raise HTTPException(404, "Image not found")

        if not os.path.exists(image.file_path):
            raise HTTPException(404, "Image file not found")

        from fastapi.responses import FileResponse
        return FileResponse(
            path=image.file_path,
            filename=image.original_filename,
            media_type=image.content_type
        )

    except Exception as e:
        raise HTTPException(500, f"Error serving file: {str(e)}")


@router.delete("/{image_id}")
async def delete_image(image_id: str):
    """Delete image"""
    try:
        result = await image_service.delete_image(image_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error deleting image: {str(e)}")


@router.get("/stats/overview")
async def get_stats():
    """Get image upload statistics"""
    try:
        total_images = await ImageModel.find().count()
        profile_count = await ImageModel.find(ImageModel.reason == ImageReason.PROFILE).count()
        product_count = await ImageModel.find(ImageModel.reason == ImageReason.PRODUCT).count()
        category_count = await ImageModel.find(ImageModel.reason == ImageReason.CATEGORY).count()

        return {
            "total_images": total_images,
            "by_reason": {
                "profile": profile_count,
                "product": product_count,
                "category": category_count
            }
        }

    except Exception as e:
        raise HTTPException(500, f"Error getting stats: {str(e)}")








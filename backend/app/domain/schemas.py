from pydantic import BaseModel
from typing import Optional, List

class FaceMatch(BaseModel):
    similarity: float
    face_id: Optional[str] = None
    bounding_box: dict
    confidence: float
    pose: dict
    quality: dict
    landmarks: List[dict]

class UnmatchedFace(BaseModel):
    face_id: Optional[str] = None
    bounding_box: dict
    confidence: float
    pose: dict
    quality: dict
    landmarks: List[dict]

class CompareFacesResponse(BaseModel):
    face_matches: Optional[List[FaceMatch]] = None
    unmatched_faces: Optional[List[UnmatchedFace]] = None
    source_image_face: Optional[dict] = None
    target_image_face: Optional[dict] = None
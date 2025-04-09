from infrastructure.rekognition_service import RekognitionServiceFactory
from domain.schemas import CompareFacesResponse, FaceMatch, UnmatchedFace

class FaceComparisonService:
    def __init__(self, rekognition_service=None):
        self.rekognition_service = rekognition_service or RekognitionServiceFactory.create()

    def compare(self, image1_bytes: bytes, image2_bytes: bytes) -> CompareFacesResponse:
        if image1_bytes is None or image2_bytes is None:
            raise ValueError("Image bytes cannot be None")

        try:
            rekognize_response = self.rekognition_service.compare_faces(image1_bytes, image2_bytes)
            if rekognize_response is None:
                raise ValueError("Rekognition service returned None")

            response = CompareFacesResponse()

            if 'FaceMatches' in rekognize_response:
                response.face_matches = [
                    FaceMatch(
                        similarity=match['Similarity'],
                        face_id=None,  # Face ID is not present in the response
                        bounding_box=match['Face']['BoundingBox'],
                        confidence=match['Face']['Confidence'],
                        pose=match['Face']['Pose'],
                        quality=match['Face']['Quality'],
                        landmarks=match['Face']['Landmarks']
                    )
                    for match in rekognize_response['FaceMatches']
                ]

            if 'UnmatchedFaces' in rekognize_response:
                response.unmatched_faces = [
                    UnmatchedFace(
                        face_id=None,  # Face ID is not present in the response
                        bounding_box=face['BoundingBox'],
                        confidence=face['Confidence'],
                        pose=face['Pose'],
                        quality=face['Quality'],
                        landmarks=face['Landmarks']
                    )
                    for face in rekognize_response['UnmatchedFaces']
                ]

            return response
        except Exception as e:
            raise ValueError(f"Error comparing faces: {e}")
import streamlit as st
import requests
from PIL import Image
import io

BACKEND_URL = "http://localhost:8000/api/v1/compare_faces/compare"  # Adjust if your backend runs on a different URL
MAX_IMAGE_SIZE_MB = 5
MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024

st.title("Face Comparison using Amazon Rekognize")

col1, col2 = st.columns(2)
uploaded_file1 = None
uploaded_file2 = None

with col1:
    uploaded_file1 = st.file_uploader("Upload First Image", type=["jpg", "jpeg", "png"])
    if uploaded_file1 is not None:
        if uploaded_file1.size > MAX_IMAGE_SIZE_BYTES:
            st.error(f"Image 1 size exceeds the limit of {MAX_IMAGE_SIZE_MB}MB. Please upload a smaller image.")
            uploaded_file1 = None  # Reset uploaded file
        else:
            st.subheader("Uploaded Image 1")
            image1 = Image.open(uploaded_file1)
            st.image(image1, use_container_width=True)

with col2:
    uploaded_file2 = st.file_uploader("Upload Second Image", type=["jpg", "jpeg", "png"])
    if uploaded_file2 is not None:
        if uploaded_file2.size > MAX_IMAGE_SIZE_BYTES:
            st.error(f"Image 2 size exceeds the limit of {MAX_IMAGE_SIZE_MB}MB. Please upload a smaller image.")
            uploaded_file2 = None  # Reset uploaded file
        else:
            st.subheader("Uploaded Image 2")
            image2 = Image.open(uploaded_file2)
            st.image(image2, use_container_width=True)

if uploaded_file1 is not None and uploaded_file2 is not None:
    if st.button("Compare Faces"):
        files = {
            "image1": (uploaded_file1.name, uploaded_file1.getvalue(), uploaded_file1.type),
            "image2": (uploaded_file2.name, uploaded_file2.getvalue(), uploaded_file2.type),
        }
        try:
            response = requests.post(BACKEND_URL, files=files)
            response.raise_for_status()  # Raise an exception for bad status codes
            result = response.json()

            if result.get("face_matches"):
                st.subheader("Face Matches:")
                for match in result["face_matches"]:
                    st.write(f"- Similarity: {match['similarity']:.2f}%")
                    st.write(f"  - Confidence: {match['confidence']:.2f}%")
                    st.write(f"  - Bounding Box: {match['bounding_box']}")
            else:
                st.info("No matching faces found with the specified similarity threshold.")

            if result.get("unmatched_faces"):
                st.subheader("Unmatched Faces in Target Image:")
                for face in result["unmatched_faces"]:
                    st.write(f"- Confidence: {face['confidence']:.2f}%")
                    st.write(f"  - Bounding Box: {face['bounding_box']}")

            if result.get("source_image_face"):
                st.subheader("Face Detected in Source Image:")
                st.write(f"- Confidence: {result['source_image_face']['Confidence']:.2f}%")
                st.write(f"- Bounding Box: {result['source_image_face']['BoundingBox']}")

            if result.get("target_image_face"):
                st.subheader("Face Detected in Target Image:")
                st.write(f"- Confidence: {result['target_image_face']['Confidence']:.2f}%")
                st.write(f"- Bounding Box: {result['target_image_face']['BoundingBox']}")

            if not result.get("face_matches") and not result.get("unmatched_faces") and not result.get("source_image_face") and not result.get("target_image_face"):
                st.warning("No faces detected in either image.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the backend: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
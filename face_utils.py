import os
import cv2
import numpy as np
import pickle
from mtcnn import MTCNN
from keras_facenet import FaceNet
from scipy.spatial.distance import cosine

# Initialize MTCNN for face detection
detector = MTCNN()

# Initialize FaceNet for embeddings (returns 512-dim vectors by default in keras-facenet, 
# although original FaceNet was often 128. keras-facenet provides standard pretrained weights)
embedder = FaceNet()

EMBEDDINGS_FILE = "embeddings.pkl"

def get_face(image_path_or_array, target_size=(160, 160)):
    """
    Extracts a face from an image.
    If image_path_or_array is a string, it reads it from disk.
    If it's a numpy array, it assumes it's an RGB image.
    """
    if isinstance(image_path_or_array, str):
        img = cv2.imread(image_path_or_array)
        if img is None:
            return None
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        img = image_path_or_array

    results = detector.detect_faces(img)
    if len(results) == 0:
        return None  # No face detected
    
    # We take the most prominent face (highest confidence or largest bounding box)
    # Typically, MTCNN sorts faces by confidence or size, but let's grab the first one
    x1, y1, width, height = results[0]['box']
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    
    face = img[y1:y2, x1:x2]
    # Resize to the target size required by FaceNet (160x160)
    face = cv2.resize(face, target_size)
    return face

def get_embedding(face_img):
    """
    Takes an already cropped and resized face image (160x160)
    and returns its embedding vector.
    """
    # Expand dimensions to (1, 160, 160, 3) format
    face_img = np.expand_dims(face_img, axis=0)
    embeddings = embedder.embeddings(face_img)
    return embeddings[0]

def train_system(dataset_folder="dataset"):
    """
    Iterates over the dataset folder, detects faces, extracts embeddings, 
    and saves them in a pickle file mapping student names to embeddings.
    """
    student_embeddings = {}
    
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
        print(f"Created {dataset_folder}. Please add student folders with images.")
        return False
    
    for student_name in os.listdir(dataset_folder):
        student_path = os.path.join(dataset_folder, student_name)
        
        if not os.path.isdir(student_path):
            continue
            
        embeddings_list = []
        for img_name in os.listdir(student_path):
            img_path = os.path.join(student_path, img_name)
            
            face = get_face(img_path)
            if face is not None:
                emb = get_embedding(face)
                embeddings_list.append(emb)
        
        if embeddings_list:
            # We take the mean of the embeddings for robustness
            avg_embedding = np.mean(embeddings_list, axis=0)
            student_embeddings[student_name] = avg_embedding
            
    with open(EMBEDDINGS_FILE, 'wb') as f:
        pickle.dump(student_embeddings, f)
        
    print("Training complete. Embeddings saved to", EMBEDDINGS_FILE)
    return True

def recognize_face(image_array, threshold=0.5):
    """
    Takes an RGB image array, detects the face, extracts its embedding,
    and compares it against loaded embeddings using cosine similarity.
    """
    if not os.path.exists(EMBEDDINGS_FILE):
        return None, "No embeddings file. Please train first."
        
    with open(EMBEDDINGS_FILE, 'rb') as f:
        student_embeddings = pickle.load(f)
        
    face = get_face(image_array)
    if face is None:
        return None, "No face detected in the given image."
        
    emb = get_embedding(face)
    
    best_match = None
    min_dist = float('inf')
    
    for student_name, stored_emb in student_embeddings.items():
        # Cosine distance ranges from 0 (identical) to 2 (opposite)
        # Similarity = 1 - distance
        dist = cosine(emb, stored_emb)
        
        if dist < min_dist:
            min_dist = dist
            best_match = student_name
            
    if min_dist < threshold:
        return best_match, min_dist
    else:
        return "Unknown", min_dist

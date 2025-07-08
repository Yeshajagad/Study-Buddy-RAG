from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import pickle
import os

class EmbeddingManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create embeddings for a list of texts"""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings
    
    def create_single_embedding(self, text: str) -> np.ndarray:
        """Create embedding for a single text"""
        embedding = self.model.encode([text], convert_to_numpy=True)
        return embedding[0]
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings"""
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    
    def save_embeddings(self, embeddings: np.ndarray, file_path: str):
        """Save embeddings to file"""
        with open(file_path, 'wb') as f:
            pickle.dump(embeddings, f)
    
    def load_embeddings(self, file_path: str) -> np.ndarray:
        """Load embeddings from file"""
        with open(file_path, 'rb') as f:
            return pickle.load(f)
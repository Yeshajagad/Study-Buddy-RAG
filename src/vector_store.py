import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import uuid
from pathlib import Path

class VectorStore:
    def __init__(self, db_path: str, collection_name: str = "study_buddy"):
        self.db_path = db_path
        self.collection_name = collection_name
        
        # Ensure directory exists
        Path(db_path).mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
    
    def add_documents(self, documents: List[str], metadatas: List[Dict], ids: Optional[List[str]] = None):
        """Add documents to the vector store"""
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query: str, n_results: int = 5) -> Dict:
        """Search for similar documents"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results
    
    def search_with_filter(self, query: str, filter_dict: Dict, n_results: int = 5) -> Dict:
        """Search with metadata filtering"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=filter_dict
        )
        return results
    
    def get_all_documents(self) -> Dict:
        """Get all documents in the collection"""
        return self.collection.get()
    
    def delete_collection(self):
        """Delete the entire collection"""
        self.client.delete_collection(name=self.collection_name)
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection"""
        return self.collection.count()
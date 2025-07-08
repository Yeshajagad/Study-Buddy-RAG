import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # OpenAI API Key (optional, for advanced features)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Embedding Model
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    # Vector Database
    VECTOR_DB_PATH = "data/vector_db"
    COLLECTION_NAME = "study_buddy"
    
    # Document Processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Difficulty Assessment
    DIFFICULTY_LEVELS = {
        "beginner": {"min_score": 0.0, "max_score": 0.3},
        "intermediate": {"min_score": 0.3, "max_score": 0.7},
        "advanced": {"min_score": 0.7, "max_score": 1.0}
    }
    
    # Quiz Generation
    DEFAULT_QUIZ_SIZE = 5
    QUIZ_TYPES = ["multiple_choice", "true_false", "short_answer"]
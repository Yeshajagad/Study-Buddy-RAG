# 📚 Study Buddy RAG - Simplified Version

A streamlined Retrieval-Augmented Generation (RAG) system for students to upload documents and ask questions about their study materials.

## ✨ Core Features

- **Document Upload**: Support for PDF, DOCX, and TXT files
- **Smart Q&A**: Ask questions about your uploaded materials
- **Simple Quiz Generation**: Generate basic quizzes from your content
- **Clean Interface**: Minimalist Streamlit interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

```bash
# Clone and setup
git clone <your-repo-url>
cd study-buddy-rag
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📁 Project Structure

```
study_buddy_rag/
├── src/
│   ├── document_processor.py    # Document processing
│   ├── vector_store.py         # Vector database
│   ├── rag_engine.py           # Main RAG functionality
│   └── quiz_generator.py       # Basic quiz generation
├── data/
│   ├── documents/              # Uploaded files
│   └── vector_db/              # Vector storage
├── app.py                      # Main Streamlit app
├── config.py                   # Configuration
└── requirements.txt            # Dependencies
```

## 🔧 Configuration (config.py)

```python
# Basic settings only
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
VECTOR_DB_PATH = "data/vector_db"
UPLOAD_DIR = "data/documents"
```

## 📦 Requirements (requirements.txt)

```
streamlit==1.28.0
chromadb==0.4.15
sentence-transformers==2.2.2
PyPDF2==3.0.1
python-docx==0.8.11
numpy==1.24.3
pandas==2.0.3
```


## 🏗️ Core Components

### 1. Document Processor (src/document_processor.py)
- Simple PDF/DOCX/TXT processing
- Basic text chunking
- No complex metadata

### 2. Vector Store (src/vector_store.py)
- ChromaDB integration
- Basic embedding storage
- Simple similarity search

### 3. RAG Engine (src/rag_engine.py)
- Question answering
- Context retrieval
- Basic response generation

### 4. Quiz Generator (src/quiz_generator.py)
- Simple multiple choice questions
- Basic question extraction
- No automatic grading

### 5. Main App (app.py)
- Clean Streamlit interface
- Three main pages:
  - Upload Documents
  - Ask Questions
  - Generate Quiz

## 🎮 How to Use

1. **Upload**: Add your study materials (PDF, DOCX, TXT)
2. **Ask**: Type questions about your materials
3. **Quiz**: Generate simple quizzes from your content

## 🔍 Example Usage

```python
# Upload a textbook chapter
# Ask: "What is photosynthesis?"
# Get: Answer based on your specific materials

# Generate quiz on "Biology Chapter 1"
# Get: 5 multiple choice questions
```

## 🛠️ Customization

### Change Embedding Model:
```python
# In config.py
EMBEDDING_MODEL = "all-mpnet-base-v2"  # Better quality
```

### Adjust Chunk Size:
```python
# For shorter documents
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
```

## 🚀 Future Additions

Start simple, then add:
- Better quiz types
- Progress tracking
- Advanced search
- More file formats

## 🐛 Troubleshooting

### Common Issues:
1. **Import errors**: Check virtual environment activation
2. **ChromaDB issues**: Delete `data/vector_db` and restart
3. **Memory problems**: Reduce `CHUNK_SIZE`

### Getting Help:
- Check file permissions
- Ensure all dependencies are installed
- Verify Python version (3.8+)

---

**Simple. Focused. Effective.** 📚✨

This simplified version removes complexity while maintaining core RAG functionality. Perfect for learning and building upon!
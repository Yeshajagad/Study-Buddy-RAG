```markdown
# 📚 Study Buddy RAG - Your Personal AI Study Assistant

A Retrieval-Augmented Generation (RAG) system designed to help students learn more effectively by providing personalized study assistance, quiz generation, and knowledge gap identification.

## ✨ Features

### 📤 Document Upload & Processing
- Support for PDF, DOCX, and TXT files
- Intelligent text chunking and preprocessing
- Vector embeddings for semantic search

### 🔍 Smart Question Answering
- Ask questions about your study materials
- Get answers tailored to your understanding level
- "Explain like I'm 5" mode for complex topics
- Difficulty-based filtering

### 🧠 Knowledge Gap Analysis
- Identify topics you struggle with based on question patterns
- Personalized study recommendations
- Track your learning progress

### 📝 Automatic Quiz Generation
- Generate quizzes on any topic from your materials
- Multiple question types: Multiple choice, True/False, Short answer
- Automatic grading and feedback
- Performance tracking

### 📊 Study Statistics
- Track your learning progress
- Monitor study patterns
- Get personalized study tips

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/study-buddy-rag.git
cd study-buddy-rag
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables (optional):**
```bash
cp .env.example .env
# Edit .env file with your OpenAI API key if you want advanced features
```

5. **Run the application:**
```bash
streamlit run app.py
```

6. **Open your browser and go to:** `http://localhost:8501`

## 📖 How to Use

### 1. Upload Your Study Materials
- Click "📤 Upload Documents" in the sidebar
- Upload your PDFs, DOCX, or TXT files
- Wait for processing to complete

### 2. Ask Questions
- Go to "🔍 Ask Questions"
- Type your question or use quick question buttons
- Get personalized answers based on your materials

### 3. Generate Quizzes
- Navigate to "📝 Generate Quiz"
- Enter a topic and configure quiz settings
- Take the quiz and get instant feedback

### 4. Track Your Progress
- Check "📊 Study Stats" for learning insights
- Use "🧠 Knowledge Gaps" to identify weak areas

## 🔧 Configuration

### Basic Settings (config.py)
- `EMBEDDING_MODEL`: Choose embedding model (default: "all-MiniLM-L6-v2")
- `CHUNK_SIZE`: Document chunk size (default: 1000)
- `CHUNK_OVERLAP`: Chunk overlap (default: 200)

### Advanced Settings
- Add OpenAI API key for enhanced question answering
- Modify difficulty assessment parameters
- Customize quiz generation settings

## 🏗️ Project Structure

```
study_buddy_rag/
├── src/                     # Core application modules
│   ├── document_processor.py   # Document processing and chunking
│   ├── embeddings.py          # Text embedding management
│   ├── vector_store.py        # Vector database operations
│   ├── rag_engine.py          # Main RAG functionality
│   ├── quiz_generator.py      # Quiz creation and evaluation
│   └── difficulty_assessor.py # Text difficulty analysis
├── data/                    # Data storage
│   ├── documents/             # Uploaded documents
│   ├── processed/             # Processed data
│   └── vector_db/             # Vector database
├── app.py                   # Main Streamlit application
├── config.py                # Configuration settings
└── requirements.txt         # Python dependencies
```

## 🎯 Key Features in Detail

### Intelligent Document Processing
- **Multi-format support**: PDFs, Word docs, and text files
- **Smart chunking**: Overlapping chunks for better context
- **Metadata extraction**: File type, word count, and more

### Advanced RAG Engine
- **Semantic search**: Find relevant information using meaning, not just keywords
- **Difficulty awareness**: Adjust responses based on user's level
- **Context understanding**: Maintain conversation context
- **Learning patterns**: Track what you ask about most

### Quiz Generation
- **Topic-based**: Generate quizzes on specific subjects
- **Multiple formats**: Various question types for comprehensive testing
- **Automatic evaluation**: Instant feedback and scoring
- **Performance tracking**: Monitor your improvement over time

### Knowledge Gap Analysis
- **Pattern recognition**: Identify topics you struggle with
- **Personalized recommendations**: Get targeted study suggestions
- **Progress tracking**: See how your understanding evolves

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the web interface
- Uses [ChromaDB](https://www.trychroma.com/) for vector storage
- Powered by [sentence-transformers](https://www.sbert.net/) for embeddings
- Text processing with [LangChain](https://langchain.com/)

## 🐛 Troubleshooting

### Common Issues

1. **"No module named 'src'"**
   - Make sure you're in the correct directory
   - Check that all files are in the right locations

2. **ChromaDB errors**
   - Delete the `data/vector_db` folder and restart
   - Ensure you have write permissions

3. **Memory issues with large files**
   - Reduce `CHUNK_SIZE` in config.py
   - Process files one at a time

4. **Slow embedding generation**
   - Consider using a smaller embedding model
   - Reduce the number of documents processed at once

### Getting Help

- Check the [Issues](https://github.com/yourusername/study-buddy-rag/issues) page
- Create a new issue with detailed description
- Include error messages and system information

## 🚀 Future Enhancements

- [ ] Support for more file formats (PowerPoint, Excel)
- [ ] Integration with popular learning management systems
- [ ] Advanced analytics and study insights
- [ ] Collaborative study features
- [ ] Mobile app version
- [ ] Integration with flashcard systems
- [ ] Audio and video content support

---

Happy studying! 📚✨
```

## 11. .env.example
```
# OpenAI API Key (optional - for advanced features)
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///study_buddy.db

# Application Settings
DEBUG=True
SECRET_KEY=your_secret_key_here
```

## 12. Installation and Setup Instructions

### Step-by-Step Setup:

1. **Create Project Directory:**
```bash
mkdir study_buddy_rag
cd study_buddy_rag
```

2. **Set up Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Create Directory Structure:**
```bash
mkdir -p src data/documents data/processed data/vector_db static templates
```

4. **Install Requirements:**
```bash
pip install -r requirements.txt
```

5. **Download NLTK Data:**
```bash
python -c "import nltk; nltk.download('punkt')"
```

6. **Run the Application:**
```bash
streamlit run app.py
```

## 13. Usage Examples

### Example 1: Basic Question Answering
```python
# Upload a biology textbook
# Ask: "What is photosynthesis?"
# Get: Detailed explanation from your specific textbook
```

### Example 2: Difficulty-Based Learning
```python
# Ask: "Explain quantum mechanics" with difficulty="beginner"
# Get: Simplified explanation suitable for beginners
```

### Example 3: Quiz Generation
```python
# Topic: "Cell Biology"
# Type: "multiple_choice"
# Questions: 10
# Get: Automatically generated quiz with answers
```

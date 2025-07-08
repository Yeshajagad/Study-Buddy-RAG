import streamlit as st
import os
from pathlib import Path
from src.document_processor import DocumentProcessor
from src.embeddings import EmbeddingManager
from src.vector_store import VectorStore
from src.rag_engine import RAGEngine
from src.quiz_generator import QuizGenerator
from config import Config

# Page configuration
st.set_page_config(
    page_title="Study Buddy RAG",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize all components"""
    processor = DocumentProcessor(Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)
    embedding_manager = EmbeddingManager(Config.EMBEDDING_MODEL)
    vector_store = VectorStore(Config.VECTOR_DB_PATH, Config.COLLECTION_NAME)
    rag_engine = RAGEngine(vector_store, embedding_manager)
    quiz_generator = QuizGenerator(vector_store)
    
    return processor, embedding_manager, vector_store, rag_engine, quiz_generator

# Load components
processor, embedding_manager, vector_store, rag_engine, quiz_generator = initialize_components()

# Sidebar
st.sidebar.title("📚 Study Buddy RAG")
st.sidebar.markdown("Upload your study materials and get personalized help!")

# Main navigation
page = st.sidebar.selectbox(
    "Choose a feature:",
    ["📤 Upload Documents", "🔍 Ask Questions", "🧠 Knowledge Gaps", "📝 Generate Quiz", "📊 Study Stats"]
)

# Session state initialization
if 'documents_uploaded' not in st.session_state:
    st.session_state.documents_uploaded = False
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}

# Main content area
if page == "📤 Upload Documents":
    st.title("📤 Upload Your Study Materials")
    st.markdown("Upload PDFs, DOCX, or TXT files to build your knowledge base.")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose your study materials",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="Upload your notes, textbooks, lecture slides, etc."
    )
    
    if uploaded_files:
        # Create documents directory if it doesn't exist
        docs_dir = Path("data/documents")
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Process uploaded files
        with st.spinner("Processing your documents..."):
            progress_bar = st.progress(0)
            
            for i, uploaded_file in enumerate(uploaded_files):
                # Save uploaded file
                file_path = docs_dir / uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process document
                try:
                    doc_data = processor.process_document(str(file_path))
                    
                    # Add to vector store
                    metadatas = []
                    for j, chunk in enumerate(doc_data['chunks']):
                        metadatas.append({
                            'file_name': doc_data['file_name'],
                            'chunk_index': j,
                            'file_type': doc_data['metadata']['file_type'],
                            'word_count': len(chunk.split())
                        })
                    
                    vector_store.add_documents(
                        documents=doc_data['chunks'],
                        metadatas=metadatas
                    )
                    
                    st.success(f"✅ Processed {uploaded_file.name}")
                    
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
                
                # Update progress
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            st.session_state.documents_uploaded = True
            st.balloons()
            st.success(f"🎉 Successfully processed {len(uploaded_files)} documents!")
    
    # Show current document count
    doc_count = vector_store.get_collection_count()
    st.info(f"📊 Current knowledge base: {doc_count} document chunks")

elif page == "🔍 Ask Questions":
    st.title("🔍 Ask Questions About Your Study Materials")
    
    if not st.session_state.documents_uploaded and vector_store.get_collection_count() == 0:
        st.warning("⚠️ Please upload some documents first!")
        st.stop()
    
    # Question input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        question = st.text_input(
            "What would you like to know?",
            placeholder="e.g., Explain photosynthesis in simple terms",
            help="Ask anything about your uploaded materials"
        )
    
    with col2:
        difficulty = st.selectbox(
            "Difficulty Level",
            ["auto", "beginner", "intermediate", "advanced"],
            help="Filter responses by difficulty"
        )
    
    # Quick question buttons
    st.markdown("**Quick Questions:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📖 Explain like I'm 5"):
            if question:
                with st.spinner("Generating simple explanation..."):
                    result = rag_engine.explain_like_im_five(question)
                    st.markdown("### 👶 Simple Explanation")
                    st.markdown(result['response'])
    
    with col2:
        if st.button("🎯 Find key concepts"):
            if question:
                with st.spinner("Finding key concepts..."):
                    result = rag_engine.query(question, n_results=5)
                    st.markdown("### 🎯 Key Concepts")
                    st.markdown(result['response'])
    
    with col3:
        if st.button("🔗 Related topics"):
            if question:
                with st.spinner("Finding related topics..."):
                    result = rag_engine.query(f"topics related to {question}", n_results=3)
                    st.markdown("### 🔗 Related Topics")
                    st.markdown(result['response'])
    
    # Main query processing
    if question:
        with st.spinner("Searching your study materials..."):
            diff_level = None if difficulty == "auto" else difficulty
            result = rag_engine.query(question, n_results=5, difficulty_level=diff_level)
            
            # Display response
            st.markdown("### 💡 Answer")
            st.markdown(result['response'])
            
            # Show understanding level
            st.markdown(f"**Understanding Level Detected:** {result['understanding_level'].title()}")
            
            # Show suggested actions
            if result['suggested_actions']:
                st.markdown("### 🎯 Suggested Next Steps")
                for action in result['suggested_actions']:
                    st.markdown(f"- {action}")
            
            # Show sources
            with st.expander("📄 Sources"):
                if result['sources']['documents'][0]:
                    for i, (doc, metadata) in enumerate(zip(
                        result['sources']['documents'][0],
                        result['sources']['metadatas'][0]
                    )):
                        st.markdown(f"**Source {i+1}:** {metadata['file_name']}")
                        st.markdown(f"```\n{doc[:200]}...\n```")
                else:
                    st.markdown("No sources found")

elif page == "🧠 Knowledge Gaps":
    st.title("🧠 Identify Your Knowledge Gaps")
    st.markdown("Analyze your question patterns to identify areas that need more study.")
    
    if st.button("🔍 Analyze My Learning Patterns"):
        with st.spinner("Analyzing your question history..."):
            gaps = rag_engine.find_knowledge_gaps()
            
            st.markdown("### 📊 Analysis Results")
            
            if gaps and gaps[0] != "Upload more documents and ask more questions to identify knowledge gaps!":
                st.markdown("**Areas that might need more attention:**")
                for gap in gaps:
                    st.markdown(f"- {gap}")
                
                # Recommendations
                st.markdown("### 💡 Recommendations")
                st.markdown("1. **Review highlighted topics** - Focus on areas you ask about frequently")
                st.markdown("2. **Create study schedule** - Dedicate extra time to weak areas")
                st.markdown("3. **Practice with quizzes** - Test your understanding")
                st.markdown("4. **Ask follow-up questions** - Dive deeper into challenging topics")
                
            else:
                st.info("💡 " + gaps[0])
                st.markdown("**Tips to get better analysis:**")
                st.markdown("- Ask more questions about your study materials")
                st.markdown("- Upload additional documents")
                st.markdown("- Use the system regularly to build a question history")

elif page == "📝 Generate Quiz":
    st.title("📝 Generate Practice Quizzes")
    st.markdown("Test your knowledge with automatically generated quizzes.")
    
    if not st.session_state.documents_uploaded and vector_store.get_collection_count() == 0:
        st.warning("⚠️ Please upload some documents first!")
        st.stop()
    
    # Quiz configuration
    col1, col2, col3 = st.columns(3)
    
    with col1:
        topic = st.text_input(
            "Quiz Topic",
            placeholder="e.g., photosynthesis, calculus, history",
            help="Enter the topic you want to be quizzed on"
        )
    
    with col2:
        num_questions = st.slider("Number of Questions", 3, 15, 5)
    
    with col3:
        quiz_type = st.selectbox(
            "Quiz Type",
            ["mixed", "multiple_choice", "true_false", "short_answer"]
        )
    
    # Generate quiz
    if st.button("🎯 Generate Quiz") and topic:
        with st.spinner("Generating your quiz..."):
            quiz_data = quiz_generator.generate_quiz(topic, num_questions, quiz_type)
            
            if 'error' in quiz_data:
                st.error(f"❌ {quiz_data['error']}")
            else:
                st.session_state.quiz_data = quiz_data
                st.session_state.quiz_answers = {}
                st.success(f"✅ Generated {len(quiz_data['questions'])} questions on {topic}")
    
    # Display quiz
    if st.session_state.quiz_data:
        quiz = st.session_state.quiz_data
        st.markdown(f"## 📋 Quiz: {quiz['topic'].title()}")
        st.markdown(f"**Questions:** {quiz['num_questions']} | **Type:** {quiz['quiz_type'].title()}")
        
        # Quiz questions
        for i, question in enumerate(quiz['questions']):
            st.markdown(f"### Question {i+1}")
            st.markdown(question['question'])
            
            if question['type'] == 'multiple_choice':
                answer = st.radio(
                    "Choose your answer:",
                    list(question['options'].values()),
                    key=f"q_{i}",
                    format_func=lambda x: f"{list(question['options'].keys())[list(question['options'].values()).index(x)]}. {x}"
                )
                if answer:
                    st.session_state.quiz_answers[str(i)] = list(question['options'].keys())[list(question['options'].values()).index(answer)]
            
            elif question['type'] == 'true_false':
                answer = st.radio(
                    "Choose your answer:",
                    ["True", "False"],
                    key=f"q_{i}"
                )
                if answer:
                    st.session_state.quiz_answers[str(i)] = answer
            
            elif question['type'] == 'short_answer':
                answer = st.text_area(
                    "Your answer:",
                    key=f"q_{i}",
                    help="Provide a brief answer"
                )
                if answer:
                    st.session_state.quiz_answers[str(i)] = answer
            
            st.markdown("---")
        
        # Submit quiz
        if st.button("📊 Submit Quiz"):
            if len(st.session_state.quiz_answers) < len(quiz['questions']):
                st.warning("⚠️ Please answer all questions before submitting!")
            else:
                with st.spinner("Evaluating your answers..."):
                    results = quiz_generator.evaluate_quiz(quiz, st.session_state.quiz_answers)
                    
                    # Display results
                    st.markdown("## 🎉 Quiz Results")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Score", f"{results['score']}/{results['total_questions']}")
                    with col2:
                        st.metric("Percentage", f"{results['percentage']:.1f}%")
                    with col3:
                        st.metric("Grade", results['grade'])
                    
                    # Performance message
                    if results['percentage'] >= 80:
                        st.success("🎉 Excellent work! You have a strong understanding of this topic.")
                    elif results['percentage'] >= 60:
                        st.info("👍 Good job! Consider reviewing the topics you missed.")
                    else:
                        st.warning("📚 Keep studying! Focus on the areas where you had difficulty.")
                    
                    # Detailed results
                    with st.expander("📋 Detailed Results"):
                        for i, result in enumerate(results['results']):
                            icon = "✅" if result['is_correct'] else "❌"
                            st.markdown(f"{icon} **Q{i+1}:** {result['question']}")
                            st.markdown(f"**Your answer:** {result['user_answer']}")
                            st.markdown(f"**Correct answer:** {result['correct_answer']}")
                            st.markdown("---")

elif page == "📊 Study Stats":
    st.title("📊 Study Statistics")
    st.markdown("Track your learning progress and study patterns.")
    
    # Document stats
    doc_count = vector_store.get_collection_count()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Document Chunks", doc_count)
    with col2:
        st.metric("❓ Questions Asked", len(rag_engine.query_history))
    with col3:
        if st.session_state.quiz_data:
            st.metric("📝 Quizzes Taken", "1+")
        else:
            st.metric("📝 Quizzes Taken", "0")
    
    # Study suggestions
    st.markdown("### 💡 Study Suggestions")
    
    if doc_count == 0:
        st.info("📤 Start by uploading your study materials!")
    elif len(rag_engine.query_history) < 5:
        st.info("❓ Ask more questions to get personalized insights!")
    else:
        st.success("🎯 You're actively using the system! Check your knowledge gaps.")
    
    # Recent activity
    if rag_engine.query_history:
        st.markdown("### 📝 Recent Questions")
        for i, query in enumerate(rag_engine.query_history[-5:]):  # Show last 5 queries
            st.markdown(f"{i+1}. {query}")
    
    # Tips
    st.markdown("### 🎯 Study Tips")
    tips = [
        "📅 Study consistently - little and often works better than cramming",
        "🎯 Focus on understanding concepts, not just memorizing facts",
        "📝 Test yourself regularly with quizzes to reinforce learning",
        "🔍 Ask questions about topics you find challenging",
        "📊 Review your knowledge gaps regularly and adjust your study plan"
    ]
    
    for tip in tips:
        st.markdown(f"- {tip}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Settings")
if st.sidebar.button("🗑️ Clear All Data"):
    if st.sidebar.checkbox("I understand this will delete all my data"):
        vector_store.delete_collection()
        st.session_state.documents_uploaded = False
        st.session_state.quiz_data = None
        st.session_state.quiz_answers = {}
        st.success("🗑️ All data cleared!")
        st.experimental_rerun()

st.sidebar.markdown("---")
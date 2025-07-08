from typing import List, Dict, Tuple
import re
from .vector_store import VectorStore
from .embeddings import EmbeddingManager
from .difficulty_assessor import DifficultyAssessor
import openai
from config import Config

class RAGEngine:
    def __init__(self, vector_store: VectorStore, embedding_manager: EmbeddingManager):
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager
        self.difficulty_assessor = DifficultyAssessor()
        self.query_history = []
        
        # Initialize OpenAI if API key is provided
        if Config.OPENAI_API_KEY:
            openai.api_key = Config.OPENAI_API_KEY
    
    def query(self, question: str, n_results: int = 3, difficulty_level: str = None) -> Dict:
        """Main query function"""
        # Store query for pattern analysis
        self.query_history.append(question)
        
        # Search for relevant documents
        search_results = self.vector_store.search(question, n_results)
        
        # Filter by difficulty if specified
        if difficulty_level:
            search_results = self._filter_by_difficulty(search_results, difficulty_level)
        
        # Generate response
        response = self._generate_response(question, search_results)
        
        # Assess user's understanding level
        understanding_level = self._assess_understanding_level(question)
        
        return {
            "question": question,
            "response": response,
            "sources": search_results,
            "understanding_level": understanding_level,
            "suggested_actions": self._suggest_actions(question, understanding_level)
        }
    
    def explain_like_im_five(self, question: str) -> Dict:
        """Provide simplified explanations"""
        search_results = self.vector_store.search(question, n_results=2)
        
        if not search_results['documents'][0]:
            return {"response": "I couldn't find information about that topic. Try uploading more study materials!"}
        
        # Create simplified explanation
        context = " ".join(search_results['documents'][0])
        simplified_response = self._create_simplified_explanation(question, context)
        
        return {
            "question": question,
            "response": simplified_response,
            "sources": search_results,
            "explanation_level": "beginner"
        }
    
    def find_knowledge_gaps(self) -> List[str]:
        """Analyze query history to identify knowledge gaps"""
        if len(self.query_history) < 5:
            return ["Upload more documents and ask more questions to identify knowledge gaps!"]
        
        # Analyze query patterns
        common_topics = self._extract_common_topics(self.query_history)
        weak_areas = self._identify_weak_areas(common_topics)
        
        return weak_areas
    
    def _filter_by_difficulty(self, search_results: Dict, difficulty_level: str) -> Dict:
        """Filter search results by difficulty level"""
        # This is a simplified version - in practice, you'd want more sophisticated difficulty assessment
        filtered_docs = []
        filtered_metadatas = []
        
        for i, doc in enumerate(search_results['documents'][0]):
            doc_difficulty = self.difficulty_assessor.assess_text_difficulty(doc)
            if self._matches_difficulty_level(doc_difficulty, difficulty_level):
                filtered_docs.append(doc)
                filtered_metadatas.append(search_results['metadatas'][0][i])
        
        return {
            "documents": [filtered_docs],
            "metadatas": [filtered_metadatas]
        }
    
    def _matches_difficulty_level(self, doc_difficulty: float, target_level: str) -> bool:
        """Check if document difficulty matches target level"""
        level_range = Config.DIFFICULTY_LEVELS.get(target_level, {"min_score": 0.0, "max_score": 1.0})
        return level_range["min_score"] <= doc_difficulty <= level_range["max_score"]
    
    def _generate_response(self, question: str, search_results: Dict) -> str:
        """Generate response based on search results"""
        if not search_results['documents'][0]:
            return "I couldn't find relevant information in your study materials. Try uploading more documents or rephrasing your question."
        
        # Combine relevant chunks
        context = " ".join(search_results['documents'][0][:3])  # Use top 3 results
        
        # Simple response generation (can be enhanced with LLM)
        response = f"Based on your study materials:\n\n{context[:500]}..."
        
        return response
    
    def _create_simplified_explanation(self, question: str, context: str) -> str:
        """Create a simplified explanation suitable for beginners"""
        # Basic simplification - in practice, you'd want to use an LLM here
        sentences = context.split('.')
        simple_sentences = []
        
        for sentence in sentences[:3]:
            if len(sentence.split()) < 20:  # Keep shorter sentences
                simple_sentences.append(sentence.strip())
        
        if simple_sentences:
            return "Here's a simple explanation:\n\n" + ". ".join(simple_sentences) + "."
        else:
            return "Let me explain this in simple terms:\n\n" + context[:200] + "..."
    
    def _assess_understanding_level(self, question: str) -> str:
        """Assess user's understanding level based on question complexity"""
        # Simple heuristic - can be enhanced
        question_words = question.lower().split()
        
        beginner_indicators = ['what', 'is', 'define', 'explain', 'basic', 'simple']
        advanced_indicators = ['analyze', 'compare', 'evaluate', 'synthesize', 'critique']
        
        beginner_count = sum(1 for word in beginner_indicators if word in question_words)
        advanced_count = sum(1 for word in advanced_indicators if word in question_words)
        
        if advanced_count > beginner_count:
            return "advanced"
        elif beginner_count > 0:
            return "beginner"
        else:
            return "intermediate"
    
    def _suggest_actions(self, question: str, understanding_level: str) -> List[str]:
        """Suggest follow-up actions based on understanding level"""
        suggestions = []
        
        if understanding_level == "beginner":
            suggestions.append("Try asking for a more detailed explanation")
            suggestions.append("Request examples to illustrate the concept")
        elif understanding_level == "intermediate":
            suggestions.append("Ask for related concepts to explore")
            suggestions.append("Request practice questions on this topic")
        else:  # advanced
            suggestions.append("Ask for critical analysis of this topic")
            suggestions.append("Request connections to other advanced concepts")
        
        return suggestions
    
    def _extract_common_topics(self, queries: List[str]) -> Dict[str, int]:
        """Extract common topics from query history"""
        topic_counts = {}
        
        for query in queries:
            # Simple keyword extraction
            words = re.findall(r'\b\w+\b', query.lower())
            for word in words:
                if len(word) > 3:  # Filter out short words
                    topic_counts[word] = topic_counts.get(word, 0) + 1
        
        return topic_counts
    
    def _identify_weak_areas(self, common_topics: Dict[str, int]) -> List[str]:
        """Identify areas where user asks many questions (potential weak areas)"""
        sorted_topics = sorted(common_topics.items(), key=lambda x: x[1], reverse=True)
        
        weak_areas = []
        for topic, count in sorted_topics[:5]:  # Top 5 most queried topics
            if count >= 3:  # Asked about 3+ times
                weak_areas.append(f"You've asked about '{topic}' {count} times - consider reviewing this topic")
        
        return weak_areas if weak_areas else ["No specific weak areas identified yet"]

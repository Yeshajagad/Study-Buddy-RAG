import random
from typing import List, Dict, Tuple
import re
from .vector_store import VectorStore

class QuizGenerator:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
    
    def generate_quiz(self, topic: str, num_questions: int = 5, quiz_type: str = "mixed") -> Dict:
        """Generate a quiz on a specific topic"""
        # Search for relevant content
        search_results = self.vector_store.search(topic, n_results=10)
        
        if not search_results['documents'][0]:
            return {"error": "No content found for this topic"}
        
        # Extract key information
        content = " ".join(search_results['documents'][0])
        
        # Generate questions based on type
        if quiz_type == "multiple_choice":
            questions = self._generate_multiple_choice(content, num_questions)
        elif quiz_type == "true_false":
            questions = self._generate_true_false(content, num_questions)
        elif quiz_type == "short_answer":
            questions = self._generate_short_answer(content, num_questions)
        else:  # mixed
            questions = self._generate_mixed_quiz(content, num_questions)
        
        return {
            "topic": topic,
            "num_questions": len(questions),
            "questions": questions,
            "quiz_type": quiz_type
        }
    
    def _generate_multiple_choice(self, content: str, num_questions: int) -> List[Dict]:
        """Generate multiple choice questions"""
        questions = []
        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 20]
        
        for i in range(min(num_questions, len(sentences))):
            sentence = sentences[i]
            
            # Extract key terms
            words = re.findall(r'\b[A-Z][a-z]+\b', sentence)  # Capitalized words
            if not words:
                continue
            
            # Create question by replacing a key term
            key_term = random.choice(words)
            question_text = sentence.replace(key_term, "____")
            
            # Generate options
            options = [key_term]
            # Add dummy options (simplified - in practice, use more sophisticated methods)
            dummy_options = ["Option A", "Option B", "Option C"]
            options.extend(dummy_options[:3])
            random.shuffle(options)
            
            correct_answer = chr(65 + options.index(key_term))  # A, B, C, D
            
            questions.append({
                "question": f"Fill in the blank: {question_text}",
                "options": {chr(65 + i): opt for i, opt in enumerate(options)},
                "correct_answer": correct_answer,
                "type": "multiple_choice"
            })
        
        return questions
    
    def _generate_true_false(self, content: str, num_questions: int) -> List[Dict]:
        """Generate true/false questions"""
        questions = []
        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 20]
        
        for i in range(min(num_questions, len(sentences))):
            sentence = sentences[i]
            
            # Half true, half false
            is_true = i % 2 == 0
            
            if not is_true:
                # Modify sentence to make it false (simplified)
                modified_sentence = self._modify_sentence_for_false(sentence)
                question_text = modified_sentence
            else:
                question_text = sentence
            
            questions.append({
                "question": f"True or False: {question_text}",
                "correct_answer": "True" if is_true else "False",
                "type": "true_false"
            })
        
        return questions
    
    def _generate_short_answer(self, content: str, num_questions: int) -> List[Dict]:
        """Generate short answer questions"""
        questions = []
        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 20]
        
        question_starters = [
            "What is", "How does", "Why is", "When did", "Where is",
            "Who was", "Which", "Explain", "Describe", "Define"
        ]
        
        for i in range(min(num_questions, len(sentences))):
            sentence = sentences[i]
            starter = random.choice(question_starters)
            
            # Extract key concept
            words = sentence.split()
            if len(words) > 5:
                key_concept = " ".join(words[:3])
                question_text = f"{starter} {key_concept.lower()}?"
                
                questions.append({
                    "question": question_text,
                    "sample_answer": sentence,
                    "type": "short_answer"
                })
        
        return questions
    
    def _generate_mixed_quiz(self, content: str, num_questions: int) -> List[Dict]:
        """Generate a mixed quiz with different question types"""
        questions = []
        
        # Distribute question types
        mc_count = num_questions // 3
        tf_count = num_questions // 3
        sa_count = num_questions - mc_count - tf_count
        
        questions.extend(self._generate_multiple_choice(content, mc_count))
        questions.extend(self._generate_true_false(content, tf_count))
        questions.extend(self._generate_short_answer(content, sa_count))
        
        random.shuffle(questions)
        return questions
    
    def _modify_sentence_for_false(self, sentence: str) -> str:
        """Modify a sentence to make it false (simplified method)"""
        # Simple modifications
        modifications = [
            ("is", "is not"),
            ("was", "was not"),
            ("can", "cannot"),
            ("will", "will not"),
            ("should", "should not")
        ]
        
        for original, replacement in modifications:
            if original in sentence.lower():
                return sentence.lower().replace(original, replacement, 1)
        
        return sentence  # Return original if no modification found
    
    def evaluate_quiz(self, quiz: Dict, user_answers: Dict) -> Dict:
        """Evaluate user's quiz answers"""
        score = 0
        total_questions = len(quiz['questions'])
        results = []
        
        for i, question in enumerate(quiz['questions']):
            user_answer = user_answers.get(str(i), "")
            
            if question['type'] in ['multiple_choice', 'true_false']:
                is_correct = user_answer.upper() == question['correct_answer'].upper()
                if is_correct:
                    score += 1
            else:  # short_answer
                # Simple keyword matching for short answers
                is_correct = self._evaluate_short_answer(user_answer, question['sample_answer'])
                if is_correct:
                    score += 1
            
            results.append({
                "question": question['question'],
                "user_answer": user_answer,
                "correct_answer": question.get('correct_answer', question.get('sample_answer', '')),
                "is_correct": is_correct
            })
        
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        return {
            "score": score,
            "total_questions": total_questions,
            "percentage": percentage,
            "grade": self._calculate_grade(percentage),
            "results": results
        }
    
    def _evaluate_short_answer(self, user_answer: str, sample_answer: str) -> bool:
        """Evaluate short answer (simplified keyword matching)"""
        user_words = set(user_answer.lower().split())
        sample_words = set(sample_answer.lower().split())
        
        # Check if user answer contains key words from sample
        key_words = [word for word in sample_words if len(word) > 3]
        matching_words = user_words.intersection(set(key_words))
        
        return len(matching_words) >= len(key_words) * 0.3  # 30% keyword match
    
    def _calculate_grade(self, percentage: float) -> str:
        """Calculate letter grade from percentage"""
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"
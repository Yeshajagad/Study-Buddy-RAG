import re
from typing import Dict, List
import nltk
from collections import Counter

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class DifficultyAssessor:
    def __init__(self):
        self.complex_words = set([
            'analyze', 'synthesize', 'evaluate', 'hypothesis', 'methodology',
            'paradigm', 'phenomenon', 'conceptual', 'theoretical', 'empirical'
        ])
    
    def assess_text_difficulty(self, text: str) -> float:
        """Assess the difficulty level of a text (0.0 = easy, 1.0 = hard)"""
        metrics = self._calculate_metrics(text)
        
        # Weighted scoring
        difficulty_score = (
            metrics['avg_sentence_length'] * 0.2 +
            metrics['complex_word_ratio'] * 0.3 +
            metrics['syllable_density'] * 0.3 +
            metrics['technical_term_ratio'] * 0.2
        )
        
        # Normalize to 0-1 range
        return min(1.0, difficulty_score / 100)
    
    def _calculate_metrics(self, text: str) -> Dict[str, float]:
        """Calculate various text complexity metrics"""
        sentences = nltk.sent_tokenize(text)
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Complex word ratio (words with 3+ syllables)
        complex_words = [word for word in words if self._count_syllables(word) >= 3]
        complex_word_ratio = len(complex_words) / len(words) if words else 0
        
        # Syllable density
        total_syllables = sum(self._count_syllables(word) for word in words)
        syllable_density = total_syllables / len(words) if words else 0
        
        # Technical term ratio
        technical_terms = [word for word in words if word in self.complex_words]
        technical_term_ratio = len(technical_terms) / len(words) if words else 0
        
        return {
            'avg_sentence_length': avg_sentence_length,
            'complex_word_ratio': complex_word_ratio * 100,
            'syllable_density': syllable_density,
            'technical_term_ratio': technical_term_ratio * 100
        }
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified method)"""
        vowels = 'aeiouy'
        syllables = 0
        prev_was_vowel = False
        
        for char in word.lower():
            if char in vowels:
                if not prev_was_vowel:
                    syllables += 1
                prev_was_vowel = True
            else:
                prev_was_vowel = False
        
        # Handle special cases
        if word.endswith('e'):
            syllables -= 1
        if syllables == 0:
            syllables = 1
        
        return syllables
    
    def categorize_difficulty(self, difficulty_score: float) -> str:
        """Categorize difficulty score into levels"""
        if difficulty_score < 0.3:
            return "beginner"
        elif difficulty_score < 0.7:
            return "intermediate"
        else:
            return "advanced"
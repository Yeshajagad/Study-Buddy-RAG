import os
import PyPDF2
import docx
from typing import List, Dict
from pathlib import Path
import re

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def process_document(self, file_path: str) -> Dict[str, any]:
        """Process a single document and return metadata + content"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            content = self._extract_pdf_content(file_path)
        elif file_ext == '.docx':
            content = self._extract_docx_content(file_path)
        elif file_ext == '.txt':
            content = self._extract_txt_content(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        # Clean and chunk the content
        cleaned_content = self._clean_text(content)
        chunks = self._create_chunks(cleaned_content)
        
        return {
            "file_path": file_path,
            "file_name": Path(file_path).name,
            "content": cleaned_content,
            "chunks": chunks,
            "metadata": {
                "file_type": file_ext,
                "chunk_count": len(chunks),
                "word_count": len(cleaned_content.split())
            }
        }
    
    def _extract_pdf_content(self, file_path: str) -> str:
        """Extract text from PDF file"""
        content = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                content += page.extract_text() + "\n"
        return content
    
    def _extract_docx_content(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(file_path)
        content = ""
        for paragraph in doc.paragraphs:
            content += paragraph.text + "\n"
        return content
    
    def _extract_txt_content(self, file_path: str) -> str:
        """Extract text from TXT file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        return text.strip()
    
    def _create_chunks(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = ' '.join(words[i:i + self.chunk_size])
            chunks.append(chunk)
        
        return chunks
# rag_pipeline.py
from typing import List, Dict
from utils.ocr_utils import extract_text_from_image, extract_text_from_pdf
from utils.nlp_utils import extract_fields
import re

class RAGPipeline:
    def __init__(self):
        # Memory me documents store karenge
        self.documents: List[str] = []

    def add_invoice(self, file_path: str) -> Dict:
        """Extract text from invoice (PDF/JPG), store & extract fields"""
        if file_path.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_image(file_path)

        self.documents.append(text)

        # NLP fields extract karna
        fields = extract_fields(text)

        return {
            "text": text,
            "fields": fields
        }

    def retrieve(self, query: str) -> List[str]:
        """Simple keyword search from stored docs"""
        results = [doc for doc in self.documents if query.lower() in doc.lower()]
        return results if results else ["No relevant info found."]

    def generate(self, query: str) -> str:
        """Generate final answer using retrieved docs"""
        retrieved_docs = self.retrieve(query)
        return f"Query: {query}\nAnswer: {retrieved_docs[0]}"

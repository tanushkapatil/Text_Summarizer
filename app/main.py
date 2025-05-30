# app/main.py
from .extractive import TextRankSummarizer
from .abstractive import AbstractiveSummarizer
from .sentiment import SentimentAnalyzer
from .utils import clean_text
import os

class TextSummarizerApp:
    def __init__(self, mode='hybrid'):
        """
        Initialize the summarizer app
        :param mode: 'extractive', 'abstractive', or 'hybrid'
        """
        self.mode = mode
        self.extractive = TextRankSummarizer()
        self.abstractive = AbstractiveSummarizer()
        self.sentiment = SentimentAnalyzer()
    
    def summarize(self, text, num_sentences=3):
        text = clean_text(text)
        
        if self.mode == 'extractive':
            summary = self.extractive.summarize(text, num_sentences)
        elif self.mode == 'abstractive':
            summary = self.abstractive.summarize(text)
        else:  # hybrid
            extractive_summary = self.extractive.summarize(text, num_sentences*2)
            summary = self.abstractive.summarize(extractive_summary)
        
        return summary
    
    def analyze_sentiment(self, text):
        return self.sentiment.analyze(text)
    
    def generate_report(self, text, num_sentences=3):
        summary = self.summarize(text, num_sentences)
        sentiment = self.analyze_sentiment(text)
        tone = self.sentiment.get_tone_description(sentiment)
        
        return {
            'summary': summary,
            'sentiment': sentiment['sentiment'],
            'confidence': sentiment['confidence'],
            'tone': tone,
            'original_length': len(text.split()),
            'summary_length': len(summary.split())
        }
    
    def process_file(self, file_path, num_sentences=3):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        return self.generate_report(text, num_sentences)
# app/sentiment.py
from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = pipeline('sentiment-analysis', 
                               model='distilbert-base-uncased-finetuned-sst-2-english')
    
    def analyze(self, text):
        result = self.analyzer(text)
        return {
            'sentiment': result[0]['label'],
            'confidence': result[0]['score']
        }
    
    def get_tone_description(self, sentiment_result):
        sentiment = sentiment_result['sentiment']
        confidence = sentiment_result['confidence']
        
        if sentiment == 'POSITIVE':
            if confidence > 0.9:
                return "Highly Positive"
            elif confidence > 0.7:
                return "Positive"
            else:
                return "Slightly Positive"
        else:
            if confidence > 0.9:
                return "Highly Negative"
            elif confidence > 0.7:
                return "Negative"
            else:
                return "Slightly Negative"
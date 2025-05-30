# app/extractive.py
import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import string

nltk.download('punkt')
nltk.download('stopwords')

class TextRankSummarizer:
    def __init__(self, language='english'):
        self.stop_words = set(stopwords.words(language))
        self.punctuation = set(string.punctuation)
    
    def preprocess(self, text):
        sentences = sent_tokenize(text)
        processed_sentences = []
        for sentence in sentences:
            words = nltk.word_tokenize(sentence.lower())
            words = [word for word in words if word not in self.stop_words and word not in self.punctuation]
            processed_sentences.append(' '.join(words))
        return sentences, processed_sentences
    
    def build_similarity_matrix(self, processed_sentences):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(processed_sentences)
        similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        return similarity_matrix
    
    def summarize(self, text, num_sentences=3):
        original_sentences, processed_sentences = self.preprocess(text)
        
        if len(original_sentences) <= num_sentences:
            return text
        
        similarity_matrix = self.build_similarity_matrix(processed_sentences)
        
        # Convert similarity matrix to graph
        similarity_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(similarity_graph)
        
        # Rank sentences
        ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(original_sentences)), reverse=True)
        
        # Select top sentences
        top_sentences = [s for _, s in ranked_sentences[:num_sentences]]
        
        # Return in original order
        summary = []
        for sentence in original_sentences:
            if sentence in top_sentences:
                summary.append(sentence)
        
        return ' '.join(summary)
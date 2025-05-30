# tests/test_extractive.py
import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extractive import TextRankSummarizer

class TestExtractiveSummarizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.long_text = """
        Artificial intelligence (AI) is transforming business operations across industries. 
        In healthcare, AI assists in diagnosing diseases with high accuracy. 
        Financial institutions use AI for fraud detection and risk assessment. 
        Retailers leverage AI for personalized recommendations and inventory management. 
        Manufacturing employs AI for predictive maintenance and quality control. 
        The technology continues to evolve, offering new applications and efficiencies.
        """
        cls.short_text = "AI is changing business."
        cls.empty_text = ""
        cls.summarizer = TextRankSummarizer()

    def test_summary_length(self):
        summary = self.summarizer.summarize(self.long_text, num_sentences=2)
        sentence_count = len([s for s in summary.split('.') if len(s.strip()) > 0])
        self.assertLessEqual(sentence_count, 2)

    def test_short_text_handling(self):
        summary = self.summarizer.summarize(self.short_text, num_sentences=3)
        self.assertEqual(summary, self.short_text)

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            self.summarizer.summarize(self.empty_text, num_sentences=2)

    def test_sentence_ordering(self):
        summary = self.summarizer.summarize(self.long_text, num_sentences=3)
        sentences_in_summary = [s.strip() for s in summary.split('.') if len(s.strip()) > 0]
        sentences_in_text = [s.strip() for s in self.long_text.split('.') if len(s.strip()) > 0]
        
        # Verify summary sentences appear in the same order as original
        last_index = -1
        for sentence in sentences_in_summary:
            current_index = sentences_in_text.index(sentence)
            self.assertGreater(current_index, last_index)
            last_index = current_index

    def test_stopword_removal(self):
        processed = self.summarizer.preprocess("This is a test sentence with stopwords.")[1][0]
        self.assertNotIn("this", processed)
        self.assertNotIn("is", processed)
        self.assertNotIn("a", processed)
        self.assertNotIn("with", processed)

if __name__ == '__main__':
    unittest.main()
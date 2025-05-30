# tests/test_sentiment.py
import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.sentiment import SentimentAnalyzer

class TestSentimentAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.positive_text = """
        We're thrilled with the outstanding results from our latest product launch! 
        Customer feedback has been overwhelmingly positive, with particular praise 
        for the intuitive user interface and exceptional performance.
        """
        cls.negative_text = """
        The service we received was absolutely terrible. Not only was the product 
        delivered two weeks late, but it arrived damaged and missing key components. 
        The customer support was unhelpful and rude throughout the entire ordeal.
        """
        cls.neutral_text = """
        The meeting was scheduled for 2 PM in the conference room. 
        All department heads were present and the agenda was followed as planned.
        """
        cls.analyzer = SentimentAnalyzer()

    def test_positive_sentiment(self):
        result = self.analyzer.analyze(self.positive_text)
        self.assertEqual(result['sentiment'], 'POSITIVE')
        self.assertGreater(result['confidence'], 0.9)

    def test_negative_sentiment(self):
        result = self.analyzer.analyze(self.negative_text)
        self.assertEqual(result['sentiment'], 'NEGATIVE')
        self.assertGreater(result['confidence'], 0.9)

    def test_neutral_sentiment(self):
        result = self.analyzer.analyze(self.neutral_text)
        # Neutral often classified as positive with lower confidence
        self.assertLess(result['confidence'], 0.7)

    def test_tone_descriptions(self):
        positive_result = {'sentiment': 'POSITIVE', 'confidence': 0.95}
        negative_result = {'sentiment': 'NEGATIVE', 'confidence': 0.92}
        weak_positive = {'sentiment': 'POSITIVE', 'confidence': 0.65}
        
        self.assertEqual(self.analyzer.get_tone_description(positive_result), "Highly Positive")
        self.assertEqual(self.analyzer.get_tone_description(negative_result), "Highly Negative")
        self.assertEqual(self.analyzer.get_tone_description(weak_positive), "Slightly Positive")

    def test_edge_cases(self):
        empty_result = self.analyzer.analyze("")
        self.assertIn(empty_result['sentiment'], ['POSITIVE', 'NEGATIVE'])  # Model will classify even empty strings

if __name__ == '__main__':
    unittest.main()
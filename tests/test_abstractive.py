# tests/test_abstractive.py
import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.abstractive import AbstractiveSummarizer

class TestAbstractiveSummarizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.long_text = """
        Climate change represents one of the greatest challenges of our time. 
        Rising global temperatures are causing more frequent extreme weather events, 
        including hurricanes, droughts, and wildfires. 
        Melting polar ice contributes to rising sea levels, threatening coastal communities. 
        Scientists warn we must limit global warming to 1.5°C to avoid catastrophic impacts. 
        This requires cutting greenhouse gas emissions by nearly half by 2030.
        """
        cls.short_text = "Climate change is important."
        cls.empty_text = ""
        cls.summarizer = AbstractiveSummarizer()

    def test_summary_generation(self):
        summary = self.summarizer.summarize(self.long_text)
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 10)
        self.assertLess(len(summary), len(self.long_text))

    def test_short_text_handling(self):
        summary = self.summarizer.summarize(self.short_text)
        self.assertIn("climate", summary.lower())

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            self.summarizer.summarize(self.empty_text)

    def test_length_parameters(self):
        short_summary = self.summarizer.summarize(self.long_text, max_length=50, min_length=20)
        long_summary = self.summarizer.summarize(self.long_text, max_length=150, min_length=100)
        self.assertLess(len(short_summary.split()), len(long_summary.split()))

    def test_model_switching(self):
        t5_summarizer = AbstractiveSummarizer(model_name='t5-small')
        summary = t5_summarizer.summarize(self.long_text)
        self.assertIsInstance(summary, str)

if __name__ == '__main__':
    unittest.main()
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sentiment import SentimentEngine

class TestSentimentAnalysis(unittest.TestCase):
    
    def setUp(self):
        """Initialize the engine before each test"""
        self.engine = SentimentEngine()

    def test_positive_sentiment(self):
        result = self.engine.analyze("I love this service, it works great!")
        self.assertEqual(result['label'], "Positive")
        self.assertGreater(result['score'], 0)

    def test_negative_sentiment(self):
        result = self.engine.analyze("This is terrible and useless.")
        self.assertEqual(result['label'], "Negative")
        self.assertLess(result['score'], 0)

    def test_neutral_sentiment(self):
        # We changed the text to be purely factual.
        # "Please" is positive, but "Click the button" is neutral.
        result = self.engine.analyze("Click on the settings button.")
        
        # Now check if it stays within the neutral range (-0.05 to 0.05)
        self.assertTrue(-0.05 <= result['score'] <= 0.05)

    def test_custom_tech_pain_words(self):
        """Test the custom lexicon we added for the assignment"""
        # "Slow" is usually neutral in standard VADER, but we made it Negative
        result = self.engine.analyze("The app is loading very slow")
        self.assertEqual(result['label'], "Negative")
        
        result = self.engine.analyze("The process is too complicated")
        self.assertEqual(result['label'], "Negative")

if __name__ == '__main__':
    unittest.main()
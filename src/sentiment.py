import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentEngine:
    def __init__(self):
        try:
            self.analyzer = SentimentIntensityAnalyzer()
        except LookupError:
            nltk.download('vader_lexicon')
            self.analyzer = SentimentIntensityAnalyzer()

        # "Universal Support Lexicon"
        # These words are generally negative in ANY customer service context 
        # (Banking, Retail, Tech, Hospitality) but are often Neutral in standard English.
        support_context = {
            # Time / Speed Issues
            'slow': -2.0,
            'slowly': -2.0,
            'delay': -2.0,
            'delayed': -2.0,
            'wait': -1.0,
            'waiting': -1.0,
            'late': -2.0,
            
            # Service Quality
            'rude': -3.0,
            'unhelpful': -2.5,
            'useless': -2.5,
            'poor': -2.0,
            'bad': -2.0,
            'terrible': -3.0,
            'worst': -3.0,
            
            # Complexity / Friction
            'hard': -1.5,
            'tough': -1.5,
            'complicated': -2.0,
            'confusing': -2.0,
            'stuck': -2.0,
            'buggy': -2.0,
            'glitchy': -2.0,
            'messy': -2.0,
            
            # Cost / Value
            'expensive': -1.5,
            'overpriced': -2.0,
            'waste': -2.5, # e.g. "waste of money/time"
        }
        self.analyzer.lexicon.update(support_context)

    def analyze(self, text):
        if not text:
            return {'score': 0.0, 'label': "Neutral", 'color': "gray"}

        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']

        # Determine label and visual color based on compound score
        if compound >= 0.05:
            return {'score': compound, 'label': "Positive", 'color': "#28a745"} # Green
        elif compound <= -0.05:
            return {'score': compound, 'label': "Negative", 'color': "#dc3545"} # Red
        else:
            return {'score': compound, 'label': "Neutral", 'color': "#6c757d"}  # Grey
# src\RAD_trading\nlp\sentiment_analysis.py
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
class SentimentAnalyzer:
    def __init__(self):
        nltk.download('vader_lexicon')
        self.sia = SentimentIntensityAnalyzer()
    def analyze_sentiment_textblob(self, text):
        blob = TextBlob(text)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
    def analyze_sentiment_vader(self, text):
        return self.sia.polarity_scores(text)
    def categorize_sentiment(self, score):
        if score > 0.05:
            return 'Positive'
        elif score < -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    def analyze_text(self, text):
        textblob_sentiment = self.analyze_sentiment_textblob(text)
        vader_sentiment = self.analyze_sentiment_vader(text)
        overall_sentiment = (textblob_sentiment['polarity'] + vader_sentiment['compound']) / 2
        return {
            'textblob': textblob_sentiment,
            'vader': vader_sentiment,
            'overall_sentiment': overall_sentiment,
            'sentiment_category': self.categorize_sentiment(overall_sentiment)
        }

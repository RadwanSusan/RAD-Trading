# src\RAD_trading\market_analysis\sentiment_analysis.py
import pandas as pd
from textblob import TextBlob
def analyze_news_sentiment(news_data):
    def get_sentiment(text):
        return TextBlob(text).sentiment.polarity
    news_data['sentiment'] = news_data['headline'].apply(get_sentiment)
    sentiment_summary = pd.DataFrame({
        'average_sentiment': news_data['sentiment'].mean(),
        'positive_news': (news_data['sentiment'] > 0).sum(),
        'negative_news': (news_data['sentiment'] < 0).sum(),
        'neutral_news': (news_data['sentiment'] == 0).sum()
    }, index=[0])
    return sentiment_summary

# src\RAD_trading\alternative_data\social_media_trends.py
import tweepy
import pandas as pd
from collections import Counter
class SocialMediaAnalyzer:
    def __init__(self, api_key, api_secret_key, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
    def get_trending_topics(self, woeid=1):  # 1 is the woeid for worldwide
        trends = self.api.get_place_trends(woeid)
        return pd.DataFrame(trends[0]["trends"])
    def analyze_tweets(self, keyword, count=100):
        tweets = tweepy.Cursor(self.api.search_tweets, q=keyword, lang="en").items(count)
        data = []
        for tweet in tweets:
            data.append({
                'text': tweet.text,
                'user': tweet.user.screen_name,
                'retweets': tweet.retweet_count,
                'favorites': tweet.favorite_count,
                'created_at': tweet.created_at
            })
        df = pd.DataFrame(data)
        # Basic analysis
        total_engagement = df['retweets'].sum() + df['favorites'].sum()
        top_users = Counter(df['user']).most_common(5)
        return {
            'tweet_count': len(df),
            'total_engagement': total_engagement,
            'avg_engagement_per_tweet': total_engagement / len(df),
            'top_users': top_users
        }

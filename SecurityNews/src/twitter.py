from configparser import ConfigParser
import os
import tweepy
import pandas as pd

configure = ConfigParser()
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_FILE = os.path.join(PROJECT_DIR, 'secNews.conf')
print(configure.read(CONFIG_FILE))
consumer_key = configure.get('TWITTER', 'consumer_key')
consumer_secret = configure.get('TWITTER', 'consumer_secret')
access_key = configure.get('TWITTER', 'access_key')
access_secret = configure.get('TWITTER', 'access_secret')


def get_tweets(hashtags, date_since, numtweet=100):
    # hashtags = [i if i.startswith('#') else '#' + i for i in hashtags]
    hashtags_qry = " OR ".join(hashtags)
    df = pd.DataFrame(columns=['username', 'description', 'location', 'following',
                               'followers', 'totaltweets', 'retweetcount', 'text', 'hashtags', 'verified', 'tweet_url'])
    tweets = tweepy.Cursor(api.search, q=hashtags_qry, lang="en",
                           since=date_since, tweet_mode="extended").items(numtweet)
    for tweet in tweets:
        print(tweet)
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        verified = tweet.user.verified
        hashtags = tweet.entities['hashtags']
        tweets_url = 'https://twitter.com/%s/status/%s' % (tweet.user.screen_name, tweet.id)
        # tweets_url = 'https://twitter.com/Drew_Brosenhaus/status/' + tweet.id_str
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])

        df.loc[len(df)] = [username, description, location, following,
                           followers, totaltweets, retweetcount, text, hashtext,
                           verified, tweets_url]

    filename = os.path.join(PROJECT_DIR, 'data', 'scraped_tweets.csv')

    # we will save our database as a CSV file.
    df.to_csv(filename)


if __name__ == '__main__':
    hash_tags = ['cyber', 'security', 'news', 'infosec', 'hack', 'vulnerability', 'exploit']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    get_tweets(hash_tags, "2021-07-04")

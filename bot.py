import tweepy
from config import create_api #importing Twtitter api
from datetime import datetime
import time
import logging
import random

#updates logs for references
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# -------> these are used track numbers related to apps twitter activity in the logs <--------
like_rate = 0 #keeps a count of likes in a day
retweet_rate = 0 #keeps a count of retweets in a day
follow_count = 0 #keeps a count of retweets in a day
follow_interval = 0 #adds 1 count every session, follows a user every 5th session
tweet_count = 0 #keeps a count of retweets in a day
tweet_interval = 0 #adds 1 count every session, posts a tweet every 10th session
# -------> these are used track numbers related to apps twitter activity in the logs <--------

#Add hashtags seperated by comma
mentions = "#hastags or @twitter-accounts"

#streaming tweets
class twitter_bot(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()


    def on_status(self, tweet):
        #------->Like<----------
        global like_rate
        if not like_rate >= 1000:
            #2 account types are ignored: 1. if an account is reply to some other user & self accounts
            if not (tweet.user.id == self.me.id or tweet.favorited):
                # if not tweet.favorited:
                    try:
                        tweet.favorite()
                        like_rate = like_rate + 1
                        logger.info('%s accounts liked today', like_rate)
                    except Exception as e:
                        logger.error("Already liked %s or Error occurred on Like method", like_rate, exc_info=False)
        else:
            print('You have liked 1000 tweets for today')
        #------->Like<----------

        time.sleep(5) #------------------->> timers to manage twitter activity from crashing app & ban

        #------->Retweet<----------
        global retweet_rate
        #2 account types are ignored: 1. if an account is reply to some other user & self accounts
        if not (tweet.user.id == self.me.id or tweet.retweeted):
            # if not tweet.retweeted:
                try:
                    tweet.retweet()
                    retweet_rate = retweet_rate + 1
                    logger.info('%s accounts retweeted today', retweet_rate)
                except Exception as e:
                    logger.error("Already retweeted %s or Error while retweeting",retweet_rate, exc_info=False)
        #------->Retweet<----------
        
        time.sleep(5)

        #------->Follow<----------
        global follow_count
        global follow_interval
        #follow every 5th user
        if follow_interval % 5 == 0:
            #2 account types are ignored: 1. if an account is reply to some other user & self accounts
            if not tweet.user.id == self.me.id:
                if self.api._lookup_friendships(self.me.id, tweet.user.id):
                        #follow user if you dont already follow
                        try:
                            self.api.create_friendship(tweet.user.id)
                            follow_count = follow_count + 1
                            logger.info('%s accounts followed today', follow_count)
                        except Exception as e:
                            logger.error("Already following %s or Error occurred while following", follow_count, exc_info=False)
        #increments 1 every session so every 5th account will be followed
        follow_interval = follow_interval + 1
        #------->Follow<----------

        time.sleep(20)

        #------->Grab & Post a Tweet<----------
        #Only post tweet every 10minutes 
        global tweet_count
        global tweet_interval
        global mentions
        if tweet_interval % 10 == 0:
            if not tweet.user.id == self.me.id:
            #Grab a streaming tweet, add tags in (mentions). Maximum Char while tweeting is 280. 
                try:
                    if not len(tweet.text) <= 162:
                        limit_char = tweet.text[:159]
                        new_char = limit_char+' '+mentions
                        # Create a tweet
                        self.api.update_status(new_char)
                        tweet_count = tweet_count +1
                        logger.info('%s accounts tweeted today. FYI: text>140', tweet_count)
                        logger.info('Current count of tweet-interval: %s', tweet_interval)
                        next_tweet = tweet_interval+10
                        logger.info('Next tweet at %sth like/retweet', next_tweet)
                    else:
                        limit_char = tweet.text[:159]
                        new_char = limit_char+' '+mentions
                        # Create a tweet
                        self.api.update_status(new_char)
                        tweet_count = tweet_count +1
                        logger.info('%s accounts tweeted today. FYI: text<140', tweet_count)
                        logger.info('Current count of tweet-interval: %s', tweet_interval)
                        next_tweet = tweet_interval+10
                        logger.info('Next tweet at %sth like/retweet', next_tweet)
                except Exception as e:
                            logger.error("Error occurred on update status", exc_info=False)
        #increments 1 every session so every 10th account will be followed
        tweet_interval = tweet_interval + 1 
        #------->Quote(post) a Tweet<----------

        time.sleep(30)
        #------->resets logs every 24hrs<----------
        now = datetime.now()
        start = ('00:00:01')
        current_time = now.strftime("%H:%M:%S")
        end = ('00:02:00')

        if start <= current_time <= end:
            like_rate = 0
            retweet_rate = 0
            follow_count = 0
            follow_interval = 0
            tweet_count = 0
            tweet_interval = 0
            logger.info('Resetting the counts to 0')
        #------->resets logs every 24hrs<----------

    #error handling
    def on_error(self, tweet):
        if tweet == 420:
            logger.error("Disconnecting the stream as you hit an rate-limit error %s", tweet)
            #returning False in on_data disconnects the stream
            return False


def main(keywords):
    api = create_api()
    tweets_listener = twitter_bot(api)
    try:
        stream = tweepy.Stream(api.auth, tweets_listener)
        stream.filter(track=keywords, languages=["en"])
    except Exception as e:
        logger.error("Stream error, sleeping for 60 seconds", exc_info=True)
        sleep(60)

    
# Insert terms to be tracked in main([]), arguments are string values held in a list
if __name__ == "__main__":
    #Below add as many keywords you wish, it will grab them and process it
    main(['keywords','that','you','wish','to','retweet','like','&', 'tweet'])
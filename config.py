import tweepy
import logging
import os

#to log errors
logger = logging.getLogger()

#Creating api endpoint
def create_api():
    CONSUMER_KEY = os.getenv("")
    CONSUMER_SECRET = os.getenv("")
    ACCESS_TOKEN = os.getenv("")
    ACCESS_TOKEN_SECRET = os.getenv("")


    #Granted Twitter API V2access
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify = True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise Exception
    logger.info("API created")
    return api

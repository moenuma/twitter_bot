from credentials import *
import tweepy
import time
import datetime

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def main():
    pass


if __name__ == '__main__':
    main()
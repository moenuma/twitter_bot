from credentials import *
import tweepy
import time
import datetime

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def who_to_follow(twitterID, name):
    '''
    Return a list of max of 30 users who mentioned twitterID and has the figure's name in their bio
    '''
    follow_list = []
    results = tweepy.Cursor(api.search, q=twitterID).items(100)
    for tweet in results:
        if len(follow_list) >= 30:
            break
        else:
            if name in tweet.user.description.lower():
                if tweet.user.screen_name not in follow_list:
                    follow_list.append(tweet.user.screen_name)

    return follow_list

def retweet_popular_tweets():
    pass

def like_popular_tweets():
    pass

def followback():
    pass

def main():
    valid = False
    while not valid:
        name = input("Enter the figure that you are fan of: ").lower()
        twitterID = input("Enter Twitter ID of the figure that you are fan of: @")
        
        try:
            user_info = api.get_user(screen_name=twitterID)
            valid = True
        except tweepy.error.TweepError:
            print("User not found")

    
    if valid:

        api.create_friendship(screen_name=twitterID)
        follow_list = who_to_follow(twitterID, name)

    


if __name__ == '__main__':
    main()
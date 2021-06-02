from credentials import *
import tweepy
import time
import datetime
import re
from collections import Counter

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
    print(follow_list)
    return follow_list

def retweet_popular_tweets():
    pass

def like_popular_tweets():
    pass

def hashtag_search(twitterID):
    '''
    Search for the current popular hashtags that your fellow fans are using
    '''
    hashtag_dict = {}
    results = tweepy.Cursor(api.search, q=twitterID).items(200)
    for tweet in results:
        hashtags = re.findall(r"#(\w+)", tweet.text)
        for hashtag in hashtags:
            if not hashtag.isdigit():
                if hashtag in hashtag_dict.keys():
                    hashtag_dict[hashtag] += 1
                else:
                    hashtag_dict[hashtag] = 1

    top10_hashtags = Counter(hashtag_dict).most_common(10)
    print("\nTop 10 Popular Hashtags at that moment: ")
    for hashtag in top10_hashtags:
        print('\t#{}'.format(hashtag[0]))
    

def follow_back():
    followers = api.followers()
    following = api.friends()
    for follower in followers:
        if follower not in following:
            api.create_friendship(screen_name=follower.screen_name)

def is_fanaccount(twitterID, fan):
    '''
    Determines whether the selected user is also a fan account
    '''
    # 1. if the figure's name is included in a bio
    # 2. if the account follows the figure


def main():
    valid = False
    while not valid:
        name = input("Enter the figure that you are fan of: ").lower()
        twitterID = input("Enter Twitter ID of the figure that you are fan of: @")
        
        try:
            twitter_info = api.get_user(screen_name=twitterID)
            valid = True
        except tweepy.error.TweepError:
            print("User not found")

    
    if valid:

        api.create_friendship(screen_name=twitterID)
        #lst = [follower.screen_name for follower in api.followers_ids()]
        #print(lst)
        #follow_back()
        #print(is_fanaccount(twitterID, "sorryiamonadiet"))
        #follow_list = who_to_follow(twitterID, name)
        hashtag_search(twitterID)

    


if __name__ == '__main__':
    main()
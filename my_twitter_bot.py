'''
MIT License

Copyright (c) 2018 Yosuke Kyle Sugi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from credentials import *
import tweepy
import time
import datetime

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    try:
        last_seen_id = int(f_read.read().strip())
    except ValueError: # no entry yet
        return
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweets():
    print('retrieving and replying to tweets...')
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(
        last_seen_id,
        tweet_mode='extended'
    )

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#helloworld' in mention.full_text.lower():
            print('found #helloworld!')
            print('responding back...')
            api.update_status('@' + mention.user.screen_name + 
                                '#HelloWorld back to you!', mention.id)


def daily_tweet():
    '''
    Make a tweet with today's day
    '''
    weekday = datetime.date.today().weekday()
    if weekday == 0:
        api.update_status("Today is Monday!")
    elif weekday == 1:
        api.update_status("Today is Tuesday!")
    elif weekday == 2:
        api.update_status("Today is Wednesday!")
    elif weekday == 3:
        api.update_status("Today is Thursday!")
    elif weekday == 4:
        api.update_status("Today is Friday!")
    elif weekday == 5:
        api.update_status("Today is Saturday!")
    elif weekday == 6:
        api.update_status("Today is Sunday!")



def main():

    today = datetime.date.today()
    daily_tweet_done = False
    
    while True:

        if today != datetime.date.today():
            today = datetime.date.today()
            daily_tweet_done = False

        # make a tweet once in a day
        if not daily_tweet_done:
            daily_tweet()
            daily_tweet_done = True

        reply_to_tweets()

        time.sleep(15)

    
    # get the timeline tweets
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

    # search for certain keyword included in tweets
    for tweet in tweepy.Cursor(api.search, q="McDonald's").items(20):
        if tweet.text[:2] != 'RT':
            print(tweet.text)

    # extract the certain user's tweets
    for tweet in tweepy.Cursor(api.user_timeline, id="McDonalds").items(20):
        if tweet.text[:2] != 'RT' and tweet.text[0] != '@':
            print(tweet.text)


    for page in tweepy.Cursor(api.user_timeline).pages(3):
        print(len(page))

    #print(api.me())

    # number of followers
    print(api.me().followers_count)
    
    # number of followng
    print(api.me().friends_count)

    # my bio
    print(api.me().description)

    # follow the user
    api.create_friendship(screen_name='McDonalds')

    # what tweets the user liked
    for tweet in api.favorites(screen_name='McDonalds'):
        print(tweet.text)
    
    # like the first tweet appearing on your timeline
    api.create_favorite(id=api.home_timeline()[0].id)

if __name__ == '__main__':
    main()
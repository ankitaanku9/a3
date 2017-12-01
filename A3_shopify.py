#This is simple script to retriieve data from Twitter by using python
import tweepy
import time #https://github.com/tweepy/tweepy
import csv

#Create an app in your Twitter and get the Keys from API keys
consumer_key = "tAtJO0fTtGqXItkvmTJhwTWdF"
consumer_secret = "j2MzolbvVxQtTF5GNEGTCZt8WJWyjeJMSwFhRBSfgUGtz5pla4"
access_key = "892546832999567360-Xx8DA02zrZ2IQ0sPazGMYQEzAbMzbOe"
access_secret = "o2AFfodujpR5e0rmfbv0OTxGxHzL57xW8TbGTy41kwrn2"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
# 
def get_profile(screen_name):
    try:
        #https://dev.twitter.com/rest/reference/get/users/show describes get_user
        user_profile = api.get_user(screen_name)
    except:
        user_profile = "broken"

    return user_profile

# We can use get_profile("username") to get particular username data
s = get_profile("Shopify")
print "Name: " + s.name
print "id: " + s.id_str
print "Location: " + s.location
print "Description: " + s.description
def get_tweets(screen_name):
    alltweets = []
    try:
        #https://developer.twitter.com/en/docs/tweets/timelines/overview describes user_timeline
        tweets = api.user_timeline(screen_name, count=200)
        print "tweets"
        alltweets.extend(tweets)
        oldest = alltweets[-1].id - 1
        print oldest
        print len(tweets)
        while len(tweets) > 0:
            tweets = api.user_timeline(screen_name, count=200, max_id=oldest)
            alltweets.extend(tweets)
            oldest = alltweets[-1].id - 1
            print "...retrieving data" % (len(alltweets))
    except:
        user_profile = "broken"
    return alltweets
       
list1 = []
t = get_tweets("Shopify")
for tweet in t:
    list1.append(tweet.retweet_count)

for tweet in t:
    if tweet.retweet_count == max(list1):
        text1 = tweet.text

with open ('tweets.csv', 'wb') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["id","user","created_at","text"])
    for tweet in t:
        if "FTC" in tweet.text:
            writer.writerow([tweet.id_str,tweet.user.screen_name,tweet.created_at,tweet.text.encode('unicode-escape')])
    t2 = get_tweets("Shopify")
    for tweet in t2:
        if "Citron" in tweet.text:
            writer.writerow([tweet.id_str,tweet.user.screen_name,tweet.created_at,tweet.text.encode('unicode-escape')])
print "Shopify's most popular tweets are: \"" + text1 + " \" count of " +str(max(list1))

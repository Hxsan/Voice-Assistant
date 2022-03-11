import tweepy

keys = []
with open('C:/Users/Hasan/Desktop/Live-NEA/keys/twitterAPIkeys.txt','r') as f:
    for line in f:
        keys.append(line.rstrip('\n'))

client = tweepy.Client(
    bearer_token= keys[0],
    consumer_key= keys[1],
    consumer_secret= keys[2],
    access_token= keys[3],
    access_token_secret= keys[4],
    )

# Uname = "BBCNews"

# def ID_Grabber(client, handle):
#     user = str(client.get_user(username= handle))
#     Response = user.split(' ')
#     id = Response[1].removeprefix('id=')
#     return id

identity = 612473
tweets = client.get_users_tweets(id = identity , max_results = 10, exclude = "retweets")
for tweet in tweets.data:
    print(tweet.text)

"""
To Do:
    Place the twitter scraper into a class
    Make sure the class is not inheriting anything
    Add a bunch of fstrings to make sure variables are changed according to textboxes
    Log each request made into a database, with tweet-id and tweet-text both having their own field
    Connect microphone object into seach query button....
"""


import twitterbot as tb
import secrets
import sys
import time

# fetches the hashtag from command line argument
text = sys.argv[1]
# fetches the credentials dictionary
# using get_credentials function
credentials = secrets.get_credentials()
# initialize the bot with your credentials
bot = tb.Twitterbot(credentials['email'], credentials['password'])
# logging in
bot.login()

with open('listOfTweetsExample.txt') as f:
    # iterating over the lines
    for line in f.readlines():
        # post a tweet
        bot.post_tweet(line)
        # wait for 10 seconds
        time.sleep(5)


# bot.post_tweet(text)

import tweepy
import os
from datetime import date
import random

# Twitter API credentials
consumer_key = os.environ['TWITTER_API_KEY']
consumer_secret = os.environ['TWITTER_API_SECRET_KEY']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# Initialize Tweepy client
try:
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    me = client.get_me(user_auth=True)
    my_username = me.data.username
    print(f"Authenticated as: @{my_username}")
except Exception as e:
    with open('logs.txt', 'a') as f:
        f.write(f"Error initializing Tweepy: {e}\n")
    exit(1)

# Check for stop flag
if os.path.exists('stop.txt'):
    print("Stop flag found, exiting.")
    with open('logs.txt', 'a') as f:
        f.write("Stopped due to stop.txt\n")
    exit(0)

# Check for "stop" mentions from your account
try:
    mentions = client.get_users_mentions(id=me.data.id, max_results=5)
    if mentions.data:
        for mention in mentions.data:
            if mention.author_id == me.data.id and "stop" in mention.text.lower():
                with open('stop.txt', 'w') as f:
                    f.write("Stopped by user request")
                print("Stop command detected, creating stop.txt")
                with open('logs.txt', 'a') as f:
                    f.write("Stopped by user request via mention\n")
                exit(0)
except Exception as e:
    with open('logs.txt', 'a') as f:
        f.write(f"Error checking mentions: {e}\n")

# Calculate days since start date (September 28, 2025)
start_date = date(2025, 2, 28)  # Change this if you want a different start
today = date.today()
day_count = (today - start_date).days + 1  # Start at Day 1

# Random tweet messages
messages = [
    f"Day {day_count} of our epic journey! 🕒 #CountUpBot",
    f"Yo, it’s Day {day_count}! Keepin’ it real. 🚀 #CountUpBot",
    f"Day {day_count} and counting! Let’s go! 💥 #CountUpBot",
    f"Another day, another count: Day {day_count}! ⏳ #CountUpBot"
]

# Post tweet
tweet_text = random.choice(messages)
try:
    response = client.create_tweet(text=tweet_text)
    print(f"Tweet posted: {tweet_text} (ID: {response.data['id']})")
    with open('logs.txt', 'a') as f:
        f.write(f"Tweeted: {tweet_text} (ID: {response.data['id']})\n")
except Exception as e:
    print(f"Error posting tweet: {e}")
    with open('logs.txt', 'a') as f:
        f.write(f"Error posting tweet: {e}\n")
    exit(1)

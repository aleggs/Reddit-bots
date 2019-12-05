import praw
import sqlite3
import pdb
import re
import os

r = praw.Reddit('bot1')
subreddit = r.subreddit("frugalmalefashion")

if not os.path.isfile("posts.txt"):
    posts = []

# for post in subreddit.new(limit = 20):
#     print("Title: ", post.title)
#     print("____________________\n")


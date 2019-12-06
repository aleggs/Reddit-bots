import praw
import os

r = praw.Reddit('ssd-bot')
bapcs = r.subreddit("buildapcsales")

if not os.path.isfile("commented_on.txt"):
    commented_on = []
else:
    with open("commented_on.txt", "r") as f:
        commented_on = f.read()
        commented_on = commented_on.split("\n")
        commented_on = list(filter(None, commented_on))

if not os.path.isfile("ssd_posts.txt"):
    ssd_posts = []
else:
    with open("ssd_posts.txt", "r") as f:
        ssd_posts = f.read()
        ssd_posts = ssd_posts.split("\n")
        ssd_posts = list(filter(None, ssd_posts))

for submission in bapcs.new(limit = 200):
    if submission.id not in commented_on and "[SSD]" in submission.title:
        commented_on.append(submission.id)
        ssd_posts.append(submission.title)



for post in ssd_posts:
    print(post)
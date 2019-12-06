import praw, pdb, os

r = praw.Reddit('first-bot')
subreddit = r.subreddit('pythonforengineers')
keywords = []
keywords.append("i love python")
if not os.path.isfile("replied_to.txt"):
    replied_to = []
else:
    with open("replied_to.txt", "r") as f:
        replied_to = f.read()
        replied_to = replied_to.split("\n")
        replied_to = list(filter(None, replied_to))



for submission in subreddit.new(limit = 10):
    if submission.id not in replied_to:
        replied_to.append(submission.id)
        if submission.title.lower():
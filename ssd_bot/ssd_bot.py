import praw, os
from helpers import *
from sheets2 import main, lookup

r = praw.Reddit('ssd_bot')
bapcs = r.subreddit("botlaunchpad")

# Creates or updates commented_on.txt
if not os.path.isfile("commented_on.txt"):
    commented_on = []
else:
    with open("commented_on.txt", "r") as f:
        commented_on = f.read()
        commented_on = commented_on.split("\n")
        commented_on = list(filter(None, commented_on))

for submission in bapcs.new(limit=10):
    # should be set based on avg posts per time interval
    if submission.id not in commented_on and "[SSD]" in submission.title:
        comment = ""
        # commented_on.append(submission.id)
        title = submission.title

        brands, models = main()
        brand, model = title_filter(title, brands, models)
        comment += "Title of post: " + title + "/ Brand: " + brand + "/ Model: " + model
        lookup(brand, model)

        # submission.reply(comment)
# to label an SSD, we need name and model
# use google sheets as a spreadsheet/database


with open("commented_on.txt", "w") as f:
    for submission_id in commented_on:
        f.write(submission_id + "\n")

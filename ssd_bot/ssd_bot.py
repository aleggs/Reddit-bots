import praw, os
from helpers import *
from sheets import main

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

# Parses title for SSD name
# Replies with information about the SSD
# Searches for u/NewMaxx comments about this SSD

for submission in bapcs.new(limit=10):
    # should be set based on avg posts per time interval
    if submission.id not in commented_on and "[SSD]" in submission.title:
        commented_on.append(submission.id)
        title = submission.title
        title = remove_spaces(title)
        brands, models = main()
        brand, model = title_filter(title, brands, models)
        
        submission.reply("Testing, here's the title: " + title + " and here's the brand: " + brand + " and here's the model: " + model)

# to label an SSD, we need name and model
# use google sheets as a spreadsheet/database


with open("commented_on.txt", "w") as f:
    for submission_id in commented_on:
        f.write(submission_id + "\n")

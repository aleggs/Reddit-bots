import praw, os
from helpers import *
from sheets import main, lookup

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
        sentence_comment = ""
        commented_on.append(submission.id)
        title = submission.title
        brands, models = main()
        brand, model = title_filter(title, brands, models)
        sentence_comment += f"This SSD seems to be a {brand} {model}."
        
        controller, dram, nandtype, category = lookup(brand, model)
        sentence_comment += f" It is {nandtype}, with a {controller} controller. {dram} for DRAM."
        sentence_comment += f" u/NewMaxx classifies this as {category}."
        # submission.reply(sentence_comment)

        info_comment = f"Serving up some information about this {brand} {model}.\n\n"
        info_comment += f"NAND type: **{nandtype}**\n\nDRAM: **{dram}**\n\nController: **{controller}**\n\n"
        info_comment += f"Classified as: **{category}**\n\n"
        # info_comment += "This bot made possible by NewMaxx and company."
        submission.reply(info_comment)

with open("commented_on.txt", "w") as f:
    for submission_id in commented_on:
        f.write(submission_id + "\n")

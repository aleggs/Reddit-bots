import praw, os, sqlite3
from helpers import *
from sheets import brands_and_models, lookup

r = praw.Reddit('ssd_bot')
bapcs = r.subreddit("botlaunchpad")
brands, models = None, None


# Creates or updates commented_on.txt
if not os.path.isfile("commented_on.txt"):
    commented_on = []
else:
    with open("commented_on.txt", "r") as f:
        commented_on = f.read()
        commented_on = commented_on.split("\n")
        commented_on = list(filter(None, commented_on))

for submission in bapcs.new(limit=10):
    if submission.id not in commented_on and "[SSD]" in submission.title:
        commented_on.append(submission.id)
        comment = ""

        title = submission.title
        brands, models = brands_and_models()
        brand, model = parse_title(title, brands, models)
        controller, dram, nandtype, category = lookup(brand, model)

        comment += f"Serving up some information about this {brand} {model}.\n\n"
        comment += f"NAND type: **{nandtype}**\n\nDRAM: **{dram}**\n\nController: **{controller}**\n\n"
        comment += f"Classified as: **{category}**\n\n"

        print(comment)
        # submission.reply(comment)

with open("commented_on.txt", "w") as f:
    for submission_id in commented_on:
        f.write(submission_id + "\n")


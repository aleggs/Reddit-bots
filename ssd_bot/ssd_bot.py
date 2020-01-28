'''
The following packages are required for proper functioning of the bot:
gspread, praw, sqlite3, oauth2client
'''

import praw, os, sheets, helpers


# Authenticating bot with PRAW
reddit = praw.Reddit('ssd_bot')
# Subreddit name
sub = reddit.subreddit("botlaunchpad")
# Desired flair to search for
flair = "[SSD]"


# Updates these variables once per run: SSD brands and models, comment database
brands, models = sheets.brands_and_models()
# comment_tracker.comment_tracker(username)

if not os.path.isfile("commented_on.txt"):
    commented_on = []
else:
    with open("commented_on.txt", "r") as f:
        commented_on = f.read()
        commented_on = commented_on.split("\n")
        commented_on = list(filter(None, commented_on))

for submission in sub.new(limit=10):
    if submission.id not in commented_on and flair in submission.title:
        commented_on.append(submission.id)
        brand, model = helpers.get_brand_and_model(submission.title, brands, models)
        controller, dram, nandtype, category = sheets.lookup(brand, model)

        comment = ""
        comment += f"Serving up some information about this {brand} {model}.\n\n"
        comment += f"NAND type: **{nandtype}**\n\nDRAM: **{dram}**\n\nController: **{controller}**\n\n"
        comment += f"Classified as: **{category}**\n\n"

        submission.reply(comment)

with open("commented_on.txt", "w") as f:
    for submission_id in commented_on:
        f.write(submission_id + "\n")


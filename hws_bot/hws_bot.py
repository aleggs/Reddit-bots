"""
The following packages are required for proper functioning of the bot:
gspread, praw, sqlite3, oauth2client
You can use "pip install -r requirements.txt" to install all the packages at once.
"""

import praw, os, sheets, helpers, relevant_comments


# Authenticating bot with PRAW
reddit = praw.Reddit('hws_bot')
# Subreddit name
sub = reddit.subreddit("hardwareswap")
# Desired flair to search for
# flair = "[SSD]"


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
        commented_on.append(submission.id) # uncomment
        brand, model = helpers.get_brand_and_model(submission.title, brands, models)
        controller, dram, nandtype, category = sheets.lookup(brand, model)

        comment = ""
        comment += f"Serving up some information about this {brand} {model}.\n\n"
        comment += f"NAND type: **{nandtype}**\n\nDRAM: **{dram}**\n\nController: **{controller}**\n\n"
        comment += f"Classified as: **{category}**\n\n"

        more_comments = relevant_comments.get_relevant_comments(brand, model, brands, models)
        print(more_comments) # delete
        comment += f"Here are some potentially relevant comments:\n\n"
        for lst in more_comments:
            comment += f"[{lst[0][:200]}...]({lst[1]})\n\n"
        submission.reply(comment)

with open("commented_on.txt", "w") as f:
    for submission_id in commented_on:
        f.write(submission_id + "\n")


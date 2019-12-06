import praw
import os

r = praw.Reddit('ssd-bot')
bapcs = r.subreddit("botlaunchpad")

if not os.path.isfile("commented_on.txt"):
    commented_on = []
else:
    with open("commented_on.txt", "r") as f:
        commented_on = f.read()
        commented_on = commented_on.split("\n")
        commented_on = list(filter(None, commented_on))

for submission in bapcs.new(limit = 20):
    if submission.id not in commented_on and "[SSD]" in submission.title:
        submission.reply("Toshiba Inland Samsung Crucial Intel E12p 660 Premium P1 EVO++")
        commented_on.append(submission.id)

with open("commented_on.txt", "w") as f:
    for submission_id in commented_on:
        f.write(submission_id + "\n")
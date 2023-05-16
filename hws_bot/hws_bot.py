"""
The following packages are required for proper functioning of the bot:
gspread, praw, oauth2client
You can use "pip install -r requirements.txt" to install all the packages at once.
"""
import praw, os, json, re
from socket import gethostname

# Authenticating bot with PRAW
if not os.path.isfile("auth.txt"):
    raise Exception("No auth file found")
else:
    with open("auth.txt", "r") as f:
        client_id, client_secret, _ = f.read().split("\n")
        user_agent = gethostname()
    f.close()
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
sub = reddit.subreddit("hardwareswap")
print(user_agent, client_id, client_secret)


# Keyword processing with regex
if not os.path.isfile("keywords.txt"):
    raise Exception("File not found: keywords.txt")
else:
    with open("keywords.txt", "r") as f:
        keywords = f.read()
        keywords = keywords.split("\n")
        keywords = list(filter(None, keywords))
    f.close()

keyword_patterns = []
for keyword in keywords:
        pattern = r'^[a-zA-Z0-9 ]+$'  # Regex pattern for alphanumeric characters only
        keyword_pattern = re.sub(r'\W+', pattern, keyword) + pattern
        keyword_patterns.append(keyword_pattern)

# Open list of (old) already processed posts
if not os.path.isfile("viewed_posts.json"):
    viewed_posts = {}
else:
    with open("viewed_posts.json", "r") as f:
        viewed_posts = json.load(f)
    f.close()

# keyword should count as a match if there's a space in the middle of a keyword; don't need to match the keyword, just the first and last word
# so like Strix 3080 would match Asus ROG Strix RTX3080 but not Strix b450i, Gigabyte 3080 or Strix x570\n RTX3080 FE

# with regex patterns, I'm not sure there's a way to do it faster than n2 time (comparing each regex pattern with whole string)
# although if you assume keywords is a constant (XD) it's N time lol

# TODO: update regex to only include after [h] and before [w] 
for submission in sub.new(limit=10):
    if submission.id not in viewed_posts:
        match_count = 0
        viewed_posts[submission.id] = submission.title[:28] + "..."
        for pattern in keyword_patterns:
            match_count = match_count + 1 if re.match(pattern, submission.title) else match_count
        if match_count >= 1:
            print(submission.permalink)


# TODO: change to an append, maybe
with open("viewed_posts.json", "w") as f:
    y = json.dumps(viewed_posts)
    f.write(y)

f.close()

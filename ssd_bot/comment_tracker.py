import praw, os, sqlite3
from helpers import *
from sheets import brands_and_models

r = praw.Reddit('ssd_bot')
keywords = ['SSD']

def comment_tracker(username):
    brands, models = brands_and_models()
    keywords.extend(brands)
    keywords.extend(models)
    # print(f"Keywords: {keywords}")
    user = r.redditor(username)

    # first time setup
    if not os.path.isfile("comments.db"):
        db = sqlite3.Connection('comments.db')
        db.execute('''CREATE TABLE comments (id PRIMARY KEY, brand, model, score, body);''')

    # every other time, just updates the database
    else:
        db = sqlite3.Connection('comments.db')
        for comment in user.comments.new(limit = 10):
            submission = comment.submission
            brand, model = parse_title(submission.title, brands, models)
            # incoming SQL Injection
            # filter if comment id in comments
            db.execute(f'''INSERT INTO comments VALUES ((?),(?),(?),(?),(?));''', [comment.id, brand, model, comment.score, comment.body])
        print(db.execute('''SELECT id, brand, model, score FROM comments''').fetchall())
    db.close()


def ssd_or_not(comment):
    # determines if the comment pertains to an SSD
    for keyword in keywords:
        if keyword.lower() in comment.body.lower():
            return comment
    
    return False

"""
The database should have 5 columns: Brand, Model, Number of upvotes, Comment ID, and Comment Body
"""
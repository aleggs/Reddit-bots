import praw, os
from helpers import *
from sheets import brands_and_models

r = praw.Reddit('ssd_bot')


def comment_tracker(username):
    brands, models = brands_and_models()
    
    if not os.path.isfile("comments.db"):
        db = sqlite3.Connection('comments.db')
        db.execute('''CREATE TABLE comments (brand, model, upvotes, id, body);''')
        db.close()

    else:
        conn = sqlite3.connect('comments.db')
        with open("comments.db", "r") as f:
            user_comments = f.read()
            user_comments = user_comments.split("\n")
            user_comments = list(filter(None, user_comments))

    user = r.redditor(username)

    for comment in user.comments.new(limit = 5):
        submission = comment.submission
        parse_title(submission.title, brands, models)
        print(f"{submission.title}\n{comment.body}\n\n")
   
    # comments = redditor.comments.new(limit = 50)
    # for comment in comments:
    #     if comment.id not in user_comments:

    with open("user_comments.txt", "w") as f:
        for comment_id in user_comments:
            f.write(comment_id + "\n")


"""
The database should have 5 columns: Brand, Model, Number of upvotes, Comment ID, and Comment Body
"""
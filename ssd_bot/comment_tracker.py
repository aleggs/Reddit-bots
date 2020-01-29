"""Comment tracker:
Parses through NewMaxx's comments, compiles all new comments into database.
Database has six columns: Comment ID, SSD (is it about an SSD), Brand, Model, Score, and Body
"""

import praw, os, sqlite3, helpers, sheets

reddit = praw.Reddit('ssd_bot')
keywords = []
username = "NewMaxx"




def comment_tracker(username = username):

    brands, models = sheets.brands_and_models()
    
    if not os.path.isfile("comments.db"):
        db = sqlite3.Connection('comments.db')
        db.execute('''CREATE TABLE comments (id PRIMARY KEY, ssd, brand, model, score, body);''')
        for comment in user.comments.all():
            brand, model = helpers.get_brand_and_model(comment.submission.title, brands, models)
            db.execute(f'''INSERT INTO comments VALUES ((?),(?),(?),(?),(?),(?));''', [comment.id, ssd_or_not(comment), brand, model, comment.score, comment.body])

    else:
        db = sqlite3.Connection('comments.db')
        for comment in user.comments.new(limit = 10):
            submission = comment.submission
            brand, model = helpers.get_brand_and_model(comment.submission.title, brands, models)
            db.execute(f'''INSERT INTO comments VALUES ((?),(?),(?),(?),(?),(?));''', [comment.id, ssd_or_not(comment), brand, model, comment.score, comment.body])
        # print(db.execute('''SELECT * FROM comments''').fetchall())
    db.close()

    # brands, models = brands_and_models()
    keywords.extend(brands)
    keywords.extend(models)
    user = r.redditor(username)


"""
How to tell if a comment is about an SSD, and what SSD it is about?
### This seems to call for some Data Science/Tensorflow :O but I don't know how to do that yet. Revisit in Summer 2020.
1. Post replied to is about an SSD.
    a) Has keywords in title.
2. Comment has keywords in it.


"""
def ssd_or_not(comment):
    # determines if the comment pertains to an SSD
    for keyword in keywords:
        if keyword.lower() in comment.body.lower():
            return comment
    
    return False

"""
The database should have 5 columns: Brand, Model, Number of upvotes, Comment ID, and Comment Body
"""
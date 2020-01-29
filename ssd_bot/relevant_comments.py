"""
The dumb version of comment tracker, no data science or machine learning involved.
Instead, it:
1. Searches the subreddit for posts that match brand and model.
2. From those posts, it:
    1. Looks at all top level comments.
    2. Sorts by number of keyword matches for specific terms (QLC, TLC, DRAM etc.)
    3. Adds to a six column database
        a) Comment ID, number of keyword matches, brand, model, link, and comment body


will need: txt file to track submissions added to database, database for comments, keywords file
"""
import praw, os, sqlite3, helpers, sheets


reddit = praw.Reddit('ssd_bot')
sub = reddit.subreddit('buildapcsales')
keywords = []


def get_relevant_comments(brand, model, brands, models):
    update_db(brand, model, brands, models)
    db = sqlite3.Connection('comments.db')
    # db = db.cursor()
    relevant_comments = db.execute(f"SELECT body, link FROM comments WHERE brand = (?) AND model = (?) AND score > 5 ORDER BY matches DESC;", [brand, model]).fetchmany(3) # descending # of matches
    return relevant_comments


def update_db(brand, model, brands, models):
    # open submissions.txt
    if not os.path.isfile("submissions.txt"):
        submissions = []
    else:
        with open("submissions.txt") as s:
            submissions = s.read()
            submissions = submissions.split("\n")
            submissions = list(filter(None, submissions))
    # open comments.db
    if not os.path.isfile("comments.db"):
        db = sqlite3.Connection('comments.db')
        db.execute('''CREATE TABLE comments (id PRIMARY KEY, matches, brand, model, link, score, body);''')
        # db = db.cursor()
    else:
        db = sqlite3.Connection('comments.db')
        # db = db.cursor()
    
    keywords = update_keywords()
    search_string = f"{brand} {model}"
    # search through submissions
    for submission in sub.search(search_string):
        if submission.id not in submissions:
            submissions.append(submission.id) # uncomment
            
            submission.comment_sort = 'best'
            for comment in submission.comments:
                brand, model = helpers.get_brand_and_model(comment.submission.title, brands, models)
                db.execute('''INSERT or IGNORE INTO comments VALUES (?,?,?,?,?,?,?);''', [comment.id, match_keywords(comment, keywords), brand, model, comment.permalink, comment.score, comment.body])
                db.commit()
    db.close()

    with open("submissions.txt", "w") as s:
        for submission in submissions:
            s.write(submission + "\n")


def update_keywords():
    brands, models = sheets.brands_and_models()
    if not os.path.isfile("keywords.txt"):
        keywords = []
    else:
        with open("keywords.txt", "r") as k:
            keywords = k.read()
            keywords = keywords.split("\n")
            keywords = list(filter(None, keywords))
    keywords.extend(brands+models)
    return keywords


def match_keywords(comment, keywords):
    matches = 0
    for keyword in keywords:
        if keyword.lower() in comment.body.lower():
            matches += 1
    return matches

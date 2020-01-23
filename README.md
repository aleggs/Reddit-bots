# Alex's Reddit bots

Currently limited to just ssd_bot.

## SSD Bot

**Built with:** Python, Flask, Google Sheets API, gspread, and PRAW

##### Core function

The core file, ssd_bot.py, is run every minute. It uses PRAW to scan r/buildapcsales for new posts, and when a submission is tagged with [SSD], it runs the main function. It then:

1. Calls Google Sheets API. It looks at NewMaxx's SSD spreadsheet, and updates an internal list of SSD brands and models.

2. Checks if the item in the title of the Reddit submission is included in the spreadsheet.

3. Looks up the item in the spreadsheet to find its row number.

4. Scans the row to get desired information.

5. Comments that information on a submission.

##### Comment parsing

The secondary function of SSD Bot is to classify and compile NewMaxx's comments about SSDs on r/bapcs into a database, (powered by SQLite and Flask) and then when the bot is summoned, link or quote from those comments. It:

1. Connects to a SQL database (comments.db).

2. Parses through u/NewMaxx's comments.

3. Adds them to comment.db, tracking comment ID, brand and model mentioned, comment score, and the text in the body of the comment.
   
   * It makes use of PRAW's comment ID feature and SQL's primary key feature to avoid duplication of comments in the database.

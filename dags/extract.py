import praw
import pandas as pd
import os
from dotenv import load_dotenv
from utils.data_cleaning import clean_data
from datetime import datetime

# Load environment variables
load_dotenv()

# Reddit API credentials from .env
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")


def extract_and_save():
    # Initialize PRAW Reddit instance
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    # Define subreddit and fetch top 100 posts
    subreddit_name = "technology"
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.hot(limit=100)

    # Extract relevant fields
    data = []
    for post in posts:
        data.append({
            "id": post.id,
            "title": post.title,
            "score": post.score,
            "num_comments": post.num_comments,
            "url": post.url,
            "created_utc": post.created_utc,
            "author": post.author.name if post.author else None,
            "flair": post.link_flair_text,
            "upvote_ratio": post.upvote_ratio
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Clean and transform the data
    df_cleaned = clean_data(df)

    today_date = datetime.today().strftime('%Y-%m-%d')

    # Save cleaned data to CSV
    csv_file = f"tech_news_{today_date}.csv"
    df_cleaned.to_csv(csv_file, index=False)

    print(f"Data extracted and saved to {csv_file}")

    return csv_file

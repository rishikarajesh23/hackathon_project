import praw
from textblob import TextBlob
import spacy
from collections import defaultdict
import re
import matplotlib.pyplot as plt
# Initialize Reddit API client
reddit = praw.Reddit(
    client_id="K3xWHKBQ3EyJ9w4hklRCcA",
    client_secret="N07feMoiN-Q4KQVZVf_pWZq_RQQBIA",
    user_agent="CodeEXP"
)


# Sentiment Analysis Function
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Returns a score between -1 (negative) and 1 (positive)

# Function to categorize sentiment
def categorize_sentiment(sentiment):
    if sentiment > 0:
        return 'Positive'
    elif sentiment == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Ask user for input: subreddits (products) to analyze
user_input = input("Enter subreddits (products) to compare (separate with commas): ")
subreddits = [sub.strip() for sub in user_input.split(',')]  # Convert input into a list of subreddits

# Initialize dictionary to hold sentiment data for each subreddit
sentiment_data = defaultdict(list)

# Fetching top posts from each subreddit
for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.hot(limit=5)  # Get top 5 posts from each subreddit
    for submission in top_posts:
        submission.comments.replace_more(limit=0)  # Flatten comments
        comments = [comment.body for comment in submission.comments.list()]

        # Analyze sentiment of the submission title + body
        post_sentiment = analyze_sentiment(submission.title + " " + submission.selftext)
        sentiment_data[subreddit_name].append(post_sentiment)

        # Analyze sentiment of each comment
        for comment in comments:
            comment_sentiment = analyze_sentiment(comment)
            sentiment_data[subreddit_name].append(comment_sentiment)

# Create a pie chart for sentiment distribution in each subreddit
fig, axes = plt.subplots(1, len(sentiment_data), figsize=(15, 6))  # Create subplots side by side

# Loop through sentiment data and plot each pie chart
for idx, (subreddit_name, sentiments) in enumerate(sentiment_data.items()):
    # Categorize the sentiments
    sentiment_categories = [categorize_sentiment(sentiment) for sentiment in sentiments]

    # Count the number of occurrences of each sentiment category
    sentiment_counts = defaultdict(int)
    for sentiment in sentiment_categories:
        sentiment_counts[sentiment] += 1

    # Prepare data for the pie chart
    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [sentiment_counts['Positive'], sentiment_counts['Neutral'], sentiment_counts['Negative']]

    # Define custom colors: Green for Positive, Yellow for Neutral, Red for Negative
    colors = ['#4CAF50', '#FFEB3B', '#F44336']  # Green, Yellow, Red

    # Plot the pie chart on the corresponding subplot
    ax = axes[idx]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.set_title(f"Sentiment Distribution for {subreddit_name}")
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.

plt.tight_layout()  # Adjust the layout to prevent overlap
plt.show()
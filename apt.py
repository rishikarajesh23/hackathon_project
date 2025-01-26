from flask import Flask, request, jsonify, render_template, redirect, url_for
import praw
from textblob import TextBlob
from collections import defaultdict
import os
import matplotlib
import matplotlib.pyplot as plt

# Set the Matplotlib backend to 'Agg' (non-interactive mode)
matplotlib.use('Agg')

app = Flask(__name__)

# Path to save pie charts
CHARTS_FOLDER = os.path.join(os.getcwd(), "static", "charts")
os.makedirs(CHARTS_FOLDER, exist_ok=True)  # Create directory if not exists
app.config["CHARTS_FOLDER"] = CHARTS_FOLDER

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

# Function to generate pie chart (non-interactive mode)
def generate_pie_chart(sentiment, subreddit_name):
    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [sentiment.get('Positive', 0), sentiment.get('Neutral', 0), sentiment.get('Negative', 0)]
    colors = ['#4CAF50', '#FFEB3B', '#F44336']  # Green, Yellow, Red

    # Create the pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title(f"Sentiment Distribution for {subreddit_name}")
    plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.

    # Save the chart as a PNG file without opening a GUI
    chart_path = os.path.join(app.config["CHARTS_FOLDER"], f"{subreddit_name}.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path

@app.route('/')
def index():
    return render_template('index.html')  # Serve the frontend

@app.route('/analyze', methods=['GET'])
def analyze():
    subreddits = request.args.get('subreddits', '')
    if not subreddits:
        return jsonify({"error": "Please provide subreddits"}), 400

    subreddit_list = [sub.strip() for sub in subreddits.split(',')]  # Parse the input
    sentiment_data = {}  # Store sentiment counts
    chart_urls = []  # Store chart URLs

    for subreddit_name in subreddit_list:
        subreddit = reddit.subreddit(subreddit_name)
        top_posts = subreddit.hot(limit=5)
        sentiments = []

        for submission in top_posts:
            submission.comments.replace_more(limit=0)
            comments = [comment.body for comment in submission.comments.list()]

            # Analyze sentiment of the submission title + body
            post_sentiment = analyze_sentiment(submission.title + " " + submission.selftext)
            sentiments.append(post_sentiment)

            # Analyze sentiment of each comment
            for comment in comments:
                comment_sentiment = analyze_sentiment(comment)
                sentiments.append(comment_sentiment)

        # Categorize the sentiments
        sentiment_categories = [categorize_sentiment(sentiment) for sentiment in sentiments]

        # Count the occurrences of each sentiment category
        sentiment_counts = defaultdict(int)
        for sentiment in sentiment_categories:
            sentiment_counts[sentiment] += 1

        sentiment_data[subreddit_name] = {
            "Positive": sentiment_counts["Positive"],
            "Neutral": sentiment_counts["Neutral"],
            "Negative": sentiment_counts["Negative"]
        }

        # Generate pie chart for the subreddit
        chart_path = generate_pie_chart(sentiment_counts, subreddit_name)
        chart_urls.append(f"/static/charts/{subreddit_name}.png")

    return render_template('results.html', sentiment_data=sentiment_data, chart_urls=chart_urls)

@app.route('/about')
def about():
    return render_template('about.html')  # Serve the About page

if __name__ == '__main__':
    app.run(debug=True)

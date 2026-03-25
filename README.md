https://docs.google.com/document/d/1_Qk7XI31gm3qvDZt0C46W3_5HwziYeJzjVo543CjyAw/edit?usp=drive_link
# 📊 ReadIT: Reddit Sentiment Analysis Tracker

## 📌 Overview

**ReadIT** is a web-based sentiment analysis tool that helps users understand the overall mood of discussions in Reddit communities. By simply entering a subreddit name, the application analyzes posts and generates a **visual sentiment breakdown** (positive, negative, neutral) using a pie chart.

---

## 🚀 Features

* 🔍 Analyze sentiment of any subreddit
* 📊 Visual representation using pie charts
* ⚡ Fast and simple user interface
* 🧠 Automated sentiment classification (Positive / Negative / Neutral)
* 🌐 Web-based application (no installation required for users)

---

## ❗ Problem Statement

Reddit hosts millions of discussions across diverse communities.
However, understanding the **overall sentiment** of a subreddit is difficult due to the sheer volume of content.

---

## 💡 Solution

**ReadIT** simplifies this by:

* Collecting subreddit data
* Performing sentiment analysis
* Presenting results in an easy-to-understand visual format

This helps users quickly grasp whether a community is generally **positive, negative, or neutral**.

---

## 🧠 How It Works

1. User enters a subreddit name
2. Backend fetches posts from Reddit
3. Sentiment analysis is performed using NLP
4. Results are categorized into:

   * Positive
   * Negative
   * Neutral
5. A **pie chart** is generated to visualize the sentiment distribution

---

## 🛠️ Tech Stack

### 💻 Software Components

* **Languages**: Python, HTML, CSS
* **Backend Framework**: Flask
* **Frontend Frameworks**: Bootstrap / W3CSS
* **Libraries**:

  * TextBlob (Sentiment Analysis)
  * Matplotlib (Visualization)
* **Tools**: Git, Postman

### ⚙️ Hardware Requirements

* No special hardware required

---

## ▶️ Installation & Setup

### 🔹 Clone the Repository

```bash
git clone https://github.com/your-username/readit-sentiment-tracker.git
cd readit-sentiment-tracker
```

### 🔹 Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔹 Run the Application

```bash
python app.py
```

### 🔹 Open in Browser

```
http://127.0.0.1:5000/
```

---

## 📊 Output Example

* Pie chart showing:

  * % Positive posts
  * % Negative posts
  * % Neutral posts

---


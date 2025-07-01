import streamlit as st
import requests
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Stack Overflow Tag Analyzer", layout="wide")
st.title("🧠 Stack Overflow Tag Analyzer")

tag = st.text_input("Enter a Stack Overflow tag (e.g., python, css, beauty, data-science)", value="python")

def fetch_questions(tag, pagesize=50):
    url = f"https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "creation",
        "tagged": tag,
        "site": "stackoverflow",
        "pagesize": pagesize,
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json()["items"]
    else:
        return []

def extract_keywords(titles):
    stopwords = set([
        "this", "that", "with", "from", "they", "would", "there", "their",
        "what", "which", "your", "have", "will", "about", "could", "should",
        "because", "while", "where", "when", "then", "them", "some", "just",
        "into", "also", "only", "being", "been", "more", "like", "than",
        "each", "most", "many", "such", "over", "other", "after", "even",
        "using", "make", "much", "does", "well", "can't", "don't", "isn't",
        "i've", "i'm", "you're", "it's", "did", "was", "were", "has", "had",
        "the", "and", "for", "you", "are", "but", "not", "all", "any", "can",
        "its", "get", "out", "too", "how", "why", "who", "what", "when", "which",
        "an", "a", "of", "in", "to", "on", "if", "as", "at", "by", "or", "be", "do", "is", "no"
    ])

    all_words = []
    for title in titles:
        words = re.findall(r'\b[a-zA-Z]{4,}\b', title.lower())
        filtered = [w for w in words if w not in stopwords]
        all_words.extend(filtered)
    common = Counter(all_words).most_common(15)
    return common


if st.button("Analyze"):
    st.info(f"Fetching recent questions tagged with '{tag}'...")
    questions = fetch_questions(tag)
    
    if not questions:
        st.error("No questions found or API error.")
    else:
        titles = [q["title"] for q in questions]
        df = pd.DataFrame({
            "Title": [q["title"] for q in questions],
            "Score": [q["score"] for q in questions],
            "Views": [q["view_count"] for q in questions],
            "Answers": [q["answer_count"] for q in questions],
            "Link": [q["link"] for q in questions],
        })

        st.subheader("📊 Top Keywords in Questions")
        keywords = extract_keywords(titles)
        words, counts = zip(*keywords)
        fig, ax = plt.subplots()
        ax.barh(words[::-1], counts[::-1], color="#6C63FF")
        ax.set_xlabel("Frequency")
        ax.set_title(f"Top Keywords in '{tag}' Questions")
        st.pyplot(fig)

        st.subheader("📋 Recent Questions Table")
        st.dataframe(df)

        st.markdown("---")
        st.markdown("✅ Real-time data from Stack Overflow • No login needed • Made with ❤️ using Streamlit")

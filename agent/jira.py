import requests
import pandas as pd
import numpy as np
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Terminal color codes for headings (optional)
c = {"y": '\033[93m', "r": '\033[91m', "g": '\033[92m', "w": '\033[0m'}

# Configuration for public JIRA server (no API key required)
JIRA_SERVER = "https://issues.apache.org/jira"
JQL_QUERY = "project = ZOOKEEPER ORDER BY created DESC"
INITIATIVES = {
    "Creativity": ["feature", "innovation"],
    "Stability": ["bug", "fix", "refactor"],
    "Performance": ["performance", "speed", "optimize"],
    "Tech Debt": ["tech debt", "refactor", "cleanup"],
}

# Step 1 — Fetch and prepare Jira data
def fetch_jira_issues(jira_server, jql):
    try:
        response = requests.get(
            f"{jira_server}/rest/api/2/search",
            timeout=20,
            params={"jql": jql, "maxResults": 500, "fields": "summary,issuetype,components,assignee"},
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        issues = response.json()["issues"]
        if not issues:
            print(f"{c['r']}[ERROR]{c['w']} No issues found. Exiting.")
            sys.exit(0)

        # Flatten data
        df = pd.DataFrame([{
            "key": i["key"],
            "type": i["fields"]["issuetype"]["name"],
            "summary": i["fields"]["summary"],
            "components": [comp["name"] for comp in i["fields"].get("components", [])],
            "assignee": (i["fields"]["assignee"] or {}).get("displayName", "Unassigned")
        } for i in issues])
        return df
    except Exception as e:
        print(f"{c['r']}[ERROR]{c['w']} Failed to fetch Jira data: {e}")
        sys.exit(1)

# Step 2 — Analyze with TF-IDF + LDA
def analyze_topics(df, n_topics=5, n_top_words=5):
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.95, min_df=2)
    X = vectorizer.fit_transform(df["summary"])

    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)

    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        topics.append((topic_idx + 1, top_words))

    print(f"{c['g']}[INFO]{c['w']} Top {n_topics} topics found in summaries:\n")
    for idx, words in topics:
        print(f"Topic {idx}: {', '.join(words)}")

    # Plot wordclouds for topics
    plot_wordclouds(lda, feature_names, n_top_words)

def plot_wordclouds(lda_model, feature_names, n_top_words=10):
    for topic_idx, topic in enumerate(lda_model.components_):
        top_words = {feature_names[i]: topic[i] for i in topic.argsort()[:-n_top_words - 1:-1]}
        wc = WordCloud(width=400, height=200, background_color='white').generate_from_frequencies(top_words)
        plt.figure(figsize=(8,4))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.title(f"Topic {topic_idx + 1} WordCloud")
        plt.show()

# Step 3 — (Optional) Tag initiatives
def map_initiatives(summary, mapping):
    tags = []
    lower_summary = summary.lower()
    for label, keywords in mapping.items():
        if any(k in lower_summary for k in keywords):
            tags.append(label)
    return tags

def classify_initiatives(df):
    df["initiatives"] = df["summary"].apply(lambda s: map_initiatives(s, INITIATIVES))
    return df

def plot_initiative_counts(df):
    from collections import Counter
    all_tags = sum(df['initiatives'].tolist(), [])
    counts = Counter(all_tags)
    if counts:
        labels, values = zip(*counts.items())
        plt.bar(labels, values, color='skyblue')
        plt.title("Initiative Tag Counts")
        plt.ylabel("Number of Issues")
        plt.show()
    else:
        print("No initiative tags found to plot.")

# Run everything
if __name__ == "__main__":
    print(f"{c['g']}[INFO]{c['w']} Fetching Jira issues...")
    df = fetch_jira_issues(JIRA_SERVER, JQL_QUERY)

    print(f"{c['g']}[INFO]{c['w']} Running topic analysis on {len(df)} issues...")
    analyze_topics(df)

    print(f"{c['g']}[INFO]{c['w']} Tagging initiatives based on keywords...")
    df = classify_initiatives(df)

    # Show bar chart for initiative tag counts
    plot_initiative_counts(df)

    print(f"\n{c['y']}Sample Output:{c['w']}")
    print(df[["key", "type", "summary", "initiatives"]].head(10).to_markdown(index=False))


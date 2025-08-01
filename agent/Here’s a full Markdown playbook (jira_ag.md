Here’s a full Markdown playbook (jira_agent_playbook.md) that walks you through turning your current JIRA analysis script into an autonomous Python agent, including installation, modular refactor, CLI, and Docker containerization.

⸻

📄 jira_agent_playbook.md

# 🧠 JIRA Analysis Agent – Playbook

This guide walks you through transforming a Python script that analyzes Apache JIRA issues into a deployable, Dockerized, CLI-based **agent** capable of fetching issues, analyzing topics, classifying initiatives, and outputting reports.

---

## 🔧 1. Prerequisites

Install Python and required libraries:

```bash
python3 -m venv venv
source venv/bin/activate

pip install -U requests pandas numpy scikit-learn matplotlib wordcloud

Optional (for future dashboard/ML extensions):

pip install -U transformers torch streamlit


⸻

🏗️ 2. Directory Structure

jira-agent/
│
├── agent/
│ ├── __init__.py
│ ├── core.py # Contains main logic
│ ├── analyzer.py # LDA, TF-IDF logic
│ ├── fetcher.py # JIRA API interaction
│ ├── classifier.py # Initiative tagging logic
│ └── visualizer.py # Charts and wordclouds
│
├── main.py # CLI entrypoint
├── requirements.txt
├── Dockerfile
└── README.md


⸻

📦 3. Core Python Modules

agent/fetcher.py

import requests
import pandas as pd

def fetch_issues(project, server):
jql = f"project = {project} ORDER BY created DESC"
response = requests.get(
f"{server}/rest/api/2/search",
timeout=20,
params={"jql": jql, "maxResults": 500, "fields": "summary,issuetype,components,assignee"},
headers={"Accept": "application/json"}
)
response.raise_for_status()
issues = response.json()["issues"]
return pd.DataFrame([{
"key": i["key"],
"type": i["fields"]["issuetype"]["name"],
"summary": i["fields"]["summary"],
"components": [comp["name"] for comp in i["fields"].get("components", [])],
"assignee": (i["fields"]["assignee"] or {}).get("displayName", "Unassigned")
} for i in issues])

agent/analyzer.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

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
return lda, feature_names, topics

agent/classifier.py

INITIATIVES = {
"Creativity": ["feature", "innovation"],
"Stability": ["bug", "fix", "refactor"],
"Performance": ["performance", "speed", "optimize"],
"Tech Debt": ["tech debt", "refactor", "cleanup"],
}

def map_initiatives(summary, mapping):
tags = []
lower = summary.lower()
for label, keywords in mapping.items():
if any(k in lower for k in keywords):
tags.append(label)
return tags

def classify(df):
df["initiatives"] = df["summary"].apply(lambda s: map_initiatives(s, INITIATIVES))
return df

agent/visualizer.py

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

def plot_wordclouds(lda, feature_names, n_top_words=10):
for topic_idx, topic in enumerate(lda.components_):
top_words = {feature_names[i]: topic[i] for i in topic.argsort()[:-n_top_words - 1:-1]}
wc = WordCloud(width=400, height=200, background_color='white').generate_from_frequencies(top_words)
plt.figure(figsize=(8,4))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.title(f"Topic {topic_idx + 1}")
plt.show()

def plot_initiative_counts(df):
all_tags = sum(df['initiatives'].tolist(), [])
counts = Counter(all_tags)
if counts:
labels, values = zip(*counts.items())
plt.bar(labels, values, color='skyblue')
plt.title("Initiative Tag Counts")
plt.ylabel("Number of Issues")
plt.show()


⸻

🚀 4. CLI Entrypoint

main.py

import argparse
from agent.fetcher import fetch_issues
from agent.analyzer import analyze_topics
from agent.classifier import classify
from agent.visualizer import plot_wordclouds, plot_initiative_counts

def main():
parser = argparse.ArgumentParser()
parser.add_argument("--project", type=str, default="ZOOKEEPER")
parser.add_argument("--server", type=str, default="https://issues.apache.org/jira")
args = parser.parse_args()

print(f"[INFO] Fetching JIRA issues for {args.project}...")
df = fetch_issues(args.project, args.server)

print(f"[INFO] Running topic modeling...")
lda, feature_names, topics = analyze_topics(df)
for idx, words in topics:
print(f"Topic {idx}: {', '.join(words)}")
plot_wordclouds(lda, feature_names)

print(f"[INFO] Classifying initiatives...")
df = classify(df)
plot_initiative_counts(df)

print("\nSample Output:")
print(df[["key", "type", "summary", "initiatives"]].head(10).to_markdown(index=False))

if __name__ == "__main__":
main()


⸻

🐳 5. Dockerfile (Optional)

FROM python:3.11-slim

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py", "--project", "ZOOKEEPER"]


⸻

📄 6. requirements.txt

requests
pandas
numpy
scikit-learn
matplotlib
wordcloud


⸻

🔁 7. Run It!

Local:

python main.py --project KAFKA

Docker:

docker build -t jira-agent .
docker run --rm jira-agent


⸻

🧠 Optional Next Steps

Feature Description
Redis Queue Add redis + rq to let the agent process jobs
Slack Bot Notify Slack with slack_sdk
Streamlit UI Live dashboard for initiative trends
GPT/NLP Upgrade Replace rules with transformer-based classifier
Jenkins Integration Run this weekly from CI/CD


⸻

🙌 You’re Done!

You now have a modular, extendable agent that can analyze Apache JIRA data and classify initiatives with topic modeling.

---

Would you like this exported as a `.md` file or zipped up with a sample project structure to get started faster?

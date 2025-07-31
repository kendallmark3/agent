import os
import pandas as pd
import matplotlib.pyplot as plt

def fetch_jira_data():
    # Placeholder - connect to JIRA API using token and pull stories
    print("Connecting to JIRA API...")
    return pd.DataFrame([
        {"summary": "Fix login bug", "points": 3, "category": "bug", "created": "2023-01-01", "resolved": "2023-01-05"},
        {"summary": "Add feature X", "points": 8, "category": "feature", "created": "2023-02-10", "resolved": "2023-02-20"},
    ])

def analyze(df):
    df['created'] = pd.to_datetime(df['created'])
    df['resolved'] = pd.to_datetime(df['resolved'])
    df['duration'] = (df['resolved'] - df['created']).dt.days
    summary = df.groupby("category")[["points", "duration"]].mean()
    print(summary)
    return summary

def generate_report(summary):
    summary.plot(kind='bar')
    plt.title("Avg Story Points and Duration by Category")
    plt.savefig("output/summary_report.png")
    print("Report saved to output/summary_report.png")

if __name__ == "__main__":
    df = fetch_jira_data()
    summary = analyze(df)
    generate_report(summary)

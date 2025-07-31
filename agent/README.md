
# InsightStrike: Automated Jira Analysis & Topic Visualization

## Overview

InsightStrike is a Python tool that connects to a Jira server, fetches issue data, analyzes issue summaries using AI topic modeling (LDA), categorizes issues by initiative types, and provides insightful visualizations like topic word clouds and initiative tag distributions.

This enables you to understand your organization’s pain points, priorities, and technical themes based on real Jira data — all with minimal setup and no intrusive access.

---

## Features

- Fetches issues from Jira using public REST API (no API key needed)
- Analyzes issue summaries using TF-IDF + Latent Dirichlet Allocation (LDA)
- Tags issues by initiatives (Creativity, Stability, Performance, Tech Debt)
- Visualizes topics with word clouds
- Shows initiative tag counts in bar charts
- Outputs a sample markdown table for quick reporting

---

## Installation

### 1. Install Python 3.11+ (if you don’t have it)

Using Homebrew on macOS:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

### 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows PowerShell
```

### 3. Install required Python packages

```bash
python3 -m pip install --upgrade pip
python3 -m pip install requests pandas numpy scikit-learn matplotlib wordcloud tabulate
```

---

## Usage

Save the script as `jira.py` and run it with:

```bash
python3 jira.py
```

---

## What the Topics Mean

The LDA model clusters related words in Jira issue summaries to reveal main themes:

- **Topic 1:** Flaky tests, ACL (access control), usage issues in Zookeeper
- **Topic 2:** Logging (Log4j), client interactions, network framework (Netty)
- **Topic 3:** Server support, software versions (possibly Java 13)
- **Topic 4:** Leader-follower roles in distributed systems, log fixes
- **Topic 5:** Security vulnerabilities (CVEs), upgrades (notably in 2022)

---

## Extending & Customizing

- Increase `maxResults` parameter in `fetch_jira_issues` to pull more tickets (max 1000 per request)
- Add pagination for thousands of tickets
- Expand or customize `INITIATIVES` keywords
- Export results to CSV, Excel, or PDF
- Integrate with Jenkins for automated scheduled runs
- Generate PDF reports with charts embedded

---

## Troubleshooting

If you see errors like `Missing optional dependency 'tabulate'`, run:

```bash
python3 -m pip install tabulate
```

---

## License

MIT License

---

Happy analyzing! 🚀

import requests

# Base URL and endpoint
BASE_URL = "https://issues.apache.org/jira"
API_ENDPOINT = "/rest/api/2/search"

# Example JQL query - adjust as needed
# This query gets 10 issues from the "ZOOKEEPER" project
params = {
    "jql": "project=ZOOKEEPER ORDER BY created DESC",
    "maxResults": 10,
    "fields": "key,summary,created,updated,status"
}

# Construct full URL
url = f"{BASE_URL}{API_ENDPOINT}"

# Make GET request (no auth needed for public projects)
response = requests.get(url, params=params)

# Check the response
if response.status_code == 200:
    data = response.json()
    print(f"Retrieved {len(data['issues'])} issues:")
    for issue in data['issues']:
        key = issue['key']
        summary = issue['fields']['summary']
        status = issue['fields']['status']['name']
        print(f"- {key}: {summary} [{status}]")
else:
    print(f"Request failed with status: {response.status_code}")
    print(response.text)
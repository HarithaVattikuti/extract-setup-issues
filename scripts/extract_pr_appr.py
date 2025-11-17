import requests

# List of repositories in "owner/repo" format
repos = [
    "actions/setup-java",
    "actions/setup-node",
    "actions/setup-python",
    "actions/setup-go",
    "actions/setup-dotnet",
    "actions/stale",
    "actions/labeler",
    "actions/publish-action"
]

token = 'YOUR_GITHUB_TOKEN'  # Replace with your token

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

for repo_full_name in repos:
    owner, repo = repo_full_name.split("/")
    print(f"\nChecking repository: {repo_full_name}")

    # Step 1: Get open pull requests
    prs_url = f'https://api.github.com/repos/{owner}/{repo}/pulls?state=open'
    prs_response = requests.get(prs_url, headers=headers)
    prs_response.raise_for_status()
    open_prs = prs_response.json()

    found_approved = False
    for pr in open_prs:
        pr_number = pr['number']
        reviews_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews'
        reviews_response = requests.get(reviews_url, headers=headers)
        reviews_response.raise_for_status()
        reviews = reviews_response.json()

        # Check for at least one approved review
        if any(review['state'] == 'APPROVED' for review in reviews):
            print(f"  APPROVED PR #{pr_number}: {pr['title']} - {pr['html_url']}")
            found_approved = True

    if not found_approved:
        print("  No open, approved PRs found.")

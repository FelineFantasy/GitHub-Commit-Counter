import datetime
import requests
from calendar import monthrange

def get_commits(username, year, token):
    url = "https://api.github.com/graphql"
    query = """
    query($username: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $username) {
        contributionsCollection(from: $from, to: $to) {
          totalCommitContributions
        }
      }
    }
    """
    variables = {
        "username": username,
        "from": f"{year}-01-01T00:00:00Z",
        "to": f"{year}-12-31T23:59:59Z"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
    data = response.json()
    return data["data"]["user"]["contributionsCollection"]["totalCommitContributions"]

def main():
    username = input("Введите GitHub username: ")
    year = int(input("Введите год (например, 2026): "))
    token = input("Введите GitHub токен: ")
    commits = get_commits(username, year, token)
    print(f"Всего коммитов за {year}: {commits}")

if __name__ == "__main__":
    main()

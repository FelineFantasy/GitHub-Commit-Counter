import datetime
import os
import requests
from calendar import monthrange

def load_env():
    """Загружает токен из .env файла."""
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("GITHUB_TOKEN="):
                    return line.strip().split("=", 1)[1]
    return None

def save_env(token):
    """Сохраняет токен в .env файл."""
    with open(".env", "w") as f:
        f.write(f"GITHUB_TOKEN={token}\n")
    try:
        os.chmod(".env", 0o600)
    except:
        pass

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

    token = load_env()
    if token:
        print("Токен загружен из .env")
    else:
        token = input("Введите GitHub токен: ")
        save_env(token)
        print("Токен сохранён в .env")

    commits = get_commits(username, year, token)
    print(f"Всего коммитов за {year}: {commits}")

if __name__ == "__main__":
    main()

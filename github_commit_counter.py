import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_token():
    """Получает токен из переменных окружения."""
    token = os.getenv("GITHUB_TOKEN")

    if token:
        print("Токен загружен из переменных окружения")
        return token

    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("GITHUB_TOKEN="):
                    token = line.strip().split("=", 1)[1]
                    print("Токен загружен из .env файла")
                    return token

    token = input("Введите GitHub токен: ")
    save_env(token)
    print("Токен сохранён в .env")
    return token

def save_env(token):
    """Сохраняет токен в .env файл."""
    with open(".env", "w") as f:
        f.write(f"GITHUB_TOKEN={token}\n")
    try:
        os.chmod(".env", 0o600)
    except:
        pass

def validate_username(username):
    """Проверяет корректность username."""
    if not username or len(username.strip()) < 1:
        return False
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-")
    return all(c in allowed_chars for c in username.strip())

def validate_year(year):
    """Проверяет корректность года."""
    current_year = datetime.now().year
    return 2008 <= year <= current_year

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

    try:
        response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
        response.raise_for_status()
        
        data = response.json()

        if "errors" in data:
            error_msg = data["errors"][0].get("message", "Unknown error")
            print(f"Ошибка API GitHub: {error_msg}")
            return None

        if not data.get("data") or not data["data"].get("user"):
            print("Пользователь не найден или нет данных")
            return None
 
        return data["data"]["user"]["contributionsCollection"]["totalCommitContributions"]

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
        return None
    except KeyError as e:
        print(f"Ошибка парсинга данных: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None

def main():
    while True:
        username = input("Введите GitHub username: ").strip()
        if validate_username(username):
            break
        print("Ошибка: неверный формат username. Используйте буквы, цифры и дефис.")

    while True:
        try:
            year = int(input("Введите год (например, 2026): "))
            if validate_year(year):
                break
            print(f"Ошибка: год должен быть между 2008 и {datetime.now().year}")
        except ValueError:
            print("Ошибка: введите число")

    token = get_token()
    commits = get_commits(username, year, token)

    if commits is not None:
        print(f"Всего коммитов за {year}: {commits}")
    else:
        print("Не удалось получить данные. Проверьте username, токен и подключение к интернету.")

if __name__ == "__main__":
    main()
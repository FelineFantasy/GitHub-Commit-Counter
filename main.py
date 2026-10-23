#!/usr/bin/env python3

"""
Fetch total GitHub user commits for a given year using GraphQL API.
"""

import os
from typing import List, Optional, Set
import argparse
import json
import sys
import requests
from datetime import datetime
import getpass


CONTRIBUTIONS_QUERY: str = """
query($username: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $username) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
    }
  }
}
"""


def get_token() -> str:
    """Получает токен из переменных окружения."""
    token: Optional[str] = os.getenv("GITHUB_TOKEN")

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

    token = getpass.getpass("Введите GitHub токен: ")
    save_env(token)
    print("Токен сохранён в .env")
    return token


def save_env(token: str) -> None:
    """Сохраняет токен в .env файл."""
    with open(".env", "w") as f:
        f.write(f"GITHUB_TOKEN={token}\n")
    try:
        os.chmod(".env", 0o600)
    except Exception:
        pass


def validate_username(username: str) -> bool:
    """Проверяет корректность username."""
    if not username or len(username.strip()) < 1:
        return False
    allowed_chars: Set[str] = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
    )
    return all(c in allowed_chars for c in username.strip())


def validate_year(year: int) -> bool:
    """Проверяет корректность года."""
    current_year: int = datetime.now().year
    return 2008 <= year <= current_year


def get_commits(username: str, year: int, token: str) -> Optional[int]:
    """Получает количество коммитов пользователя за указанный год."""
    url: str = "https://api.github.com/graphql"
    query: str = CONTRIBUTIONS_QUERY
    variables: dict = {
        "username": username,
        "from": f"{year}-01-01T00:00:00Z",
        "to": f"{year}-12-31T23:59:59Z"
    }
    headers: dict = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
        response.raise_for_status()

        data: dict = response.json()

        if "errors" in data:
            error_msg: str = data["errors"][0].get("message", "Unknown error")
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


def prompt_username() -> str:
    """Запрашивает username, пока не будет введён корректный."""
    while True:
        username: str = input("Введите GitHub username: ").strip()
        if validate_username(username):
            return username
        print("Ошибка: неверный формат username. Используйте буквы, цифры и дефис.")


def prompt_year() -> int:
    """Запрашивает год, пока не будет введён корректный."""
    while True:
        try:
            year: int = int(input("Введите год (например, 2026): "))
            if validate_year(year):
                return year
            print(f"Ошибка: год должен быть между 2008 и {datetime.now().year}")
        except ValueError:
            print("Ошибка: введите число")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Считает количество коммитов GitHub-пользователя за указанный год."
    )
    parser.add_argument("username", nargs="?", help="GitHub username")
    parser.add_argument("year", nargs="?", type=int, help="год (2008 или позже)")
    parser.add_argument(
        "--json",
        action="store_true",
        help="вывести результат в формате JSON (удобно для скриптов)",
    )
    return parser.parse_args(argv)


def print_error(message: str, as_json: bool = False) -> None:
    """Выводит ошибку в выбранном формате."""
    if as_json:
        print(json.dumps({"error": message}, ensure_ascii=False))
    else:
        print(message)


def main(argv: Optional[List[str]] = None) -> int:
    """Основная функция программы. Возвращает код выхода."""
    args: argparse.Namespace = parse_args(argv)
    username: str

    if args.username is None:
        username = prompt_username()
    else:
        username = args.username.strip()
        if not validate_username(username):
            print_error(
                "Ошибка: неверный формат username. Используйте буквы, цифры и дефис.",
                args.json,
            )
            return 1

    year: int

    if args.year is None:
        year = prompt_year()
    else:
        year = args.year
        if not validate_year(year):
            print_error(
                f"Ошибка: год должен быть между 2008 и {datetime.now().year}",
                args.json,
            )
            return 1

    token: str = get_token()
    commits: Optional[int] = get_commits(username, year, token)

    if commits is None:
        print_error(
            "Не удалось получить данные. Проверьте username, токен и подключение к интернету.",
            args.json,
        )
        return 1

    if args.json:
        print(
            json.dumps(
                {"username": username, "year": year, "commits": commits},
                ensure_ascii=False,
            )
        )
    else:
        print(f"Всего коммитов за {year}: {commits}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

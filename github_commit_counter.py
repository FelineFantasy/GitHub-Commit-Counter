import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from calendar import monthrange


def progress_bar(month):
    equals = "=" * month
    spaces = " " * (12 - month)
    bar = equals + ">" + spaces
    print(f"\r[{bar}] {month}/12", end="", flush=True)


def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    username = input("Введите GitHub username: ")

    while True:
        try:
            year = int(input("Введите год (например, 2026): "))
            if year < 2008 or year > datetime.datetime.now().year:
                print(f"Ошибка: год должен быть между 2008 и {datetime.datetime.now().year}")
                continue
            break
        except ValueError:
            print("Ошибка: год должен быть числом!")

    print(f"\nПодсчет коммитов для {username} за {year} год...\n")

    total_commits = 0

    try:
        for month in range(1, 13):
            last_day = monthrange(year, month)[1]
            from_date = f"{year}-{month:02d}-01"
            to_date = f"{year}-{month:02d}-{last_day:02d}"

            url = (
                f"https://github.com/{username}?tab=overview&from={from_date}"
                f"&to={to_date}"
            )
            driver.get(url)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            commits = soup.find_all("span", class_="color-fg-default ws-normal text-left")

            month_commits = 0
            for commit in commits:
                try:
                    text = commit.text.strip()
                    if text and " " in text:
                        month_commits += int(text.split()[1])
                except (ValueError, IndexError):
                    pass

            total_commits += month_commits
            progress_bar(month)

        print(f"\n\nвсего за {year} год: {total_commits} коммитов")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()

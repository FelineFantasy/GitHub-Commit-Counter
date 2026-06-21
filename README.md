# 📊 GitHub Commit Counter

Counts the number of a GitHub user's commits for a specified year using Selenium.

## 🎯 Features

- Asks for a username and a year
- Parses GitHub using Selenium
- Displays the commit count broken down by month
- Shows the total number of commits for the year

## 📦 Installation

```bash
pip install -r requirements.txt
```
*Note: Chrome and ChromeDriver are also required (must be in your PATH or in the same directory).*

## 🚀 Usage

```bash
python github_commit_counter.py
```

## 📝 Example Output

```text
Введите GitHub username: FelineFantasy
Введите год (например, 2026): 2026

Подсчет коммитов для FelineFantasy за 2026 год...

[===>         ] 3/12
[========>    ] 8/12
[============>] 12/12

всего за 2026 год: 161 коммитов
```

## ⚠️ Notes

- Runs in headless mode (the browser window will not open).
- Web scraping may fail if GitHub changes its HTML layout.

---

## 🙏 Inspiration

The progress bar was inspired by the beautiful progress bars in Cargo (Rust's build system).
I loved how it looked and decided to bring it into my Python project.
Thank you, Cargo! 🦀

---

## 👤 Author
- **FelineFantasy**
- **License**: MIT

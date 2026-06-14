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
Enter GitHub username: FelineFantasy
Enter year (e.g., 2026): 2026

Counting commits for FelineFantasy for 2026...

[===>         ] 3/12
[========>    ] 8/12
[============>] 12/12

Total for 2026: 161 commits
```

## ⚠️ Notes

- Runs in headless mode (the browser window will not open).
- Includes a `time.sleep(1)` delay between requests for stability.
- Web scraping may fail if GitHub changes its HTML layout.

## 👤 Author
- **FelineFantasy**
- **License**: MIT

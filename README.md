# 📊 GitHub Commit Counter

Counts the total number of commits made by a GitHub user in a specified year using the GitHub GraphQL API.

## 🎯 Features

- Asks for a GitHub username, a year, and a personal access token
- Uses GitHub's GraphQL API for fast and reliable data retrieval
- Displays the total number of commits for the specified year

## 📦 Installation

```bash
pip install -r requirements.txt
```

### Requirements
- Python 3.6+
- `requests` library
- GitHub Personal Access Token (see setup below)

### Setting up a GitHub Token
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name and select the `repo` scope (or `public_repo` for public repositories only)
4. Generate and copy your token

## 🚀 Usage

```bash
python github_commit_counter.py
```

### Interactive Input
The script will prompt you for:
1. **GitHub username** - The user whose commits you want to count
2. **Year** - The year to check (e.g., 2026)
3. **GitHub token** - Your personal access token (input will be hidden for security)

## 📝 Example Output

```text
Введите GitHub username: FelineFantasy
Введите год (например, 2026): 2026
Введите GitHub токен: ghp_xxxxxxxxxxxxxxxxxxxx

Всего коммитов за 2026: 161
```

## ⚠️ Notes

- A GitHub token is **required** to use the GitHub GraphQL API
- Rate limits apply based on your token type:
  - Unauthenticated: 60 requests/hour (not used in this script)
  - Authenticated: 5,000 requests/hour
- The token does not need to be stored in the code; it's entered at runtime

## 🛠 Technical Details

- Uses GitHub's official GraphQL API endpoint
- Queries `contributionsCollection` for accurate commit counting
- Handles date ranges automatically for the full year

## ❗ Common Issues

- **Invalid token**: Ensure your token has the correct permissions
- **Rate limiting**: If you hit the limit, wait an hour and try again
- **User not found**: Verify the username is spelled correctly

---

## 👤 Author
- **FelineFantasy**
- **License**: MIT

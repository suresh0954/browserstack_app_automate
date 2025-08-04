# browserstack_app_automate

End-to-end Appium tests on BrowserStack App Automate using Python, Pytest, and the BrowserStack SDK. Tests are run on Android devices using a sample `.apk` file.

---

## ✅ Features

- Run tests on real Android devices via BrowserStack
- Parallel test execution using `pytest-xdist`
- Sample test: Search functionality on Wikipedia Android app
- Uses `browserstack.yml` for build-level config
- Local `.apk` upload handled via BrowserStack CLI

---

## 🔧 Setup

## 1. Clone the repo
```bash
git clone https://github.com/suresh0954/browserstack_app_automate.git
cd browserstack_app_automate
```

## 2. Create virtual environment & install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Add credentials

Create a file named creds.sh in the root:
```Bash
export BROWSERSTACK_USERNAME="your_username"
export BROWSERSTACK_ACCESS_KEY="your_access_key"
```
Then run:
```
source creds.sh
```

## 📲 App Upload

Use the BrowserStack CLI to upload your app and get an app_url or app_id:

```Bash
browserstack-curl -u "$BROWSERSTACK_USERNAME:$BROWSERSTACK_ACCESS_KEY" \
-X POST "https://api-cloud.browserstack.com/app-automate/upload" \
-F "file=@/path/to/WikipediaSample.apk"
```
Update APP_ID in conftest.py accordingly.

## 🚀 Run Tests

Run all tests in parallel on 2 Android devices:

```Bash
pytest -n 2 tests/
```
Run a specific test file:
```Bash
pytest tests/test_sample_2.py

## 📁 Repo Structure

```
browserstack_app_automate/
├── tests/
│   └── test_sample_2.py
├── conftest.py
├── browserstack.yml
├── creds.sh
├── requirements.txt
└── README.md
```

## 🔍 Sample Test Flow

Tests the search feature in the Wikipedia Android app:

Launch app
Tap search button
Type a query
Wait for results to appear

## 🔐 Security & Best Practices

- Store credentials in creds.sh, not hardcoded in scripts
- Do not commit creds.sh or venv folder
- Add .gitignore with:

```Bash
venv/
__pycache__/
*.pyc
creds.sh
```



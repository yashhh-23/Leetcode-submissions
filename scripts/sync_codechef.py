import os
import json
import requests
from datetime import datetime

# ── Config from environment ──────────────────────────────────────────────────
USERNAME   = os.environ["CODECHEF_USERNAME"]
SESSION    = os.environ["CODECHEF_SESSION"]
GH_TOKEN   = os.environ["GITHUB_TOKEN"]
GH_REPO    = os.environ["GITHUB_REPOSITORY"]   # e.g. yashhh-23/Leetcode-submissions
OUTPUT_DIR = "codechef"

SESS_COOKIE_NAME = "SESS93b6022d778ee317bf48f7dbffe03173"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Cookie": f"{SESS_COOKIE_NAME}={SESSION}",
    "Referer": "https://www.codechef.com",
}

# ── Fetch accepted submissions from CodeChef API ─────────────────────────────
def fetch_submissions(limit=20, offset=0):
    url = f"https://www.codechef.com/api/submissions?username={USERNAME}&result=AC&limit={limit}&offset={offset}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()

def fetch_all_submissions():
    submissions = []
    offset = 0
    limit  = 20
    while True:
        data = fetch_submissions(limit=limit, offset=offset)
        batch = data.get("data", [])
        if not batch:
            break
        submissions.extend(batch)
        if len(batch) < limit:
            break
        offset += limit
    return submissions

# ── GitHub API helpers ────────────────────────────────────────────────────────
def gh_headers():
    return {
        "Authorization": f"token {GH_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

def get_existing_file(path):
    url = f"https://api.github.com/repos/{GH_REPO}/contents/{path}"
    resp = requests.get(url, headers=gh_headers())
    if resp.status_code == 200:
        return resp.json()
    return None

def commit_file(path, content, message):
    import base64
    url  = f"https://api.github.com/repos/{GH_REPO}/contents/{path}"
    b64  = base64.b64encode(content.encode()).decode()
    body = {"message": message, "content": b64}
    existing = get_existing_file(path)
    if existing:
        body["sha"] = existing["sha"]
    resp = requests.put(url, headers=gh_headers(), json=body)
    return resp.status_code in (200, 201)

# ── Extension map ────────────────────────────────────────────────────────────
EXT = {
    "C": "c", "C++": "cpp", "C++14": "cpp", "C++17": "cpp",
    "Java": "java", "Java 8": "java",
    "Python": "py", "Python3": "py", "PyPy3": "py",
    "JavaScript": "js",
}

def get_ext(lang):
    for key, ext in EXT.items():
        if key.lower() in lang.lower():
            return ext
    return "txt"

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print(f"Fetching accepted submissions for {USERNAME}...")
    subs = fetch_all_submissions()
    print(f"Found {len(subs)} accepted submissions.")

    synced = 0
    for sub in subs:
        problem_code = sub.get("problemCode") or sub.get("problem_code", "unknown")
        language     = sub.get("language", "txt")
        code         = sub.get("sourceCode") or sub.get("source_code", "")
        if not code:
            print(f"  Skipping {problem_code} — no source code returned.")
            continue

        ext      = get_ext(language)
        filename = f"{OUTPUT_DIR}/{problem_code}/{problem_code}.{ext}"
        message  = f"[CodeChef Sync] {problem_code} ({language})"

        ok = commit_file(filename, code, message)
        status = "✓" if ok else "✗"
        print(f"  {status} {problem_code}.{ext}")
        if ok:
            synced += 1

    print(f"\nDone — {synced}/{len(subs)} submissions synced to '{OUTPUT_DIR}/' folder.")

if __name__ == "__main__":
    main()

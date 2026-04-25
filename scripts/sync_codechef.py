import os
import base64
import requests

# ── Config ───────────────────────────────────────────────────────────────────
USERNAME         = os.environ["CODECHEF_USERNAME"]
SESSION          = os.environ["CODECHEF_SESSION"]
GH_TOKEN         = os.environ["GITHUB_TOKEN"]
GH_REPO          = os.environ["GITHUB_REPOSITORY"]
OUTPUT_DIR       = "codechef"
SESS_COOKIE_NAME = "SESS93b6022d778ee317bf48f7dbffe03173"

# Full browser-like headers to avoid 403
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": f"https://www.codechef.com/users/{USERNAME}",
    "Cookie": f"{SESS_COOKIE_NAME}={SESSION}",
}

# ── Fetch all AC submissions via /recent/user endpoint ───────────────────────
def fetch_page(page=1):
    url = f"https://www.codechef.com/recent/user?page={page}&user_handle={USERNAME}&status=AC"
    r = requests.get(url, headers=HEADERS, timeout=30)
    print(f"  [{r.status_code}] GET {url}")
    r.raise_for_status()
    return r.json()

def fetch_all():
    results = []
    page = 1
    while True:
        data    = fetch_page(page)
        batch   = data.get("data", [])
        if not batch:
            break
        results.extend(batch)
        total = int(data.get("totalPages", 1))
        if page >= total:
            break
        page += 1
    return results

# ── GitHub helpers ───────────────────────────────────────────────────────────
GH_HEADERS = {
    "Authorization": f"token {GH_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def get_sha(path):
    r = requests.get(
        f"https://api.github.com/repos/{GH_REPO}/contents/{path}",
        headers=GH_HEADERS,
    )
    if r.status_code == 200:
        j = r.json()
        if isinstance(j, dict):
            return j.get("sha")
    return None

def push_file(path, content, message):
    b64  = base64.b64encode(content.encode("utf-8", errors="replace")).decode()
    body = {"message": message, "content": b64}
    sha  = get_sha(path)
    if sha:
        body["sha"] = sha
    r = requests.put(
        f"https://api.github.com/repos/{GH_REPO}/contents/{path}",
        headers=GH_HEADERS,
        json=body,
    )
    return r.status_code in (200, 201)

# ── Language -> extension ────────────────────────────────────────────────────
EXT_MAP = {
    "c": "c", "c++": "cpp", "c++14": "cpp", "c++17": "cpp",
    "java": "java", "java8": "java",
    "python": "py", "python3": "py", "pypy3": "py",
    "javascript": "js",
}

def ext(lang):
    return EXT_MAP.get(lang.lower().replace(" ", "").replace("+", "p"), "txt")

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print(f"Fetching AC submissions for {USERNAME} ...")
    try:
        subs = fetch_all()
    except Exception as e:
        print(f"FATAL: {e}")
        raise

    print(f"Total AC submissions found: {len(subs)}")
    ok_count = 0

    for sub in subs:
        code_key  = sub.get("problemCode") or sub.get("problem_code", "UNKNOWN")
        lang      = sub.get("language") or sub.get("languageName", "txt")
        code      = sub.get("sourceCode") or sub.get("source_code", "")

        if not code:
            print(f"  SKIP {code_key} — no source code returned")
            continue

        file_ext  = ext(lang)
        path      = f"{OUTPUT_DIR}/{code_key}/{code_key}.{file_ext}"
        msg       = f"[CodeChef Sync] {code_key} ({lang})"

        ok = push_file(path, code, msg)
        print(f"  {'OK  ' if ok else 'FAIL'} {path}")
        if ok:
            ok_count += 1

    print(f"\nDone: {ok_count}/{len(subs)} pushed to '{OUTPUT_DIR}/'")

if __name__ == "__main__":
    main()

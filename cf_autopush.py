"""
Codeforces Auto-Pusher: Automatically push accepted Codeforces solutions to GitHub.
Uses the Codeforces API to fetch accepted submissions
and the GitHub API (PyGithub) to push them to a repository.
"""
import base64
import hashlib
import json
import os
import random
import re
import string
import sys
import time
from typing import Dict, List, Optional, Set

import requests
from github import Auth, Github, GithubException, InputGitTreeElement

# -- Configuration from environment variables --
CF_API_KEY = os.environ.get("CF_API_KEY", "")
CF_API_SECRET = os.environ.get("CF_API_SECRET", "")
CF_HANDLE = os.environ.get("CF_HANDLE", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "")
GITHUB_TARGET_DIR = os.environ.get("GITHUB_TARGET_DIR", "CodeForces")

CF_API_BASE = "https://codeforces.com/api"
STATE_FILE = f"{GITHUB_TARGET_DIR}/pushed.json" if GITHUB_TARGET_DIR else "pushed.json"
BATCH_SIZE = 50

LANG_EXT_MAP = {
    "GNU C": ".c", "GNU C11": ".c", "GNU C17": ".c", "C": ".c",
    "GNU C++": ".cpp", "GNU C++0x": ".cpp", "GNU C++11": ".cpp",
    "GNU C++14": ".cpp", "GNU C++17": ".cpp", "GNU C++17 (64)": ".cpp",
    "GNU C++20 (64)": ".cpp", "MS C++": ".cpp", "MS C++ 2017": ".cpp",
    "Clang++17 Diagnostics": ".cpp", "Clang++20 Diagnostics": ".cpp",
    "Java 8": ".java", "Java 11": ".java", "Java 17": ".java",
    "Java 21": ".java",
    "Python 2": ".py", "Python 3": ".py", "PyPy 2": ".py",
    "PyPy 3": ".py", "PyPy 3-64": ".py",
    "JavaScript": ".js", "Node.js": ".js",
    "TypeScript": ".ts",
    "Go": ".go",
    "Rust 2021": ".rs", "Rust": ".rs",
    "Kotlin": ".kt",
    "Scala": ".scala",
    "Ruby": ".rb",
    "PHP": ".php",
    "Haskell": ".hs",
    "D": ".d",
    "OCaml": ".ml",
    "Pascal": ".pas",
    "Perl": ".pl",
    "Swift": ".swift",
    "C#": ".cs", "Mono C#": ".cs",
}


def get_ext(lang: str) -> str:
    return LANG_EXT_MAP.get(lang, ".txt")


def make_api_sig(method: str, params: dict) -> tuple:
    rand = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    param_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    to_hash = f"{rand}/{method}?{param_str}#{CF_API_SECRET}"
    sig = hashlib.sha512(to_hash.encode()).hexdigest()
    return rand, sig


def cf_api_call(method: str, params: dict) -> dict:
    params["apiKey"] = CF_API_KEY
    params["time"] = int(time.time())
    rand, sig = make_api_sig(method, params)
    params["apiSig"] = rand + sig
    url = f"{CF_API_BASE}/{method}"
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "OK":
        raise RuntimeError(f"CF API error: {data.get('comment', data)}")
    return data["result"]


def fetch_accepted_submissions(handle: str) -> List[dict]:
    print(f"Fetching submissions for {handle}...")
    subs = cf_api_call("user.status", {"handle": handle, "from": 1, "count": 10000})
    accepted = [s for s in subs if s.get("verdict") == "OK"]
    print(f"Found {len(accepted)} accepted submissions.")
    return accepted


def get_source_code(sub: dict) -> Optional[str]:
    try:
        result = cf_api_call(
            "contest.status",
            {"contestId": sub["contestId"], "handle": CF_HANDLE,
             "from": 1, "count": 10000},
        )
        for s in result:
            if s["id"] == sub["id"]:
                raw = s.get("sourceBase64", "")
                if raw:
                    return base64.b64decode(raw).decode(errors="replace")
        return None
    except Exception as e:
        print(f"  Could not fetch source for submission {sub['id']}: {e}")
        return None


def sanitize(name: str) -> str:
    return re.sub(r'[^\w\s-]', '', name).strip().replace(" ", "_")


def load_state(repo, path: str) -> Set[int]:
    try:
        f = repo.get_contents(path)
        data = json.loads(f.decoded_content)
        return set(data.get("pushed", []))
    except GithubException:
        return set()


def save_state(repo, path: str, pushed_ids: Set[int], sha: Optional[str]):
    content = json.dumps({"pushed": sorted(pushed_ids)}, indent=2)
    if sha:
        repo.update_file(path, "Update pushed.json state", content, sha)
    else:
        repo.create_file(path, "Create pushed.json state", content)


def push_submissions(submissions: List[dict], pushed_ids: Set[int], repo):
    new_ids = set()
    tree_elements = []
    branch = repo.get_branch(repo.default_branch)
    base_tree = repo.get_git_tree(branch.commit.sha)

    to_push = [s for s in submissions if s["id"] not in pushed_ids]
    print(f"{len(to_push)} new submissions to push.")
    if not to_push:
        return

    for sub in to_push:
        problem = sub.get("problem", {})
        contest_id = sub.get("contestId", "unknown")
        problem_index = problem.get("index", "X")
        problem_name = sanitize(problem.get("name", "unknown"))
        lang = sub.get("programmingLanguage", "")
        ext = get_ext(lang)
        filename = f"{problem_index}_{problem_name}{ext}"
        folder = f"{GITHUB_TARGET_DIR}/{contest_id}" if GITHUB_TARGET_DIR else str(contest_id)
        path = f"{folder}/{filename}"

        print(f"  Fetching source for: {path}")
        source = get_source_code(sub)
        if source is None:
            print(f"  Skipping (no source).")
            continue

        blob = repo.create_git_blob(base64.b64encode(source.encode()).decode(), "base64")
        tree_elements.append(InputGitTreeElement(path=path, mode="100644", type="blob", sha=blob.sha))
        new_ids.add(sub["id"])
        time.sleep(0.5)

        if len(tree_elements) >= BATCH_SIZE:
            _commit_batch(repo, tree_elements, branch, base_tree, pushed_ids, new_ids)
            tree_elements = []
            new_ids = set()
            branch = repo.get_branch(repo.default_branch)
            base_tree = repo.get_git_tree(branch.commit.sha)

    if tree_elements:
        _commit_batch(repo, tree_elements, branch, base_tree, pushed_ids, new_ids)


def _commit_batch(repo, elements, branch, base_tree, pushed_ids, new_ids):
    new_tree = repo.create_git_tree(elements, base_tree)
    parent = repo.get_git_commit(branch.commit.sha)
    commit = repo.create_git_commit(
        f"[CF Sync] Add {len(elements)} Codeforces solution(s)",
        new_tree, [parent]
    )
    ref = repo.get_git_ref(f"heads/{repo.default_branch}")
    ref.edit(commit.sha)
    pushed_ids.update(new_ids)
    try:
        state_file = repo.get_contents(STATE_FILE)
        sha = state_file.sha
    except GithubException:
        sha = None
    save_state(repo, STATE_FILE, pushed_ids, sha)
    print(f"  Committed batch of {len(elements)} files.")


def main():
    if not all([CF_API_KEY, CF_API_SECRET, CF_HANDLE, GITHUB_TOKEN, GITHUB_REPO]):
        print("Missing required environment variables.")
        sys.exit(1)

    auth = Auth.Token(GITHUB_TOKEN)
    g = Github(auth=auth)
    repo = g.get_repo(GITHUB_REPO)
    print(f"Connected to repo: {repo.full_name}")

    pushed_ids = load_state(repo, STATE_FILE)
    print(f"Already pushed: {len(pushed_ids)} submissions.")

    submissions = fetch_accepted_submissions(CF_HANDLE)
    push_submissions(submissions, pushed_ids, repo)
    print("Done!")


if __name__ == "__main__":
    main()

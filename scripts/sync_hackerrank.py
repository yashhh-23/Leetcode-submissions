import os
import json
import requests
from datetime import datetime

HRANK_SESSION = os.environ['HRANK_SESSION']
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
GITHUB_REPO = os.environ['GITHUB_REPO']
DEST_FOLDER = 'hackerrank'

EXT_MAP = {
    'python': 'py', 'python3': 'py', 'java': 'java', 'java8': 'java',
    'java15': 'java', 'cpp': 'cpp', 'cpp14': 'cpp', 'cpp17': 'cpp',
    'c': 'c', 'javascript': 'js', 'typescript': 'ts', 'ruby': 'rb',
    'go': 'go', 'scala': 'scala', 'kotlin': 'kt', 'swift': 'swift',
    'csharp': 'cs', 'r': 'r', 'perl': 'pl', 'php': 'php', 'sql': 'sql',
}

HEADERS = {
    'Cookie': f'_hrank_session={HRANK_SESSION}',
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json',
}

GH_HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}


def get_submissions():
    submissions = []
    offset = 0
    limit = 50
    while True:
        url = f'https://www.hackerrank.com/rest/contests/master/submissions/?offset={offset}&limit={limit}'
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            print(f'Failed to fetch submissions: {resp.status_code}')
            break
        data = resp.json()
        models = data.get('models', [])
        if not models:
            break
        for sub in models:
            if sub.get('status') == 'Accepted':
                submissions.append(sub)
        if len(models) < limit:
            break
        offset += limit
    return submissions


def get_file_on_github(path):
    url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{path}'
    resp = requests.get(url, headers=GH_HEADERS)
    if resp.status_code == 200:
        return resp.json()
    return None


def push_to_github(path, content, message, sha=None):
    import base64
    url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{path}'
    encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    payload = {'message': message, 'content': encoded}
    if sha:
        payload['sha'] = sha
    resp = requests.put(url, headers=GH_HEADERS, json=payload)
    return resp.status_code in (200, 201)


def main():
    print('Fetching HackerRank accepted submissions...')
    submissions = get_submissions()
    print(f'Found {len(submissions)} accepted submissions.')

    synced = 0
    for sub in submissions:
        challenge_slug = sub.get('challenge', {}).get('slug', 'unknown')
        language = sub.get('language', 'txt').lower()
        code = sub.get('code', '')
        if not code:
            continue
        ext = EXT_MAP.get(language, 'txt')
        file_path = f'{DEST_FOLDER}/{challenge_slug}/solution.{ext}'
        existing = get_file_on_github(file_path)
        sha = existing['sha'] if existing else None
        commit_msg = f'[HackerRank Sync] {challenge_slug} ({language})'
        success = push_to_github(file_path, code, commit_msg, sha)
        if success:
            print(f'Synced: {file_path}')
            synced += 1
        else:
            print(f'Failed: {file_path}')

    print(f'Done! Synced {synced}/{len(submissions)} submissions.')


if __name__ == '__main__':
    main()

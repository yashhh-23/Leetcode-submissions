import os
import requests
import subprocess

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
}


def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'CMD ERROR: {result.stderr}')
    return result


def get_submissions():
    submissions = []
    offset = 0
    limit = 50
    while True:
        url = f'https://www.hackerrank.com/rest/contests/master/submissions/?offset={offset}&limit={limit}'
        resp = requests.get(url, headers=HEADERS)
        print(f'API status: {resp.status_code}')
        if resp.status_code != 200:
            print(f'Response: {resp.text[:300]}')
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


def setup_git():
    run('git config user.email "github-actions@github.com"')
    run('git config user.name "GitHub Actions"')
    repo_url = f'https://x-access-token:{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git'
    run(f'git remote set-url origin {repo_url}')


def main():
    print('Fetching HackerRank accepted submissions...')
    submissions = get_submissions()
    print(f'Found {len(submissions)} accepted submissions.')

    if not submissions:
        print('Nothing to sync.')
        return

    setup_git()
    synced = 0

    for sub in submissions:
        challenge_slug = sub.get('challenge', {}).get('slug', 'unknown')
        language = sub.get('language', 'txt').lower()
        code = sub.get('code', '')
        if not code:
            print(f'No code for: {challenge_slug}')
            continue
        ext = EXT_MAP.get(language, 'txt')
        file_path = f'{DEST_FOLDER}/{challenge_slug}/solution.{ext}'

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)

        run(f'git add {file_path}')
        commit_msg = f'[HackerRank Sync] {challenge_slug} ({language})'
        result = run(f'git diff --cached --quiet || git commit -m "{commit_msg}"')
        synced += 1
        print(f'Staged: {file_path}')

    if synced > 0:
        push = run('git push origin main')
        print(f'Push result: {push.stdout} {push.stderr}')

    print(f'Done! Synced {synced}/{len(submissions)} submissions.')


if __name__ == '__main__':
    main()

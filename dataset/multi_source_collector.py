import os
import json
import requests
from github import Github
import time
from tqdm import tqdm
import argparse

class DatasetCollector:
    def __init__(self, github_token=None):
        self.github_token = github_token
        self.github = Github(github_token) if github_token else None
        self.dataset = []

    def collect_from_github_search(self, query="vulnerable OR security flaw", language="python", max_repos=100):
        """Collect code snippets from GitHub search"""
        if not self.github:
            print("GitHub token required for GitHub collection")
            return

        repos = self.github.search_repositories(query=f"{query} language:{language}", sort="stars", order="desc")
        collected = 0

        for repo in tqdm(repos[:max_repos], desc="Collecting from GitHub"):
            try:
                contents = repo.get_contents("")
                for content_file in contents:
                    if content_file.type == "file" and content_file.name.endswith(('.py', '.c', '.cpp', '.js')):
                        try:
                            code = content_file.decoded_content.decode('utf-8')
                            if len(code) > 100 and len(code) < 5000:  # Reasonable size
                                self.dataset.append({
                                    'source': 'github',
                                    'repo': repo.full_name,
                                    'file': content_file.path,
                                    'language': language,
                                    'code': code,
                                    'vulnerable': self.detect_vulnerability(code, language),  # Basic detection
                                    'url': content_file.html_url
                                })
                                collected += 1
                                if collected >= 1000:  # Limit per source
                                    break
                        except:
                            continue
                if collected >= 1000:
                    break
            except:
                continue

    def collect_from_cve_database(self, max_cves=500):
        """Collect from NVD CVE database"""
        url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
        params = {
            'resultsPerPage': 100,
            'startIndex': 0
        }

        collected = 0
        while collected < max_cves:
            try:
                response = requests.get(url, params=params)
                data = response.json()

                for cve in data['result']['CVE_Items']:
                    cve_id = cve['cve']['CVE_data_meta']['ID']
                    description = cve['cve']['description']['description_data'][0]['value']

                    # Extract code-like snippets from description if any
                    if 'code' in description.lower() or any(kw in description.lower() for kw in ['sql', 'exec', 'eval', 'system']):
                        self.dataset.append({
                            'source': 'cve',
                            'cve_id': cve_id,
                            'description': description,
                            'language': 'unknown',
                            'code': '',  # Will need manual extraction
                            'vulnerable': True,
                            'url': f"https://nvd.nist.gov/vuln/detail/{cve_id}"
                        })
                        collected += 1

                params['startIndex'] += 100
                time.sleep(1)  # Rate limiting

            except:
                break

    def collect_from_owasp(self):
        """Collect from OWASP examples"""
        owasp_examples = [
            {
                'language': 'python',
                'code': '''
def vulnerable_sql(user_input):
    import sqlite3
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    cursor.execute(query)
    return cursor.fetchall()
                ''',
                'vulnerable': True,
                'type': 'sql_injection'
            },
            {
                'language': 'c',
                'code': '''
#include <stdio.h>
#include <string.h>

void vulnerable_buffer(char *input) {
    char buffer[10];
    strcpy(buffer, input);  // Buffer overflow
    printf("%s\\n", buffer);
}
                ''',
                'vulnerable': True,
                'type': 'buffer_overflow'
            }
        ]

        for example in owasp_examples:
            self.dataset.append({
                'source': 'owasp',
                'language': example['language'],
                'code': example['code'],
                'vulnerable': example['vulnerable'],
                'type': example.get('type', 'unknown')
            })

    def detect_vulnerability(self, code, language):
        """Basic vulnerability detection"""
        vulnerable_patterns = {
            'python': ['exec(', 'eval(', 'input(', 'os.system(', 'subprocess.call('],
            'c': ['strcpy(', 'sprintf(', 'gets(', 'scanf('],
            'javascript': ['eval(', 'document.write(', 'innerHTML']
        }

        patterns = vulnerable_patterns.get(language, [])
        return any(pattern in code for pattern in patterns)

    def save_dataset(self, output_file):
        """Save collected dataset"""
        with open(output_file, 'w') as f:
            json.dump(self.dataset, f, indent=2)
        print(f"Saved {len(self.dataset)} samples to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Multi-Source Dataset Collector")
    parser.add_argument("--github-token", help="GitHub API token")
    parser.add_argument("--output", default="dataset/multi_source_dataset.json", help="Output file")
    parser.add_argument("--max-github", type=int, default=50, help="Max GitHub repos")
    parser.add_argument("--max-cve", type=int, default=200, help="Max CVE entries")
    args = parser.parse_args()

    collector = DatasetCollector(args.github_token)

    print("Collecting from OWASP examples...")
    collector.collect_from_owasp()

    print("Collecting from CVE database...")
    collector.collect_from_cve_database(args.max_cve)

    if args.github_token:
        print("Collecting from GitHub...")
        for lang in ['python', 'c', 'cpp', 'javascript']:
            collector.collect_from_github_search(language=lang, max_repos=args.max_github)

    collector.save_dataset(args.output)

if __name__ == "__main__":
    main()
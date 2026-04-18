import os
import json
import requests
import time
from tqdm import tqdm
import argparse
from typing import Optional

try:
    from github import Github
except ImportError:
    Github = None

class DatasetCollector:
    def __init__(self, github_token=None):
        self.github_token = github_token
        self.github = Github(github_token) if (github_token and Github is not None) else None
        self.dataset = []

    def collect_from_github_search(self, query="vulnerable OR security flaw", language="python", max_repos=100):
        """Collect code snippets from GitHub search"""
        if not self.github:
            if self.github_token and Github is None:
                print("PyGithub is not installed. Install it to enable GitHub collection.")
            else:
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

    @staticmethod
    def _extract_cve_info(item: dict) -> Optional[dict]:
        """
        Normalize CVE payloads from both NVD v2.0 and v1.0 APIs.
        Returns None if required fields are missing.
        """
        # NVD 2.0 shape
        cve_block = item.get("cve")
        if cve_block:
            cve_id = cve_block.get("id")
            descriptions = cve_block.get("descriptions", [])
            description = next((d.get("value", "") for d in descriptions if d.get("lang") == "en"), "")
            if not description and descriptions:
                description = descriptions[0].get("value", "")
            if cve_id and description:
                return {"cve_id": cve_id, "description": description}

        # NVD 1.0 shape
        cve = item.get("cve", {})
        cve_meta = cve.get("CVE_data_meta", {})
        cve_id = cve_meta.get("ID")
        desc_entries = cve.get("description", {}).get("description_data", [])
        description = desc_entries[0].get("value", "") if desc_entries else ""
        if cve_id and description:
            return {"cve_id": cve_id, "description": description}

        return None

    def collect_from_cve_database(self, max_cves=500):
        """Collect CVE descriptions from NVD API."""
        endpoint = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        start_index = 0
        page_size = 100
        collected = 0

        while collected < max_cves:
            params = {"resultsPerPage": page_size, "startIndex": start_index}
            try:
                response = requests.get(endpoint, params=params, timeout=20)
                response.raise_for_status()
                data = response.json()

                items = data.get("vulnerabilities", [])
                if not items:
                    break

                for wrapped in items:
                    parsed = self._extract_cve_info(wrapped)
                    if not parsed:
                        continue

                    description = parsed["description"]
                    cve_id = parsed["cve_id"]

                    # Keep entries likely to contain executable/security-relevant behavior text
                    if "code" in description.lower() or any(
                        kw in description.lower() for kw in ["sql", "exec", "eval", "system", "command injection"]
                    ):
                        self.dataset.append({
                            "source": "cve",
                            "cve_id": cve_id,
                            "description": description,
                            "language": "unknown",
                            "code": "",  # No direct snippet in most CVE entries
                            "vulnerable": True,
                            "url": f"https://nvd.nist.gov/vuln/detail/{cve_id}"
                        })
                        collected += 1
                        if collected >= max_cves:
                            break

                start_index += page_size
                time.sleep(0.8)  # Basic rate limiting
            except Exception as e:
                print(f"CVE collection stopped at {collected} items due to error: {e}")
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
            },
            {
                'language': 'python',
                'code': '''
def safe_sql(user_input):
    import sqlite3
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))
    return cursor.fetchall()
                ''',
                'vulnerable': False,
                'type': 'safe_query'
            },
            {
                'language': 'c',
                'code': '''
#include <stdio.h>
#include <string.h>

void safe_buffer(char *input) {
    char buffer[10];
    strncpy(buffer, input, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\\0';
    printf("%s\\n", buffer);
}
                ''',
                'vulnerable': False,
                'type': 'safe_buffer_copy'
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
    print(f"Current samples: {len(collector.dataset)}")

    print("Collecting from CVE database...")
    collector.collect_from_cve_database(args.max_cve)
    print(f"Current samples: {len(collector.dataset)}")

    if args.github_token:
        print("Collecting from GitHub...")
        for lang in ['python', 'c', 'cpp', 'javascript']:
            collector.collect_from_github_search(language=lang, max_repos=args.max_github)

    collector.save_dataset(args.output)

if __name__ == "__main__":
    main()

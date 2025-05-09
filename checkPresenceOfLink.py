# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 11:49:37 2025

Exports pages linking to a target URL to Excel
replace with URL of site to scan on line 64
replace with to search for on line 65
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import pandas as pd

def find_pages_with_target_link(start_url, target_link):
    visited = set()
    queue = deque([start_url])
    domain = urlparse(start_url).netloc
    results = []

    while queue:
        current_url = queue.popleft()
        if current_url in visited:
            continue
        visited.add(current_url)

        try:
            response = requests.get(current_url, timeout=10)
            if response.status_code != 200:
                continue
        except requests.RequestException:
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        found_target = False

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            absolute_link = urljoin(current_url, href)

            # Check if this link matches the target
            if absolute_link.startswith(target_link):
                found_target = True

            # Crawl only internal links
            parsed_link = urlparse(absolute_link)
            if parsed_link.netloc == domain and absolute_link not in visited:
                queue.append(absolute_link)

        if found_target:
            print(f"Page linking to target found: {current_url}")
            results.append({'Page URL': current_url})

    # Export to Excel
    if results:
        df = pd.DataFrame(results)
        df.to_excel("pages_with_target_link4.xlsx", index=False)
        print("Results exported to 'pages_with_target_link.xlsx'")
    else:
        print("No pages found linking to the target.")

if __name__ == "__main__":
    start_url = "https://www.websitetoscan.com"
    target_link = "https://www.websitetoscan.com/link/"
    find_pages_with_target_link(start_url, target_link)

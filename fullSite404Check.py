# -*- coding: utf-8 -*-
"""
Crawls a site and finds all 404 (broken) or unreachable links, ignoring mailto and tel links. - creates excel sheet
Change url to one you want to scan on line 77
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import pandas as pd

def find_broken_links(start_url):
    visited_pages = set()
    broken_links = []
    queue = deque([start_url])
    domain = urlparse(start_url).netloc

    while queue:
        current_page = queue.popleft()
        if current_page in visited_pages:
            continue
        visited_pages.add(current_page)

        try:
            response = requests.get(current_page, timeout=10)
            if response.status_code != 200:
                print(f"Could not load page: {current_page}")
                continue
        except requests.RequestException:
            print(f"Request failed: {current_page}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href'].strip()

            # Skip mailto: and tel:
            if href.startswith('mailto:') or href.startswith('tel:'):
                continue

            absolute_link = urljoin(current_page, href)
            parsed_link = urlparse(absolute_link)

            # Only enqueue internal links
            if parsed_link.netloc == domain and absolute_link not in visited_pages:
                queue.append(absolute_link)

            # Check the link status
            try:
                link_response = requests.head(absolute_link, allow_redirects=True, timeout=10)
                if link_response.status_code == 404:
                    print(f"Broken link (404): {absolute_link} on page {current_page}")
                    broken_links.append({
                        'Source Page': current_page,
                        'Broken Link': absolute_link,
                        'Error Type': '404 Not Found'
                    })
            except requests.RequestException:
                print(f"Error checking link: {absolute_link}")
                broken_links.append({
                    'Source Page': current_page,
                    'Broken Link': absolute_link,
                    'Error Type': 'Failed to Load'
                })

    # Export results
    if broken_links:
        df = pd.DataFrame(broken_links)
        df.to_excel("full_site_broken_links_report.xlsx", index=False)
        print("Broken links exported to 'broken_links_report.xlsx'")
    else:
        print("No broken links found.")

if __name__ == "__main__":
    start_url = "https://www.yoursite.com"
    find_broken_links(start_url)

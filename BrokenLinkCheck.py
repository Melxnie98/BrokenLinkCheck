# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 15:00:11 2025

@author: MelanieLeonard
"""

import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin  # handle relative URLs

def check_broken_links(url, username, password):
    # Send a GET request with basic authentication
    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    # If page req is successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links
        links = soup.find_all('a', href=True)

        # Loop through links
        for link in links:
            link_url = link['href']
            link_text = link.get_text().strip()

            # Convert relative URL to absolute URL
            full_url = urljoin(url, link_url)

            # Make sure the link is not empty or fragment
            if full_url and full_url != "#":
                # Try to send a GET request to the link
                try:
                    link_response = requests.get(full_url, auth=HTTPBasicAuth(username, password))

                    # If 404 , print the broken & text
                    if link_response.status_code == 404:
                        print(f"Broken link: {full_url}")
                        print(f"Text: {link_text}")
                except requests.exceptions.RequestException as e:
                    # Catch other request exceptions (like invalid URLs)
                    print(f"Error with link: {full_url}")
                    print(f"Text: {link_text}")
                    print(f"Exception: {e}")
    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")

if __name__ == "__main__":
    url = input("Enter the URL to check for broken links: ")
    username = input("Enter your site username: ")
    password = input("Enter your site password: ")
    check_broken_links(url, username, password)

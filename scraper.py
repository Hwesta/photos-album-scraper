#!/usr/bin/env python3
import argparse
import re

import requests
from bs4 import BeautifulSoup


def filter_bg_image(attr):
    return attr and re.compile('background-image: url').search(attr)


def main(album_url):
    print(f"Fetching {album_url}")
    # Get URL?
    try:
        response = requests.get(album_url)
    except Exception:
        print(f"Error fetching {album_url}")
        return

    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    # Title: tag.name = title
    for tag in soup.find_all(True):
        print('TAG HERE', tag.name)
        if tag.name not in ('script', 'html', 'head', 'base', 'meta', 'link', 'style', 'body', 'svg', 'defs', 'radialgradient'):
            print(tag.name)
        if tag.name == 'div':
            print(tag.attrs)
    # for tag in soup.find_all(style=filter_bg_image):
    #     print(tag)
    # This isn't giving me the same thing I'm seeing in a browser
    # Look at manually saving as har file, using haralyzer package to work with it


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        "Scrapes Google Photos into static HTML page with images")
    parser.add_argument(
        'album_url', help='URL to Google photos album to scrape')
    args = parser.parse_args()
    main(**vars(args))

#!/usr/bin/env python3
import argparse
import json
import re

import requests
from bs4 import BeautifulSoup


class Album:
    """Handle fetching and parsing a Google Photo album"""

    PROTOBUF_REGEX = r"^AF_initDataCallback"

    def __init__(self, album_url):
        self.album_url = album_url
        self.soup = None
        self.protobuf = None

    def get_album(self, parser="html.parser"):
        """Fetch album from URL, parse to protobuf"""
        print(f"Fetching {self.album_url}")

        try:
            response = requests.get(self.album_url)
        except Exception:
            print(f"Error fetching {self.album_url}")
            return

        print(f"Parsing response with {parser}")
        self.soup = BeautifulSoup(response.text, features=parser)

        # Find the spot where the protobuf is defined
        target = self.soup.find_all(string=re.compile(self.PROTOBUF_REGEX))[0]
        start = target.find("[")
        end = target.rfind("]") + 1

        # Load the protobuf to json. If this works we probably have the right thing
        self.protobuf = json.loads(target[start:end])
        print("Found protobuf")

    def write_protobuf(self, protobuf_output):
        """Write the protobuf as formatted JSON."""
        print(f"Writing protobuf to {protobuf_output}")
        if self.protobuf is None:
            raise RuntimeError("Must run get_album() first")

        with open(protobuf_output, "w") as f:
            json.dump(self.protobuf, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Scrapes Google Photos into static HTML page with images"
    )
    parser.add_argument("album_url", help="URL to Google photos album to scrape")
    parser.add_argument(
        "--protobuf-output", help="Write the raw protobuf output to this file, if given"
    )
    args = parser.parse_args()

    album = Album(args.album_url)
    album.get_album()

    if args.protobuf_output:
        album.write_protobuf(args.protobuf_output)

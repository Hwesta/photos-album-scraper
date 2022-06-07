#!/usr/bin/env python3
import argparse
import json
import re

import requests
from bs4 import BeautifulSoup


def main(album_url, protobuf_output):
    print(f"Fetching {album_url}")

    # Get album
    try:
        response = requests.get(album_url)
    except Exception:
        print(f"Error fetching {album_url}")
        return

    print("Parsing response")
    soup = BeautifulSoup(response.text, features="html.parser")

    # find the spot where the protobuf is defined
    target = soup.find_all(string=re.compile("^AF_initDataCallback"))[0]
    start = target.find("[")
    end = target.rfind("]") + 1

    # load the protobuf to json
    protobuf = json.loads(target[start:end])

    print(f"found protobuf, writing to {protobuf_output}")

    # write to file
    with open(protobuf_output, "w") as f:
        json.dump(protobuf, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Scrapes Google Photos into static HTML page with images"
    )
    parser.add_argument("album_url", help="URL to Google photos album to scrape")
    parser.add_argument("protobuf_output", help="file to write")
    args = parser.parse_args()
    main(**vars(args))

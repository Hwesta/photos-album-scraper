#!/usr/bin/env python3
import argparse

from photoalbum.album import Album

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

    album.parse_enrichments()

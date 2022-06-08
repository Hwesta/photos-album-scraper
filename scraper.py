#!/usr/bin/env python3
import argparse

from photoalbum.album import Album

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Scrapes Google Photos into static HTML page with images"
    )
    parser.add_argument("album_url", help="URL to Google photos album to scrape")

    parser.add_argument(
        "--protobuf-input",
        help="Read the raw protobuf output from this file and use it",
    )
    parser.add_argument(
        "--protobuf-output", help="Write the raw protobuf output to this file, if given"
    )

    parser.add_argument(
        "--fetch", action="store_true", help="Fetch the album from the URL"
    )
    parser.add_argument(
        "--load", action="store_true", help="Load the protobuf from protobuf-input"
    )
    parser.add_argument("--parse", action="store_true", help="Parse the response")
    parser.add_argument("--ordering", action="store_true", help="ordering experiment")
    args = parser.parse_args()

    album = Album(args.album_url)
    if args.fetch:
        album.get_album()
    elif args.load:
        album.load_protobuf(args.protobuf_input)

    if args.protobuf_output:
        album.write_protobuf(args.protobuf_output)

    if args.parse:
        album.parse_enrichments()
        album.parse_images()

    if args.ordering:
        album.print_ordered()

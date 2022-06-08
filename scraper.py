#!/usr/bin/env python3
import argparse

from photoalbum.album import Album

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Scrapes Google Photos into static HTML page with images"
    )

    # Where to get data - 1 required
    parser.add_argument(
        "--fetch",
        metavar="URL",
        help="Fetch the album from this URl, if given",
    )
    parser.add_argument(
        "--load",
        metavar="FILENAME",
        help="Load the raw protobuf from this file, if given",
    )

    # What to do with it - any or all
    parser.add_argument(
        "--protobuf-output",
        metavar="FILENAME",
        help="Write the raw protobuf output to this file, if given",
    )
    parser.add_argument("--ordering", action="store_true", help="ordering experiment")
    parser.add_argument(
        "--render", metavar="FILENAME", help="Render HTML to this file, if given"
    )

    args = parser.parse_args()
    if not (args.fetch or args.load):
        parser.error("Must specify one of --fetch or --load")

    album = Album()
    if args.fetch:
        album.get_album(args.fetch)
    elif args.load:
        album.load_protobuf(args.load)

    if args.protobuf_output:
        album.write_protobuf(args.protobuf_output)

    album.parse_protobuf()

    if args.ordering:
        album.print_ordered()

    if args.render:
        album.render_html(args.render)

#!/usr/bin/env python3
import argparse
from pathlib import Path

from photoalbum.album import Album

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Scrapes a Google Photos album into static HTML page with images.\n"
    )

    # Where to get data - 1 required
    source_group = parser.add_argument_group(
        "Album Source",
        "Where to fetch the album from. Exactly one of these is required.",
    )
    source_group.add_argument(
        "--fetch",
        metavar="URL",
        help="Fetch the album from a URL",
    )
    source_group.add_argument(
        "--load",
        metavar="FILENAME",
        type=Path,
        help="Load the album info from a previously-saved protobuf file. See also --save-protobuf",
    )

    # What to do with it - any or all
    behaviour_group = parser.add_argument_group(
        "Behaviour", "All of these are optional. Probably you want --download --render"
    )
    behaviour_group.add_argument(
        "--download",
        action="store_true",
        help="Download images for the album into --output-directory",
    )
    behaviour_group.add_argument(
        "--render",
        action="store_true",
        help="Render the full album to HTML. See also --html-file-name",
    )
    behaviour_group.add_argument(
        "--save-protobuf",
        metavar="PATH/TO/FILENAME",
        type=Path,
        help="Write the album's protobuf output to this file. Useful for debugging, or saving the raw album info so the HTML can be changed and re-rendered. See also --load",
    )
    behaviour_group.add_argument(
        "--print-ordering", action="store_true", help="Print each item in sorted order"
    )

    # Output options
    config_group = parser.add_argument_group(
        "Output", "Override where the saved album goes"
    )
    config_group.add_argument(
        "--output-directory",
        metavar="PATH",
        type=Path,
        help="Path to where the album directory is created. --album-directory-name is inside this. Default: this directory",
    )
    config_group.add_argument(
        "--album-directory-name",
        metavar="DIRECTORY-NAME",
        type=Path,
        help="Name of the subdirectory to put the album in. Default: slugified album name",
    )
    config_group.add_argument(
        "--html-filename",
        metavar="FILENAME",
        type=Path,
        help="HTML output file name. Default: index.html",
    )

    args = parser.parse_args()
    if not (args.fetch or args.load):
        parser.error("Must specify one of --fetch or --load")
    if args.fetch and args.load:
        parser.error("Only one of --fetch and --load may be specified")

    album = Album()
    if args.fetch:
        album.get_album(args.fetch)
    elif args.load:
        album.load_protobuf(args.load)

    if args.save_protobuf:
        album.write_protobuf(args.save_protobuf)

    album.parse_protobuf()

    if args.output_directory:
        album.output_directory = args.output_directory
    if args.album_directory_name:
        album.album_directory = args.album_directory_name
    if args.html_filename:
        album.html_filename = args.html_filename

    if args.print_ordering:
        album.print_ordering()

    if args.download:
        album.download_images()

    if args.render:
        if not args.download:
            album.find_local_images()
        album.render_html()

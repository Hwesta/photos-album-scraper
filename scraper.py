#!/usr/bin/env python3
import argparse
from pathlib import Path

from photoalbum.album import Album

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrapes a Google Photos album into a static HTML page with locally saved images, including text and maps."
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

    # What to do with it - any or all can be given
    behaviour_group = parser.add_argument_group(
        "Behaviour", "All of these are optional. Probably you want --download --render"
    )
    behaviour_group.add_argument(
        "--download",
        action="store_true",
        help="Download all images in the album",
    )
    behaviour_group.add_argument(
        "--render",
        action="store_true",
        help="Render the album to a HTML page using local images. See also --html-file-name",
    )
    behaviour_group.add_argument(
        "--save-protobuf",
        metavar="PATH/TO/FILENAME",
        type=Path,
        help="Write the album's protobuf output to this file. Useful for debugging, or saving the album info so the HTML can be changed and re-rendered. See also --load",
    )
    behaviour_group.add_argument(
        "--print-ordering",
        action="store_true",
        help="Print each item in sorted order. Mostly for debugging.",
    )

    # Image download options
    image_group = parser.add_argument_group(
        "Image download",
        "Configure how images are downloaded. Only relevant with --download",
    )
    image_group.add_argument(
        "--max-width",
        type=int,
        default=None,
        help="Maximum width for downloaded images",
    )
    image_group.add_argument(
        "--max-height",
        type=int,
        default=None,
        help="Maximum height for downloaded images",
    )
    image_group.add_argument(
        "--redownload",
        action="store_true",
        help="Force all images to be downloaded, even if they already exist. Useful if --max-width or --max-height changed.",
    )

    # Output options
    config_group = parser.add_argument_group(
        "Output", "Override where the saved album goes."
    )
    config_group.add_argument(
        "--output-directory",
        metavar="PATH",
        type=Path,
        help="Path to where the album directory is created. `album-directory-name` is created inside here. Default: current directory",
    )
    config_group.add_argument(
        "--album-directory-name",
        metavar="DIRECTORY-NAME",
        type=Path,
        help="Name of the subdirectory to put the album images and HTML file in. Default: slugified album name",
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
        album.download_images(
            max_width=args.max_width,
            max_height=args.max_height,
            redownload=args.redownload,
        )

    if args.render:
        if not args.download:
            album.find_local_images()
        album.render_html()

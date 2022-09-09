import mimetypes
from pathlib import Path

import magic
import requests


class Image:
    """An image in an album

    [
        "AF1QipOlQgoYJGjKaFOMHJkYqQVH4zxkn9brxgwXHhq2", # Not the ID. part of productURL? seems stable-ish
        [
            "baseURL",
            <width>,
            <height>,
            null,
            [],
            null,
            [],
            null,
            null,
            [
                13155507
            ]
        ],
        <date, unix epoch, photo taken>,
        "TOt7ob2rr6UBovGSirT8orZJDaM", # not the ID, but stable across requests & remove/re-add to album
        <tz offset, seconds, probably for date taken>,
        <date, unix epoch, added to album?>,
        [
            "AF1QipMN6zXOdB5TdqYqMm_qJ4Q0699P" # data-actor-media-key - owner?
        ],
        [ # same in both images
            [
                2
            ],
            [
                31,
                false,
                true
            ],
            [
                36,
                false,
                true
            ],
            [
                8
            ],
            [
                21
            ],
            [
                19
            ],
            [
                22
            ]
        ],
        2,
        null,
        null,
        null,
        [],
        null,
        19222, # same in both images
        [],
        { # related to ordering?
            "101428965": [
                0,
                "vdh9cohf070000000000004k"  # this value changes when reordered
            ]
        }
    ],

    """

    ORDERING_DICT_IDX = 16
    ORDERING_KEY = "101428965"

    def __init__(self, protobuf):
        self.protobuf = protobuf
        self.render_template = "image.html.j2"
        self.ordering_str = None
        self.base_url = None
        self.width = None
        self.height = None
        self.file_id = None
        self.relative_path = None

    def __repr__(self):
        return repr(self.protobuf)

    def __str__(self):
        return f"Image: {self.file_id} {self.base_url} {self.width}x{self.height} path: {self.relative_path}"

    def parse_protobuf(self):
        self.base_url = self.protobuf[1][0]
        self.width = self.protobuf[1][1]
        self.height = self.protobuf[1][2]
        self.file_id = self.protobuf[3]
        self.ordering_str = self.protobuf[self.ORDERING_DICT_IDX][self.ORDERING_KEY][1]

    def download_image(
        self, directory: Path, max_width=None, max_height=None, redownload=False
    ):
        """Download the images from base_url"""
        # TODO videos?
        if self.find_local_image(directory):
            if redownload:
                print(f"Found {directory / self.relative_path}, overwriting")
            else:
                print(f"Found {directory / self.relative_path}, not re-downloading")
                return

        # Construct URL
        if max_width or max_height:
            max_width = max_width or self.width
            max_height = max_height or self.height
            url = f"{self.base_url}=w{max_width}-h{max_height}"
        else:
            url = f"{self.base_url}=d"

        # Get
        print(f"Downloading file from {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching {url}: {response.status_code}")
            return

        # Guess extension
        mimetype = magic.from_buffer(response.content, mime=True)
        extension = mimetypes.guess_extension(mimetype) or ""
        self.relative_path = Path(self.file_id).with_suffix(extension)

        # Write
        write_path = directory / self.relative_path
        print(f"Writing file to {write_path}")
        write_path.write_bytes(response.content)
        return write_path

    def find_local_image(self, directory: Path):
        """Check `directory` for the image"""
        matches = list(directory.glob(f"{self.file_id}.*"))
        if len(matches) == 0:
            print(f"No file found for {directory / self.file_id}.*")
            return
        elif len(matches) > 1:
            raise RuntimeError(f"Multiple files found for {directory / self.file_id}.*")
        self.relative_path = matches[0].relative_to(directory)
        print(f"Found {self.relative_path}")
        return self.relative_path

import itertools
import json
import re
from pathlib import Path
import datetime as dt

import jinja2
import requests
from bs4 import BeautifulSoup
from slugify import slugify

from .enrichments import Enrichments
from .image import Image


class Album:
    """Handle fetching and parsing a Google Photo album

    Album metadata protobuf:

    [
        "AF1QipMaVrVFbtt8l-Heg2t-7p0yod3BuybzNin9WkPwCbzhGCr0QMTr7Asw3SeLuNj0Rw",
        "test album",  # album name
        [
            1766970855000,  # album start date
            1767035799000,  # album end date
            null,
            null,
            1767052993626,
            [
                1766970855000,  # album start date again
                -28800000  # timezone offset, in milliseconds, may be missing
            ],
            [
                1767035799000,  # album end date again
                -28800000  # timezone offset, in milliseconds, may be missing
            ],
            1767054718292,
            1767054012534
        ],
        "https://video-downloads.googleusercontent.com/ADGPM2nptxkckt0nsBsoMEadvsFMhloS_0g65TP0a0ZYPBAub0Zsv8uAe-1mIm7Hg2bspZZrPiapMsBRsPgKedHluQ7g3Wx0GlR_jxlJLMD5zVpghijcfne4dms5cx1sIh8dVM-5vYLKjVon43Wmir7sByAuHwnXzaMhfDIBmkJZ7Q8FaXCgMegSwY3uPGEwbuDHgnYyw37km8gZossqI-Tvhopz25xl_KxF16MzIemSPIrs4NfzDxAMAI5HLbt1RHvkCLSAsC0Z",
        [
            "https://lh3.googleusercontent.com/pw/AP1GczPwrRdPOjEwHnFMPUBZcdBC7NO4FlOaD6V5zCiL_85z3MGAbAy2qMZCfTCmFZDhMCElLqf0efbSG08O61w50hJCCmEKuxJ9hhPLVBEP7NtUn_gbkXiN",
            4080,
            3072,
            null,
            null,
            null,
            null,
            null,
            [
                4080,
                3072,
                1,
                null,
                [
                    "Google",
                    "Pixel 8",
                    null,
                    6.9,
                    1.68,
                    715,
                    0.016665,
                    null,
                    1
                ]
            ],
            [
                8550514
            ],
            2,
            [
                [
                    1,
                    1
                ]
            ]
        ],
        [
            "AF1QipMONMVh7jZJYcnONYiiFbxYCw58",
            "112739106865382918830",
            null,
            null,
            null,
            [
                "AF1QipMONMVh7jZJYcnONYiiFbxYCw58",
                "112739106865382918830"
            ],
            null,
            null,
            null,
            null,
            null,
            [
                "Holly Becker",
                1,
                null,
                "Holly"
            ],
            [
                "https://lh3.googleusercontent.com/a/ACg8ocIA01_pYooL3Ql2i_N_R2VhyiJMORKC9Ze7yv8OGaxS-keH"
            ],
            null,
            null,
            null,
            null,
            [
                2
            ]
        ],
        [
            [
                31,
                0,
                1
            ],
            [
                36,
                0,
                1
            ],
            [
                8
            ],
            [
                21
            ],
            [
                24,
                0,
                1
            ],
            [
                25,
                0,
                1
            ],
            [
                32,
                0,
                1
            ]
        ],
        "AF1QipMaVrVFbtt8l-Heg2t-7p0yod3BuybzNin9WkPwCbzhGCr0QMTr7Asw3SeLuNj0Rw",
        1,
        [
            [
                "AF1QipMONMVh7jZJYcnONYiiFbxYCw58",
                "112739106865382918830",
                null,
                null,
                null,
                [
                    "AF1QipMONMVh7jZJYcnONYiiFbxYCw58",
                    "112739106865382918830"
                ],
                null,
                null,
                null,
                null,
                null,
                [
                    "Holly Becker",
                    1,
                    null,
                    "Holly"
                ],
                [
                    "https://lh3.googleusercontent.com/a/ACg8ocIA01_pYooL3Ql2i_N_R2VhyiJMORKC9Ze7yv8OGaxS-keH"
                ],
                null,
                null,
                null,
                null,
                [
                    2
                ]
            ]
        ],
        [
            1,
            1,
            [
                [
                    1,
                    1
                ],
                [
                    2,
                    1
                ],
                [
                    1,
                    2
                ],
                [
                    2,
                    2
                ],
                [
                    3,
                    1
                ]
            ],
            [
                3
            ]
        ],
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        "",
        "QkF1RXhRZkJBWkxKUVRRc19KekNndmQ3ZmR4bDRB",
        1,
        3,
        null,
        null,
        null,
        [
            19997
        ],
        0,
        null,
        [
            [
                [
                    "AF1QipMONMVh7jZJYcnONYiiFbxYCw58",
                    "112739106865382918830"
                ],
                null,
                null,
                [
                    "Holly Becker",
                    1,
                    null,
                    "Holly"
                ],
                [
                    1767054012534,
                    1767052993626
                ],
                1,
                null,
                null,
                null,
                null,
                null,
                [
                    "https://lh3.googleusercontent.com/a/ACg8ocIA01_pYooL3Ql2i_N_R2VhyiJMORKC9Ze7yv8OGaxS-keH"
                ],
                null,
                2
            ]
        ],
        null,
        [
            1,
            0
        ],
        1,
        "https://photos.app.goo.gl/PKvcAQ9jFEcGNvFFA",
        null,
        5,
        {
            "39": [
                null,
                null,
                null,
                null,
                [
                    3
                ],
                [
                    null,
                    10
                ]
            ],
            "117194011": [
                []
            ]
        }
    ],

    """

    PROTOBUF_REGEX = r"^AF_initDataCallback"
    IMAGE_ARRAY_INDEX = 1
    ALBUM_ARRAY_INDEX = 3
    ENRICHMENT_ARRAY_INDEX = 4

    HTML_TEMPLATE = "index.html.j2"

    def __init__(self) -> None:
        self.album_url: str | None = None
        self.soup: BeautifulSoup | None = None
        self.protobuf: list = []
        self.name: str = "default album name"
        self.start_date: dt.datetime = dt.datetime.now()
        self.end_date: dt.datetime = dt.datetime.now()
        self.enrichments: list[Enrichments] = []
        self.images: list[Image] = []

        self.output_directory = Path(".")
        self.album_directory: Path = Path("album-name")
        self.html_filename = "index.html"

    def get_album(self, album_url: str, parser: str = "html.parser") -> None:
        """Fetch album from URL, parse to protobuf"""
        self.album_url = album_url
        print(f"Fetching {self.album_url}")

        try:
            response = requests.get(self.album_url)
        except Exception:
            print(f"Error fetching {self.album_url}")
            return

        print(f"Parsing response with {parser}")
        self.soup = BeautifulSoup(response.text, features=parser)

        # Find the spot where the protobuf is defined
        possibilities = self.soup.find_all(string=re.compile(self.PROTOBUF_REGEX))
        target = possibilities[1]
        start = target.find("[")
        end = target.rfind("]") + 1

        # Load the protobuf to json. If this works we probably have the right thing
        self.protobuf = json.loads(target[start:end])
        print("Found protobuf")

    def load_protobuf(self, protobuf_file: Path) -> None:
        """Read the protobuf from a JSON file"""
        print(f"Loading protobuf from {protobuf_file}")
        with open(protobuf_file, "r") as f:
            self.protobuf = json.load(f)

    def write_protobuf(self, protobuf_file: Path) -> None:
        """Write the protobuf as formatted JSON."""
        if self.protobuf is None:
            raise RuntimeError("Must fetch or load album first")

        print(f"Writing protobuf to {protobuf_file}")
        with protobuf_file.open("w") as f:
            json.dump(self.protobuf, f, indent=4)

    def parse_start_end_dates(self) -> tuple[dt.datetime, dt.datetime]:
        album_protobuf = self.protobuf[self.ALBUM_ARRAY_INDEX]
        start_date_unix = album_protobuf[2][0]  # or [2][5][0]
        start_date_unix /= 1000  # convert from milliseconds to seconds
        try:
            start_date_timezone = album_protobuf[2][5][1]
        except IndexError:
            start_date_timezone = 8 * 60 * 60 * 100  # UTC-8
        start_date = dt.datetime.fromtimestamp(start_date_unix) + dt.timedelta(
            milliseconds=start_date_timezone
        )

        end_date_unix = album_protobuf[2][1]  # or [2][6][0]
        end_date_unix /= 1000  # convert from milliseconds to seconds
        try:
            end_date_timezone = album_protobuf[2][6][1]
        except IndexError:
            end_date_timezone = 8 * 60 * 60 * 100  # UTC-8
        end_date = dt.datetime.fromtimestamp(end_date_unix) + dt.timedelta(
            milliseconds=start_date_timezone
        )
        return start_date, end_date

    def parse_protobuf(self) -> None:
        """Parse the protobuf to get album, image, text and map info"""
        if self.protobuf is None:
            raise RuntimeError("Must fetch or load album first")
        self.name = self.protobuf[self.ALBUM_ARRAY_INDEX][1]
        self.start_date, self.end_date = self.parse_start_end_dates()
        self._parse_enrichments()
        self._parse_images()
        self.album_directory = Path(slugify(self.name))

    def _parse_images(self) -> None:
        """Parse the images array in the protobuf"""
        print("Parsing images")
        self.images = []
        for img in self.protobuf[self.IMAGE_ARRAY_INDEX]:
            image = Image(img)
            image.parse_protobuf()
            self.images.append(image)

    def _parse_enrichments(self) -> None:
        """Parse the text, maps and locations from the protobuf"""
        print("Parsing enrichments (text, maps, locations)")
        self.enrichments = []
        for enrichment in self.protobuf[self.ENRICHMENT_ARRAY_INDEX]:
            enrichment = Enrichments.create_enrichment(enrichment)
            if not enrichment:
                continue
            enrichment.parse_protobuf()
            self.enrichments.append(enrichment)

    @property
    def full_directory(self) -> Path:
        """Full output path"""
        return self.output_directory / self.album_directory

    def download_images(
        self,
        max_width: int | None = None,
        max_height: int | None = None,
        redownload: bool = False,
    ) -> None:
        """Download all images in the album to `full_directory`"""
        print(f"Downloading images to {self.full_directory}")
        self.full_directory.mkdir(parents=True, exist_ok=True)
        for image in self.images:
            image.download_image(
                self.full_directory,
                max_width=max_width,
                max_height=max_height,
                redownload=redownload,
            )

    def find_local_images(self) -> None:
        """Check `full_directory` to see if all images are there already"""
        print(f"Checking {self.full_directory} for existing images")
        for image in self.images:
            image.find_local_image(self.full_directory)

    def ordered_items(self) -> list[Enrichments | Image]:
        """All items in the album, sorted in display order"""
        assert self.enrichments
        assert self.images
        ordering_dict: dict[str, Enrichments | Image] = {
            x.ordering_str: x for x in self.enrichments + self.images
        }
        ordered_items = [ordering_dict[k] for k in sorted(ordering_dict)]

        # Set first/last in group flags
        for classname, adjacent_items in itertools.groupby(
            ordered_items, key=lambda x: type(x).__name__
        ):
            adjacent_items = list(adjacent_items)
            adjacent_items[0].first_in_group = True
            adjacent_items[-1].last_in_group = True

        return ordered_items

    def print_ordering(self) -> None:
        """Print the album items in sorted order"""
        for item in self.ordered_items():
            print(item)

    def render_html(self) -> Path:
        """Render the album to a HTML file."""
        env = jinja2.Environment(
            loader=jinja2.PackageLoader(__name__),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        page_template = env.get_template(self.HTML_TEMPLATE)
        html = page_template.render(album=self, items=self.ordered_items())
        html_file = self.full_directory / self.html_filename
        self.full_directory.mkdir(parents=True, exist_ok=True)
        print(f"Writing HTML to {html_file}")
        html_file.write_text(html)
        return html_file

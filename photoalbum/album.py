import json
import re
from pathlib import Path

import jinja2
import requests
from bs4 import BeautifulSoup
from slugify import slugify

from .enrichments import Enrichments
from .image import Image


class Album:
    """Handle fetching and parsing a Google Photo album"""

    PROTOBUF_REGEX = r"^AF_initDataCallback"
    IMAGE_ARRAY_INDEX = 1
    ALBUM_ARRAY_INDEX = 3
    ENRICHMENT_ARRAY_INDEX = 4

    HTML_TEMPLATE = "index.html.j2"

    def __init__(self) -> None:
        self.album_url: str | None = None
        self.soup = None
        self.protobuf: list | None = None
        self.name: str | None = None
        self.enrichments: list[Enrichments] | None = None
        self.images: list[Image] | None = None

        self.output_directory = Path(".")
        self.album_directory = None
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
        target = self.soup.find_all(string=re.compile(self.PROTOBUF_REGEX))[0]
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

    def parse_protobuf(self) -> None:
        """Parse the protobuf to get album, image, text and map info"""
        if self.protobuf is None:
            raise RuntimeError("Must fetch or load album first")
        self.name = self.protobuf[self.ALBUM_ARRAY_INDEX][1]
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
        return [ordering_dict[k] for k in sorted(ordering_dict)]

    def print_ordering(self) -> None:
        """Print the album items in sorted order"""
        for item in self.ordered_items():
            print(item)

    def render_html(self) -> Path:
        """Render the album to a HTML file."""
        env = jinja2.Environment(loader=jinja2.PackageLoader(__name__))
        page_template = env.get_template(self.HTML_TEMPLATE)
        html = page_template.render(album=self, items=self.ordered_items())
        html_file = self.full_directory / self.html_filename
        self.full_directory.mkdir(parents=True, exist_ok=True)
        print(f"Writing HTML to {html_file}")
        html_file.write_text(html)
        return html_file

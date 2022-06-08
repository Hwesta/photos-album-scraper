import json
import re

import requests
from bs4 import BeautifulSoup

from .enrichments import Enrichments
from .image import Image


class Album:
    """Handle fetching and parsing a Google Photo album"""

    PROTOBUF_REGEX = r"^AF_initDataCallback"
    IMAGE_ARRAY_INDEX = 1
    ALBUM_ARRAY_INDEX = 3
    ENRICHMENT_ARRAY_INDEX = 4

    def __init__(self):
        self.album_url = None
        self.soup = None
        self.protobuf = None
        self.name = None
        self.enrichments = None
        self.images = None

    def get_album(self, album_url, parser="html.parser"):
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

    def load_protobuf(self, protobuf_file):
        """Read the protobuf from a JSON file"""
        print(f"Loading protobuf from {protobuf_file}")
        with open(protobuf_file, "r") as f:
            self.protobuf = json.load(f)

    def write_protobuf(self, protobuf_file):
        """Write the protobuf as formatted JSON."""
        print(f"Writing protobuf to {protobuf_file}")
        if self.protobuf is None:
            raise RuntimeError("Must run get_album() first")

        with open(protobuf_file, "w") as f:
            json.dump(self.protobuf, f, indent=4)

    def parse_protobuf(self):
        self.name = self.protobuf[self.ALBUM_ARRAY_INDEX][1]
        print("name", self.name)

        self._parse_enrichments()
        self._parse_images()
        print()

    def _parse_images(self):
        print("Parsing images")
        self.images = []
        for img in self.protobuf[self.IMAGE_ARRAY_INDEX]:
            image = Image(img)
            image.parse_protobuf()
            print(image)
            self.images.append(image)

    def _parse_enrichments(self):
        print("Parsing enrichments")
        self.enrichments = []
        for enrichment in self.protobuf[self.ENRICHMENT_ARRAY_INDEX]:
            enrichment = Enrichments.create_enrichment(enrichment)
            if not enrichment:
                continue
            enrichment.parse_protobuf()
            print(enrichment)
            self.enrichments.append(enrichment)

    def print_ordered(self):
        ordering_dict = {x.ordering_str: x for x in self.enrichments + self.images}
        for k in sorted(ordering_dict.keys()):
            print(k, ordering_dict[k])

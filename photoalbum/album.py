import json
import re

import requests
from bs4 import BeautifulSoup

from .enrichments import Enrichments


class Album:
    """Handle fetching and parsing a Google Photo album"""

    PROTOBUF_REGEX = r"^AF_initDataCallback"
    IMAGE_ARRAY_INDEX = 1
    ENRICHMENT_ARRAY_INDEX = 4

    def __init__(self, album_url):
        self.album_url = album_url
        self.soup = None
        self.protobuf = None

    def get_album(self, parser="html.parser"):
        """Fetch album from URL, parse to protobuf"""
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

    def write_protobuf(self, protobuf_output):
        """Write the protobuf as formatted JSON."""
        print(f"Writing protobuf to {protobuf_output}")
        if self.protobuf is None:
            raise RuntimeError("Must run get_album() first")

        with open(protobuf_output, "w") as f:
            json.dump(self.protobuf, f, indent=4)

    def parse_enrichments(self):
        print("Parsing enrichments")
        self.enrichments = []
        for enrichment in self.protobuf[self.ENRICHMENT_ARRAY_INDEX]:
            enrichment = Enrichments.create_enrichment(enrichment)
            if not enrichment:
                continue
            enrichment.parse_protobuf()
            print(enrichment)
            self.enrichments.append(enrichment)

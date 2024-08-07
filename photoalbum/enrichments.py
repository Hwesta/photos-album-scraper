import typing as t


class Enrichments:
    """Parse an enrichment (text, location or map)

    [
        "AF1QipPIawvW8shUbT4NGrGEPaZdIEgTBE900SoMc-oudntXjsUWy5x4", # unclear
        null,
        null,
        null,
        null,
        null,
        null,
        [],
        null,
        null,
        null,
        null,
        [],
        null,
        null,
        [],
        {
            "99218341": [
                [
                    1, # number indicating what type
                    # type specific info
                ]
            ],
            "101428965": [
                # Ordering info, probably
            ]
        }
    ]
    """

    DICT_IDX = 16
    DATA_KEY = "99218341"
    ORDERING_KEY = "101428965"  # probably

    @classmethod
    def create_enrichment(cls, enrichment: list) -> Enrichments | None:
        child_cls = cls.get_class(enrichment)
        if not child_cls:
            return None
        return child_cls(enrichment)

    @classmethod
    def get_class(cls, arr: list) -> type[Enrichments]:
        data_dict = arr[cls.DICT_IDX]
        type_key = data_dict[cls.DATA_KEY][0][0]
        # class_map can't be a class attribute because the child classes aren't defined when the class is defined
        class_map = {
            1: Text,
            2: Location,
            3: Map,
        }
        return class_map[type_key]

    def __init__(self, protobuf: list) -> None:
        self.protobuf = protobuf
        self.ordering_str: str | None = None
        self.render_template: str = ""

    def __repr__(self) -> str:
        return repr(self.protobuf)

    def parse_protobuf(self) -> None:
        raise NotImplementedError("Implement in child class")


class Text(Enrichments):
    """A text box

    "99218341": [
        [
            1,
            [
                "text to display"
            ]
        ]
    ]
    """

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super(Text, self).__init__(*args, **kwargs)
        self.render_template = "text.html.j2"
        self.text_str: str | None = None

    def __str__(self) -> str:
        return f'Text: "{self.text_str}"'

    def parse_protobuf(self) -> None:
        data_dict = self.protobuf[self.DICT_IDX]
        self.text_str = data_dict[self.DATA_KEY][0][1][0]
        self.ordering_str = data_dict[self.ORDERING_KEY][1]


class Location(Enrichments):
    """A location

    "99218341": [
        [
            2,
            null,
            [
                null,
                [
                    [
                        3,
                        [
                            [
                                "6090683026124656563", # unsure
                                "13515749891091067787" # unsure
                            ]
                        ],
                        null,
                        "Big text (main location)",
                        "small text (subscript, eg province, country)",
                        [
                            <lat>,
                            <lon>
                        ],
                        null,
                        0
                    ]
                ]
            ]
        ]
    ]
    """

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super(Location, self).__init__(*args, **kwargs)
        self.render_template = "location.html.j2"
        self.main_text: str | None = None
        self.additional_text: str | None = None
        self.lat: float | None = None
        self.lon: float | None = None

    def __str__(self) -> str:
        return f'Location: "{self.main_text}", "{self.additional_text}" ({self.lat},{self.lon})'

    def parse_protobuf(self, protobuf_is_inner: bool = False) -> None:
        if protobuf_is_inner:  # inside a Map
            inner_array = self.protobuf
        else:  # standalone
            data_dict = self.protobuf[self.DICT_IDX]
            inner_array = data_dict[self.DATA_KEY][0][2][1][0]
            self.ordering_str = data_dict[self.ORDERING_KEY][1]
        self.main_text = inner_array[3]
        try:
            self.additional_text = inner_array[4]
        except IndexError:
            self.additional_text = ""
        try:
            # Move decimal over 7 digits for lat/lon
            self.lat = inner_array[5][0] * 10**-7
            self.lon = inner_array[5][1] * 10**-7
        except (IndexError, TypeError):
            self.lat = None
            self.lon = None


class Map(Enrichments):
    """A map going between two locations

    "99218341": [
        [
            3,
            null,
            null,
            [
                null,
                null,
                null,
                [
                    [ # source
                        3,
                        [
                            [
                                "6090683026124656563",
                                "13515749891091067787"
                            ]
                        ],
                        null,
                        "big text (main location)",
                        "small text (context info)",
                        [
                            <lat>,
                            <lon>
                        ],
                        null,
                        0
                    ]
                ],
                [
                    [ # destination
                        3,
                        [
                            [
                                "5177074476702594547",
                                "1472861389740886636"
                            ]
                        ],
                        null,
                        "big text (main location)",
                        "small text (context info)",
                        [
                            <lat>,
                            <lon>
                        ],
                        null,
                        0
                    ]
                ]
            ]
        ]
    ],
    """

    def __init__(self, *args: t.Any, **kwargs: t.Any):
        super(Map, self).__init__(*args, **kwargs)
        self.render_template = "map.html.j2"
        self.source_location: Location | None = None
        self.destination_location: Location | None = None

    def __str__(self) -> str:
        return f"Map: {self.source_location} to {self.destination_location}"

    def parse_protobuf(self) -> None:
        data_dict = self.protobuf[self.DICT_IDX]
        source_protobuf = data_dict[self.DATA_KEY][0][3][3][0]
        dest_protobuf = data_dict[self.DATA_KEY][0][3][4][0]
        self.source_location = Location(source_protobuf)
        self.source_location.parse_protobuf(protobuf_is_inner=True)
        self.destination_location = Location(dest_protobuf)
        self.destination_location.parse_protobuf(protobuf_is_inner=True)
        self.ordering_str = data_dict[self.ORDERING_KEY][1]

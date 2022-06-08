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
    def create_enrichment(cls, enrichment):
        child_cls = cls.get_class(enrichment)
        if not child_cls:
            return None
        return child_cls(enrichment)

    @classmethod
    def get_class(cls, arr):
        data_dict = arr[cls.DICT_IDX]
        type_key = data_dict[cls.DATA_KEY][0][0]
        # class_map can't be a class attribute because the child classes aren't defined when the class is defined
        class_map = {
            1: Text,
            2: Location,
            3: Map,
        }
        return class_map[type_key]

    def __init__(self, protobuf):
        self.protobuf = protobuf
        self.ordering_str = None

    def __repr__(self):
        return repr(self.protobuf)

    def parse_protobuf(self):
        raise NotImplementedError("Implement in child class")

    def to_html(self):
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

    def __init__(self, *args, **kwargs):
        super(Text, self).__init__(*args, **kwargs)
        self.text_str = None

    def __str__(self):
        return f'Text: "{self.text_str}"'

    def parse_protobuf(self):
        data_dict = self.protobuf[self.DICT_IDX]
        self.text_str = data_dict[self.DATA_KEY][0][1][0]


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

    def __init__(self, *args, **kwargs):
        super(Location, self).__init__(*args, **kwargs)
        self.main_text = None
        self.additional_text = None
        self.lat = None
        self.lon = None

    def __str__(self):
        return f'Location: "{self.main_text}", "{self.additional_text}" ({self.lat},{self.lon})'

    def parse_protobuf(self, protobuf_is_inner=False):
        # Allow reuse by Map
        if protobuf_is_inner:
            inner_array = self.protobuf
        else:
            data_dict = self.protobuf[self.DICT_IDX]
            inner_array = data_dict[self.DATA_KEY][0][2][1][0]
        self.main_text = inner_array[3]
        self.additional_text = inner_array[4]
        # Move decimal over 7 digits for lat/lon
        self.lat = inner_array[5][0] * 10**-7
        self.lon = inner_array[5][1] * 10**-7


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

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        self.source_location = None
        self.destination_location = None

    def __str__(self):
        return f"Map: {self.source_location} to {self.destination_location}"

    def parse_protobuf(self):
        data_dict = self.protobuf[self.DICT_IDX]
        source_protobuf = data_dict[self.DATA_KEY][0][3][3][0]
        dest_protobuf = data_dict[self.DATA_KEY][0][3][4][0]
        self.source_location = Location(source_protobuf)
        self.source_location.parse_protobuf(protobuf_is_inner=True)
        self.destination_location = Location(dest_protobuf)
        self.destination_location.parse_protobuf(protobuf_is_inner=True)

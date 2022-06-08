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
        "TOt7ob2rr6UBovGSirT8orZJDaM",
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

    def __init__(self, protobuf):
        self.protobuf = protobuf
        self.ordering_str = None
        self.base_url = None
        self.width = None
        self.height = None

    def __repr__(self):
        return repr(self.protobuf)

    def __str__(self):
        return f"Image: {self.base_url} {self.width}x{self.height}"

    def parse_protobuf(self):
        self.base_url = self.protobuf[1][0]
        self.width = self.protobuf[1][1]
        self.height = self.protobuf[1][2]

    def to_html(self):
        raise NotImplementedError("Implement in child class")

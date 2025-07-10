from enum import Enum


class ScrapType(Enum):
    ONE_LINE = "oneline"

class ScrapOrderType(Enum):
    LIKE = "likes"
    VIEW = "views"
    LATEST = "latest"
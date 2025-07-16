from enum import Enum


class ScrapType(Enum):
    ONE_LINE = "oneline"
    FIVE_LINE = "fiveline"
    INSIGHT = "insight"
    BASIC = "basic"


class ScrapOrderType(Enum):
    LIKE = "likes"
    VIEW = "views"
    LATEST = "latest"
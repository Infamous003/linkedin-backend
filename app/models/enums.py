from enum import Enum

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class Status(str, Enum):
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    DRAFT = "draft"


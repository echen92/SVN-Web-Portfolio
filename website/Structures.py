"""
This class represents the structure of a project in a Subversion repo
"""


class Assignment:
    def __init__(self, name, date, revision, author, message=None):
        self.name = name
        self.date = date
        self.revision = revision
        self.author = author
        self.message = message
        self.files = {}  # File objects keyed by file path


class File:
    def __init__(self, name, size, ftype):
        self.name = name
        self.size = size
        self.ftype = ftype
        self.revisions = {}  # RevInfo objects keyed by revision number


class RevInfo:
    def __init__(self, date, author, message=None):
        self.date = date
        self.author = author
        self.message = message
class Album:
    def __init__(self, interpret, name):
        self.interpret = interpret
        self.name = name

    def __str__(self):
        return "[Interpret: {}; Album: {}]".format(self.interpret, self.name)


class AlbumParseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def parse(string, delimiter):
    parts = string.split(delimiter)
    if len(parts) > 2:
        raise AlbumParseError("Couldn't parse '{}' because it contains the delimiter '{}' more than one time!".format(string, delimiter))
    trimmed = [part.strip() for part in parts]
    return Album(trimmed[0], trimmed[1])

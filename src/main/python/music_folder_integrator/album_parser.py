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
    index_of_first_delimiter = string.index(delimiter)
    interpret = string[:index_of_first_delimiter].strip().replace("_", " ")
    album_name = string[index_of_first_delimiter + 1:].strip().replace("_", " ")
    return Album(interpret, album_name)

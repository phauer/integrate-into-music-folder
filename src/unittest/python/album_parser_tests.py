import unittest

from music_folder_integrator import album_parser


class AlbumParserTests(unittest.TestCase):
    def test_happy_path(self):
        album = album_parser.parse("My Band - Super Album", "-")
        self.assertEqual("My Band", album.interpret)
        self.assertEqual("Super Album", album.name)

    def test_multiple_delimiter(self):
        album = album_parser.parse("My Band - Super Album - 2006", "-")
        self.assertEqual("My Band", album.interpret)
        self.assertEqual("Super Album - 2006", album.name)

    def test_remove_underscores(self):
        album = album_parser.parse("My_Band - Super_Album", "-")
        self.assertEqual("My Band", album.interpret)
        self.assertEqual("Super Album", album.name)

if __name__ == '__main__':
    unittest.main()


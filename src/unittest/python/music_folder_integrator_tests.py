import sys
import unittest

from path import path  # path.py
from treelib import Tree

import music_folder_integrator

TEST_OUTPUT = path('..\\..\\..\\test_output\\').abspath()

# TODO test simulate


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        TEST_OUTPUT.rmtree()
        TEST_OUTPUT.makedirs()

    def test_happy_path(self):
        test_name = sys._getframe().f_code.co_name
        root_path = TEST_OUTPUT.joinpath(test_name)
        clear(root_path)
        downloads_source_tree = Tree()
        downloads_source_tree.create_node(identifier="download_folder_1")
        downloads_source_tree.create_node(identifier="Should Not Be Used", parent="download_folder_1")
        downloads_source_tree.create_node(identifier="F-S-F---W-I-B--T-I-H--2013", parent="download_folder_1")
        downloads_source_tree.create_node(identifier="F S F - W I B, T I H (2013)", parent="F-S-F---W-I-B--T-I-H--2013")
        downloads_source_tree.create_node(identifier="song1.mp3", parent="F S F - W I B, T I H (2013)")
        downloads_source_tree.create_node(identifier="song2.mp3", parent="F S F - W I B, T I H (2013)")
        downloads_source_tree.create_node(identifier="song3.mp3", parent="F S F - W I B, T I H (2013)")
        print("Creating test downloads folder:")
        downloads_source_tree.show()
        created_download_root_folder = create_dummy_download_folder(root_path, downloads_source_tree)

        music_folder = root_path.joinpath("music_folder_1")
        if not music_folder.exists():
            music_folder.mkdir()

        music_folder_integrator.integrate(
            source_download_folder=created_download_root_folder,
            target_music_folder=music_folder,
            simulate=False)

        expected_music_folder_tree = Tree()
        expected_music_folder_tree.create_node(identifier="music_folder_1")
        expected_music_folder_tree.create_node(identifier="F S F", parent="music_folder_1")
        expected_music_folder_tree.create_node(identifier="W I B, T I H (2013)", parent="F S F")
        expected_music_folder_tree.create_node(identifier="song1.mp3", parent="W I B, T I H (2013)")
        expected_music_folder_tree.create_node(identifier="song2.mp3", parent="W I B, T I H (2013)")
        expected_music_folder_tree.create_node(identifier="song3.mp3", parent="W I B, T I H (2013)")
        print("Expecting the following music folder:")
        expected_music_folder_tree.show()
        self.compare_actual_folder_with_tree(root_path, expected_music_folder_tree)

    def compare_actual_folder_with_tree(self, root, tree):
        root_name = tree.root
        root_path = root.joinpath(root_name)
        print(root_path)
        self.assertTrue(root_path.exists(), "The path {} should exist, but doesn't".format(root_path))
        children = tree.children(root_name)
        for children in children:
            subtree = tree.subtree(children.identifier)
            self.compare_actual_folder_with_tree(root_path, subtree)


def create_dummy_download_folder(root, tree):
    root_name = tree.root
    root_path = root.joinpath(root_name)

    if not root_path.exists():
        print("Creating {}".format(root_path))
        if root_name.endswith(".mp3"):
            root_path.touch()
        else:
            root_path.mkdir()

    children = tree.children(root_name)
    for children in children:
        subtree = tree.subtree(children.identifier)
        create_dummy_download_folder(root_path, subtree)
    return root_path


def clear(folder):
    if folder.exists():
        folder.rmtree()
    folder.makedirs()


if __name__ == '__main__':
    unittest.main()

import os
import shutil
import unittest
from integrate_into_music_folder import music_folder_integrator
from treelib import Node, Tree

TEST_OUTPUT = os.path.abspath('..\\test_output\\')


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        shutil.rmtree(TEST_OUTPUT)
        os.makedirs(TEST_OUTPUT)

    def test_print(self):
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
        created_download_root_folder = create_dummy_download_folder(TEST_OUTPUT, downloads_source_tree)

        music_folder = os.path.join(TEST_OUTPUT, "music_folder_1")
        clear(music_folder)

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
        self.compare_actual_folder_with_tree(TEST_OUTPUT, expected_music_folder_tree)

    def compare_actual_folder_with_tree(self, root, tree):
        root_name = tree.root
        root_path = os.path.join(root, root_name)
        print(root_path)
        self.assertTrue(os.path.exists(root_path), "The path {} should exist, but doesn't".format(root_path))
        children = tree.children(root_name)
        for children in children:
            subtree = tree.subtree(children.identifier)
            self.compare_actual_folder_with_tree(root_path, subtree)


def create_dummy_download_folder(root, tree):
    root_name = tree.root
    root_path = os.path.join(root, root_name)

    if not os.path.exists(root_path):
        print("Creating {}".format(root_path))
        if root_name.endswith(".mp3"):
            open(root_path, 'a').close()
        else:
            os.mkdir(root_path)

    children = tree.children(root_name)
    for children in children:
        subtree = tree.subtree(children.identifier)
        create_dummy_download_folder(root_path, subtree)
    return root_path


def clear(music_folder):
    if os.path.exists(music_folder):
        shutil.rmtree(music_folder)
    os.makedirs(music_folder)


if __name__ == '__main__':
    unittest.main()

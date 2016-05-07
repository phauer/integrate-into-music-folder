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

        # TODO compare precisely utilizing a tree data structure
        new_album_folder = os.path.join(music_folder, "F S F", "W I B, T I H (2013)")
        self.assertTrue(os.path.exists(new_album_folder), "The folder {} doesn't exist".format(new_album_folder))
        copied_files = os.listdir(new_album_folder)
        self.assertTrue(len(copied_files) > 0)  # TODO check for each mp3 file


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

import unittest

from path import path  # path.py
from treelib import Tree

from music_folder_integrator import integrator

TEST_OUTPUT = path('../../../test_output').abspath()
# set "Working Directory" to project root, when running this test directly out of the IDE


class IntegratorTests(unittest.TestCase):
    def setUp(self):
        if TEST_OUTPUT.exists():
            TEST_OUTPUT.rmtree()
        TEST_OUTPUT.makedirs()
        test_name = self.id().split(".")[-1]
        self.root_path = TEST_OUTPUT.joinpath(test_name)
        self.root_path.makedirs()
        print("====== {} ====== ".format(test_name))

    def test_happy_path(self):
        downloads_source_tree = Tree()
        downloads_source_tree.create_node(identifier="download_folder")
        downloads_source_tree.create_node(identifier="Should Not Be Used", parent="download_folder")
        downloads_source_tree.create_node(identifier="F-S-F---W-I-B--T-I-H--2013", parent="download_folder")
        downloads_source_tree.create_node(identifier="F S F - W I B, T I H (2013)", parent="F-S-F---W-I-B--T-I-H--2013")
        downloads_source_tree.create_node(identifier="song1.mp3", parent="F S F - W I B, T I H (2013)")
        downloads_source_tree.create_node(identifier="song2.mp3", parent="F S F - W I B, T I H (2013)")
        downloads_source_tree.create_node(identifier="song3.mp3", parent="F S F - W I B, T I H (2013)")
        created_download_root_folder = create_dummy_download_folder_with_output(self.root_path, downloads_source_tree)

        music_folder = self.root_path.joinpath("music_folder")
        music_folder.mkdir()

        integrator.integrate(
            source_download_folder=created_download_root_folder,
            target_music_folder=music_folder,
            ask_before_copy=False)

        expected_music_folder_tree = Tree()
        expected_music_folder_tree.create_node(identifier="music_folder")
        expected_music_folder_tree.create_node(identifier="F S F", parent="music_folder")
        expected_music_folder_tree.create_node(identifier="W I B, T I H (2013)", parent="F S F")
        expected_music_folder_tree.create_node(identifier="song1.mp3", parent="W I B, T I H (2013)")
        expected_music_folder_tree.create_node(identifier="song2.mp3", parent="W I B, T I H (2013)")
        expected_music_folder_tree.create_node(identifier="song3.mp3", parent="W I B, T I H (2013)")
        self.compare_actual_folder_with_tree_with_output(self.root_path, expected_music_folder_tree)

    def test_multiple_delimiter_remove_underscore(self):
        downloads_source_tree = Tree()
        downloads_source_tree.create_node(identifier="download_folder")
        downloads_source_tree.create_node(identifier="S P-T O F T T-2016-C4", parent="download_folder")
        downloads_source_tree.create_node(identifier="S_P-T_O_F_T_T-2016-C4", parent="S P-T O F T T-2016-C4")
        downloads_source_tree.create_node(identifier="song1.mp3", parent="S_P-T_O_F_T_T-2016-C4")
        created_download_root_folder = create_dummy_download_folder_with_output(self.root_path, downloads_source_tree)

        music_folder = self.root_path.joinpath("music_folder")
        music_folder.mkdir()

        integrator.integrate(
            source_download_folder=created_download_root_folder,
            target_music_folder=music_folder,
            ask_before_copy=False)

        expected_music_folder_tree = Tree()
        expected_music_folder_tree.create_node(identifier="music_folder")
        expected_music_folder_tree.create_node(identifier="S P", parent="music_folder")
        expected_music_folder_tree.create_node(identifier="T O F T T-2016-C4", parent="S P")
        expected_music_folder_tree.create_node(identifier="song1.mp3", parent="T O F T T-2016-C4")
        self.compare_actual_folder_with_tree_with_output(self.root_path, expected_music_folder_tree)

    def test_latest_folder_contains_nothing(self):
        downloads_source_tree = Tree()
        downloads_source_tree.create_node(identifier="download_folder")
        downloads_source_tree.create_node(identifier="Should Not Be Used", parent="download_folder")
        downloads_source_tree.create_node(identifier="F-S-F---W-I-B--T-I-H--2013", parent="download_folder")
        created_download_root_folder = create_dummy_download_folder_with_output(self.root_path, downloads_source_tree)

        music_folder = self.root_path.joinpath("music_folder")
        music_folder.mkdir()

        with self.assertRaisesRegex(integrator.IntegrationError, "'The latest folder .* has no child folder.'"):
            integrator.integrate(
                source_download_folder=created_download_root_folder,
                target_music_folder=music_folder,
                ask_before_copy=False)

    def compare_actual_folder_with_tree_with_output(self, root_path, expected_music_folder_tree):
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


def create_dummy_download_folder_with_output(root_path, downloads_source_tree):
    print("Creating test downloads folder:")
    downloads_source_tree.show()
    created_download_root_folder = create_dummy_download_folder(root_path, downloads_source_tree)
    return created_download_root_folder


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

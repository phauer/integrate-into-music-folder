import click
from music_folder_integrator import album_parser
from path import path


def integrate(source_download_folder: path, target_music_folder: path, ask_before_copy: bool):
    if not target_music_folder.exists():
        raise IntegrationError("The target folder '{}' doesn't exist.".format(target_music_folder))
    latest_folder = source_download_folder.joinpath(get_latest_folder(source_download_folder))
    print("Analyzing latest file {}".format(latest_folder))
    if len(latest_folder.listdir()) == 0:
        raise IntegrationError("The latest folder '{}' has no child folder.".format(latest_folder))
    downloads_album_folder = latest_folder.listdir()[0]
    album = album_parser.parse(downloads_album_folder.basename(), "-")
    print("Parsed album folder name {}. Result: {}".format(downloads_album_folder.basename(), album))
    target_interpret_folder = create_interpret_folder_if_necessary(album.interpret, target_music_folder, ask_before_copy)

    wanted_target_album_folder = target_interpret_folder.joinpath(album.name)
    if wanted_target_album_folder.exists():
        raise IntegrationError("The target album folder {} already exists.".format(wanted_target_album_folder))
    print("I'm going to copy \n\t{} \n\tto \n\t{}".format(downloads_album_folder, wanted_target_album_folder))
    if (ask_before_copy and click.confirm('Are you okay with this?')) or not ask_before_copy:
        downloads_album_folder.copytree(wanted_target_album_folder)
        click.echo("Copied successfully")
        print("Cleanup: Removing old folder in downloads folder: {}".format(latest_folder))
        latest_folder.rmtree()
        return wanted_target_album_folder


def create_interpret_folder_if_necessary(interpret: str, target_music_folder: path, ask_before_copy: bool) -> path:
    target_interpret_folder = target_music_folder.joinpath(interpret)
    if target_interpret_folder.exists():
        print("The following Interpret folder will be used: {}".format(target_interpret_folder))
    else:
        print("The following Interpret folder will be created: {}".format(target_interpret_folder))
        if (ask_before_copy and click.confirm('Are you okay with this?')) or not ask_before_copy:
            target_interpret_folder.mkdir()
    return target_interpret_folder


def get_latest_folder(dir_path: path) -> str:
    files = [file for file in dir_path.listdir()]
    files.sort(key=lambda file: dir_path.joinpath(file).getctime(), reverse=True)
    return files[0]


class IntegrationError(Exception):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return repr(self.value)

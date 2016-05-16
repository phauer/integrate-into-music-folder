import click
from music_folder_integrator import album_parser


def integrate(source_download_folder, target_music_folder, simulate):
    if not target_music_folder.exists():
        raise IntegrationError("The target folder {} doesn't exist.".format(target_music_folder))
    latest_folder = source_download_folder.joinpath(get_latest_folder(source_download_folder))
    print("Analyzing latest file {}".format(latest_folder))
    if len(latest_folder.listdir()) == 0:
        raise IntegrationError("The latest folder {} has no child folder.".format(latest_folder))
    downloads_album_folder = latest_folder.listdir()[0]
    album = album_parser.parse(downloads_album_folder.basename(), "-")
    print("Parsed album folder name {}. Result: {}".format(downloads_album_folder.basename(), album))
    target_interpret_folder = create_interpret_folder_if_necessary(album.interpret, target_music_folder, simulate)

    wanted_target_album_folder = target_interpret_folder.joinpath(album.name)
    if wanted_target_album_folder.exists():
        raise IntegrationError("The target album folder {} already exists.".format(wanted_target_album_folder))
    print("I'm going to copy \n\t{} \n\tto \n\t{}".format(downloads_album_folder, wanted_target_album_folder))
    if simulate:
        print("This was only a simulation. Nothing happened so far.")
    else:
        if click.confirm('Are you okay with this?'):
            downloads_album_folder.copytree(wanted_target_album_folder)
            click.echo("Copied successfully")
            print("Cleanup: Removing old folder in downloads folder: {}".format(downloads_album_folder))
            downloads_album_folder.rmtree()
        else:
            click.echo("Process was aborted.")


def create_interpret_folder_if_necessary(interpret, target_music_folder, simulate):
    target_interpret_folder = target_music_folder.joinpath(interpret)
    if target_interpret_folder.exists():
        print("The following Interpret folder will be used: {}".format(target_interpret_folder))
    else:
        print("The following Interpret folder will be created: {}".format(target_interpret_folder))
        if not simulate:
            target_interpret_folder.mkdir()
    return target_interpret_folder


def get_latest_folder(dir_path):
    files = [file for file in dir_path.listdir()]
    files.sort(key=lambda file: dir_path.joinpath(file).getctime(), reverse=True)
    return files[0]


class IntegrationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

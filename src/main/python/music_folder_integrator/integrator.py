from music_folder_integrator import album_parser


def integrate(source_download_folder, target_music_folder, simulate):
    if not target_music_folder.exists():
        raise IntegrationError("The target folder {} doesn't exist.".format(target_music_folder))
    print("Analyzing {}. Target: {}".format(source_download_folder, target_music_folder))
    latest_folder = source_download_folder.joinpath(get_latest_folder(source_download_folder))
    print("Analyzing latest file {}".format(latest_folder))
    if len(latest_folder.listdir()) == 0:
        raise IntegrationError("The latest folder {} has no child folder.".format(latest_folder))
    downloads_album_folder = latest_folder.listdir()[0]
    print("Parsing album folder name '{}'".format(downloads_album_folder.basename()))
    album = album_parser.parse(downloads_album_folder.basename(), "-")
    print("Parsing result: {}".format(album))
    target_interpret_folder = create_interpret_folder_if_necessary(album.interpret, target_music_folder, simulate)

    print("Moving {} into {}".format(downloads_album_folder, target_interpret_folder))
    downloads_album_folder.move(target_interpret_folder)

    target_album_folder_old_name = target_interpret_folder.joinpath(downloads_album_folder.basename())
    wanted_target_album_folder = target_interpret_folder.joinpath(album.name)
    print("Renaming from {} to {}".format(target_album_folder_old_name, wanted_target_album_folder))
    target_album_folder_old_name.rename(wanted_target_album_folder)


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

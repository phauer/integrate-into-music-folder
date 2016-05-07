import os
import album_parser
import shutil


# TODO use PyBuilder
# TODO add year if not present
def integrate(source_download_folder, target_music_folder, simulate):
    # TODO better use path.py module. http://stackoverflow.com/a/58417
    print("Analyzing {}. Target: {}".format(source_download_folder, target_music_folder))
    latest_folder = os.path.join(source_download_folder, get_latest_folder(source_download_folder))
    print("Analyzing latest file {}".format(latest_folder))
    actual_album_folder_name = os.listdir(latest_folder)[0]
    print("Parsing album folder name '{}'".format(actual_album_folder_name))
    album = album_parser.parse(actual_album_folder_name, "-")
    print("Parsing result: {}".format(album))
    target_interpret_folder = create_interpret_folder_if_necessary(album.interpret, target_music_folder, simulate)

    actual_album_folder_path = os.path.join(latest_folder, actual_album_folder_name)
    print("Moving {} into {}".format(actual_album_folder_path, target_interpret_folder))
    shutil.move(src=actual_album_folder_path, dst=target_interpret_folder)

    target_album_folder = os.path.join(target_interpret_folder, actual_album_folder_name)
    wanted_target_album_folder = os.path.join(target_interpret_folder, album.name)
    print("Renaming from {} to {}".format(target_album_folder, wanted_target_album_folder))
    os.rename(src=target_album_folder, dst=wanted_target_album_folder)


def create_interpret_folder_if_necessary(interpret, target_music_folder, simulate):
    target_interpret_folder = os.path.join(target_music_folder, interpret)
    if os.path.exists(target_interpret_folder):
        print("The following Interpret folder will be used: {}".format(target_interpret_folder))
    else:
        print("The following Interpret folder will be created: {}".format(target_interpret_folder))
        if not simulate:
            os.mkdir(target_interpret_folder)
    return target_interpret_folder


def get_latest_folder(dir_path):
    files = [file for file in os.listdir(dir_path)]
    files.sort(key=lambda file: os.path.getctime(os.path.join(dir_path, file)), reverse=True)
    return files[0]


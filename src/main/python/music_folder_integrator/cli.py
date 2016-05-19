import sys
import click
from path import path
from os.path import expanduser
sys.path.append("..")
# print(sys.path)
from music_folder_integrator import integrator


@click.command()
@click.option('--src', type=click.Path(exists=True, file_okay=False, dir_okay=True), default=expanduser("~\Downloads"), prompt="Source download folder", help='Source download folder. e.g. C:\\Users\\User\\Downloads')
@click.option('--dist', type=click.Path(exists=True, file_okay=False, dir_okay=True), default=expanduser("~\Music"), prompt="Target music folder", help='Target music folder. e.g. C:\\Users\\User\\Music')
@click.option('--ask-before-copy', is_flag=True, default=False, help="Ask the user before the actual coping happens")
def execute(src, dist, ask_before_copy):
    """Integrates a album folder in the download folder into your music library."""

    src_path = path(src)
    dist_path = path(dist)
    try:
        integrator.integrate(
            source_download_folder=src_path,
            target_music_folder=dist_path,
            ask_before_copy=ask_before_copy)
    except integrator.IntegrationError as e:
        print("An error occurred: {}".format(e))

if __name__ == '__main__':
    execute()


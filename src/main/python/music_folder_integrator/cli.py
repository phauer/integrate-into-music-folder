import sys
import click
from path import path  # path.py
from os.path import expanduser
sys.path.append("..")
# print(sys.path)
from music_folder_integrator import integrator


# python cli.py --simulate --src=C:\Users\Ahoi\Downloads\JDownloader --dist=D:\Music

@click.command()
@click.option('--src', type=click.Path(exists=True, file_okay=False, dir_okay=True), default=expanduser("~\Downloads"), prompt="Source download folder", help='Source download folder. e.g. C:\\Users\\User\\Downloads')
@click.option('--dist', type=click.Path(exists=True, file_okay=False, dir_okay=True), default=expanduser("~\Music"), prompt="Target music folder", help='Target music folder. e.g. C:\\Users\\User\\Music')
@click.option('--simulate', is_flag=True, default=False, help="Only output the necessary actions. Don't do it")
def execute(src, dist, simulate):
    """Integrates a album folder in the download folder into your music library."""

    # TODO use click.confirm to ask for final permission before actual copying. maybe this makes simulate mode obsolete.
    # value = click.prompt('writer peter')
    # if value == "peter":
    #     print("peter!!!")
    # if click.confirm('Do you want to continue?'):
    #     click.echo('Well done!')
    src_path = path(src)
    dist_path = path(dist)
    click.echo('src: {}'.format(src_path))
    click.echo('dist: {}'.format(dist_path))
    click.echo('simulate: {}'.format(simulate))
    try:
        integrator.integrate(
            source_download_folder=src_path,
            target_music_folder=dist_path,
            simulate=simulate)
    except integrator.IntegrationError as e:
        print("An error occurred: {}".format(e))

if __name__ == '__main__':
    execute()


from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
# use_plugin("python.coverage")
use_plugin("python.install_dependencies")

default_task = ['clean', 'publish']


@init
def set_properties(project):
    project.depends_on_requirements("requirements.txt")


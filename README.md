# integrate-into-music-folder
TODO description, installation and usage

## Development

### Getting Started
- requires Python 3.5. Test with `python3 --version`.

Install pip and venv if you haven't already.
```
$ sudo apt install python-pip
$ sudo apt install python3-venv # or sudo apt install virtualenv
```

Project:
```
# git clone and move to project directory
$ python3 -m venv venv #or virtualenv -p python3 venv
$ . venv-activate.sh
$ pip install pybuilder
$ pyb install_dependencies
$ pyb # runs tests and builds the project
# ...
$ deactivate # deactivates venv
```

### Setting up IntelliJ IDEA/PyCharm
- Configure the venv:
  - File > Project Structure > Project > Project SDK > New
  - Python SDK > Create VirtualEnv
  - Set "Base Interpreter" to the python3 under <project>/venv/bin/python3.5
  - Set "Location" to <project>/venv
- Python Facet
  - File > Project Structure > Facets. Add Python Facet and set interpreter of venv
- `Project Structure... > Modules`. Mark `src/main/python` and `src/unittest/python` as source folder. Mark `target` as excluded folder.
- IntelliJ doesn't compile my code. Code changes doesn't take effect. `File > Settings > Build, Execution, Deployment > Compiler`. Check "Make project automatically".

### Installation
- `pip install TODO-1.0.dev0.tar.gz`
- add `~/.local/bin` to PATH
- call via `TODO.py`

### Uninstallation
`pip uninstall TODO`
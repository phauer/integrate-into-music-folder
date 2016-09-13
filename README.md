# integrate-into-music-folder
TODO description

## Installation and Usage
```
# git clone and cd into dir
$ pyb
$ pip install target/dist/integrate-into-music-folder-1.0.dev0/dist/integrate-into-music-folder-1.0.dev0.tar.gz 
# optionally add "~/.local/bin" to PATH
$ integrate-into-music-folder --help
```

### Deinstallation
```
pip uninstall integrate-into-music-folder
```

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
  - File > Project Structure > Project > Project SDK > Add Local
  - Set path to `<path>/<project root>/venv/bin/python3`
- Python Facet
  - File > Project Structure > Facets. Add Python Facet and set interpreter of venv
- `Project Structure... > Modules`. Mark `src/main/python` and `src/unittest/python` as source folder. Mark `target` as excluded folder.
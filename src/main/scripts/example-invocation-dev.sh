#!/bin/bash
echo "Let's start..."
cd D:/Development/integrate-into-music-folder/src/main/python/music_folder_integrator/
python cli.py --src=C:/Your/Download/Folder --dist=D:/Music --ask-before-copy
read -p "Please press any key..."

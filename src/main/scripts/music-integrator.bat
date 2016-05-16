@ECHO OFF
SET currentWorkingDir=%cd%
SET scriptFolder=%~dp0
SET packagePath=%scriptFolder%..\music_folder_integrator
cd %packagePath%
python cli.py %*
cd %currentWorkingDir%
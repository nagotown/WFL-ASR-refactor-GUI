@echo off
echo The files associated with the GUI should be placed in the root of your WFL-ASR-refactor folder.
echo For models to be detected, you must have a subfolder named `models` containing your models.
echo.
echo For the GUI to work, you must have the customtkinter package installed.
echo This batch file activates a conda environment named `ctk`.
echo.
echo The command generator uses a conda environment named `wfl` by default.
echo.

cd %~dp0
if exist "%~dp0\miniconda" (
	set "conda_hook=%~dp0\miniconda\condabin\conda_hook.bat"
) else if exist "C:\Users\%username%\anaconda3" (
	set "conda_hook=C:\Users\%username%\anaconda3\condabin\conda_hook.bat"
) else if exist "C:\Users\%username%\miniconda3" (
	set "conda_hook=C:\Users\%username%\miniconda3\condabin\conda_hook.bat"
) else if exist "C:\Users\%username%\anaconda" (
	set "conda_hook=C:\Users\%username%\anaconda\condabin\conda_hook.bat"
) else if exist "C:\Users\%username%\miniconda" (
	set "conda_hook=C:\Users\%username%\miniconda\condabin\conda_hook.bat"
) else if exist "C:\ProgramData\anaconda3" (
	set "conda_hook=C:\ProgramData\anaconda3\condabin\conda_hook.bat"
) else if exist "C:\ProgramData\miniconda3" (
	set "conda_hook=C:\ProgramData\miniconda3\condabin\conda_hook.bat"
) else if exist "C:\ProgramData\anaconda" (
	set "conda_hook=C:\ProgramData\anaconda\condabin\conda_hook.bat"
) else if exist "C:\ProgramData\miniconda" (
	set "conda_hook=C:\ProgramData\miniconda\condabin\conda_hook.bat"
) else (
	echo Conda not located, proceeding anyways...
)

call %conda_hook%

echo Launching GUI...
cd ..
call conda activate wfl && python ./WFL-ASR-refactor-GUI/wfl_gui.py

pause
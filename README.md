# WFL-ASR refactor GUI
A CustomTkinter GUI for the [WFL-ASR refactor](https://github.com/MLo7Ghinsan/WFL-ASR/tree/refactor) branch.

Special thanks to [Aster](https://github.com/agentasteriski) and [Ghin](https://github.com/MLo7Ghinsan).

## Setup
Download the repo [here](https://github.com/nagotown/WFL-ASR-refactor-GUI/archive/refs/heads/main.zip), then extract to a subfolder in your `WFL-ASR-refactor` folder.

To function properly, your model folders must be in `WFL-ASR-refactor/models`. 

## Requirements
Tested on Python `3.11.15`.

```
pip install customtkinter
```

or

```
pip install -r requirements.txt
```

## Additional Info
- `refactorgui.bat` opens `wfl_gui.py` after activating a conda environment named `ctk`.  
You can change it to your preferred environment, or if `customtkinter` is in your base environment, you can remove `conda activate ctk &&` from line 37.

- The command generator in the GUI automatically adds `conda activate wfl &&` to the command.  
If you have a different environment for WFL, you can edit it in the textbox before running inference.  
If WFL's dependencies are in your base environment, you can remove `conda activate wfl &&` from the textbox.  
For a more permanent solution, you can comment out line 354 in `refactorgui.py`.

# wf-sentient-tracker
A small Qt5 tray application that will check the [world state API](http://content.warframe.com/dynamic/worldState.php) every 60 seconds for the sentient anomaly spawns at Veil Proxima. It will play a sound clip and send a message with the spawn location when it spawns or de-spawns. Double click tray icon to show the window, mouse over tray icon to display the status, right click tray icon for menu. You can disable the sound, messages, tray icon and "close to tray" functionality using the check boxes in the window.

**Be warned that the sounds may be loud**. Use the buttons to test the volume and have the application appear in your volume mixer.

# Customization

To change the sound clips open the application, press the "Open config directory" button and copy a `spawn.wav` and/or `despawn.wav` into there. Don't edit the `settings.json` file in there unless you know what you are doing. 

**Note:** *The file needs to be a .wav format and has to be named `spawn` or `despawn`.*

The config directory is located at `~/.config/sentient-tracker` if a `~/.config` directory already exists (linux users) or `~/.sentient-tracker` if it doesn't exist. On windows you can access this directory by typing `%HOMEPATH%` into the file explorer address bar.

# Installation

## .exe file

Download the the .exe file from the latest release on the [release page](https://github.com/Kanjirito/wf-sentient-tracker/releases), save it in whatever directory you want and just run it.

## Source code / python

There are 2 ways.

**Note for Linux users:** *To have the application use your system qt theme you have to install PyQt5 from your linux repo and not using pip (it will work but will look worse).*

### pip package

Copy this repo, `cd` into it and do 
```
pip install .
```
for a global install or 
```
pip install --user .
``` 
for a user install. 

This will install the requirements for you. The application will be available as `sentient-tracker`

### Not pip

Copy this repo, `cd` into it, install the requirements (either from the Pifile or requirements.txt) and run `Sentient Tracker.py` (on windows change the filename to .pyw to hide the console).


### Requirements

- requests
- PyQt5

I tested it on python 3.7 and 3.8 though it should work on any python3 version.


# Creating the .exe file

The .exe was made using [pyinstaller](https://www.pyinstaller.org/). You have to be on windows (or using wine). It is recommended to use a virtual environment with only the required packages installed.

To create it run this command while in the repo directory

```
pyinstaller "Sentient Tracker.py" -F -w --clean -i "wf_sentient_tracker\resources\favicon.ico" --add-data "wf_sentient_tracker\resources";"resources"
```

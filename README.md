# wf-sentient-tracker
A small Qt5 tray application that will check the [world state API](http://content.warframe.com/dynamic/worldState.php) every 60 seconds for the sentient anomaly spawns at Veil Proxima. It will play a sound clip and send a message with the spawn location when it spawns or de-spawns. Double click tray icon to show the window, mouse over tray icon to display the status, right click tray icon for menu. You can disable the sound, messages and "close to tray" functionality using the check boxes in the window.

**Be warned that the sounds may be loud**. Use the buttons to test the volume and have the application appear in your volume mixer.

# Installation

## .exe file

Download the the .exe file from the latest release on the [release page](https://github.com/Kanjirito/wf-sentient-tracker/releases), save it in whatever directory you want and just run it. The application will come with a Lotus sound clip for the spawn and a Grineer sound clip for the de-spawn, if you want to use other sounds create a `resources` folder in the same place as the .exe file and put your `spawn.wav` and/or `despawn.wav` in there.

**Note:** *The file needs to be a .wav format and has to be named `spawn` or `despawn`.*


## Source code / python

Copy this repo, install the requirements (either from the Pifile or requirements.txt) and run `main.py` (change the filename to .pyw to hide the console on windows). I don't plan on putting this on PyPI but I'll probably make it a package in the near future.

You can change the sounds in the same way as above but you need to have sound files and a `icon.png` in the `resources` folder otherwise it will crash when there are no sound clips and won't display a tray icon (it will still run in the background) if no `icon.png` is present.

### Requirements

- requests
- PyQt5

I tested it on python 3.7 and 3.8 though it should work on any python3 version.

**Note for Linux users:** *To have the application use your system qt theme you have to install PyQt5 from your linux repo and not using pip.*

# wf-sentient-tracker
A small Qt tray application that will check the [world state API](http://content.warframe.com/dynamic/worldState.php) every 60 seconds for the sentient anomaly spawns at Veil Proxima. It will make a sounds and send a message with the spawn location when it spawns and will also notify when it despawns.

**Be warned that the sounds may be very loud**. You can change the notification sound by replacing the sounds files in the resources directory (they have to be a .wav file).

## Requirements

- requests
- PyQt5

**Note:** *To have the application use your system qt theme you have to install PyQt5 from your linux repo and not pip*
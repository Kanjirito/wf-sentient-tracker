# Release History

## v1.1.0 (19-12-27)

### New
- settings directory at `~/.config/sentient-tracker` or `~/.sentient-tracker` for the `settings.json` file and custom spawn sounds
- new button to open the settings directory
- platform selection
- time stamps of last know spawn/de-spawn for each platform
- a simple help/about window
- turned the repo into a pip package
- entry script for the new package
- tray icon visibility setting


### Changes
- worker now uses QTimer instead of a `while` loop
- some doc strings and code clean up
- switched to signals from direct calls to the worker

### Fixes
- spelling mistakes
- thread is now properly closed when quitting



## v1.0.0 (19-12-21)

Initial release
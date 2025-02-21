# Pymodoro

## Overview
A simple pomodoro CLI application

## Dependencies
To install dependencies, run:
```
pip install -r requirements.txt
```

## Usage
To run the program, use the following command:
```
python pymodoro.py [options]
```
Running without options sets the values as defined in config.ini

### Options
| Argument                                | Description                                                                            |
|-----------------------------------------|----------------------------------------------------------------------------------------|
| -h, --help                              | Show help                                                                              |
| -ft, --focustime                        | Sets the time for focus segments (in minutes)                                          |
| -bt, --breaktime                        | Sets the time for break segments (in minutes)                                          |
| -l, --loops                             | Sets the number of loops (loop = focus segment + break segment)                        |
| -ri, --require_interaction              | Sets whether or not the user is required to give input to continue to the next segment (True/False) |
| -v, --volume                            | Sets the volume (From 0 to 1)                                                          |


## Configuration
Custom sounds, keybindings, default settings and other options can be changed by editing the config.ini file.


To set custom sounds, simply change the path for the corresponding option (can be absolute or relative).
* For example: focusendsound = D:/sounds/custom_sound.mp3


If you break something in the config or want to reset to defaults, you can run the resetConfig.py

(NOTE: some audio file formats may not work!)

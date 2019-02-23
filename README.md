# SC2GoalTracker
A light-weight, hands-free tool that gets data from SC2 replays.

# How to install and use
1) Download and install [Python 2.7](https://www.python.org/downloads/release/python-2715/)
2) Open up command prompt and move into the scripts folder within the Python 2.7 installation folder (e.g. cd "C:\Python27\Scripts")
3) Install watchdog from the command prompt [pip install watchdog](https://pythonhosted.org/watchdog/)
4) Install s2protocol from the command prompt [pip install s2protocol](https://github.com/Blizzard/s2protocol/blob/master/docs/tutorial.rst)
5) Install kivy and it's dependencies from the command prompt 
[pip install --upgrade pip wheel setuptools](https://kivy.org/doc/stable/installation/installation-windows.html)
pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
pip install kivy.deps.gstreamer
pip install kivy
6) Download this repository from the "Clone or Download" button
7) Setup the settings.SC2GT file as you want [see here](https://github.com/SC2GoalTracker/SC2GoalTracker/blob/master/README.md#Setting-up-the-settings-file)
[Highly recommended optional step] Move all your old replays into another folder that is not in the replay_folder specified in the settings file
8) In the "SC2GoalTracker" folder, double click the "sc2_goal_tracker.py" [will bring up a cmd window as well] or the "sc2_goal_tracker_no_console.pyw" [no console output/cmd window]

# Setting up the settings file
Customization can be adjusted in the settings.SC2GT for now which can be opened using notepad and is right next to the executable
* main_race_only - [[True/False]] Only tracks replays of race specified in the "main_race" field
* main_race - [[Protoss/Terran/Zerg]] - No support for random atm, only way is to turn "main_race_only" to False
* player_id - ID of the player SC2 profile, which this program needs to work, see [How to get player_id](https://github.com/SC2GoalTracker/SC2GoalTracker/blob/master/README.md#How-to-get-player-id) below
* twitch_messages_on - [[True/False]] Random messages that apppear based on how well / badly the player is doing in their goal / in their winrates
* replay_folder - Path to the replay folder the player wants to be tracked
* today_goal - Goal for today in minutes
* week_goal - Goal for the week [resets every Sunday] in minutes
* auto_anchor - [[True/False]] Anchors the window in a pseudo fullscreen mode in the corner specified in auto_anchor_corner
* auto_anchor_corner - [[bottom/top left/right]] Corner in which the window will run
* auto_anchor_left_right_offset - Amount of offset the window will start in [[can use to offset into another monitor if values are set high enough e.g. 1920 for a 1920x1080 monitor with auto_anchor_corner bottom right will anchor the program to the bottom right of the second monitor that is on the right of the first one]]
* auto_anchor_bottom_top_offset - Amount offset for the window's y axis. [[Defaults to adjust for Windows taskbar along the bottom]]

# Q&A
### This program's buggy as heck / I want to do X  
There's a lot of bugs at the moment, and customization is a little limited for the time being. Please check the [Issues tab](https://github.com/SC2GoalTracker/SC2GoalTracker/issues) to see what I'm aware of and what I would like to work on. Please add anything that I'm missing!  

### Multiple monitor support?  
Currently players will have to change the auto_anchor_left_right_offset /or auto_anchor_bottom_top_offset fields enough to make it place in another monitor

### Why was minutes played chosen as the stat tracked?
Minutes played was the stat that I wanted to track as I played. Games where a player gets cheesed/cheeses doesn't last as long as a macro game, so the time spent making proper decisions and accurate actions isn't as long.

### Why a desktop app vs a web app?
The decision to make a desktop app was made because having a persistent application which is visible at all times makes it harder to ignore. If you create a shortcut to the file you can also make it run on startup which is what I do. [Here's a link on how to do that for Windows 10](https://support.microsoft.com/en-us/help/4026268/windows-10-change-startup-apps)

# How to get player id
[optional]Go to rankedftw.com   
[optional]Find yourself  
[optional]Hit Battle.net profile  
In the starcraft2.com URL for the profile you want to track, it will be the number at the end
(e.g. https://starcraft2.com/en-gb/profile/3/1/##NUMBER_YOU_WANT###)

# Acknowledgements
**Watchdog** https://pythonhosted.org/watchdog/ - For new file creation detection
**Kivy** https://kivy.org/#home - For creating the window/GUI
**S2 Protocol** https://github.com/Blizzard/s2protocol - From Blizzard to get data from replays  

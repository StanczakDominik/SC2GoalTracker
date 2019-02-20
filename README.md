# SC2GoalTracker
A light-weight, hands-free tool that gets data from SC2 replays.

# How to use
Customization can be adjusted in the settings.SC2GT for now which can be opened using notepad
* main_race_only - [[True/False]] Only tracks replays of race specified in the "main_race" field
* main_race - [[Protoss/Terran/Zerg]] - No support for random atm, only way is to turn "main_race_only" to False
* player_id - ID of the player SC2 profile, NEEDS to be able to work, see (How to get player_id) below[https://github.com/SC2GoalTracker/SC2GoalTracker/blob/master/README.md#How-to-get-player-id]
* twitch_messages_on - [[True/False]] Random messages that apppear based on how well / badly the player is doing in their goal / in their winrates
* replay_folder - Path to the replay folder the player wants to be tracked, needs to have the double forward slash
* today_goal - Goal for today in minutes
* week_goal - Goal for the week [resets every Sunday] in minutes
* auto_anchor - [[True/False]] Anchors the window in a pseudo fullscreen mode in the corner specified in auto_anchor_corner
* auto_anchor_corner - [[bottom/top left/right]] Corner in which the window will run
* auto_anchor_left_right_offset - Amount of offset the window will start in [[can use to offset into another monitor if values are set high enough e.g. 1920 for a 1920x1080 monitor with auto_anchor_corner bottom right will anchor the program to the bottom right of the second monitor that is on the right of the first one]]
* auto_anchor_bottom_top_offset - Amount offset for the window's y axis. [[Defaults to adjust for Windows taskbar along the bottom]]

# Q&A
This program's buggy as heck / I want to do X
- There's a lot of bugs at the moment, and customization is a little limited for the time being. Please check the Issues tab to see what I'm aware of and what I would like to work on. Please add anything that I'm missing!
Multiple monitor support?
- Currently players will have to change the auto_anchor_left_right_offset /or auto_anchor_bottom_top_offset fields enough to make it place in another monitor

# How to get player id
[optional]Go to rankedftw.com
[optional]Find yourself
[optional]Hit Battle.net profile
In the starcraft2.com URL for the profile you want to track, it will be the number at the end
(e.g. https://starcraft2.com/en-gb/profile/3/1/##NUMBER_YOU_WANT###)

# Acknowledgements
**Watchdog** https://pythonhosted.org/watchdog/ - For callback when a new replay is created
**Kivy** https://kivy.org/#home - For creating the window
**S2 Protocol** https://github.com/Blizzard/s2protocol - From Blizzard to get data from replays
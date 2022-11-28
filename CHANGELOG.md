# Changelog

All notable changes to this project will be documented in this file.

## [pre-2.0.1] - 2022-11-28

- Updated Architect's Ring compatibility for `geartilegenerator.py`

## [pre-2.0.0] - 2022-11-26

Monumenta-Items pre-release 2 offers a whole new section to the user interface: Equipment!

Now you can view King's Valley and Celsian Isles equipment in a whole new section of the UI. Just input your items in the gearr2 list in `constants.py` and run the app to have a beautiful view of your charms and equipment. 

Future releases will include Architect's Ring equipment compatibility and user input of items directly into the UI.

To upgrade, download the new repository and run the app. No new packages need to be installed!

### Major Changes

-`geartilegenerator.py` which gets data from `constants.Constants` and displays equipment information alongside charm information

-updated `charmtilegenerator.py` with class type 

### Changed Features

-repositioned charm and gear info on two seperate grids to stop charms and gear offsetting each other

-updated `constants.Constants` with data for equipment stat colors and class colors

-repositioned info to left side of item frames

## [pre-1.0.0] - 2022-11-24

Monumenta-Items pre-release 1 now offers tkinter user interface compatibility!

This pre-release only offers a UI that displays charm info, and UI charm inputs are still in the making, but it has full charm info display. 

To upgrade, make sure tkinter is installed in your virtual environment or as a system package.

### Major Changes

-`charmtilegenerator.py` which gets the data from `constants.Constants` and creates a functioning user interface

-tkinter compatibility for clean and simple user interface

### Changed Features

- moved `getitemstats()` to `getbuild.py`

- refractored `tmp_gear.py` to `constants.py`

- updated `constants.py` with colors and constants

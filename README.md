================================================================================
  PATHFINDER CALENDAR CONVERTER
  Converts Gregorian dates to the Pathfinder RPG (Golarion) calendar system
================================================================================

DESCRIPTION
-----------
A simple Windows GUI application that takes a standard calendar date and
converts it to the Pathfinder RPG in-world calendar used on the planet
Golarion.  It also supports a "Delta" offset so you can quickly calculate
dates a number of days before or after the selected date.

CONVERSIONS APPLIED
-------------------
  Day of week:
    Monday    -> Moonday
    Tuesday   -> Toilday
    Wednesday -> Wealday
    Thursday  -> Oathday
    Friday    -> Fireday
    Saturday  -> Starday
    Sunday    -> Sunday

  Month:
    January   -> Abadius       July      -> Erastus
    February  -> Calistril     August    -> Arodus
    March     -> Pharast       September -> Rova
    April     -> Gozran        October   -> Lamashan
    May       -> Desnus        November  -> Neth
    June      -> Sarenith      December  -> Kuthona

  Year: Gregorian year minus 1032, suffixed with "IA"
    (e.g. 2026 AD -> 994 IA)

  Output format example:
    Wealday, 10th of Sarenith, in the year 994 IA

DELTA FEATURE
-------------
  Enter a positive or negative whole number in the "Delta" box to offset the
  selected date by that many days.  The converted result updates live as you
  type.  Selecting a new date clears the Delta field automatically.
  Any non-integer input displays "Error".

================================================================================
  HOW TO RUN (pre-compiled .exe)
================================================================================

  Simply double-click PathfinderCalendar.exe.
  No Python installation is required.

================================================================================
  HOW TO COMPILE FROM SOURCE
================================================================================

REQUIREMENTS
------------
  - Python 3.10 or newer  (https://www.python.org/downloads/)
  - pip (included with Python)

STEP 1 - Install dependencies
------------------------------
  Open a terminal / command prompt and run:

    pip install tkcalendar pyinstaller

STEP 2 - Compile to a standalone .exe
--------------------------------------
  Navigate to the folder containing pathfinder_calendar.py and run:

    python -m PyInstaller --onefile --windowed --name "PathfinderCalendar" pathfinder_calendar.py

  The finished executable will be placed in the "dist" sub-folder:
    dist\PathfinderCalendar.exe

STEP 3 - Run
------------
  Double-click dist\PathfinderCalendar.exe  (or move it anywhere you like).

DEPENDENCIES
------------
  tkcalendar  >= 1.6   https://pypi.org/project/tkcalendar/
  babel       >= 2.0   (installed automatically with tkcalendar)
  pyinstaller >= 6.0   https://pypi.org/project/pyinstaller/
  tkinter              (bundled with the standard Python installer on Windows)

================================================================================
  AI PROMPT USED TO GENERATE THIS PROJECT
================================================================================

The following prompt was submitted to Claude (Anthropic) to generate the
source code and build instructions for this project:

---

"Can you create me a simple software program that has a calendar drop down and
when a date is selected, it converts the days from Mon - Sunday to Moonday,
Toilday, Wealday, Oathday, Fireday, Starday, and Sunday respectively.  Can it
also change the month from Jan - Dec -> Abadius, Calistril, Pharast, Gozran,
Desnus, Sarenith, Erastus, Arodus, Rova, Lamashan, Neth, and Kuthona
respectively, Subtract 1032 years from the year. write out the date selected
in the following format (example, Wednesday June 6th 2026) Wealday, 10th of
Sarenith, in the year 934 IA.

Additionally, add a text box with a caption specifying "Delta", when a whole
number (either negative or positive) is added here, it will add or subtract
that many days from the selected day in the same format as above.  This
calculation should occur live when a date is added and updated automatically
when the number is changed.  Having a character that is not numberic will cause
the conversion to just say "Error".

When a new date is selected the delta should clear and the text should be
updated with the new date.

This should be compiled into an .exe file and open a simple GUI with a grey
background of appropriate size to contain the data.  There should be a close
button at the bottom that exits."

---

================================================================================
  LICENSE
================================================================================

This project is released as-is for personal and community use.
Pathfinder is a trademark of Paizo Inc.  This tool is an unofficial fan
utility and is not affiliated with or endorsed by Paizo Inc.

================================================================================
  SPECIAL THANKS
===================================================================================

This tool was forged in the fires of necessity to track the twisting timelines of Golarion. Special thanks to the crew who inspired its creation:

* Our Game Master (Ian): For weaving an incredible world, handling my calendar-pedantry like a absolute champ, and terrifying us with the anomalies of Tosen and the surrounding areas. 
* The Hollow Oath members of The Grey Ledger:
  ** Akkyt: For ensuring a fair fight, even for enemy wizards and helping Kinyscus to discover the temoral anomalies.
  ** Soranus: For helping Kinyscus conive new and fun ways to remove combatants and keeping the party grounded.
  ** Neponthes: For keeping a loaded D20 in her back pocket and being a terrifying whirlwind.

May our dates align and our timelines remain unbroken. 


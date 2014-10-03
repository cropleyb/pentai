PentAI by Bruce Cropley

Pente is a strategy board game for two or more players, created in 1977 by Gary Gabrel. The board game is owned by Hasbro and is/was distributed via Winning Moves, however there are many computer versions of Pente out there.
If you succeed at making money out of PentAI, you will most likely encounter their legal department.
Pente has a very small number of rules, it is quick to play (~5mins), but takes years to master.
PentAI is an app that plays Pente. The Artificial Intelligence (AI) can play at an advanced level, but it can be set to a very basic level where it blunders most of the time, and everything in between.

Dependencies
------------
User Interface: Kivy 1.8.1
Persistence:    ZODB 4.0.0 & zlibstorage

Status
------
Platform        Builds & Runs   Package
OS X            Yes             Yes, except for NSScreen
iOS (iPad Air)  Yes?            Yes?, but it's a nightmare.
Windows         Yes?            Not tried
Linux           Yes             Not tried
Android         Not tried       Not tried

High level AI design
--------------------
http://www.bruce-cropley.com/pentai

Music
-----
The music is all original, by me (Bruce Cropley)

Build Dependencies
------------------
Install Kivy and all its dependencies as per the kivy website instructions

Install ZODB with:
kivy pip install ZODB
kivy pip install zlibstorage

Before it will run, you will need to build the cython modules (see below)

Build and test for development (OS X/Windows)
------------------------------
I use the text editor vim, and have a few key maps set up to do several frequently repeated tasks:

Build the cython extensions with:
kivy ./setup.py build_ext --inplace
map <silent> ,b :wa<CR>:!kivy $PENTAIPATH/setup.py build_ext --inplace<CR>

Run all the unit tests (<1s) with:
kivy ./pentai/t_all.py
map <silent> ,t :wa<CR>:!kivy $PENTAIPATH/pentai/t_all.py<CR>

Run the AI subsystem tests (<20s):
kivy ./pentai/ai/t_ai_subsystem.py
map <silent> ,a :wa<CR>:!kivy $PENTAIPATH/pentai/ai/t_ai_subsystem.py<CR>

Run the AI in matches against itself (no visuals)
kivy ./pentai/run_ai.py
map <silent> ,r :wa<CR>:!kivy $PENTAIPATH/pentai/run_ai.py<CR>

Run the app:
kivy ./main.py -m inspector
map <silent> ,k :wa<CR>:!kivy $PENTAIPATH/main.py -m inspector<CR>

Build for iOS
-------------
(on OS X)
Needs XCode to Build and test on the iOS simulator
To test on a real iPad, you will also need an iOS developers' license.
Clone the kivy-ios package from github, then make changes from the pentai/iOS directory. There are more tips there.

Package for OS X
----------------
Basically as per the Kivy packaging instructions, with the added difficulty of packaging ZODB and PentAI's cythonized AI code.

Run AI
------
There is a very hacky script that I have used to compare various AI player settings: pentai.run_ai
I have deliberately left lots of dead code in there to show what can be done with it. If you want to get repeatable results, turn the openings book off for both players.

Build openings book
-------------------
The openings book is built from many games played by good players.
There is a tradeoff between the size of the distributed app, and the time taken to build the openings DB. Representing each game as series of moves takes less space than representing each entire state of the board for matching against during games. However, at the moment, the full openings DB is distributed as part of the package.

To build db.fs.openings (on a desktop machine):
(delete it first or it will grow with duplicates)
python pentai/db/openings_builder.py

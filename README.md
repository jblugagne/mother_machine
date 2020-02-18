# mother_machine

This is a python script to generate the mother machine GDSII file that is contained in this repo (mother_machine.gds) with [KLayout](http://www.klayout.de/)
Please use it as a quick and dirty example to learn how to make similar microlfuidic masks designs.

In order to run it in Klayout, please change the path to the github repo at the beginning of generator.py, and then in KLayout: Macros > Macros development > Import file (import generator.py) and then run the script.
You may or may not need to launch KLayout in [edit mode](https://www.klayout.de/0.24/doc/manual/edit_mode.html)

This file is designed to feature both microfabrication layers, the thin growth chambers/traps one and the thick flow channels one, on the same chrome mask to reduce cost. If you would rather have two pre-aligned masks, set spacing_layers to 0 and selectively comment either line with mask.insert(final) at the end of the file to get GDSIIs with just one of the two layers.

Note: I just updated the code to python 3. If python 2 worked better for you, check out previous commits.

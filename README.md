# mother_machine

This is a python script to generate the mother machine GDSII file that is contained in this repo (mother_machine.gds) with [KLayout](http://www.klayout.de/).
Please feel free to use it as a quick and dirty example to learn how to make similar microfluidic masks designs, or even to replicate this design.

In order to run it in Klayout, please change the path to the github repo at the beginning of generator.py, and then in KLayout: Macros > Macros development > Import file (import generator.py) and then run the script.
You may or may not need to launch KLayout in [edit mode](https://www.klayout.de/0.24/doc/manual/edit_mode.html)

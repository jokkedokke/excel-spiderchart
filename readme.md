# Spider chart tool for Excel statistics file

## Usage
If you are using Pycharm, the tool should be able to import the required libraries when you
open up the directory. If not, please see requirement.txt for the necessary libraries and
import the manually (Project settings -> Project <project name> -> Interpreter)

The application is a streamlit application, so you should probably define a new run target
for the project. If the virtual environment and the required libraries have been imported correctly,
go to 

>**Run** -> **Edit configurations** 

then add a new python run target, and change the following values:

>**Script path**
> 
This should point to streamlit executable, usually in found in either
><project dir>/venv/bin/streamlit

or if you are on Windows,

> <project dir>\venv\bin\streamlit.exe
                                         

**Parameters** 
>run "main.py"

**Working directory**

Working directory should point to the same directory where rest of the files are, namely
the root directory of the Python project.

Then all you need to do is to just Run... from the Run-menu, and your computer should open up a browser window
and run the project automagically with some debug printing to see what is being printed.

## Excel file stucture

A sample Excel file can be found in the form of sample.xlsx . The assumptions for the Excel file format are
* Each worksheet will be printed out to own spider chart with the name of the worksheet
* The first column should contain the player name, and the column should be named "Player"
* All the other columns should contain the category name in the first header row, and the numerical values
in the following rows. Other formats (dates, strings) will probably explode the tool

All the files are written in the directory called "images"


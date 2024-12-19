Functionally Graded Material Script for Abaqus (Beta)

Overview

This Python script implements functionally graded material (FGM) behavior in Abaqus for analyzing the autofrettage process of a cylinder.
The script is designed to define material properties that vary along the radial direction of the cylinder and automate key steps in the simulation process.

Features

Automates the creation of models in Abaqus.
Defines material properties as a function of radial distance.
Supports the simulation of the autofrettage process, including elastic and plastic zones.
Includes customizable parameters for cylinder geometry, and loading conditions

Requirements

Abaqus/CAE: Version 6.13 (Should work on higher versions)
Python: The script is compatible with Abaqus Python environment (typically Python 3)

How to Use

Prepare the Environment:
Ensure that Abaqus is installed and accessible from your system's command line.
Place the script in a working directory.

Customize Input Parameters:
Open the script in a text editor. (Eg. Notepad++, Visual Studio, Vim)
Edit the following key parameters to match your simulation setup:

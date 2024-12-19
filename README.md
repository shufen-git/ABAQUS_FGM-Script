# Functionally Graded Material Script (Beta version) for ABAQUS

## Overview

This Python script implements functionally graded material (FGM) behavior in Abaqus for analyzing the autofrettage process of a cylinder
The script is designed to define material properties that vary along the radial direction of the cylinder and automate key steps in the simulation process

## Features

- Automates the creation of models in ABAQUS
- Defines material properties as a function of radial distance
- Supports the simulation of the autofrettage process, including elastic and plastic zones
- Includes customizable parameters for cylinder geometry, and loading conditions

## Requirements

- Abaqus/CAE: Version 6.13 (Should work on higher versions)
- Python: The script is compatible with Abaqus Python environment (typically Python 3)

## How to Use

- Prepare the Environment:
- Ensure that Abaqus is installed and accessible from your system's command line.
- Place the script in a working directory.

## Customize Input Parameters:
- Open the script in a text editor. (Eg. Notepad++, Visual Studio, Vim)
- Edit the following key parameters to match your simulation setup:
```
a=0.01					      # Inner radius  
b=0.03					      # Outer radius  
l=0.06					      # Half length of the cylinder  
t=b-a					        # Thickness  
  
meshradial=50		      # Elements along radial direction  
meshlength=20		      # Elements along axial direction  
bias=5				        # Bias factor  
maxincrement=0.01	    # Increment  
```
### ----------------------- This part is optional ----------------------------

* To obtain the material properties of the FGM in the output database  
* Go to ABAQUS GUI  
* Go to Model > Keywords > Edit Keywords
* Scroll down and find the following
```
*Depvar  
7,  
```
Replace the above entirely with the following lines:  

```
**  
*DEPVAR  
** number of variables  
 7  
** variables list  
 1, Ceramic_volume  
 2, Metal_volume  
 3, E_FGM  
 4, nu_FGM  
 5, sy_FGM  
 6, k_FGM  
 7, alpha_FGM  
 **
```

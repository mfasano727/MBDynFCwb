## Multibody Dynamic FreeCAD Workbench
MBDynFCwb - Multibody Dynamic (MBDyn) FreeCAD Workbench (FCwb) based on code from MBDyn GSoC project.

### Introduction

This is the start of a preprocessor MBDyn with FreeCAD. It is a modification of the MBDyn's GSOC project using scripted objects. 

### Structure

The MBDyn model gets saved in scripted objects. A write command is used on the scripted objects to write a MBDyn input file. There is command to create rigid bodies; when you create a rigid body it also creates a structural node at the center of gravity with an orientation rotated as the part is in FreeCad. A command to create structural nodes there are commands to create revolute pin and revolute hinge joints.

### Prerequisites

* [**FreeCAD** v0.19.x](https://github.com/FreeCAD/FreeCAD/releases/tag/0.19_pre)
* [**Assembly4** External Workbench](https://github.com/Zolko-123/FreeCAD_Assembly4) installed via the [FreeCAD Addon Manager](https://wiki.freecadweb.org/Std_AddonMgr)
The asm4 branch requires FreeCAD v0.19 because you need assembly4 workbench (see the Assembly 4 workbench for minimum revision number) 

### Installation

Windows users can get a windows build of MBDyn here  
http://www.aero.polimi.it/masarati/Download/mbdyn/mbdyn-1.7.2-win32.zip  

### Command Reference

Commands can be found in the `FreeCAD MBDyn workbench with Assembly 4 instructions` page of the [wiki](https://github.com/mfasano727/MBDynFCwb/wiki/FreeCAD-MBDyn-workbench-with-Assembly-4-instructions) 

### Tutorial
A tutorial is found in the [Pendulum Tutorial](https://github.com/mfasano727/MBDynFCwb/wiki/Pendulum-Tutorial) page of the wiki    


### Feedback

There is a discussion of the project in the FreeCAD forum. Please post your feedback/suggestions/bugs directly to the [thread](https://forum.freecadweb.org/viewtopic.php?f=18&t=39165&start=100).
  

### TODO
There are many ways other than add more MBDyn entities to improve the workbench.
Here is a list, not in order of importance.
* General
    - [ ] add names to the MBDyn scripted objects and use them as variables in the input file to make it more readable
    - [ ] use `Propertylink` in the MBDyn objects so they can change with the FreeCAD model.
* Workbench structure
    - [ ] make the workbench compatible with the new style workbench.
* Robustness
    - [ ] add exception handling, like making line editors in pyside only accept numbers where applicable.
* Tree view layout
    - [ ] Updrage the tree view layout to separate the model, the simulations and the results.(**In Progress**)
    - [ ] Add "FreeCAD style" icons to each tree entities
* Post Processing
    - [ ] include force and torque indicators. (`pivy.coin`)
    - [ ] code for graphing velocity, acceleration etc. (`pivy.coin`)
    - [ ] plot data (`matplotlib`)
    - [ ] create curves to visualyse node path
* Testing
    - [ ] Add unit tests

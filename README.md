# MBDynFCwb
FreeCAD workbench based on code from MBDyn Google summer of code project.

This is the start of a preprocessor MBDyn with FreeCAD. It is  modified MBDyn's GSOC project using scripted objects. The MBDyn model gets saved in scripted objects. A write command used the scripted objects to write a MBDyn input file. there is command to create rigid bodies; when you create a rigid body it also created a structural node at the center of gravity with an orientation rotated as the part is in FreeCad. A command to create structural nodes there are commands to create revolute pin and revolute hinge joints.

The asm4 branch requires FreeCAD v0.19  because you need assembly4 workbench. (see the assembly 4 workbench for minimum revision number) 

Windows users can get a windows build of MBDyn here  
http://www.aero.polimi.it/masarati/Download/mbdyn/mbdyn-1.7.2-win32.zip  

Commands can be found in the "FreeCAD MBDyn workbench with Assembly 4 instructions" page of the wiki  
[commands](https://github.com/mfasano727/MBDynFCwb/wiki/FreeCAD-MBDyn-workbench-with-Assembly-4-instructions) 

A tutorial is found in the "Pendulum Tutorial" page of the wiki    
[tutorial](https://github.com/mfasano727/MBDynFCwb/wiki/Pendulum-Tutorial)


There is a discussion of the project in the FreeCAD forum here.  
https://forum.freecadweb.org/viewtopic.php?f=18&t=39165&start=100

## TODO list
There are many ways other than add more MBDyn entities to improve the workbench.
Here is a list, not in order of importance.
* Workbench structure
    * make the workbench compatible with the new style workbench.
* Robustness
    * add exception handling, like making line editors in pyside only accept numbers where applicable.
* Tree view layout
    * Updrage the tree view layout to separate the model, the simulations and the results.(**In Progress**)
    * Add "freecad style" icons to each tree entities
* Post Processing
    * include force and torque indicators. (pivy.coin)
    * code for graphing velocity, acceleration etc. (pivy.coin)
    * plot data (matplotlib)
    * create curves to visualyse node path
* add names to the MBDyn scripted objects and use them as variables in the input file to make it more readable
* use Propertylink in the MBDyn objects so they can change with the FreeCAD model.
* test more

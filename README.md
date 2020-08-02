# MBDynFCwb
FreeCAD workbench based on code from MBDyn Google summer of code project.

This is the start of a preprocessor MBDyn with FreeCAD. It is  modified MBDyn's GSOC project using scripted objects. The MBDyn model gets saved in scripted objects. A write command used the scripted objects to write a MBDyn input file. there is command to create rigid bodies; when you create a rigid body it also created a structural node at the center of gravity with an orientation rotated as the part is in FreeCad. A command to create structural nodes there are commands to create revolute pin and revolute hinge joints.

The asm4 branch requires FreeCAD v0.19  because you need assembly4 workbench. (see the assembly 4 workbench for minimum revision number) 

Windows users can get a windows build of MBDyn here  
http://www.aero.polimi.it/masarati/Download/mbdyn/mbdyn-1.7.2-win32.zip  

Instructions can be found in the "FreeCAD MBDyn workbench with Assembly 4 instructions" page of the wiki  
[instructions](https://github.com/mfasano727/MBDynFCwb/wiki/FreeCAD-MBDyn-workbench-with-Assembly-4-instructions) 

A tutorial is found in the "Pendulum Tutorial" page of the wiki    
[tutorial](https://github.com/mfasano727/MBDynFCwb/wiki/Pendulum-Tutorial)


There is a discussion of the project in the FreeCAD forum here.  
https://forum.freecadweb.org/viewtopic.php?f=18&t=39165&start=100

TODO list
There are many ways other than add more MBDyn elements to improve the workbench.
Here is a list, not in order of importance.

* make the workbench compatible with the new style workbench.
* add exception handling, like making line editors in pyside only accept numbers where applicable.
* include more in the post processing, like force and torque indicators. code for graphing velocity, acceleration etc.
* add names to the MBDyn scripted objects and use them as variables in the input file to make it more readable
* use Propertylink in the MBDyn objects so they can change with the FreeCAD model.
* test more

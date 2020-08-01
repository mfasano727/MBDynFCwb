# MBDynFCwb
FreeCAD workbench based on code from MBDyn Google summer of code project.

This is the start of a preprocessor MBDyn with FreeCAD. It is  modified MBDyn's GSOC project using scripted objects. The MBDyn model gets saved in scripted objects. A write command used the scripted objects to write a MBDyn input file. there is command to create rigid bodies; when you create a rigid body it also created a structural node at the center of gravity with an orientation rotated as the part is in FreeCad. A command to create structural nodes there are commands to create revolute pin and revolute hinge joints.

The asm4 branch requires FreeCAD v0.19  because you need assembly4 workbench. (see the assembly 4 workbench for minimum revision number)  

windows users can get a windows build of MBDyn here
http://www.aero.polimi.it/masarati/Download/mbdyn/mbdyn-1.7.2-win32.zip

There is a discussion of the project in the FreeCAD forum here.
https://forum.freecadweb.org/viewtopic.php?f=18&t=39165&start=100


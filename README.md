# MBDynFCwb
FreeCAD workbench based on code from MBDyn Google summer of code project.

This is the start of a preprocessor MBDyn with FreeCAD. It is  modified MBDyn's GSOC project using scripted objects. The MBDyn model gets saved in scripted objects. A write command used the scripted objects to write a MBDyn input file. there is command to create rigid bodies; when you create a rigid body it also created a structural node at the center of gravity with an orientation rotated as the part is in FreeCad. A command to create structural nodes there are commands to create revolute pin and revolute hinge joints.

The todo list is endless. I am sure the program is infested with bugs. post-processing is obvious item.


import FreeCAD as App

#----------------WorkbenchCreationLayout
def createTree():
    """ Creation of the main tree layout
    """
    from MBDyn_objects.ObjectProxy.MBDynBaseContainer import BaseContainer
    from MBDyn_objects.ObjectProxy.MBDynWorkbench import WorkbenchContainer

    doc = App.ActiveDocument

    # Base Container
    root = doc.addObject('App::DocumentObjectGroupPython', "MBDyn Workbench")
    WorkbenchContainer(root)

    # Model Container
    model = doc.addObject('App::DocumentObjectGroupPython', "MBDyn Model")
    BaseContainer(model, "MBDyn::ModelContainer")
    root.addObject(model)

    #References Container
    references = doc.addObject('App::DocumentObjectGroupPython', "References")
    BaseContainer(references, "MBDyn::ReferencesContainer")
    model.addObject(references)

    #Nodes Container
    nodes = doc.addObject('App::DocumentObjectGroupPython', "Nodes")
    BaseContainer(nodes, "MBDyn::NodesContainer")
    model.addObject(nodes)

    #elements Container
    elements = doc.addObject('App::DocumentObjectGroupPython', "Elements")
    BaseContainer(elements, "MBDyn::ElementsContainer")
    model.addObject(elements)

    # bodies Container
    bodies = doc.addObject('App::DocumentObjectGroupPython', "Bodies")
    BaseContainer(bodies, "MBDyn::BodiesContainer")
    elements.addObject(bodies)

    #Joint Container
    joints = doc.addObject('App::DocumentObjectGroupPython', "Joints")
    BaseContainer(joints, "MBDyn::JointsContainer")
    elements.addObject(joints)

    #Loads Container
    loads = doc.addObject('App::DocumentObjectGroupPython', "Loads")
    BaseContainer(loads, "MBDyn::LoadsContainer")
    elements.addObject(loads)

    #Drive Caller Container
    driveCaller = doc.addObject('App::DocumentObjectGroupPython', "Drive Caller")
    BaseContainer(driveCaller, "MBDyn::DriveCallerContainer")
    elements.addObject(driveCaller)

    #Simulation Container
    simulations = doc.addObject('App::DocumentObjectGroupPython', "Simulations")
    BaseContainer(simulations, "MBDyn::SimulationsContainer")
    root.addObject(simulations)

    if App.GuiUp:
        from MBDyn_objects.ViewProxy.view_base_container import ViewProviderBaseContainer
        ViewProviderBaseContainer(root.ViewObject)
        ViewProviderBaseContainer(model.ViewObject)
        ViewProviderBaseContainer(references.ViewObject)
        ViewProviderBaseContainer(nodes.ViewObject)
        ViewProviderBaseContainer(elements.ViewObject)
        ViewProviderBaseContainer(bodies.ViewObject)
        ViewProviderBaseContainer(joints.ViewObject)
        ViewProviderBaseContainer(loads.ViewObject)
        ViewProviderBaseContainer(driveCaller.ViewObject)
        ViewProviderBaseContainer(simulations.ViewObject)

    doc.recompute()
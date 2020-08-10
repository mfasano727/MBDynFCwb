import FreeCAD as App
import FreeCADGui as Gui




#----------------WorkbenchCreationLayout
def createTree():
    """ Creation of the main tree layout
    TODO: Add the Drive caller container
    """
    from MBDyn_objects.MBDynBaseContainer import BaseContainer
    from MBDyn_objects.MBDynWorkbench import WorkbenchContainer

    doc = App.ActiveDocument

    # Base Container
    root = doc.addObject('App::DocumentObjectGroupPython', "MBDyn Workbench")
    WorkbenchContainer(root)
    
    # Model Container
    model = doc.addObject('App::DocumentObjectGroupPython', "Model")
    BaseContainer(model, "MBDyn::ModelContainer")
    root.addObject(model)
    
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
        from MBDyn_viewproviders.view_base_container import ViewProviderBaseContainer
        ViewProviderBaseContainer(root.ViewObject)
        ViewProviderBaseContainer(model.ViewObject)
        ViewProviderBaseContainer(nodes.ViewObject)
        ViewProviderBaseContainer(elements.ViewObject)
        ViewProviderBaseContainer(bodies.ViewObject)
        ViewProviderBaseContainer(joints.ViewObject)
        ViewProviderBaseContainer(simulations.ViewObject)
    
    doc.recompute()

#----------------Simulation creation
def createSimulation():
    """
    Creation of a simulation container
    a creation container is composed of
        - the simulation featurepython
        - The load Container: var name: SimNameLoads, label: Loads
        - The Results container: var name: SimeNameResults, label: Results
    """
    from MBDyn_objects.MBDynBaseContainer import BaseContainer
    from MBDyn_objects.MBDynSimulation import Simulation
    
    doc = App.ActiveDocument

    sim = doc.addObject('App::DocumentObjectGroupPython', "MySim")
    Simulation(sim)
    sim.Document.Simulations.addObject(sim) # add the sim to the simulations group

    # Deactivate the duplicate label to name all loads container: Loads and all Results container: Results
    SavedParameter = App.ParamGet("User parameter:BaseApp/Preferences/Document").GetBool("DuplicateLabels",False)
    App.ParamGet("User parameter:BaseApp/Preferences/Document").SetBool("DuplicateLabels",True) 

    name = "Loads"
    loads = doc.addObject('App::DocumentObjectGroupPython', name)
    BaseContainer(loads, "MBDyn::LoadsContainer")
    sim.addObject(loads) # add the loads to the simulation group
    loads.Label = "Loads"
    loads.setEditorMode("Label",2) # Hide object parameter

    name = "Results"
    results = doc.addObject('App::DocumentObjectGroupPython', name)
    BaseContainer(results, "MBDyn::ResultsContainer")
    sim.addObject(results) # add the results to the simulation group
    results.Label = "Results"
    results.setEditorMode("Label",2) # Hide object parameter
    results.setEditorMode("Group",2) # Hide object parameter

    # set saved parameter value
    App.ParamGet("User parameter:BaseApp/Preferences/Document").SetBool("DuplicateLabels",SavedParameter)

    if App.GuiUp:
        from MBDyn_viewproviders.view_base_container import ViewProviderBaseContainer
        from MBDyn_viewproviders.view_simulation import ViewProviderSimulation
        ViewProviderSimulation(sim.ViewObject)
        ViewProviderBaseContainer(loads.ViewObject)
        ViewProviderBaseContainer(results.ViewObject)

    doc.recompute()

import FreeCAD as App

# ----------------Simulation creation
def createSimulation(doc, sim_parameter):
    """
    Creation of a simulation container
    a creation container is composed of
        - the simulation featurepython
        - The load Container: var name: SimNameLoads, label: Loads
        - The Results container: var name: SimeNameResults, label: Results
    """
    from MBDyn_objects.ObjectProxy.MBDynBaseContainer import BaseContainer
    from MBDyn_objects.ObjectProxy.MBDynSimulation import Simulation

    simulations_container = doc.Simulations
    i = len(simulations_container.Group)

    sim = doc.addObject('App::DocumentObjectGroupPython', "MySim" + str(i))
    print(sim.Name)
    Simulation(sim, sim_parameter)
    simulations_container.addObjects([sim]) # add the sim to the simulations group

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
        from MBDyn_objects.ViewProxy.view_base_container import ViewProviderBaseContainer
        from MBDyn_objects.ViewProxy.view_simulation import ViewProviderSimulation
        ViewProviderSimulation(sim.ViewObject)
        ViewProviderBaseContainer(loads.ViewObject)
        ViewProviderBaseContainer(results.ViewObject)

    doc.recompute()